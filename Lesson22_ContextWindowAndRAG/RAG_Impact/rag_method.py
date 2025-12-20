"""RAG method: Retrieval Augmented Generation with vector search.

This module implements the RAG approach:
1. Chunk documents into smaller pieces
2. Generate embeddings for each chunk
3. Store in vector database
4. Retrieve top K most relevant chunks for query
5. Query Claude with only retrieved chunks
"""

import time
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
import chromadb
import config
from query_processor import query_claude_with_timing
from logger_setup import get_logger

logger = get_logger()

# Global embedding model (singleton pattern - load once)
_embedding_model = None


def get_embedding_model() -> SentenceTransformer:
    """
    Lazy load embedding model (singleton).

    Returns:
        SentenceTransformer model

    Note:
        Model is loaded only once and cached globally for efficiency.
    """
    global _embedding_model
    if _embedding_model is None:
        logger.info(f"Loading embedding model: {config.EMBEDDING_MODEL}")
        _embedding_model = SentenceTransformer(config.EMBEDDING_MODEL)
        logger.info("Embedding model loaded successfully")
    return _embedding_model


def chunk_text(
    text: str,
    chunk_size: int = None,
    overlap: int = None
) -> List[str]:
    """
    Split text into overlapping chunks by word count.

    Args:
        text: Input text
        chunk_size: Words per chunk (default: from config)
        overlap: Word overlap between chunks (default: from config)

    Returns:
        List of text chunks

    Example:
        >>> text = "word " * 1000
        >>> chunks = chunk_text(text, chunk_size=500, overlap=50)
        >>> len(chunks) >= 2
        True
    """
    if chunk_size is None:
        chunk_size = config.CHUNK_SIZE
    if overlap is None:
        overlap = config.CHUNK_OVERLAP

    # Split into words
    words = text.split()

    # If text is shorter than chunk_size, return as-is
    if len(words) <= chunk_size:
        return [text]

    chunks = []
    step = chunk_size - overlap

    for i in range(0, len(words), step):
        chunk_words = words[i:i + chunk_size]
        chunk_text = " ".join(chunk_words)
        chunks.append(chunk_text)

        # Stop if we've reached the end
        if i + chunk_size >= len(words):
            break

    return chunks


def build_vector_db(documents: List[str]) -> chromadb.Collection:
    """
    Build vector database from all documents.

    Process:
    1. Chunk all documents
    2. Generate embeddings for all chunks
    3. Create ChromaDB collection
    4. Add chunks with embeddings

    Args:
        documents: List of document texts

    Returns:
        ChromaDB collection with all chunks

    Example:
        >>> collection = build_vector_db(documents)
        >>> print(f"Created DB with {collection.count()} chunks")
    """
    logger.info("Building vector database...")

    # Chunk all documents
    all_chunks = []
    chunk_metadata = []

    for doc_idx, doc in enumerate(documents):
        doc_chunks = chunk_text(doc)

        for chunk_idx, chunk in enumerate(doc_chunks):
            chunk_id = f"doc{doc_idx}_chunk{chunk_idx}"
            all_chunks.append(chunk)
            chunk_metadata.append({
                "id": chunk_id,
                "doc_index": doc_idx,
                "chunk_index": chunk_idx
            })

    logger.info(f"Created {len(all_chunks)} chunks from {len(documents)} documents")

    # Generate embeddings
    logger.info("Generating embeddings...")
    model = get_embedding_model()
    embeddings = model.encode(all_chunks, show_progress_bar=False)
    logger.info(f"Generated embeddings: shape {embeddings.shape}")

    # Create ChromaDB collection
    client = chromadb.Client()
    collection = client.create_collection(
        name="documents",
        metadata={"description": "PDF document chunks"}
    )

    # Add chunks to collection
    collection.add(
        ids=[meta["id"] for meta in chunk_metadata],
        embeddings=embeddings.tolist(),
        documents=all_chunks,
        metadatas=[{"doc_idx": meta["doc_index"]} for meta in chunk_metadata]
    )

    logger.info(f"Vector database built successfully: {collection.count()} chunks")
    return collection


def retrieve_top_k(
    query: str,
    collection: chromadb.Collection,
    k: int = None
) -> List[str]:
    """
    Retrieve top K most relevant chunks.

    Args:
        query: Question string
        collection: Vector database collection
        k: Number of chunks to retrieve (default: from config)

    Returns:
        List of top K chunk texts

    Example:
        >>> chunks = retrieve_top_k("side effects?", collection, k=3)
        >>> len(chunks) == 3
        True
    """
    if k is None:
        k = config.TOP_K_CHUNKS

    # Generate query embedding
    model = get_embedding_model()
    query_embedding = model.encode([query])[0]

    # Search collection
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=k
    )

    # Extract texts
    top_chunks = results["documents"][0]

    logger.debug(f"Retrieved top {k} chunks (total: {len(top_chunks)})")
    return top_chunks


def run_rag_iterations(
    api_key: str,
    documents: List[str],
    query: str,
    iterations: int = None
) -> List[Dict[str, Any]]:
    """
    Run multiple RAG iterations.

    Note: Vector DB built once (before iterations), then queries run
    multiple times for consistent timing measurement.

    Args:
        api_key: Anthropic API key
        documents: List of document texts
        query: Question to ask
        iterations: Number of test iterations (default: from config)

    Returns:
        List of result dictionaries

    Example:
        >>> results = run_rag_iterations(api_key, docs, "Query?", iterations=5)
    """
    if iterations is None:
        iterations = config.ITERATIONS

    logger.info("=" * 50)
    logger.info(f"RAG METHOD ({iterations} iterations)")
    logger.info("=" * 50)

    # Build vector DB once (before iterations)
    logger.info("Building vector database...")
    collection = build_vector_db(documents)

    results = []

    for i in range(1, iterations + 1):
        logger.info(f"Iteration {i}/{iterations}...")

        # Time the full RAG pipeline (retrieve + query)
        start_time = time.time()

        # Retrieve top K chunks
        top_chunks = retrieve_top_k(query, collection, config.TOP_K_CHUNKS)

        # Combine chunks
        rag_context = "\n\n--- CHUNK ---\n\n".join(top_chunks)

        # Query Claude with retrieved chunks
        result = query_claude_with_timing(api_key, rag_context, query)

        # Update time to include retrieval
        total_time = time.time() - start_time
        result["time_seconds"] = total_time

        # Add metadata
        result["iteration"] = i
        result["method"] = "rag"
        result["chunks_retrieved"] = len(top_chunks)

        # Store result
        results.append(result)

        # Log summary
        logger.info(
            f"Iteration {i}/{iterations} complete: "
            f"Time: {result['time_seconds']:.2f}s, "
            f"Tokens: {result['input_tokens']:,}/{result['output_tokens']:,}, "
            f"Cost: ${result['cost']:.4f}"
        )

        # Delay between iterations (except after last one)
        if i < iterations:
            delay = config.RETRY_DELAY
            logger.debug(f"Waiting {delay}s before next iteration...")
            print(f"⏳ Waiting {delay}s before next iteration...", end="", flush=True)
            for remaining in range(delay, 0, -1):
                print(f"\r⏳ Waiting {remaining}s before next iteration...", end="", flush=True)
                time.sleep(1)
            print("\r✓ Ready for next iteration" + " " * 30)

    logger.info(f"RAG method: {iterations} iterations completed")
    return results
