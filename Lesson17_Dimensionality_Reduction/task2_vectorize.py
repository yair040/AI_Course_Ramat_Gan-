"""
Task 2: Convert sentences to normalized vector embeddings
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from utils import (
    load_sentences, save_vectors, Timer, verify_normalization,
    SENTENCES_FILE, NORMALIZED_FILE, EMBEDDING_MODEL
)


def load_embedding_model(model_name: str = EMBEDDING_MODEL):
    """
    Load sentence transformer model

    Args:
        model_name: Name of the sentence transformer model

    Returns:
        Loaded model
    """
    print(f"  Loading model: {model_name}")
    model = SentenceTransformer(model_name)
    embedding_dim = model.get_sentence_embedding_dimension()
    print(f"  ✓ Model loaded successfully")
    print(f"  ✓ Embedding dimension: {embedding_dim}")
    return model


def vectorize_sentences(sentences: list, model) -> np.ndarray:
    """
    Convert sentences to embeddings

    Args:
        sentences: List of sentence strings
        model: Sentence transformer model

    Returns:
        Array of embeddings (N, embedding_dim)
    """
    print(f"  Converting {len(sentences)} sentences to vectors...")
    embeddings = model.encode(
        sentences,
        show_progress_bar=True,
        batch_size=32,
        convert_to_numpy=True
    )
    print(f"  ✓ Vectorization complete")
    return embeddings


def normalize_vectors(vectors: np.ndarray) -> np.ndarray:
    """
    L2 normalization to unit length

    Args:
        vectors: Array of vectors (N, dim)

    Returns:
        Normalized vectors (N, dim)
    """
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    normalized = vectors / norms
    return normalized


def verify_and_report_normalization(vectors: np.ndarray):
    """
    Verify normalization and print statistics

    Args:
        vectors: Array of vectors to verify
    """
    norms = np.linalg.norm(vectors, axis=1)
    print(f"\n  Normalization Verification:")
    print(f"    Min norm: {norms.min():.8f}")
    print(f"    Max norm: {norms.max():.8f}")
    print(f"    Mean norm: {norms.mean():.8f}")
    print(f"    Std norm: {norms.std():.8f}")

    if verify_normalization(vectors):
        print(f"    ✓ All vectors are normalized (unit length)")
    else:
        print(f"    ⚠ Warning: Some vectors are not normalized")


def main():
    """Main execution for Task 2"""
    print("=" * 60)
    print("TASK 2: Vectorize Sentences")
    print("=" * 60)

    # Load sentences
    print(f"\nLoading sentences from {SENTENCES_FILE}...")
    sentences = load_sentences(SENTENCES_FILE)
    print(f"✓ Loaded {len(sentences)} sentences")

    # Load model
    with Timer("Loading embedding model"):
        model = load_embedding_model(EMBEDDING_MODEL)

    # Vectorize
    with Timer("Vectorizing sentences"):
        vectors = vectorize_sentences(sentences, model)

    # Print vector statistics
    print(f"\n✓ Vector shape: {vectors.shape}")
    print(f"  (Rows: {vectors.shape[0]} sentences, Columns: {vectors.shape[1]} dimensions)")

    # Normalize
    with Timer("Normalizing vectors"):
        normalized = normalize_vectors(vectors)

    # Verify normalization
    verify_and_report_normalization(normalized)

    # Save
    print(f"\nSaving normalized vectors to {NORMALIZED_FILE}...")
    save_vectors(normalized, NORMALIZED_FILE)
    print(f"✓ Normalized vectors saved successfully")

    # Summary
    print(f"\n{'─' * 60}")
    print(f"Summary:")
    print(f"  Input: {len(sentences)} sentences")
    print(f"  Output: {normalized.shape[0]} vectors × {normalized.shape[1]} dimensions")
    print(f"  All vectors normalized to unit length")
    print(f"{'─' * 60}")

    return normalized


if __name__ == "__main__":
    main()
