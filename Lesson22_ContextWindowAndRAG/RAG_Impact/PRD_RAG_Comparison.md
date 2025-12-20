# Product Requirements Document (PRD)
# Context Window vs RAG Performance Comparison

**Project Name:** Context Window vs RAG Benchmarking Tool
**Author:** Yair Levi
**Version:** 1.0
**Date:** 2025-12-15
**Platform:** WSL (Linux)

---

## Executive Summary

This program empirically compares two document retrieval methods for querying information from multiple PDF documents:
1. **Context Window Method**: Loading all 20 PDF documents directly into Claude's context window
2. **RAG Method**: Using Retrieval Augmented Generation with vector search to load only the top 3 most relevant chunks

The goal is to measure and compare response time, answer quality, token usage, and cost efficiency between these approaches across 5 iterations each.

---

## Problem Statement

### Current Challenge
When querying information from multiple documents, developers must choose between:
- **Full Context Loading**: Simple but potentially slow, expensive, and may hit context limits
- **RAG (Retrieval Augmented Generation)**: More complex setup but potentially faster, cheaper, and more scalable

### Research Question
**"Is RAG faster and more cost-effective than full context loading for multi-document queries?"**

---

## Project Goals

### Primary Goals
1. Implement both retrieval methods with identical test conditions
2. Execute 5 test iterations per method (10 total queries)
3. Measure response time accurately for each method
4. Compare answer quality and consistency across methods
5. Generate statistical analysis and visual comparisons

### Secondary Goals
1. Demonstrate professional Python package structure
2. Showcase API key security best practices
3. Implement ring buffer logging (20 files × 16MB)
4. Use multiprocessing where beneficial
5. Create publication-quality visualizations

---

## Technical Requirements

### Environment
- **Platform**: WSL (Windows Subsystem for Linux)
- **Python**: 3.8+ with virtual environment
- **Working Directory**: All operations in current working directory
- **Path Style**: Relative paths only (no absolute paths)

### API Requirements
- **Service**: Anthropic API
- **Model**: `claude-haiku-4-5-20250929` (Haiku 4.5) - cost optimization
- **API Key**: Read from `api_key.dat` file (NEVER exposed in logs/console)
- **Security**: No hardcoded keys, no key logging, validate before use

### Document Requirements
- **Format**: PDF files
- **Location**: `./docs/` subfolder
- **Count**: 20 PDF documents
- **Content**: Medical/pharmaceutical information (for target query)

### Code Structure
```
context_window_vs_rag/
├── __init__.py                  # Package initialization
├── main.py                      # Entry point and orchestration
├── config.py                    # Configuration constants
├── logger_setup.py              # Ring buffer logging setup
├── pdf_loader.py                # PDF reading and text extraction
├── context_window_method.py     # Full context implementation
├── rag_method.py                # RAG implementation (embed + retrieve)
├── query_processor.py           # API calls with timing
├── results_analyzer.py          # Statistical analysis
└── visualization.py             # Graph generation
```

### File Size Constraint
- **Maximum**: 150-200 lines per Python file
- **Rationale**: Maintainability, modularity, and code clarity

### Logging Requirements
- **Level**: INFO and above
- **Format**: Ring buffer
- **Buffer Size**: 20 files × 16MB each (320MB total)
- **Location**: `./log/` subfolder
- **Behavior**: When file 20 is full, overwrite file 1 (circular)
- **Implementation**: `RotatingFileHandler` with proper configuration

---

## Functional Requirements

### FR1: Context Window Method

**Description**: Load all 20 PDF documents into Claude's context window and query.

**Process**:
1. Read all 20 PDF files from `./docs/` directory
2. Extract text content from each PDF using pdfplumber or PyPDF2
3. Concatenate all extracted text into single context
4. Construct prompt: `<all_documents>\n\nQuestion: {query}`
5. Send to Anthropic API
6. **Start timer** before API call
7. Receive response
8. **Stop timer** after response received
9. Record: answer text, response time, token counts

**Input**:
- 20 PDF documents from `./docs/`
- Query: "What are the side effects of taking calcium carbonate?"

**Output**:
- Answer text (string)
- Response time in seconds (float)
- Input token count (int)
- Output token count (int)
- Estimated cost (float)

**Success Criteria**:
- All 20 PDFs successfully loaded and processed
- API returns valid response
- Time measured accurately (±50ms precision)
- No API key exposure
- Token counts captured from API response

**Constraints**:
- Must handle PDF parsing errors gracefully
- Must validate total tokens don't exceed model limit (200K for Haiku 4.5)
- Must implement retry logic for API failures

### FR2: RAG Method

**Description**: Build vector database from PDFs, retrieve top 3 relevant chunks, then query.

**Process**:
1. **Setup Phase** (one-time per test run):
   a. Read all 20 PDF files from `./docs/`
   b. Extract text from each PDF
   c. Split text into chunks (500 words with 50-word overlap)
   d. Generate embeddings for each chunk using sentence-transformers
   e. Store embeddings in vector database (ChromaDB or FAISS)

2. **Query Phase** (per iteration):
   a. Generate query embedding
   b. Search vector database for top 3 most similar chunks
   c. Construct prompt with only these 3 chunks
   d. **Start timer**
   e. Send to Anthropic API
   f. Receive response
   g. **Stop timer**
   h. Record: answer text, response time, token counts

**Input**:
- 20 PDF documents from `./docs/`
- Query: "What are the side effects of taking calcium carbonate?"

**Output**:
- Answer text (string)
- Response time in seconds (float) - **includes embedding generation time**
- Input token count (int)
- Output token count (int)
- Estimated cost (float)
- Retrieved chunk indices (list)

**Success Criteria**:
- Vector database successfully built
- Top 3 chunks retrieved for each query
- API returns valid response
- Time includes full RAG pipeline (embedding + retrieval + API)
- Significant token reduction vs Context Window method

**Configuration**:
```python
CHUNK_SIZE = 500  # words per chunk
CHUNK_OVERLAP = 50  # word overlap between chunks
TOP_K = 3  # number of chunks to retrieve
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Fast and efficient
```

**Constraints**:
- Embedding generation should be cached (one-time cost)
- Vector search must be efficient (< 1 second)
- Must handle missing chunks gracefully

### FR3: Iterative Testing

**Description**: Run each method 5 times to collect statistical data.

**Process**:
1. Initialize results storage (list of dictionaries)
2. **Context Window Method**:
   - Run 5 iterations
   - For each iteration: load docs, query, record metrics
   - Small delay between iterations (2 seconds) to avoid rate limiting
3. **RAG Method**:
   - Build vector database once (before iterations)
   - Run 5 iterations
   - For each iteration: retrieve chunks, query, record metrics
   - Small delay between iterations (2 seconds)
4. Save all raw results to JSON file

**Output**:
```json
{
  "context_window": [
    {
      "iteration": 1,
      "answer": "...",
      "time_seconds": 12.34,
      "input_tokens": 145632,
      "output_tokens": 87,
      "cost": 0.1165
    },
    ...
  ],
  "rag": [
    {
      "iteration": 1,
      "answer": "...",
      "time_seconds": 2.15,
      "input_tokens": 1842,
      "output_tokens": 91,
      "cost": 0.0014
    },
    ...
  ]
}
```

**Success Criteria**:
- All 10 queries complete successfully (5 per method)
- Consistent results across iterations within same method
- No API errors or timeouts
- Results saved to disk for analysis

### FR4: Statistical Analysis

**Description**: Calculate statistics and compare methods.

**Metrics to Calculate**:

**Per Method**:
- **Response Time**: mean, std dev, min, max, median
- **Input Tokens**: mean, std dev
- **Output Tokens**: mean, std dev
- **Total Tokens**: mean, std dev
- **Cost per Query**: mean, std dev, total cost
- **Answer Length**: mean, std dev (word count)

**Comparison Metrics**:
- **Time Savings**: `(CW_time - RAG_time) / CW_time × 100%`
- **Token Savings**: `(CW_tokens - RAG_tokens) / CW_tokens × 100%`
- **Cost Savings**: `(CW_cost - RAG_cost) / CW_cost × 100%`
- **Answer Similarity**: Semantic similarity between CW and RAG answers (using sentence-transformers)

**Output**:
```
============================================
RESULTS SUMMARY
============================================

Context Window Method:
  Response Time: 12.34 ± 1.23s (range: 10.45 - 14.56s)
  Input Tokens:  145,632 ± 234
  Output Tokens: 87 ± 12
  Cost per Query: $0.117 ± $0.001
  Total Cost (5 queries): $0.585

RAG Method:
  Response Time: 2.15 ± 0.45s (range: 1.67 - 2.89s)
  Input Tokens:  1,842 ± 156
  Output Tokens: 91 ± 8
  Cost per Query: $0.0015 ± $0.0001
  Total Cost (5 queries): $0.0075

Comparison:
  Time Savings: 82.6% (RAG is 5.7x faster)
  Token Savings: 98.7% (RAG uses 99% fewer input tokens)
  Cost Savings: 98.7% (RAG is 78x cheaper)
  Answer Similarity: 0.91 (highly similar answers)
```

**Success Criteria**:
- Statistics calculated correctly
- Clear performance winner identified
- Savings percentages accurate
- Summary table readable and professional

### FR5: Visualization

**Description**: Generate publication-quality comparison graphs.

**Required Charts**:

**Chart 1: Response Time Comparison**
- Type: Bar chart with error bars (mean ± std dev)
- X-axis: Method (Context Window, RAG)
- Y-axis: Response Time (seconds)
- Colors: Blue for CW, Green for RAG
- Title: "Response Time Comparison: Context Window vs RAG"
- Filename: `response_time_comparison.png`

**Chart 2: Token Usage Comparison**
- Type: Grouped bar chart
- X-axis: Method
- Y-axis: Token Count
- Groups: Input Tokens, Output Tokens
- Colors: Orange for input, Purple for output
- Title: "Token Usage Comparison"
- Filename: `token_usage_comparison.png`

**Chart 3: Cost Comparison**
- Type: Bar chart
- X-axis: Method
- Y-axis: Cost ($USD)
- Show per-query cost and total cost (5 queries)
- Title: "Cost Comparison: Context Window vs RAG"
- Filename: `cost_comparison.png`

**Chart 4: Iteration Timeline**
- Type: Line plot
- X-axis: Iteration (1-5)
- Y-axis: Response Time (seconds)
- Two lines: Context Window (blue), RAG (green)
- Markers for each data point
- Title: "Response Time Across Iterations"
- Filename: `iterations_timeline.png`

**Chart 5: Combined Dashboard** (optional bonus)
- Type: 2×2 subplot grid
- Contains all 4 charts above in single image
- Filename: `results_dashboard.png`

**Output Format**:
- PNG files with 300 DPI resolution
- Size: 10×6 inches per chart
- Font: Readable size (12pt for labels, 14pt for titles)

**Success Criteria**:
- All graphs generated successfully
- Graphs are publication-quality
- Data accurately represented
- Labels and legends clear
- Files saved to current directory

---

## Non-Functional Requirements

### NFR1: Performance
- **Document Loading**: Use multiprocessing for parallel PDF extraction (20 PDFs)
- **Embedding Generation**: Batch processing for efficiency
- **Vector Search**: < 1 second retrieval time
- **Total Execution**: < 5 minutes for all 10 queries (excluding API wait time)

### NFR2: Security
- API key **never** printed to console
- API key **never** written to logs
- API key read from file only
- Validate API key format (starts with "sk-ant-")
- No sensitive data in error messages
- API key file should be in `.gitignore`

### NFR3: Reliability
- **Retry Logic**: 3 attempts with exponential backoff (1s, 2s, 4s)
- **Error Handling**: Graceful handling of:
  - Missing PDF files
  - Corrupted PDFs
  - API failures
  - Network timeouts
  - Rate limiting
- **Validation**: Check API responses before processing
- **Logging**: All errors logged with context

### NFR4: Maintainability
- Clear separation of concerns (one responsibility per module)
- Comprehensive docstrings (all functions and classes)
- Type hints throughout codebase
- PEP 8 compliant code style
- Configuration in `config.py` only
- No magic numbers in code

### NFR5: Usability
- Single command execution: `python -m context_window_vs_rag`
- Clear progress indicators (e.g., "Processing iteration 3/5...")
- Informative console output
- Summary report automatically displayed
- Graphs automatically generated
- Results saved to JSON for later analysis

---

## Data Flow

### Context Window Method Flow
```
20 PDFs → Extract Text (parallel) → Concatenate All
                                          ↓
                                    API Query → Response
                                          ↓
                                    Time Measured
```

### RAG Method Flow
```
20 PDFs → Extract Text (parallel) → Chunk Text → Generate Embeddings
                                          ↓
                                    Vector Database
                                          ↓
Query → Query Embedding → Vector Search → Top 3 Chunks
                                          ↓
                                    API Query → Response
                                          ↓
                                    Time Measured (includes all steps)
```

---

## API Specifications

### Anthropic API

**Model**: `claude-haiku-4-5-20250929`

**Message Format**:
```python
client.messages.create(
    model="claude-haiku-4-5-20250929",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": f"{document_content}\n\nQuestion: {query}"
        }
    ]
)
```

**Response Format**:
```python
{
    "id": "msg_...",
    "content": [{"text": "..."}],
    "usage": {
        "input_tokens": 12345,
        "output_tokens": 234
    }
}
```

**Pricing** (Haiku 4.5):
- Input: ~$0.80 per million tokens
- Output: ~$4.00 per million tokens

**Rate Limits**:
- Implement 2-second delays between requests
- Retry with exponential backoff on 429 errors

---

## Configuration Constants (config.py)

```python
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

---

## Module Specifications

### main.py (150-200 lines)
**Responsibilities**:
- Initialize logging
- Load API key
- Create results storage
- Run Context Window method (5 iterations)
- Run RAG method (5 iterations)
- Call statistical analysis
- Call visualization
- Print summary
- Save results to JSON

**Key Functions**:
```python
def main():
    """Main orchestration function."""
    pass

def run_context_window_tests(api_key: str) -> List[Dict]:
    """Run 5 Context Window iterations."""
    pass

def run_rag_tests(api_key: str) -> List[Dict]:
    """Run 5 RAG iterations."""
    pass
```

### pdf_loader.py (150-200 lines)
**Responsibilities**:
- Load PDF files
- Extract text using pdfplumber (primary) or PyPDF2 (fallback)
- Handle corrupted PDFs
- Use multiprocessing for parallel loading

**Key Functions**:
```python
def load_single_pdf(pdf_path: str) -> str:
    """Load and extract text from one PDF."""
    pass

def load_all_pdfs(docs_dir: str) -> List[str]:
    """Load all PDFs using multiprocessing."""
    pass

def validate_pdf(pdf_path: str) -> bool:
    """Check if PDF is readable."""
    pass
```

### context_window_method.py (150-200 lines)
**Responsibilities**:
- Concatenate all document texts
- Format prompt for API
- Execute query via query_processor
- Return results

**Key Functions**:
```python
def prepare_context(documents: List[str]) -> str:
    """Concatenate all documents."""
    pass

def query_full_context(api_key: str, documents: List[str], query: str) -> Dict:
    """Query with full context."""
    pass
```

### rag_method.py (150-200 lines)
**Responsibilities**:
- Text chunking with overlap
- Generate embeddings
- Build/load vector database
- Retrieve top K chunks
- Query with retrieved chunks

**Key Functions**:
```python
def chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:
    """Split text into overlapping chunks."""
    pass

def build_vector_db(documents: List[str]) -> VectorDatabase:
    """Build vector database from documents."""
    pass

def retrieve_top_k(query: str, vector_db: VectorDatabase, k: int) -> List[str]:
    """Retrieve top K most relevant chunks."""
    pass

def query_with_rag(api_key: str, documents: List[str], query: str) -> Dict:
    """Query using RAG pipeline."""
    pass
```

### query_processor.py (150-200 lines)
**Responsibilities**:
- Initialize Anthropic client
- Execute API calls with timing
- Implement retry logic
- Extract response and usage stats

**Key Functions**:
```python
def create_client(api_key: str) -> anthropic.Anthropic:
    """Create Anthropic client."""
    pass

def query_claude(client: anthropic.Anthropic, content: str, query: str) -> Dict:
    """Query Claude with timing and retry logic."""
    pass

def calculate_cost(input_tokens: int, output_tokens: int) -> float:
    """Calculate cost in USD."""
    pass
```

### results_analyzer.py (150-200 lines)
**Responsibilities**:
- Calculate statistics (mean, std, min, max)
- Compare methods
- Calculate savings percentages
- Compute answer similarity
- Generate summary report

**Key Functions**:
```python
def calculate_stats(results: List[Dict]) -> Dict:
    """Calculate statistical metrics."""
    pass

def compare_methods(cw_results: List[Dict], rag_results: List[Dict]) -> Dict:
    """Compare Context Window vs RAG."""
    pass

def calculate_similarity(answer1: str, answer2: str) -> float:
    """Calculate semantic similarity between answers."""
    pass

def print_summary(comparison: Dict) -> None:
    """Print formatted summary report."""
    pass
```

### visualization.py (150-200 lines)
**Responsibilities**:
- Generate all comparison charts
- Format plots professionally
- Save to PNG files

**Key Functions**:
```python
def plot_response_time(cw_stats: Dict, rag_stats: Dict) -> None:
    """Generate response time comparison chart."""
    pass

def plot_token_usage(cw_stats: Dict, rag_stats: Dict) -> None:
    """Generate token usage comparison chart."""
    pass

def plot_cost_comparison(cw_stats: Dict, rag_stats: Dict) -> None:
    """Generate cost comparison chart."""
    pass

def plot_iterations_timeline(cw_results: List[Dict], rag_results: List[Dict]) -> None:
    """Generate iteration timeline chart."""
    pass
```

### logger_setup.py (50-100 lines)
**Responsibilities**:
- Configure ring buffer logging
- Create log directory if needed
- Return configured logger

**Key Functions**:
```python
def setup_logger(name: str = "context_window_vs_rag") -> logging.Logger:
    """Setup ring buffer logger."""
    pass
```

### config.py (50-100 lines)
**Responsibilities**:
- Store all configuration constants
- No logic, pure configuration

---

## Dependencies (requirements.txt)

```txt
# Core Dependencies
anthropic>=0.40.0              # Anthropic API client
python-dotenv>=1.0.0           # Optional: environment variables

# PDF Processing
PyPDF2>=3.0.0                  # PDF reading
pdfplumber>=0.10.0             # Robust PDF extraction

# RAG Components
sentence-transformers>=2.2.0   # Text embeddings
chromadb>=0.4.0                # Vector database
# OR: faiss-cpu>=1.7.4         # Alternative vector database

# NLP
transformers>=4.30.0           # Transformer models
torch>=2.0.0                   # PyTorch for embeddings

# Visualization
matplotlib>=3.7.0              # Plotting
seaborn>=0.12.0                # Enhanced visualizations

# Data Processing
numpy>=1.24.0                  # Numerical operations
pandas>=2.0.0                  # Data manipulation (optional)

# Utilities
tqdm>=4.65.0                   # Progress bars
tiktoken>=0.5.0                # Token counting (optional)
```

---

## Expected Results

### Hypothesis
- **Response Time**: RAG should be 3-10× faster than Context Window
- **Token Usage**: RAG should use ~99% fewer input tokens
- **Cost**: RAG should be ~98% cheaper per query
- **Answer Quality**: Both methods should produce similar, correct answers

### Example Output

**Console**:
```
[INFO] Initializing Context Window vs RAG comparison...
[INFO] Loaded API key successfully
[INFO] Loading 20 PDFs from ./docs/...
[INFO] Loaded 20 PDFs (total: 234,567 words)

========================================
CONTEXT WINDOW METHOD (5 iterations)
========================================
[INFO] Iteration 1/5: Query time 12.34s, Tokens: 145632/87
[INFO] Iteration 2/5: Query time 11.89s, Tokens: 145632/92
[INFO] Iteration 3/5: Query time 13.01s, Tokens: 145632/85
[INFO] Iteration 4/5: Query time 12.67s, Tokens: 145632/88
[INFO] Iteration 5/5: Query time 12.45s, Tokens: 145632/90

========================================
RAG METHOD (5 iterations)
========================================
[INFO] Building vector database...
[INFO] Generated 1,234 chunks from 20 documents
[INFO] Vector database built successfully
[INFO] Iteration 1/5: Query time 2.15s, Tokens: 1842/91
[INFO] Iteration 2/5: Query time 2.08s, Tokens: 1856/89
[INFO] Iteration 3/5: Query time 2.23s, Tokens: 1831/93
[INFO] Iteration 4/5: Query time 2.11s, Tokens: 1849/90
[INFO] Iteration 5/5: Query time 2.18s, Tokens: 1838/92

========================================
RESULTS SUMMARY
========================================

Context Window Method:
  Response Time: 12.47 ± 0.42s
  Input Tokens:  145,632 ± 0
  Output Tokens: 88 ± 3
  Cost per Query: $0.117
  Total Cost: $0.585

RAG Method:
  Response Time: 2.15 ± 0.06s
  Input Tokens:  1,843 ± 10
  Output Tokens: 91 ± 2
  Cost per Query: $0.0015
  Total Cost: $0.0075

Comparison:
  Time Savings: 82.8% (RAG is 5.8× faster)
  Token Savings: 98.7% (RAG uses 98.7% fewer tokens)
  Cost Savings: 98.7% (RAG is 78× cheaper)
  Answer Similarity: 0.93 (highly consistent)

[INFO] Graphs saved successfully
[INFO] Results saved to results.json
```

---

## Testing Strategy

### Unit Tests
- PDF loading (valid and corrupted files)
- Text extraction accuracy
- Chunking logic (overlap validation)
- Embedding generation
- Vector search retrieval

### Integration Tests
- End-to-end Context Window method
- End-to-end RAG pipeline
- API interaction with retry logic
- Results collection and analysis

### Validation Tests
- API key loading and validation
- Directory creation
- Log rotation behavior
- Graph generation

---

## Success Criteria

### Program Success
- All 10 queries (5 per method) complete successfully
- Both methods return valid, relevant answers
- Time measurements accurate and consistent
- Graphs generated and saved
- Logs written correctly to ring buffer
- No API key exposure

### Research Success
- Clear performance difference demonstrated
- RAG shows measurable speed advantage
- RAG shows significant cost savings
- Answer quality comparable between methods
- Results reproducible across runs

---

## Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| PDFs exceed context limit | High | Critical | Monitor token counts, truncate if needed |
| API rate limiting | Medium | Medium | Add delays, implement retry logic |
| PDF parsing failures | Medium | Medium | Use multiple libraries, validate before processing |
| RAG retrieves wrong chunks | Medium | High | Tune chunk size and Top K, validate retrieval |
| Embedding generation slow | Low | Low | Use efficient model (MiniLM), cache embeddings |
| High API costs | Low | Medium | Use Haiku model, limit iterations |

---

## Timeline Estimate

1. **Setup** (30 min): Environment, dependencies, directory structure
2. **Core Modules** (3 hours): pdf_loader, query_processor, logger_setup
3. **Methods** (2 hours): context_window_method, rag_method
4. **Analysis** (1 hour): results_analyzer, statistical calculations
5. **Visualization** (1 hour): All charts
6. **Integration** (1 hour): main.py orchestration
7. **Testing** (1 hour): Unit and integration tests
8. **Documentation** (1 hour): Comments, docstrings, README

**Total**: ~10 hours development time

---

## Future Enhancements

- Test with different queries
- Support multiple document formats (DOCX, TXT, HTML)
- Configurable chunk sizes and overlap
- Multiple embedding model comparison
- Different Top K values comparison
- Web dashboard for real-time monitoring
- Export to CSV/Excel for further analysis
- Automatic hyperparameter tuning for RAG

---

## References

- [Anthropic API Documentation](https://docs.anthropic.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [PDFPlumber Documentation](https://github.com/jsvine/pdfplumber)
- [Python Multiprocessing](https://docs.python.org/3/library/multiprocessing.html)
- [RAG Best Practices](https://python.langchain.com/docs/use_cases/question_answering/)

---

**Document Status**: ✅ Approved for Development
**Author**: Yair Levi
**Last Updated**: 2025-12-15
