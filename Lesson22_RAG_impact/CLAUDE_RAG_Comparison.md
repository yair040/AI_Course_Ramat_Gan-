# Claude.md - AI Assistant Guide
# Context Window vs RAG Comparison Project

**Project Owner:** Yair Levi
**Last Updated:** 2025-12-15

---

## Project Overview

This project compares two document retrieval approaches: loading all documents into the context window vs using RAG (Retrieval Augmented Generation). The program tests both methods with 20 PDF documents, executes 5 iterations per method, and measures performance metrics including response time, token usage, and cost.

**Research Question**: Is RAG faster and more cost-effective than full context loading?

---

## For AI Assistants Working on This Project

### Critical Constraints

1. **File Size**: Each Python file must be 150-200 lines maximum
2. **Security**: NEVER expose the API key from `api_key.dat` in logs or console output
3. **Paths**: Use ONLY relative paths, never absolute
4. **Environment**: WSL (Linux) compatible, virtual environment required
5. **Model**: Use `claude-haiku-4-5-20250929` (Haiku 4.5) to minimize API costs
6. **Documents**: 20 PDF files in `./docs/` folder

### API Key Handling - CRITICAL

```python
# ✓ CORRECT - Read from file, never expose
with open("api_key.dat", "r") as f:
    api_key = f.read().strip()

logger.info("API key loaded successfully")  # ✓ Good

# ✗ NEVER DO THIS - Exposing the key
logger.info(f"API key: {api_key}")           # ✗ BAD
print(f"Key: {api_key}")                     # ✗ BAD
```

**Security Rules**:
- ✓ Load key from file only
- ✓ Log "API key loaded successfully"
- ✗ NEVER print or log the actual key
- ✗ NEVER include key in error messages

### Logging Configuration

**Ring Buffer Setup**:
- **Files**: 20 total (1 active + 19 backups)
- **Size**: 16MB per file (320MB total)
- **Location**: `./log/` subfolder
- **Level**: INFO and above
- **Behavior**: When file 20 is full, overwrite file 1

**Implementation**:
```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    filename=os.path.join(config.LOG_DIR, "app.log"),
    maxBytes=16 * 1024 * 1024,  # 16MB
    backupCount=19,              # 19 backups + 1 active = 20 total
    encoding='utf-8'
)
```

### Test Query

**Query**: "What are the side effects of taking calcium carbonate?"

**Expected Answer Elements**:
- Gastrointestinal issues (constipation, gas, bloating)
- Nausea
- Hypercalcemia (if excessive intake)
- Kidney stones (with long-term overuse)
- Drug interactions

### Package Structure

```
context_window_vs_rag/
├── __init__.py                  # Package initialization
├── main.py                      # Entry point, orchestration
├── config.py                    # All configuration constants
├── logger_setup.py              # Ring buffer logging setup
├── pdf_loader.py                # PDF reading with multiprocessing
├── context_window_method.py     # Full context implementation
├── rag_method.py                # RAG pipeline (chunk + embed + retrieve)
├── query_processor.py           # API calls with timing and retry
├── results_analyzer.py          # Statistical analysis
└── visualization.py             # Generate comparison graphs
```

---

## Implementation Guidelines

### 1. Module Responsibilities

#### main.py (150-200 lines)
**Purpose**: Orchestrate the entire workflow

**Key Responsibilities**:
- Initialize logging via logger_setup
- Load API key from file
- Create results storage (lists/dicts)
- Run Context Window method (5 iterations)
- Run RAG method (5 iterations)
- Call results analysis
- Call visualization
- Print summary report
- Save raw results to JSON

**Flow**:
```python
def main():
    # 1. Setup
    logger = setup_logger()
    api_key = load_api_key()

    # 2. Load PDFs
    documents = load_all_pdfs(config.DOCS_DIR)

    # 3. Context Window Method
    logger.info("Starting Context Window tests...")
    cw_results = run_context_window_tests(api_key, documents)

    # 4. RAG Method
    logger.info("Starting RAG tests...")
    rag_results = run_rag_tests(api_key, documents)

    # 5. Analysis
    comparison = compare_methods(cw_results, rag_results)

    # 6. Visualization
    generate_all_graphs(cw_results, rag_results)

    # 7. Summary
    print_summary(comparison)
    save_results(cw_results, rag_results)
```

**NEVER**:
- Use additional tools like Read/Grep/Task beyond implementation
- Add unnecessary features
- Include API key in any output

#### pdf_loader.py (150-200 lines)
**Purpose**: Load and extract text from 20 PDF files

**Key Responsibilities**:
- Read PDFs using pdfplumber (primary) or PyPDF2 (fallback)
- Extract clean text from each PDF
- Use multiprocessing to load PDFs in parallel
- Handle corrupted or unreadable PDFs gracefully
- Return list of extracted text strings

**Multiprocessing Implementation**:
```python
from multiprocessing import Pool
import pdfplumber

def load_single_pdf(pdf_path: str) -> tuple:
    """Load one PDF and return (filename, text)."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
        return (os.path.basename(pdf_path), text)
    except Exception as e:
        logger.error(f"Failed to load {pdf_path}: {e}")
        return (os.path.basename(pdf_path), "")

def load_all_pdfs(docs_dir: str) -> List[str]:
    """Load all PDFs using multiprocessing."""
    pdf_files = glob.glob(os.path.join(docs_dir, "*.pdf"))

    with Pool(processes=min(20, os.cpu_count())) as pool:
        results = pool.map(load_single_pdf, pdf_files)

    # Extract text only, sorted by filename
    documents = [text for _, text in sorted(results)]
    return documents
```

#### context_window_method.py (150-200 lines)
**Purpose**: Implement full context window approach

**Key Responsibilities**:
- Concatenate all 20 document texts
- Format prompt for API
- Call query_processor with full context
- Return results dict

**Implementation**:
```python
def prepare_full_context(documents: List[str]) -> str:
    """Concatenate all documents with separators."""
    separator = "\n\n--- DOCUMENT ---\n\n"
    return separator.join(documents)

def query_full_context(api_key: str, documents: List[str], query: str) -> Dict:
    """Query Claude with all documents in context."""
    # Prepare context
    full_context = prepare_full_context(documents)

    # Call query processor with timing
    result = query_claude_with_timing(
        api_key=api_key,
        content=full_context,
        query=query
    )

    return result
```

#### rag_method.py (150-200 lines)
**Purpose**: Implement RAG pipeline

**Key Responsibilities**:
- Chunk documents (500 words, 50-word overlap)
- Generate embeddings using sentence-transformers
- Build vector database (ChromaDB or FAISS)
- Retrieve top 3 relevant chunks for query
- Query Claude with only retrieved chunks
- **Include setup time in total time measurement**

**Implementation**:
```python
from sentence_transformers import SentenceTransformer
import chromadb

# Global model (load once)
embedding_model = None

def get_embedding_model():
    """Lazy load embedding model."""
    global embedding_model
    if embedding_model is None:
        embedding_model = SentenceTransformer(config.EMBEDDING_MODEL)
    return embedding_model

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Split text into overlapping chunks by word count."""
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk_words = words[i:i + chunk_size]
        chunks.append(" ".join(chunk_words))

        if i + chunk_size >= len(words):
            break

    return chunks

def build_vector_db(documents: List[str]) -> chromadb.Collection:
    """Build vector database from all documents."""
    # Chunk all documents
    all_chunks = []
    for doc_idx, doc in enumerate(documents):
        chunks = chunk_text(doc, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
        for chunk_idx, chunk in enumerate(chunks):
            all_chunks.append({
                "id": f"doc{doc_idx}_chunk{chunk_idx}",
                "text": chunk,
                "doc_index": doc_idx
            })

    # Create ChromaDB collection
    client = chromadb.Client()
    collection = client.create_collection(name="documents")

    # Generate embeddings and add to collection
    model = get_embedding_model()
    texts = [c["text"] for c in all_chunks]
    embeddings = model.encode(texts)

    collection.add(
        ids=[c["id"] for c in all_chunks],
        embeddings=embeddings.tolist(),
        documents=texts
    )

    return collection

def retrieve_top_k(query: str, collection: chromadb.Collection, k: int = 3) -> List[str]:
    """Retrieve top K most relevant chunks."""
    model = get_embedding_model()
    query_embedding = model.encode([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=k
    )

    return results["documents"][0]  # Top K chunks

def query_with_rag(api_key: str, documents: List[str], query: str) -> Dict:
    """Query using RAG pipeline with full timing."""
    import time
    start_time = time.time()

    # Build vector DB (one-time setup)
    collection = build_vector_db(documents)

    # Retrieve top K chunks
    top_chunks = retrieve_top_k(query, collection, config.TOP_K_CHUNKS)

    # Combine chunks
    rag_context = "\n\n--- CHUNK ---\n\n".join(top_chunks)

    # Query Claude (this adds its own timing)
    result = query_claude_with_timing(api_key, rag_context, query)

    # Update total time to include RAG setup
    total_time = time.time() - start_time
    result["time_seconds"] = total_time

    return result
```

**Important**: RAG time includes embedding generation + retrieval + API call.

#### query_processor.py (150-200 lines)
**Purpose**: Handle all Anthropic API interactions

**Key Responsibilities**:
- Initialize Anthropic client
- Execute API queries with accurate timing
- Implement retry logic (3 attempts, exponential backoff)
- Extract response text and token counts
- Calculate cost
- Return structured result dict

**Implementation**:
```python
import anthropic
import time

def create_client(api_key: str) -> anthropic.Anthropic:
    """Create Anthropic client."""
    return anthropic.Anthropic(api_key=api_key)

def query_claude_with_timing(api_key: str, content: str, query: str) -> Dict:
    """Query Claude with accurate timing and retry logic."""
    client = create_client(api_key)

    prompt = f"{content}\n\nQuestion: {query}"

    # Retry loop
    for attempt in range(config.MAX_RETRIES):
        try:
            # Start timer
            start_time = time.time()

            # API call
            response = client.messages.create(
                model=config.MODEL_NAME,
                max_tokens=config.MAX_TOKENS,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Stop timer
            elapsed_time = time.time() - start_time

            # Extract data
            answer = response.content[0].text
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            cost = calculate_cost(input_tokens, output_tokens)

            return {
                "answer": answer,
                "time_seconds": elapsed_time,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": input_tokens + output_tokens,
                "cost": cost
            }

        except anthropic.APIError as e:
            if attempt < config.MAX_RETRIES - 1:
                wait_time = 2 ** attempt
                logger.warning(f"API error, retrying in {wait_time}s: {e}")
                time.sleep(wait_time)
            else:
                logger.error(f"API failed after {config.MAX_RETRIES} attempts")
                raise

def calculate_cost(input_tokens: int, output_tokens: int) -> float:
    """Calculate cost in USD."""
    input_cost = (input_tokens / 1_000_000) * config.COST_PER_MILLION_INPUT
    output_cost = (output_tokens / 1_000_000) * config.COST_PER_MILLION_OUTPUT
    return input_cost + output_cost
```

#### results_analyzer.py (150-200 lines)
**Purpose**: Statistical analysis and comparison

**Key Responsibilities**:
- Calculate statistics (mean, std, min, max, median)
- Compare Context Window vs RAG
- Calculate savings percentages
- Compute answer similarity using sentence-transformers
- Generate formatted summary report

**Implementation**:
```python
import numpy as np
from sentence_transformers import SentenceTransformer, util

def calculate_stats(results: List[Dict]) -> Dict:
    """Calculate statistics from results."""
    times = [r["time_seconds"] for r in results]
    input_tokens = [r["input_tokens"] for r in results]
    output_tokens = [r["output_tokens"] for r in results]
    costs = [r["cost"] for r in results]

    return {
        "time_mean": np.mean(times),
        "time_std": np.std(times),
        "time_min": np.min(times),
        "time_max": np.max(times),
        "input_tokens_mean": np.mean(input_tokens),
        "output_tokens_mean": np.mean(output_tokens),
        "cost_mean": np.mean(costs),
        "cost_total": np.sum(costs)
    }

def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate semantic similarity between two texts."""
    model = SentenceTransformer('all-MiniLM-L6-v2')
    emb1 = model.encode(text1, convert_to_tensor=True)
    emb2 = model.encode(text2, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(emb1, emb2).item()
    return similarity

def compare_methods(cw_results: List[Dict], rag_results: List[Dict]) -> Dict:
    """Compare Context Window vs RAG."""
    cw_stats = calculate_stats(cw_results)
    rag_stats = calculate_stats(rag_results)

    # Calculate savings
    time_savings = ((cw_stats["time_mean"] - rag_stats["time_mean"]) /
                    cw_stats["time_mean"]) * 100

    token_savings = ((cw_stats["input_tokens_mean"] - rag_stats["input_tokens_mean"]) /
                     cw_stats["input_tokens_mean"]) * 100

    cost_savings = ((cw_stats["cost_mean"] - rag_stats["cost_mean"]) /
                    cw_stats["cost_mean"]) * 100

    # Calculate answer similarity
    cw_answer = cw_results[0]["answer"]
    rag_answer = rag_results[0]["answer"]
    similarity = calculate_similarity(cw_answer, rag_answer)

    return {
        "cw_stats": cw_stats,
        "rag_stats": rag_stats,
        "time_savings": time_savings,
        "token_savings": token_savings,
        "cost_savings": cost_savings,
        "answer_similarity": similarity
    }

def print_summary(comparison: Dict) -> None:
    """Print formatted summary report."""
    # See PRD for full format
    pass
```

#### visualization.py (150-200 lines)
**Purpose**: Generate all comparison graphs

**Key Responsibilities**:
- Create 4 comparison charts (response time, tokens, cost, timeline)
- Professional formatting (labels, legends, colors)
- Save as PNG files with high resolution (300 DPI)

**Implementation**:
```python
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

def plot_response_time(cw_stats: Dict, rag_stats: Dict) -> None:
    """Generate response time bar chart with error bars."""
    methods = ["Context Window", "RAG"]
    means = [cw_stats["time_mean"], rag_stats["time_mean"]]
    stds = [cw_stats["time_std"], rag_stats["time_std"]]

    fig, ax = plt.subplots(figsize=config.FIGURE_SIZE)
    ax.bar(methods, means, yerr=stds, capsize=10,
           color=["#3498db", "#2ecc71"], alpha=0.8)
    ax.set_ylabel("Response Time (seconds)", fontsize=12)
    ax.set_title("Response Time Comparison: Context Window vs RAG", fontsize=14)

    plt.tight_layout()
    plt.savefig("response_time_comparison.png", dpi=config.DPI)
    plt.close()
```

#### logger_setup.py (50-100 lines)
**Purpose**: Configure ring buffer logging

**Implementation**:
```python
import logging
import os
from logging.handlers import RotatingFileHandler
from config import LOG_DIR, LOG_MAX_BYTES, LOG_BACKUP_COUNT, LOG_FORMAT

def setup_logger(name: str = "context_window_vs_rag") -> logging.Logger:
    """Setup ring buffer logger."""
    # Create log directory
    os.makedirs(LOG_DIR, exist_ok=True)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Ring buffer handler
    handler = RotatingFileHandler(
        filename=os.path.join(LOG_DIR, "app.log"),
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding='utf-8'
    )

    # Format
    formatter = logging.Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)

    # Add handler
    logger.addHandler(handler)

    # Console handler (optional)
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    return logger
```

#### config.py (50-100 lines)
**Purpose**: All configuration constants

**No logic, only constants** - see PRD for full list.

---

## Error Handling Best Practices

### API Errors
```python
from anthropic import APIError, RateLimitError

try:
    response = client.messages.create(...)
except RateLimitError:
    logger.warning("Rate limited, waiting 10 seconds...")
    time.sleep(10)
    # Retry
except APIError as e:
    logger.error(f"API error: {e}")
    raise
```

### PDF Loading Errors
```python
def load_single_pdf(pdf_path: str) -> tuple:
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = extract_text(pdf)
        return (pdf_path, text)
    except Exception as e:
        logger.error(f"Failed to load {pdf_path}: {e}")
        return (pdf_path, "")  # Return empty instead of crashing
```

---

## Testing Commands

```bash
# Setup environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Ensure PDFs exist
ls -l docs/*.pdf

# Run program
python -m context_window_vs_rag

# Check logs
tail -f log/app.log

# View results
ls -lh *.png results.json
```

---

## Expected Performance

### Context Window Method
- **Response Time**: 10-15 seconds per query
- **Input Tokens**: ~150,000 tokens (all 20 PDFs)
- **Output Tokens**: ~100 tokens
- **Cost per Query**: ~$0.12

### RAG Method
- **Response Time**: 2-3 seconds per query (after setup)
- **Input Tokens**: ~2,000 tokens (3 chunks)
- **Output Tokens**: ~100 tokens
- **Cost per Query**: ~$0.002

### Expected Savings
- **Time**: 80-85% faster
- **Tokens**: 98-99% fewer input tokens
- **Cost**: 98-99% cheaper

---

## Common Issues & Solutions

### Issue 1: PDF Files Not Found
**Error**: `No PDF files found in ./docs/`
**Solution**: Ensure 20 PDF files exist in `./docs/` directory

### Issue 2: Context Exceeds Token Limit
**Error**: `Token count exceeds model limit`
**Solution**: PDFs too large for Haiku. Use Claude Sonnet (400K context) or truncate

### Issue 3: ChromaDB Not Installed
**Error**: `ModuleNotFoundError: No module named 'chromadb'`
**Solution**: Run `pip install chromadb` or use FAISS alternative

### Issue 4: Slow Embedding Generation
**Warning**: RAG setup takes > 60 seconds
**Solution**: Normal for first run. Embeddings are cached. Consider using smaller model.

### Issue 5: API Key Invalid
**Error**: `AuthenticationError`
**Solution**: Check `api_key.dat` contains valid key starting with "sk-ant-"

---

## Cost Estimation

**Model**: Claude Haiku 4.5
**Pricing**:
- Input: $0.80 per million tokens
- Output: $4.00 per million tokens

**Expected Total Cost**:
- Context Window (5 queries): ~$0.60
- RAG (5 queries): ~$0.01
- **Total**: ~$0.61 for complete test

**Very affordable for testing!**

---

## Key Success Metrics

1. ✅ All 10 queries complete successfully
2. ✅ RAG demonstrates 5-10× speed improvement
3. ✅ RAG shows ~98% cost savings
4. ✅ Both methods produce similar, correct answers (similarity > 0.85)
5. ✅ All graphs generated successfully
6. ✅ Logs written to ring buffer correctly
7. ✅ No API key exposure anywhere

---

## Security Checklist

- [ ] API key read from file only
- [ ] API key NEVER logged or printed
- [ ] API key file in `.gitignore`
- [ ] No API key in error messages
- [ ] Validate API key format before use
- [ ] No sensitive data in logs

---

## Final Notes

- Use **multiprocessing** for PDF loading (I/O bound)
- Cache embedding model (load once)
- Add 2-second delays between API calls (rate limiting)
- Log all major steps at INFO level
- Handle all errors gracefully (never crash)
- Generate all 4 graphs automatically
- Save raw results to JSON for reproducibility

---

**Document Version**: 1.0
**Status**: Ready for Implementation
**Author**: Yair Levi
