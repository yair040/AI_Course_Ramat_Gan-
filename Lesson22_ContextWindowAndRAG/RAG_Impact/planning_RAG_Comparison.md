# Planning Document
# Context Window vs RAG Comparison Project

**Project**: Context Window vs RAG Performance Benchmarking
**Author**: Yair Levi
**Date**: 2025-12-15

---

## Table of Contents

1. [Overview](#overview)
2. [Development Phases](#development-phases)
3. [Module Dependencies](#module-dependencies)
4. [Implementation Order](#implementation-order)
5. [Testing Strategy](#testing-strategy)
6. [Timeline](#timeline)
7. [Risk Management](#risk-management)

---

## Overview

### Project Goal
Build a Python package that empirically compares Context Window vs RAG methods for document retrieval across 20 PDF files.

### Key Metrics
- Response time (seconds)
- Token usage (input/output)
- Cost (USD)
- Answer quality (semantic similarity)

### Deliverables
- Python package: `context_window_vs_rag/`
- 4 visualization graphs
- Statistical summary report
- Raw results JSON file
- Ring buffer logs (20 × 16MB)

---

## Development Phases

### Phase 1: Setup & Configuration
**Duration**: 30 minutes

**Tasks**:
1. Create directory structure
2. Create virtual environment
3. Create `requirements.txt`
4. Install dependencies
5. Create `config.py` with all constants
6. Create `.gitignore` (include `api_key.dat`, `venv/`, `__pycache__/`)
7. Verify `api_key.dat` exists and is valid
8. Verify `./docs/` contains 20 PDF files

**Deliverables**:
- Working virtual environment
- Installed dependencies
- Configuration file
- Validated environment

**Success Criteria**:
- `pip install -r requirements.txt` succeeds
- `import anthropic` works
- API key file exists and readable

---

### Phase 2: Core Infrastructure
**Duration**: 1 hour

#### Task 2.1: Logger Setup (30 min)
**File**: `logger_setup.py`

**Implementation**:
```python
def setup_logger(name: str = "context_window_vs_rag") -> logging.Logger:
    """
    Setup ring buffer logger with 20 files × 16MB.

    Returns:
        Configured logger instance
    """
    # Create log directory
    # Configure RotatingFileHandler
    # Add console handler
    # Return logger
```

**Testing**:
- Log directory created automatically
- Logs written to files
- Rotation works (create 20+ test logs)

#### Task 2.2: Config Module (15 min)
**File**: `config.py`

**Contents**:
- All paths (docs, log, results)
- API settings (model, tokens, timeout)
- RAG settings (chunk size, overlap, top K)
- Test settings (iterations, query)
- Logging settings
- Visualization settings
- Cost settings

**Testing**:
- All imports work
- No syntax errors
- Constants accessible

#### Task 2.3: Package Initialization (15 min)
**File**: `__init__.py`

**Contents**:
```python
"""
Context Window vs RAG Comparison Package.

Compares full context loading vs RAG for document retrieval.
"""

__version__ = "1.0.0"
__author__ = "Yair Levi"

# Import main function for easy access
from .main import main

__all__ = ["main"]
```

**Testing**:
- Package imports correctly: `import context_window_vs_rag`
- Version accessible: `context_window_vs_rag.__version__`

---

### Phase 3: PDF Processing
**Duration**: 45 minutes

#### Task 3.1: PDF Loader (45 min)
**File**: `pdf_loader.py`

**Functions**:
```python
def load_single_pdf(pdf_path: str) -> Tuple[str, str]:
    """
    Load one PDF and extract text.

    Args:
        pdf_path: Path to PDF file

    Returns:
        (filename, extracted_text)
    """
    # Try pdfplumber first
    # Fallback to PyPDF2
    # Handle errors gracefully
    # Return (filename, text)

def load_all_pdfs(docs_dir: str) -> List[str]:
    """
    Load all PDFs using multiprocessing.

    Args:
        docs_dir: Directory containing PDF files

    Returns:
        List of extracted text strings (sorted by filename)
    """
    # Get all PDF file paths
    # Use multiprocessing.Pool
    # Load in parallel
    # Sort by filename
    # Return list of texts

def validate_pdf(pdf_path: str) -> bool:
    """
    Check if PDF is readable.

    Args:
        pdf_path: Path to PDF file

    Returns:
        True if readable, False otherwise
    """
    # Try to open and read first page
    # Return success status
```

**Testing**:
- Load single PDF successfully
- Extract readable text
- Handle corrupted PDF gracefully
- Multiprocessing works (load 20 PDFs)
- Output sorted correctly

**Edge Cases**:
- Empty PDF
- Corrupted PDF
- Scanned PDF (image-only, no text)
- Password-protected PDF

---

### Phase 4: Query Processing
**Duration**: 45 minutes

#### Task 4.1: Query Processor (45 min)
**File**: `query_processor.py`

**Functions**:
```python
def create_client(api_key: str) -> anthropic.Anthropic:
    """Create Anthropic API client."""
    # Validate API key format
    # Create and return client

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
    """
    # Create client
    # Build prompt
    # Start timer
    # API call with retry logic
    # Stop timer
    # Extract response
    # Calculate cost
    # Return structured result

def calculate_cost(input_tokens: int, output_tokens: int) -> float:
    """Calculate cost in USD based on Haiku pricing."""
    # Input: $0.80 per million
    # Output: $4.00 per million
    # Return total cost
```

**Testing**:
- API client creation succeeds
- Query returns valid response
- Timing accurate (compare with manual timing)
- Token counts match API response
- Cost calculation correct
- Retry logic works (simulate API failure)

**Error Handling**:
- Authentication errors
- Rate limiting (429 errors)
- Timeout errors
- Network errors
- Invalid responses

---

### Phase 5: Context Window Method
**Duration**: 30 minutes

#### Task 5.1: Context Window Implementation (30 min)
**File**: `context_window_method.py`

**Functions**:
```python
def prepare_full_context(documents: List[str]) -> str:
    """
    Concatenate all documents with separators.

    Args:
        documents: List of document texts

    Returns:
        Single concatenated string
    """
    # Join with clear separators
    # Return full context

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
        Result dictionary with answer, time, tokens, cost
    """
    # Prepare full context
    # Call query_processor
    # Return result

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
        List of result dictionaries
    """
    # Loop through iterations
    # Call query_full_context each time
    # Add iteration number to result
    # Add delay between iterations
    # Return all results
```

**Testing**:
- Context concatenation correct
- All documents included
- Query returns valid answer
- Timing measured correctly
- Multiple iterations work
- Results list structured correctly

---

### Phase 6: RAG Method
**Duration**: 1.5 hours

#### Task 6.1: Text Chunking (20 min)
**Function**: `chunk_text()`

**Implementation**:
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
        chunk_size: Words per chunk
        overlap: Word overlap between chunks

    Returns:
        List of text chunks
    """
    # Split into words
    # Create sliding window chunks
    # Handle edge cases (text shorter than chunk_size)
    # Return list of chunks
```

**Testing**:
- Chunks have correct word count (±5 words tolerance)
- Overlap works correctly
- Last chunk handled properly
- Short texts handled (< chunk_size)

#### Task 6.2: Embedding Generation (30 min)
**Functions**: `get_embedding_model()`, `generate_embeddings()`

**Implementation**:
```python
# Global model (load once)
_embedding_model = None

def get_embedding_model() -> SentenceTransformer:
    """Lazy load embedding model (singleton pattern)."""
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer(config.EMBEDDING_MODEL)
    return _embedding_model

def generate_embeddings(texts: List[str]) -> np.ndarray:
    """
    Generate embeddings for list of texts.

    Args:
        texts: List of text strings

    Returns:
        Numpy array of embeddings (shape: [n_texts, embedding_dim])
    """
    # Get model
    # Encode texts (batch processing)
    # Return embeddings
```

**Testing**:
- Model loads successfully
- Embeddings generated correctly
- Model loaded only once (singleton)
- Batch processing works

#### Task 6.3: Vector Database (40 min)
**Functions**: `build_vector_db()`, `retrieve_top_k()`

**Implementation**:
```python
def build_vector_db(documents: List[str]) -> chromadb.Collection:
    """
    Build vector database from all documents.

    Args:
        documents: List of document texts

    Returns:
        ChromaDB collection with all chunks
    """
    # Chunk all documents
    # Track document indices
    # Generate embeddings
    # Create ChromaDB collection
    # Add chunks with embeddings
    # Return collection

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
    """
    # Generate query embedding
    # Search collection
    # Extract top K results
    # Return chunk texts

def query_with_rag(
    api_key: str,
    documents: List[str],
    query: str
) -> Dict[str, Any]:
    """
    Query using full RAG pipeline with timing.

    Args:
        api_key: Anthropic API key
        documents: List of document texts
        query: Question to ask

    Returns:
        Result dictionary (includes RAG setup time)
    """
    # Start timer
    # Build vector database
    # Retrieve top K chunks
    # Combine chunks
    # Query Claude
    # Stop timer (full pipeline)
    # Update time in result
    # Return result

def run_rag_iterations(
    api_key: str,
    documents: List[str],
    query: str,
    iterations: int = 5
) -> List[Dict[str, Any]]:
    """
    Run multiple RAG iterations.

    Note: Vector DB built once, queries run multiple times.

    Args:
        api_key: Anthropic API key
        documents: List of document texts
        query: Question to ask
        iterations: Number of test iterations

    Returns:
        List of result dictionaries
    """
    # Build vector DB once (before iterations)
    # Loop through iterations
    # Each iteration: retrieve + query
    # Add delay between iterations
    # Return all results
```

**Testing**:
- Chunking produces expected number of chunks
- Vector database builds successfully
- Retrieval returns K chunks
- Retrieved chunks are relevant
- Full pipeline timing accurate
- Multiple iterations work

---

### Phase 7: Analysis & Visualization
**Duration**: 1.5 hours

#### Task 7.1: Statistical Analysis (45 min)
**File**: `results_analyzer.py`

**Functions**:
```python
def calculate_stats(results: List[Dict]) -> Dict[str, float]:
    """Calculate mean, std, min, max for all metrics."""
    # Extract metrics from results
    # Calculate statistics
    # Return structured dict

def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate semantic similarity using sentence-transformers."""
    # Load model
    # Generate embeddings
    # Calculate cosine similarity
    # Return score

def compare_methods(
    cw_results: List[Dict],
    rag_results: List[Dict]
) -> Dict[str, Any]:
    """
    Compare Context Window vs RAG methods.

    Returns:
        {
            "cw_stats": {...},
            "rag_stats": {...},
            "time_savings": float,
            "token_savings": float,
            "cost_savings": float,
            "answer_similarity": float
        }
    """
    # Calculate stats for each method
    # Calculate savings percentages
    # Calculate answer similarity
    # Return comparison dict

def print_summary(comparison: Dict) -> None:
    """Print formatted summary report to console."""
    # Extract stats
    # Format nicely
    # Print report
```

**Testing**:
- Statistics calculated correctly
- Savings percentages accurate
- Similarity score reasonable (0.8-1.0)
- Summary report readable

#### Task 7.2: Visualization (45 min)
**File**: `visualization.py`

**Functions**:
```python
def plot_response_time(cw_stats: Dict, rag_stats: Dict) -> None:
    """Generate response time bar chart with error bars."""
    # Create figure
    # Plot bars with error bars
    # Add labels, title
    # Save PNG

def plot_token_usage(cw_stats: Dict, rag_stats: Dict) -> None:
    """Generate token usage grouped bar chart."""
    # Create figure
    # Plot grouped bars (input vs output)
    # Add labels, title
    # Save PNG

def plot_cost_comparison(cw_stats: Dict, rag_stats: Dict) -> None:
    """Generate cost comparison bar chart."""
    # Create figure
    # Plot bars
    # Add labels, title
    # Save PNG

def plot_iterations_timeline(
    cw_results: List[Dict],
    rag_results: List[Dict]
) -> None:
    """Generate iteration timeline line plot."""
    # Create figure
    # Plot two lines
    # Add markers
    # Add labels, title, legend
    # Save PNG

def generate_all_graphs(
    cw_results: List[Dict],
    rag_results: List[Dict]
) -> None:
    """Generate all visualization graphs."""
    # Calculate stats
    # Call all plot functions
    # Log completion
```

**Testing**:
- All 4 graphs generated
- Graphs have correct data
- Labels and titles clear
- PNG files saved correctly
- High resolution (300 DPI)

---

### Phase 8: Main Orchestration
**Duration**: 45 minutes

#### Task 8.1: Main Module (45 min)
**File**: `main.py`

**Functions**:
```python
def load_api_key() -> str:
    """Load API key from file with validation."""
    # Read from api_key.dat
    # Strip whitespace
    # Validate format
    # Return key (NEVER log it)

def save_results_to_json(
    cw_results: List[Dict],
    rag_results: List[Dict],
    filename: str = "results.json"
) -> None:
    """Save raw results to JSON file."""
    # Create results dict
    # Add metadata (timestamp, etc.)
    # Write to JSON file

def main() -> None:
    """
    Main orchestration function.

    Workflow:
    1. Setup (logging, API key, directories)
    2. Load PDFs
    3. Run Context Window tests (5 iterations)
    4. Run RAG tests (5 iterations)
    5. Analyze results
    6. Generate visualizations
    7. Print summary
    8. Save results
    """
    # 1. Setup
    logger = setup_logger()
    logger.info("Starting Context Window vs RAG comparison...")

    api_key = load_api_key()
    logger.info("API key loaded successfully")

    # 2. Load PDFs
    logger.info(f"Loading PDFs from {config.DOCS_DIR}...")
    documents = load_all_pdfs(config.DOCS_DIR)
    logger.info(f"Loaded {len(documents)} documents")

    # 3. Context Window Method
    logger.info("="*50)
    logger.info("CONTEXT WINDOW METHOD (5 iterations)")
    logger.info("="*50)
    cw_results = run_context_window_iterations(
        api_key, documents, config.QUERY, config.ITERATIONS
    )

    # 4. RAG Method
    logger.info("="*50)
    logger.info("RAG METHOD (5 iterations)")
    logger.info("="*50)
    rag_results = run_rag_iterations(
        api_key, documents, config.QUERY, config.ITERATIONS
    )

    # 5. Analysis
    logger.info("Analyzing results...")
    comparison = compare_methods(cw_results, rag_results)

    # 6. Visualization
    logger.info("Generating graphs...")
    generate_all_graphs(cw_results, rag_results)
    logger.info("Graphs saved successfully")

    # 7. Summary
    print("\n" + "="*50)
    print("RESULTS SUMMARY")
    print("="*50 + "\n")
    print_summary(comparison)

    # 8. Save Results
    save_results_to_json(cw_results, rag_results)
    logger.info("Results saved to results.json")

if __name__ == "__main__":
    main()
```

**Testing**:
- End-to-end flow works
- All steps execute correctly
- Errors handled gracefully
- Logs written correctly
- Summary printed
- Results saved

---

## Module Dependencies

### Dependency Graph

```
main.py
├── logger_setup.py
├── config.py
├── pdf_loader.py
├── context_window_method.py
│   ├── query_processor.py
│   └── config.py
├── rag_method.py
│   ├── query_processor.py
│   └── config.py
├── results_analyzer.py
│   └── config.py
└── visualization.py
    └── config.py
```

### Import Order

1. **config.py** (no dependencies)
2. **logger_setup.py** (depends on config)
3. **query_processor.py** (depends on config)
4. **pdf_loader.py** (depends on config, logger_setup)
5. **context_window_method.py** (depends on query_processor)
6. **rag_method.py** (depends on query_processor)
7. **results_analyzer.py** (depends on config)
8. **visualization.py** (depends on config)
9. **main.py** (depends on all)

---

## Implementation Order

### Recommended Sequence

1. ✅ Create `requirements.txt`
2. ✅ Create `config.py`
3. ✅ Create `logger_setup.py` → **Test logging**
4. ✅ Create `pdf_loader.py` → **Test with 2-3 PDFs**
5. ✅ Create `query_processor.py` → **Test with sample text**
6. ✅ Create `context_window_method.py` → **Test with small docs**
7. ✅ Create `rag_method.py` → **Test with small docs**
8. ✅ Create `results_analyzer.py` → **Test with mock results**
9. ✅ Create `visualization.py` → **Test with mock data**
10. ✅ Create `main.py` → **Test end-to-end**
11. ✅ Create `__init__.py`
12. ✅ Final integration testing

---

## Testing Strategy

### Unit Testing (Per Module)

**logger_setup.py**:
- Log directory created
- Logs written to files
- Rotation works correctly

**pdf_loader.py**:
- Single PDF loads correctly
- Multiprocessing works
- Error handling for corrupted PDFs

**query_processor.py**:
- API client created
- Query returns valid response
- Timing accurate
- Retry logic works

**context_window_method.py**:
- Context concatenation correct
- Multiple iterations work

**rag_method.py**:
- Chunking produces correct chunks
- Embeddings generated
- Vector search works
- Top K retrieval correct

**results_analyzer.py**:
- Statistics calculated correctly
- Similarity score reasonable

**visualization.py**:
- All graphs generated
- PNG files saved

### Integration Testing

**Test 1: Small Scale**
- Use 2-3 small PDFs
- Run 2 iterations per method
- Verify end-to-end flow

**Test 2: Full Scale**
- Use all 20 PDFs
- Run 5 iterations per method
- Verify performance metrics

**Test 3: Error Handling**
- Remove API key → Should fail gracefully
- Corrupt a PDF → Should skip and continue
- Simulate API failure → Should retry

### Validation Testing

**Manual Checks**:
1. Read generated answers (both methods)
2. Verify answers are relevant and correct
3. Check graphs are readable and accurate
4. Verify token counts match API responses
5. Validate cost calculations

---

## Timeline

### Estimated Development Time

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Setup & Configuration | 30 min | 0:30 |
| Core Infrastructure | 1 hour | 1:30 |
| PDF Processing | 45 min | 2:15 |
| Query Processing | 45 min | 3:00 |
| Context Window Method | 30 min | 3:30 |
| RAG Method | 1.5 hours | 5:00 |
| Analysis & Visualization | 1.5 hours | 6:30 |
| Main Orchestration | 45 min | 7:15 |
| Testing & Debugging | 1.5 hours | 8:45 |
| Documentation | 1 hour | 9:45 |

**Total Estimated Time**: ~10 hours

### Milestone Schedule

**Milestone 1** (Day 1): Core infrastructure complete
- config, logger, pdf_loader, query_processor done
- Can load PDFs and query API

**Milestone 2** (Day 2): Both methods implemented
- context_window_method and rag_method done
- Can run both methods successfully

**Milestone 3** (Day 3): Analysis and visualization complete
- results_analyzer and visualization done
- Can generate all graphs

**Milestone 4** (Day 3): Integration and testing
- main.py orchestration complete
- All tests passing
- End-to-end flow works

**Milestone 5** (Day 4): Documentation and polish
- All documentation complete
- Code cleaned and commented
- Ready for delivery

---

## Risk Management

### Technical Risks

**Risk 1: PDFs Exceed Context Limit**
- **Probability**: High
- **Impact**: Critical
- **Mitigation**:
  - Monitor token counts
  - Warn if approaching limit
  - Truncate or use Claude Sonnet (400K context)
  - Document the issue

**Risk 2: RAG Retrieves Irrelevant Chunks**
- **Probability**: Medium
- **Impact**: High (incorrect answers)
- **Mitigation**:
  - Tune chunk size (test 300, 500, 700 words)
  - Adjust Top K (test 2, 3, 5 chunks)
  - Use better embedding model if needed
  - Log retrieved chunks for inspection

**Risk 3: API Rate Limiting**
- **Probability**: Medium
- **Impact**: Medium (delays)
- **Mitigation**:
  - Add 2-second delays between queries
  - Implement exponential backoff
  - Handle 429 errors gracefully
  - Consider batch API if available

**Risk 4: Slow Embedding Generation**
- **Probability**: Low
- **Impact**: Low (one-time cost)
- **Mitigation**:
  - Use efficient model (MiniLM)
  - Batch processing
  - Cache embeddings
  - Show progress bar

### Project Risks

**Risk 5: Scope Creep**
- **Probability**: Medium
- **Impact**: Medium
- **Mitigation**:
  - Stick to core requirements
  - Document "future enhancements" separately
  - Focus on 4 graphs only
  - No web interface in v1

**Risk 6: Time Overrun**
- **Probability**: Medium
- **Impact**: Medium
- **Mitigation**:
  - Prioritize core functionality
  - Test incrementally
  - Reuse existing libraries
  - Keep modules simple

---

## Quality Checklist

### Code Quality

- [ ] All modules 150-200 lines maximum
- [ ] PEP 8 compliant
- [ ] Type hints throughout
- [ ] Comprehensive docstrings
- [ ] No magic numbers (use config)
- [ ] Error handling in all modules
- [ ] No code duplication

### Security

- [ ] API key never logged
- [ ] API key never printed
- [ ] API key file in .gitignore
- [ ] Key validation before use
- [ ] No sensitive data in errors

### Testing

- [ ] All unit tests pass
- [ ] Integration tests pass
- [ ] Manual validation complete
- [ ] Edge cases handled
- [ ] Error scenarios tested

### Documentation

- [ ] PRD complete
- [ ] Claude.md complete
- [ ] planning.md complete (this document)
- [ ] tasks.md complete
- [ ] README.md complete
- [ ] All functions documented
- [ ] Code comments where needed

### Deliverables

- [ ] All 9 Python modules created
- [ ] requirements.txt created
- [ ] __init__.py created
- [ ] All 4 graphs generated
- [ ] Results JSON saved
- [ ] Logs written to ring buffer
- [ ] Summary report printed

---

## Success Criteria

### Functional Success

1. ✅ Program runs end-to-end without crashes
2. ✅ All 10 queries (5 per method) complete successfully
3. ✅ Both methods return relevant, correct answers
4. ✅ Time measurements accurate and consistent
5. ✅ All 4 graphs generated and saved
6. ✅ Statistical summary printed correctly
7. ✅ Results saved to JSON

### Performance Success

1. ✅ RAG demonstrates 5-10× speed improvement over Context Window
2. ✅ RAG uses ~98% fewer input tokens
3. ✅ RAG achieves ~98% cost savings
4. ✅ Answer similarity score > 0.85 (both methods produce similar answers)
5. ✅ Total execution time < 5 minutes (excluding API wait time)

### Quality Success

1. ✅ No API key exposure anywhere
2. ✅ All modules within 150-200 line limit
3. ✅ Code is clean, readable, and well-documented
4. ✅ Logs are informative and properly formatted
5. ✅ Graphs are publication-quality
6. ✅ No errors or warnings in logs (except expected ones)

---

## Post-Completion Tasks

1. **Validation**:
   - Manually review all generated answers
   - Verify calculations (tokens, costs, savings)
   - Check graph accuracy

2. **Documentation**:
   - Update README with results
   - Add example output to documentation
   - Document any deviations from plan

3. **Cleanup**:
   - Remove test files
   - Clean up commented code
   - Verify .gitignore is complete

4. **Archival**:
   - Save results JSON
   - Export sample logs
   - Save all graphs
   - Create project archive

---

**Planning Document Status**: ✅ Complete
**Ready for Implementation**: Yes
**Author**: Yair Levi
**Version**: 1.0
**Date**: 2025-12-15
