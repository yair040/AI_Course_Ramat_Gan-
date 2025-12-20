# Tasks Document
# Context Window vs RAG Comparison Project

**Project**: Context Window vs RAG Performance Benchmarking
**Author**: Yair Levi
**Date**: 2025-12-15

---

## Task Categories

1. [Setup Tasks](#setup-tasks)
2. [Core Infrastructure Tasks](#core-infrastructure-tasks)
3. [PDF Processing Tasks](#pdf-processing-tasks)
4. [API Integration Tasks](#api-integration-tasks)
5. [Method Implementation Tasks](#method-implementation-tasks)
6. [Analysis Tasks](#analysis-tasks)
7. [Visualization Tasks](#visualization-tasks)
8. [Integration Tasks](#integration-tasks)
9. [Testing Tasks](#testing-tasks)
10. [Documentation Tasks](#documentation-tasks)

---

## Setup Tasks

### SETUP-001: Create Project Structure
**Priority**: Critical
**Duration**: 10 min
**Dependencies**: None

**Steps**:
1. Create directory: `context_window_vs_rag/`
2. Create subdirectories:
   - `./log/`
   - `./results/`
   - `./docs/` (if not exists)
3. Verify 20 PDF files in `./docs/`
4. Verify `api_key.dat` exists in root

**Acceptance Criteria**:
- [ ] All directories exist
- [ ] 20 PDFs present in `./docs/`
- [ ] `api_key.dat` exists and readable

---

### SETUP-002: Create Virtual Environment
**Priority**: Critical
**Duration**: 5 min
**Dependencies**: SETUP-001

**Steps**:
```bash
python3 -m venv venv
source venv/bin/activate  # WSL/Linux
```

**Acceptance Criteria**:
- [ ] Virtual environment created
- [ ] Virtual environment activated
- [ ] `which python` shows venv path

---

### SETUP-003: Create requirements.txt
**Priority**: Critical
**Duration**: 10 min
**Dependencies**: None

**Content**:
```txt
# Core Dependencies
anthropic>=0.40.0
python-dotenv>=1.0.0

# PDF Processing
PyPDF2>=3.0.0
pdfplumber>=0.10.0

# RAG Components
sentence-transformers>=2.2.0
chromadb>=0.4.0

# NLP & ML
transformers>=4.30.0
torch>=2.0.0

# Visualization
matplotlib>=3.7.0
seaborn>=0.12.0

# Data Processing
numpy>=1.24.0

# Utilities
tqdm>=4.65.0
```

**Acceptance Criteria**:
- [ ] requirements.txt created
- [ ] All required packages listed
- [ ] Version constraints specified

---

### SETUP-004: Install Dependencies
**Priority**: Critical
**Duration**: 10 min
**Dependencies**: SETUP-002, SETUP-003

**Steps**:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Acceptance Criteria**:
- [ ] All packages installed successfully
- [ ] No error messages
- [ ] Can import anthropic, pdfplumber, chromadb, etc.

---

### SETUP-005: Create .gitignore
**Priority**: High
**Duration**: 5 min
**Dependencies**: None

**Content**:
```
# Virtual Environment
venv/
env/

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# API Keys
api_key.dat
.env

# Logs
log/
*.log

# Results
results/
*.png
*.json

# Vector Database
vector_db/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

**Acceptance Criteria**:
- [ ] .gitignore created
- [ ] api_key.dat excluded
- [ ] All sensitive files excluded

---

## Core Infrastructure Tasks

### CORE-001: Create config.py
**Priority**: Critical
**Duration**: 20 min
**Dependencies**: None
**File**: `context_window_vs_rag/config.py`

**Implementation**:
```python
"""Configuration constants for Context Window vs RAG comparison."""

import os

# Paths
DOCS_DIR = "./docs"
LOG_DIR = "./log"
RESULTS_DIR = "./results"
API_KEY_FILE = "./api_key.dat"

# API Settings
MODEL_NAME = "claude-haiku-4-5-20250929"
MAX_TOKENS = 1024
API_TIMEOUT = 120  # seconds
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds between queries

# RAG Settings
CHUNK_SIZE = 500  # words
CHUNK_OVERLAP = 50  # words
TOP_K_CHUNKS = 3
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
VECTOR_DB_DIR = "./vector_db"

# Test Settings
ITERATIONS = 5
QUERY = "What are the side effects of taking calcium carbonate?"

# Logging Settings
LOG_LEVEL = "INFO"
LOG_MAX_BYTES = 16 * 1024 * 1024  # 16MB
LOG_BACKUP_COUNT = 19  # Total 20 files (1 active + 19 backups)
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Visualization Settings
DPI = 300
FIGURE_SIZE = (10, 6)
OUTPUT_DIR = "."

# Cost Settings (USD per million tokens)
COST_PER_MILLION_INPUT = 0.80
COST_PER_MILLION_OUTPUT = 4.00
```

**Acceptance Criteria**:
- [ ] File created with all constants
- [ ] No logic, only configuration
- [ ] Can import: `from context_window_vs_rag import config`
- [ ] Line count: 50-100 lines

---

### CORE-002: Create logger_setup.py
**Priority**: Critical
**Duration**: 30 min
**Dependencies**: CORE-001
**File**: `context_window_vs_rag/logger_setup.py`

**Implementation**:
```python
"""Logging setup with ring buffer (20 files × 16MB)."""

import logging
import os
from logging.handlers import RotatingFileHandler
from . import config


def setup_logger(name: str = "context_window_vs_rag") -> logging.Logger:
    """
    Setup ring buffer logger.

    Creates a logger that writes to 20 rotating log files (16MB each).
    When the 20th file is full, it overwrites the first file.

    Args:
        name: Logger name

    Returns:
        Configured logger instance

    Example:
        >>> logger = setup_logger()
        >>> logger.info("Test message")
    """
    # Create log directory
    os.makedirs(config.LOG_DIR, exist_ok=True)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, config.LOG_LEVEL))

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # File handler (ring buffer)
    file_handler = RotatingFileHandler(
        filename=os.path.join(config.LOG_DIR, "app.log"),
        maxBytes=config.LOG_MAX_BYTES,
        backupCount=config.LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(config.LOG_FORMAT)
    file_handler.setFormatter(file_formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        "%(levelname)s: %(message)s"
    )
    console_handler.setFormatter(console_formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
```

**Testing**:
```python
logger = setup_logger()
logger.info("Test message 1")
logger.warning("Test warning")
logger.error("Test error")
```

**Acceptance Criteria**:
- [ ] Logger created successfully
- [ ] Log directory created automatically
- [ ] Logs written to `./log/app.log`
- [ ] Console output visible
- [ ] Line count: 50-100 lines

---

### CORE-003: Create __init__.py
**Priority**: High
**Duration**: 10 min
**Dependencies**: None
**File**: `context_window_vs_rag/__init__.py`

**Implementation**:
```python
"""
Context Window vs RAG Comparison Package.

Empirically compares full context loading vs RAG (Retrieval Augmented
Generation) for document retrieval from 20 PDF files.

Metrics compared:
- Response time
- Token usage
- Cost
- Answer quality

Usage:
    python -m context_window_vs_rag
"""

__version__ = "1.0.0"
__author__ = "Yair Levi"
__email__ = "yair@example.com"

# Import main function for easy access
from .main import main

__all__ = ["main"]
```

**Acceptance Criteria**:
- [ ] Package imports correctly
- [ ] Version accessible
- [ ] Line count: < 50 lines

---

## PDF Processing Tasks

### PDF-001: Implement load_single_pdf()
**Priority**: Critical
**Duration**: 20 min
**Dependencies**: CORE-001, CORE-002
**File**: `context_window_vs_rag/pdf_loader.py`
**Function**: `load_single_pdf()`

**Signature**:
```python
def load_single_pdf(pdf_path: str) -> Tuple[str, str]:
    """
    Load one PDF and extract text.

    Args:
        pdf_path: Path to PDF file

    Returns:
        (filename, extracted_text)

    Raises:
        None (handles errors gracefully, returns empty string on failure)
    """
```

**Implementation Steps**:
1. Try pdfplumber.open()
2. Iterate through pages
3. Extract text from each page
4. Concatenate all text
5. On error: log warning, return (filename, "")

**Testing**:
```python
filename, text = load_single_pdf("./docs/sample.pdf")
assert len(text) > 0
assert isinstance(text, str)
```

**Acceptance Criteria**:
- [ ] Loads PDF successfully
- [ ] Extracts readable text
- [ ] Handles corrupted PDFs gracefully
- [ ] Returns tuple (filename, text)

---

### PDF-002: Implement load_all_pdfs()
**Priority**: Critical
**Duration**: 25 min
**Dependencies**: PDF-001
**File**: `context_window_vs_rag/pdf_loader.py`
**Function**: `load_all_pdfs()`

**Signature**:
```python
def load_all_pdfs(docs_dir: str) -> List[str]:
    """
    Load all PDFs using multiprocessing.

    Args:
        docs_dir: Directory containing PDF files

    Returns:
        List of extracted text strings (sorted by filename)

    Example:
        >>> documents = load_all_pdfs("./docs")
        >>> len(documents)
        20
    """
```

**Implementation Steps**:
1. Get list of PDF files using glob
2. Create multiprocessing.Pool
3. Use pool.map() with load_single_pdf
4. Sort results by filename
5. Extract text only (discard filenames)
6. Return list of texts

**Testing**:
```python
documents = load_all_pdfs("./docs")
assert len(documents) == 20
assert all(isinstance(doc, str) for doc in documents)
```

**Acceptance Criteria**:
- [ ] Loads all 20 PDFs
- [ ] Uses multiprocessing
- [ ] Returns sorted list
- [ ] Total function: 30-40 lines

---

### PDF-003: Implement validate_pdf()
**Priority**: Medium
**Duration**: 10 min
**Dependencies**: PDF-001
**File**: `context_window_vs_rag/pdf_loader.py`
**Function**: `validate_pdf()`

**Signature**:
```python
def validate_pdf(pdf_path: str) -> bool:
    """
    Check if PDF is readable.

    Args:
        pdf_path: Path to PDF file

    Returns:
        True if readable, False otherwise
    """
```

**Acceptance Criteria**:
- [ ] Returns True for valid PDFs
- [ ] Returns False for corrupted PDFs
- [ ] No exceptions raised

---

### PDF-004: Complete pdf_loader.py
**Priority**: Critical
**Duration**: 15 min
**Dependencies**: PDF-001, PDF-002, PDF-003
**File**: `context_window_vs_rag/pdf_loader.py`

**Tasks**:
1. Add module docstring
2. Add imports
3. Add logger initialization
4. Add type hints
5. Add comprehensive docstrings
6. Add error handling

**Acceptance Criteria**:
- [ ] All functions implemented
- [ ] Module docstring present
- [ ] Line count: 150-200 lines
- [ ] Passes all tests

---

## API Integration Tasks

### API-001: Implement create_client()
**Priority**: Critical
**Duration**: 10 min
**Dependencies**: CORE-001, CORE-002
**File**: `context_window_vs_rag/query_processor.py`
**Function**: `create_client()`

**Signature**:
```python
def create_client(api_key: str) -> anthropic.Anthropic:
    """
    Create Anthropic API client.

    Args:
        api_key: Anthropic API key

    Returns:
        Configured Anthropic client

    Raises:
        ValueError: If API key format is invalid
    """
```

**Implementation**:
```python
import anthropic

def create_client(api_key: str) -> anthropic.Anthropic:
    # Validate key format
    if not api_key.startswith("sk-ant-"):
        raise ValueError("Invalid API key format")

    # Create client
    client = anthropic.Anthropic(api_key=api_key)
    return client
```

**Acceptance Criteria**:
- [ ] Client created successfully
- [ ] Key validation works
- [ ] Invalid key raises ValueError

---

### API-002: Implement calculate_cost()
**Priority**: High
**Duration**: 10 min
**Dependencies**: CORE-001
**File**: `context_window_vs_rag/query_processor.py`
**Function**: `calculate_cost()`

**Signature**:
```python
def calculate_cost(input_tokens: int, output_tokens: int) -> float:
    """
    Calculate cost in USD based on Haiku 4.5 pricing.

    Pricing:
    - Input: $0.80 per million tokens
    - Output: $4.00 per million tokens

    Args:
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens

    Returns:
        Total cost in USD

    Example:
        >>> calculate_cost(10000, 500)
        0.01
    """
```

**Implementation**:
```python
def calculate_cost(input_tokens: int, output_tokens: int) -> float:
    input_cost = (input_tokens / 1_000_000) * config.COST_PER_MILLION_INPUT
    output_cost = (output_tokens / 1_000_000) * config.COST_PER_MILLION_OUTPUT
    return input_cost + output_cost
```

**Testing**:
```python
assert calculate_cost(1_000_000, 0) == 0.80
assert calculate_cost(0, 1_000_000) == 4.00
assert calculate_cost(10_000, 500) == 0.01
```

**Acceptance Criteria**:
- [ ] Cost calculation correct
- [ ] Handles edge cases (0 tokens)
- [ ] Returns float

---

### API-003: Implement query_claude_with_timing()
**Priority**: Critical
**Duration**: 40 min
**Dependencies**: API-001, API-002
**File**: `context_window_vs_rag/query_processor.py`
**Function**: `query_claude_with_timing()`

**Signature**:
```python
def query_claude_with_timing(
    api_key: str,
    content: str,
    query: str
) -> Dict[str, Any]:
    """
    Query Claude with accurate timing and retry logic.

    Args:
        api_key: Anthropic API key
        content: Document content (full or chunks)
        query: Question to ask

    Returns:
        {
            "answer": str,
            "time_seconds": float,
            "input_tokens": int,
            "output_tokens": int,
            "total_tokens": int,
            "cost": float
        }

    Raises:
        anthropic.APIError: If API fails after max retries
    """
```

**Implementation Steps**:
1. Create client
2. Build prompt: `f"{content}\n\nQuestion: {query}"`
3. Start timer (time.time())
4. Implement retry loop (max 3 attempts)
5. API call: client.messages.create()
6. Stop timer
7. Extract response, tokens
8. Calculate cost
9. Return structured dict

**Testing**:
```python
result = query_claude_with_timing(api_key, "Test content", "What is this?")
assert "answer" in result
assert result["time_seconds"] > 0
assert result["input_tokens"] > 0
```

**Acceptance Criteria**:
- [ ] Returns valid response
- [ ] Timing accurate (±50ms)
- [ ] Retry logic works
- [ ] Token counts extracted
- [ ] Cost calculated
- [ ] Function: 60-80 lines

---

### API-004: Complete query_processor.py
**Priority**: Critical
**Duration**: 15 min
**Dependencies**: API-001, API-002, API-003
**File**: `context_window_vs_rag/query_processor.py`

**Tasks**:
1. Add module docstring
2. Add all imports
3. Add logger initialization
4. Add type hints throughout
5. Add comprehensive docstrings
6. Add error handling

**Acceptance Criteria**:
- [ ] All functions implemented
- [ ] Module complete
- [ ] Line count: 150-200 lines
- [ ] Passes all tests

---

## Method Implementation Tasks

### METHOD-001: Implement prepare_full_context()
**Priority**: High
**Duration**: 10 min
**Dependencies**: None
**File**: `context_window_vs_rag/context_window_method.py`
**Function**: `prepare_full_context()`

**Signature**:
```python
def prepare_full_context(documents: List[str]) -> str:
    """
    Concatenate all documents with separators.

    Args:
        documents: List of document texts

    Returns:
        Single concatenated string with document separators

    Example:
        >>> docs = ["Doc 1", "Doc 2"]
        >>> prepare_full_context(docs)
        'Doc 1\\n\\n--- DOCUMENT ---\\n\\nDoc 2'
    """
```

**Acceptance Criteria**:
- [ ] All documents concatenated
- [ ] Clear separators used
- [ ] Returns single string

---

### METHOD-002: Implement query_full_context()
**Priority**: Critical
**Duration**: 15 min
**Dependencies**: METHOD-001, API-003
**File**: `context_window_vs_rag/context_window_method.py`
**Function**: `query_full_context()`

**Signature**:
```python
def query_full_context(
    api_key: str,
    documents: List[str],
    query: str
) -> Dict[str, Any]:
    """
    Query Claude with all documents in context.

    Args:
        api_key: Anthropic API key
        documents: List of document texts
        query: Question to ask

    Returns:
        Result dictionary from query_processor
    """
```

**Acceptance Criteria**:
- [ ] Calls prepare_full_context()
- [ ] Calls query_claude_with_timing()
- [ ] Returns result dict

---

### METHOD-003: Implement run_context_window_iterations()
**Priority**: Critical
**Duration**: 20 min
**Dependencies**: METHOD-002
**File**: `context_window_vs_rag/context_window_method.py`
**Function**: `run_context_window_iterations()`

**Signature**:
```python
def run_context_window_iterations(
    api_key: str,
    documents: List[str],
    query: str,
    iterations: int = 5
) -> List[Dict[str, Any]]:
    """
    Run multiple iterations of Context Window method.

    Args:
        api_key: Anthropic API key
        documents: List of document texts
        query: Question to ask
        iterations: Number of test iterations

    Returns:
        List of result dictionaries (one per iteration)
    """
```

**Implementation**:
```python
results = []
for i in range(1, iterations + 1):
    logger.info(f"Iteration {i}/{iterations}...")
    result = query_full_context(api_key, documents, query)
    result["iteration"] = i
    results.append(result)

    # Log summary
    logger.info(f"Time: {result['time_seconds']:.2f}s, "
                f"Tokens: {result['input_tokens']}/{result['output_tokens']}")

    # Delay between iterations (rate limiting)
    if i < iterations:
        time.sleep(config.RETRY_DELAY)

return results
```

**Acceptance Criteria**:
- [ ] Runs N iterations
- [ ] Each iteration logged
- [ ] Delays between iterations
- [ ] Returns list of results

---

### METHOD-004: Complete context_window_method.py
**Priority**: Critical
**Duration**: 15 min
**Dependencies**: METHOD-001, METHOD-002, METHOD-003
**File**: `context_window_vs_rag/context_window_method.py`

**Acceptance Criteria**:
- [ ] All functions implemented
- [ ] Module docstring present
- [ ] Line count: 150-200 lines
- [ ] Passes all tests

---

### METHOD-005: Implement chunk_text()
**Priority**: Critical
**Duration**: 25 min
**Dependencies**: CORE-001
**File**: `context_window_vs_rag/rag_method.py`
**Function**: `chunk_text()`

**Signature**:
```python
def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50
) -> List[str]:
    """
    Split text into overlapping chunks by word count.

    Args:
        text: Input text
        chunk_size: Words per chunk (default: 500)
        overlap: Word overlap between chunks (default: 50)

    Returns:
        List of text chunks

    Example:
        >>> text = "word " * 1000
        >>> chunks = chunk_text(text, chunk_size=500, overlap=50)
        >>> len(chunks)
        3
    """
```

**Implementation**:
```python
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    words = text.split()

    if len(words) <= chunk_size:
        return [text]

    chunks = []
    step = chunk_size - overlap

    for i in range(0, len(words), step):
        chunk_words = words[i:i + chunk_size]
        chunks.append(" ".join(chunk_words))

        if i + chunk_size >= len(words):
            break

    return chunks
```

**Testing**:
```python
# Test normal case
text = "word " * 1000
chunks = chunk_text(text, chunk_size=500, overlap=50)
assert len(chunks) > 1

# Test short text
short = "word " * 100
chunks = chunk_text(short, chunk_size=500)
assert len(chunks) == 1

# Test overlap
chunk1_words = chunks[0].split()
chunk2_words = chunks[1].split()
# Last 50 words of chunk1 should match first 50 of chunk2
assert chunk1_words[-50:] == chunk2_words[:50]
```

**Acceptance Criteria**:
- [ ] Chunks have correct word count
- [ ] Overlap works correctly
- [ ] Handles short texts
- [ ] Function: 20-30 lines

---

### METHOD-006: Implement get_embedding_model()
**Priority**: High
**Duration**: 10 min
**Dependencies**: CORE-001
**File**: `context_window_vs_rag/rag_method.py`
**Function**: `get_embedding_model()`

**Implementation**:
```python
from sentence_transformers import SentenceTransformer

# Global model (singleton pattern)
_embedding_model = None

def get_embedding_model() -> SentenceTransformer:
    """
    Lazy load embedding model (singleton).

    Returns:
        SentenceTransformer model

    Note:
        Model is loaded only once and cached globally.
    """
    global _embedding_model
    if _embedding_model is None:
        logger.info(f"Loading embedding model: {config.EMBEDDING_MODEL}")
        _embedding_model = SentenceTransformer(config.EMBEDDING_MODEL)
        logger.info("Embedding model loaded successfully")
    return _embedding_model
```

**Acceptance Criteria**:
- [ ] Model loads successfully
- [ ] Singleton pattern works (loaded once)
- [ ] Returns SentenceTransformer instance

---

### METHOD-007: Implement build_vector_db()
**Priority**: Critical
**Duration**: 40 min
**Dependencies**: METHOD-005, METHOD-006
**File**: `context_window_vs_rag/rag_method.py`
**Function**: `build_vector_db()`

**Signature**:
```python
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
        >>> docs = load_all_pdfs("./docs")
        >>> collection = build_vector_db(docs)
        >>> collection.count()
        1234
    """
```

**Implementation Steps**:
1. Chunk all documents
2. Track metadata (doc index, chunk index)
3. Get embedding model
4. Generate embeddings (batch)
5. Create ChromaDB collection
6. Add chunks to collection
7. Return collection

**Acceptance Criteria**:
- [ ] All documents chunked
- [ ] Embeddings generated
- [ ] Collection created successfully
- [ ] Function: 40-60 lines

---

### METHOD-008: Implement retrieve_top_k()
**Priority**: Critical
**Duration**: 20 min
**Dependencies**: METHOD-006, METHOD-007
**File**: `context_window_vs_rag/rag_method.py`
**Function**: `retrieve_top_k()`

**Signature**:
```python
def retrieve_top_k(
    query: str,
    collection: chromadb.Collection,
    k: int = 3
) -> List[str]:
    """
    Retrieve top K most relevant chunks.

    Args:
        query: Question string
        collection: Vector database collection
        k: Number of chunks to retrieve

    Returns:
        List of top K chunk texts

    Example:
        >>> chunks = retrieve_top_k("side effects?", collection, k=3)
        >>> len(chunks)
        3
    """
```

**Implementation**:
```python
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
return top_chunks
```

**Acceptance Criteria**:
- [ ] Returns exactly K chunks
- [ ] Chunks are relevant (manual inspection)
- [ ] Function: 15-25 lines

---

### METHOD-009: Implement query_with_rag()
**Priority**: Critical
**Duration**: 25 min
**Dependencies**: METHOD-007, METHOD-008, API-003
**File**: `context_window_vs_rag/rag_method.py`
**Function**: `query_with_rag()`

**Signature**:
```python
def query_with_rag(
    api_key: str,
    documents: List[str],
    query: str
) -> Dict[str, Any]:
    """
    Query using full RAG pipeline with timing.

    Pipeline:
    1. Build vector database (includes chunking + embedding)
    2. Retrieve top K chunks
    3. Query Claude with retrieved chunks

    Time measurement includes all steps.

    Args:
        api_key: Anthropic API key
        documents: List of document texts
        query: Question to ask

    Returns:
        Result dictionary with full pipeline time
    """
```

**Implementation**:
```python
import time

start_time = time.time()

# Build vector DB
collection = build_vector_db(documents)

# Retrieve top K
top_chunks = retrieve_top_k(query, collection, config.TOP_K_CHUNKS)

# Combine chunks
rag_context = "\n\n--- CHUNK ---\n\n".join(top_chunks)

# Query Claude
result = query_claude_with_timing(api_key, rag_context, query)

# Update total time
total_time = time.time() - start_time
result["time_seconds"] = total_time
result["rag_chunks"] = len(top_chunks)

return result
```

**Acceptance Criteria**:
- [ ] Full pipeline executed
- [ ] Time includes all steps
- [ ] Returns result dict

---

### METHOD-010: Implement run_rag_iterations()
**Priority**: Critical
**Duration**: 20 min
**Dependencies**: METHOD-009
**File**: `context_window_vs_rag/rag_method.py`
**Function**: `run_rag_iterations()`

**Signature**:
```python
def run_rag_iterations(
    api_key: str,
    documents: List[str],
    query: str,
    iterations: int = 5
) -> List[Dict[str, Any]]:
    """
    Run multiple RAG iterations.

    Note: Vector DB built once (before iterations), then queries run
    multiple times for consistent timing measurement.

    Args:
        api_key: Anthropic API key
        documents: List of document texts
        query: Question to ask
        iterations: Number of test iterations

    Returns:
        List of result dictionaries
    """
```

**Implementation**:
```python
# Build vector DB once
logger.info("Building vector database...")
collection = build_vector_db(documents)
logger.info(f"Vector database built: {collection.count()} chunks")

results = []
for i in range(1, iterations + 1):
    logger.info(f"Iteration {i}/{iterations}...")

    # Retrieve and query (timed)
    start_time = time.time()
    top_chunks = retrieve_top_k(query, collection, config.TOP_K_CHUNKS)
    rag_context = "\n\n--- CHUNK ---\n\n".join(top_chunks)
    result = query_claude_with_timing(api_key, rag_context, query)
    result["time_seconds"] = time.time() - start_time

    result["iteration"] = i
    results.append(result)

    # Log summary
    logger.info(f"Time: {result['time_seconds']:.2f}s, "
                f"Tokens: {result['input_tokens']}/{result['output_tokens']}")

    if i < iterations:
        time.sleep(config.RETRY_DELAY)

return results
```

**Acceptance Criteria**:
- [ ] Vector DB built once
- [ ] Multiple iterations work
- [ ] Timing consistent
- [ ] Function: 30-40 lines

---

### METHOD-011: Complete rag_method.py
**Priority**: Critical
**Duration**: 20 min
**Dependencies**: METHOD-005 through METHOD-010
**File**: `context_window_vs_rag/rag_method.py`

**Tasks**:
1. Add module docstring
2. Add all imports
3. Add logger initialization
4. Ensure all functions complete
5. Add type hints
6. Add comprehensive docstrings

**Acceptance Criteria**:
- [ ] All functions implemented
- [ ] Module complete
- [ ] Line count: 150-200 lines
- [ ] Passes all tests

---

## Analysis Tasks

### ANALYSIS-001: Implement calculate_stats()
**Priority**: High
**Duration**: 20 min
**Dependencies**: CORE-001
**File**: `context_window_vs_rag/results_analyzer.py`
**Function**: `calculate_stats()`

**Signature**:
```python
def calculate_stats(results: List[Dict]) -> Dict[str, float]:
    """
    Calculate statistics from results.

    Metrics calculated:
    - time_mean, time_std, time_min, time_max
    - input_tokens_mean, input_tokens_std
    - output_tokens_mean, output_tokens_std
    - cost_mean, cost_std, cost_total

    Args:
        results: List of result dictionaries

    Returns:
        Dictionary of statistical metrics
    """
```

**Implementation**:
```python
import numpy as np

def calculate_stats(results: List[Dict]) -> Dict[str, float]:
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
        "input_tokens_std": np.std(input_tokens),
        "output_tokens_mean": np.mean(output_tokens),
        "output_tokens_std": np.std(output_tokens),
        "cost_mean": np.mean(costs),
        "cost_std": np.std(costs),
        "cost_total": np.sum(costs)
    }
```

**Acceptance Criteria**:
- [ ] All statistics calculated
- [ ] Uses numpy for calculations
- [ ] Returns structured dict

---

### ANALYSIS-002: Implement calculate_similarity()
**Priority**: Medium
**Duration**: 15 min
**Dependencies**: None
**File**: `context_window_vs_rag/results_analyzer.py`
**Function**: `calculate_similarity()`

**Signature**:
```python
def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculate semantic similarity between two texts.

    Uses sentence-transformers with cosine similarity.

    Args:
        text1: First text
        text2: Second text

    Returns:
        Similarity score (0-1, where 1 is identical)

    Example:
        >>> sim = calculate_similarity("Ben Gurion", "Ben Gurion")
        >>> sim > 0.99
        True
    """
```

**Implementation**:
```python
from sentence_transformers import SentenceTransformer, util

def calculate_similarity(text1: str, text2: str) -> float:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    emb1 = model.encode(text1, convert_to_tensor=True)
    emb2 = model.encode(text2, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(emb1, emb2).item()
    return similarity
```

**Acceptance Criteria**:
- [ ] Returns float 0-1
- [ ] Identical texts score > 0.99
- [ ] Different texts score < 0.5

---

### ANALYSIS-003: Implement compare_methods()
**Priority**: Critical
**Duration**: 25 min
**Dependencies**: ANALYSIS-001, ANALYSIS-002
**File**: `context_window_vs_rag/results_analyzer.py`
**Function**: `compare_methods()`

**Signature**:
```python
def compare_methods(
    cw_results: List[Dict],
    rag_results: List[Dict]
) -> Dict[str, Any]:
    """
    Compare Context Window vs RAG methods.

    Calculates:
    - Statistics for each method
    - Savings percentages (time, tokens, cost)
    - Answer similarity

    Args:
        cw_results: Context Window results
        rag_results: RAG results

    Returns:
        Comparison dictionary
    """
```

**Acceptance Criteria**:
- [ ] Both methods compared
- [ ] Savings calculated correctly
- [ ] Answer similarity computed
- [ ] Function: 30-40 lines

---

### ANALYSIS-004: Implement print_summary()
**Priority**: High
**Duration**: 30 min
**Dependencies**: ANALYSIS-003
**File**: `context_window_vs_rag/results_analyzer.py`
**Function**: `print_summary()`

**Signature**:
```python
def print_summary(comparison: Dict) -> None:
    """
    Print formatted summary report to console.

    Format:
    - Context Window statistics
    - RAG statistics
    - Comparison metrics (savings)

    Args:
        comparison: Comparison dictionary from compare_methods()
    """
```

**Acceptance Criteria**:
- [ ] Report is readable
- [ ] All metrics displayed
- [ ] Professional formatting
- [ ] Function: 40-60 lines

---

### ANALYSIS-005: Complete results_analyzer.py
**Priority**: Critical
**Duration**: 15 min
**Dependencies**: ANALYSIS-001 through ANALYSIS-004
**File**: `context_window_vs_rag/results_analyzer.py`

**Acceptance Criteria**:
- [ ] All functions implemented
- [ ] Module complete
- [ ] Line count: 150-200 lines
- [ ] Passes all tests

---

## Visualization Tasks

### VIZ-001: Implement plot_response_time()
**Priority**: High
**Duration**: 20 min
**Dependencies**: CORE-001
**File**: `context_window_vs_rag/visualization.py`
**Function**: `plot_response_time()`

**Acceptance Criteria**:
- [ ] Bar chart with error bars
- [ ] Clear labels and title
- [ ] PNG saved successfully
- [ ] Function: 20-30 lines

---

### VIZ-002: Implement plot_token_usage()
**Priority**: High
**Duration**: 20 min
**Dependencies**: CORE-001
**File**: `context_window_vs_rag/visualization.py`
**Function**: `plot_token_usage()`

**Acceptance Criteria**:
- [ ] Grouped bar chart
- [ ] Input vs output tokens shown
- [ ] PNG saved successfully

---

### VIZ-003: Implement plot_cost_comparison()
**Priority**: High
**Duration**: 20 min
**Dependencies**: CORE-001
**File**: `context_window_vs_rag/visualization.py`
**Function**: `plot_cost_comparison()`

**Acceptance Criteria**:
- [ ] Bar chart created
- [ ] Cost displayed in USD
- [ ] PNG saved successfully

---

### VIZ-004: Implement plot_iterations_timeline()
**Priority**: High
**Duration**: 25 min
**Dependencies**: CORE-001
**File**: `context_window_vs_rag/visualization.py`
**Function**: `plot_iterations_timeline()`

**Acceptance Criteria**:
- [ ] Line plot with markers
- [ ] Two lines (CW and RAG)
- [ ] Legend present
- [ ] PNG saved successfully

---

### VIZ-005: Implement generate_all_graphs()
**Priority**: High
**Duration**: 15 min
**Dependencies**: VIZ-001 through VIZ-004
**File**: `context_window_vs_rag/visualization.py`
**Function**: `generate_all_graphs()`

**Acceptance Criteria**:
- [ ] Calls all plot functions
- [ ] All 4 graphs generated
- [ ] Logs completion

---

### VIZ-006: Complete visualization.py
**Priority**: Critical
**Duration**: 15 min
**Dependencies**: VIZ-001 through VIZ-005
**File**: `context_window_vs_rag/visualization.py`

**Acceptance Criteria**:
- [ ] All functions implemented
- [ ] Module complete
- [ ] Line count: 150-200 lines
- [ ] Passes all tests

---

## Integration Tasks

### INT-001: Implement load_api_key()
**Priority**: Critical
**Duration**: 15 min
**Dependencies**: CORE-001, CORE-002
**File**: `context_window_vs_rag/main.py`
**Function**: `load_api_key()`

**Signature**:
```python
def load_api_key() -> str:
    """
    Load API key from file with validation.

    Returns:
        API key string

    Raises:
        FileNotFoundError: If api_key.dat not found
        ValueError: If API key format is invalid

    SECURITY: Never logs or prints the actual API key.
    """
```

**Acceptance Criteria**:
- [ ] Reads from file
- [ ] Validates format
- [ ] NEVER logs the key
- [ ] Function: 15-20 lines

---

### INT-002: Implement save_results_to_json()
**Priority**: Medium
**Duration**: 15 min
**Dependencies**: None
**File**: `context_window_vs_rag/main.py`
**Function**: `save_results_to_json()`

**Acceptance Criteria**:
- [ ] Saves to JSON file
- [ ] Includes metadata (timestamp, etc.)
- [ ] Formatted nicely (indent=2)

---

### INT-003: Implement main()
**Priority**: Critical
**Duration**: 45 min
**Dependencies**: All previous tasks
**File**: `context_window_vs_rag/main.py`
**Function**: `main()`

**Workflow**:
1. Setup (logging, API key)
2. Load PDFs
3. Run Context Window tests
4. Run RAG tests
5. Analyze results
6. Generate visualizations
7. Print summary
8. Save results

**Acceptance Criteria**:
- [ ] Complete end-to-end flow
- [ ] All steps execute correctly
- [ ] Errors handled gracefully
- [ ] Function: 80-100 lines

---

### INT-004: Complete main.py
**Priority**: Critical
**Duration**: 20 min
**Dependencies**: INT-001, INT-002, INT-003
**File**: `context_window_vs_rag/main.py`

**Acceptance Criteria**:
- [ ] All functions implemented
- [ ] Module complete
- [ ] Line count: 150-200 lines
- [ ] __main__ block present

---

## Testing Tasks

### TEST-001: Unit Test Logger
**Priority**: High
**Duration**: 15 min

**Tests**:
- Logger created successfully
- Log directory created
- Logs written to files
- Console output visible

---

### TEST-002: Unit Test PDF Loader
**Priority**: High
**Duration**: 20 min

**Tests**:
- Single PDF loads correctly
- All PDFs load (multiprocessing)
- Corrupted PDF handled
- Output sorted by filename

---

### TEST-003: Unit Test Query Processor
**Priority**: High
**Duration**: 25 min

**Tests**:
- API client created
- Query returns valid response
- Timing accurate
- Cost calculation correct
- Retry logic works

---

### TEST-004: Unit Test RAG Components
**Priority**: High
**Duration**: 30 min

**Tests**:
- Chunking produces correct chunks
- Overlap works
- Embeddings generated
- Vector search retrieves K chunks

---

### TEST-005: Integration Test (Small Scale)
**Priority**: Critical
**Duration**: 30 min

**Test Setup**:
- Use 2-3 small PDFs
- Run 2 iterations per method

**Validation**:
- End-to-end flow works
- Both methods return answers
- Graphs generated
- Results saved

---

### TEST-006: Integration Test (Full Scale)
**Priority**: Critical
**Duration**: 45 min

**Test Setup**:
- Use all 20 PDFs
- Run 5 iterations per method

**Validation**:
- All 10 queries complete
- RAG faster than Context Window
- Token savings significant
- Cost savings significant
- Answer quality good

---

## Documentation Tasks

### DOC-001: Create README.md
**Priority**: High
**Duration**: 30 min

**Contents**:
- Project overview
- Installation instructions
- Usage guide
- Example output
- Troubleshooting

---

### DOC-002: Add Function Docstrings
**Priority**: High
**Duration**: 30 min

**Tasks**:
- All functions have docstrings
- Args and returns documented
- Examples provided where helpful

---

### DOC-003: Add Module Docstrings
**Priority**: Medium
**Duration**: 15 min

**Tasks**:
- All modules have docstrings
- Purpose clearly stated
- Usage examples provided

---

**Total Tasks**: 74
**Total Estimated Time**: ~10-12 hours
**Status**: Ready for Implementation
