# Product Requirements Document (PRD)
# Context Window Size Impact on Search Accuracy

**Author:** Yair Levi
**Version:** 1.0
**Date:** 2025-12-14

---

## 1. Executive Summary

This program is a research tool designed to test the hypothesis that search accuracy in Large Language Models (LLMs) degrades as the context window size increases beyond a certain threshold. The tool will systematically test Claude Haiku 4.5's ability to retrieve specific information from documents of varying sizes (2,000 to 50,000 words) and provide quantitative results on accuracy and performance.

---

## 2. Objectives

### Primary Objective
Test whether Claude's ability to accurately answer queries decreases as document size increases within the context window.

### Secondary Objectives
- Measure query execution time across different document sizes
- Track token usage for each document
- Visualize the relationship between document size, accuracy, and execution time
- Provide reproducible results for further research

---

## 3. Technical Requirements

### 3.1 Environment
- **Platform:** Windows Subsystem for Linux (WSL)
- **Python:** 3.8+ in virtual environment
- **Package Structure:** Proper Python package with `__init__.py`
- **Path Management:** Use relative paths only (no absolute paths)

### 3.2 Code Organization
- **File Size Limit:** 150-200 lines per Python file
- **Modularity:** Separate concerns into different modules
- **Package Structure:**
  ```
  context_window_test/
  ├── __init__.py
  ├── main.py
  ├── document_generator.py
  ├── query_processor.py
  ├── accuracy_checker.py
  ├── visualization.py
  ├── logger_setup.py
  └── config.py
  ```

### 3.3 Performance
- **Multiprocessing:** Utilize multiprocessing where possible (document generation, parallel queries if API allows)
- **Async Operations:** Consider async/await for API calls if beneficial

### 3.4 Logging
- **Level:** INFO and above (INFO, WARNING, ERROR, CRITICAL)
- **Format:** Ring buffer with 20 log files
- **File Size:** 16MB per log file
- **Rotation:** When the 20th file is full, overwrite the 1st file
- **Location:** `./log/` subfolder
- **Handler:** RotatingFileHandler with proper configuration

### 3.5 Security
- **API Key Management:**
  - Read from `api_key.dat` in current folder
  - Never expose or log the API key
  - Handle file read errors gracefully
  - Validate key format before use

### 3.6 External Dependencies
- **Anthropic API:** Claude Haiku 4.5 model
- **NLP Library:** For semantic similarity comparison (e.g., sentence-transformers, scikit-learn with TfidfVectorizer, or spaCy)
- **Visualization:** matplotlib or plotly
- **Other:** Standard libraries (multiprocessing, logging, json, time, pathlib)

---

## 4. Functional Requirements

### 4.1 Document Generation (Step 1)
**Input:** None
**Output:** 7 text documents in `./files/` subfolder

**Specifications:**
- **Documents:**
  1. doc_2000.txt - 2,000 words
  2. doc_5000.txt - 5,000 words
  3. doc_10000.txt - 10,000 words
  4. doc_20000.txt - 20,000 words
  5. doc_30000.txt - 30,000 words
  6. doc_40000.txt - 40,000 words
  7. doc_50000.txt - 50,000 words

- **Content:**
  - English text (Lorem ipsum or generated content)
  - **Critical Sentence:** "The first prime minister of Israel was Ben Gurion"
  - **Placement:** Inserted at the middle of each document
  - **Format:** Plain text (.txt)

### 4.2 Data Structure (Step 2)
**Global Variable:** `results_list` (List of dictionaries)

**Dictionary Schema per document:**
```python
{
    "document_name": str,          # e.g., "doc_2000.txt"
    "word_count": int,              # Target word count
    "token_count": int,             # Actual tokens in context window
    "query_time": float,            # Seconds to complete query
    "accuracy": int,                # 1 for correct, 0 for incorrect
    "response": str,                # Actual response from Claude
    "similarity_score": float       # NLP similarity score
}
```

### 4.3 Query Processing (Step 4)
For each of the 7 documents:

**a. Load Document**
- Read document from `./files/` subfolder
- Load into Claude's context window via Anthropic API
- Use Claude Haiku 4.5 model

**b. Execute Query**
- **Query:** "Who was the first Prime Minister of Israel?"
- Send query to Anthropic API with document as context

**c. Measure Time**
- Start timer before API call
- Stop timer after receiving response
- Store elapsed time in `query_time`

**d. Evaluate Accuracy**
- **Expected Answer:** "Ben Gurion was the first Prime Minister of Israel"
- **Method:** Use NLP semantic similarity
- **Threshold:** Define similarity threshold (e.g., 0.85)
- If similarity >= threshold: `accuracy = 1`
- If similarity < threshold: `accuracy = 0`
- Store similarity score for analysis

**e. Count Tokens**
- Use Anthropic's tokenization method or tiktoken library
- Count tokens in the document
- Store in `token_count`

**f. Store Results**
- Update corresponding dictionary in `results_list`

### 4.4 Results Visualization (Step 7)
**Generate Graphs:**

**Graph 1: Dual Y-axis Plot**
- **X-axis:** Token count (or word count)
- **Left Y-axis:** Query execution time (seconds)
- **Right Y-axis:** Accuracy (0 or 1)
- **Plot Types:**
  - Line/scatter plot for execution time
  - Bar plot or scatter for accuracy
- **Output:** Save as `results_graph.png` in current folder

**Graph 2: Optional - Similarity Scores**
- **X-axis:** Token count
- **Y-axis:** Similarity score (0-1)
- Shows gradual degradation if hypothesis is correct

**Console Output:**
- Print summary table with all metrics
- Highlight any documents where accuracy = 0

---

## 5. Non-Functional Requirements

### 5.1 Reliability
- Graceful error handling for API failures
- Retry logic for transient API errors (3 retries with exponential backoff)
- Validate API responses before processing

### 5.2 Maintainability
- Clear function and variable naming
- Docstrings for all functions
- Type hints where appropriate
- Configuration via `config.py`

### 5.3 Performance
- Total execution time < 10 minutes (estimated)
- Efficient document generation (use templates)
- Minimize API calls (one per document)

### 5.4 Usability
- Single command execution: `python -m context_window_test`
- Clear console output showing progress
- Informative error messages

---

## 6. Configuration Parameters

Store in `config.py`:
```python
# API Configuration
API_KEY_FILE = "api_key.dat"
MODEL_NAME = "claude-haiku-4-5-20250929"  # Claude Haiku 4.5
MAX_TOKENS = 4096  # For response

# Document Configuration
WORD_COUNTS = [2000, 5000, 10000, 20000, 30000, 40000, 50000]
TARGET_SENTENCE = "The first prime minister of Israel was Ben Gurion"
FILES_DIR = "./files"

# Query Configuration
QUERY = "Who was the first Prime Minister of Israel?"
EXPECTED_ANSWER = "Ben Gurion was the first Prime Minister of Israel"
SIMILARITY_THRESHOLD = 0.85

# Logging Configuration
LOG_DIR = "./log"
LOG_FILE_SIZE = 16 * 1024 * 1024  # 16MB
LOG_FILE_COUNT = 20
LOG_LEVEL = "INFO"

# Visualization
OUTPUT_GRAPH = "results_graph.png"
```

---

## 7. Success Criteria

### Program Success
- All 7 documents generated successfully
- All 7 queries executed without errors
- Results collected and stored correctly
- Graph generated and saved
- Logs written to ring buffer correctly

### Research Success
- Clear trend visible in results (accuracy vs. document size)
- Statistical significance in time measurements
- Reproducible results across runs

---

## 8. Risks and Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| API rate limiting | High | Add delays between calls, implement retry logic |
| API cost overrun | Medium | Use Haiku (cheapest), limit to 7 documents |
| Inaccurate similarity detection | High | Test multiple NLP methods, adjust threshold |
| Token counting mismatch | Medium | Use official Anthropic tokenizer |
| Memory issues with large docs | Medium | Stream file reading, optimize memory |

---

## 9. Testing Strategy

### Unit Tests
- Document generation (word count accuracy)
- Sentence insertion (correct placement)
- Similarity calculation (known examples)

### Integration Tests
- API connection and authentication
- End-to-end flow with small documents
- Logging verification

### Validation Tests
- Manual verification of 1-2 responses
- Token count accuracy check
- Graph output visual inspection

---

## 10. Deliverables

1. **Python Package:** `context_window_test/`
2. **Documentation:**
   - PRD.md (this document)
   - Claude.md (project overview for AI assistance)
   - planning.md (implementation plan)
   - tasks.md (task breakdown)
3. **Configuration:**
   - requirements.txt
   - config.py
4. **Runtime Artifacts:**
   - 7 text documents in `./files/`
   - Log files in `./log/`
   - results_graph.png
   - results.json (optional: raw data export)

---

## 11. Future Enhancements

- Test multiple models (Claude Sonnet, Opus)
- Test different query types (math, reasoning, etc.)
- Add statistical analysis (p-values, confidence intervals)
- Export results to CSV for further analysis
- Web dashboard for real-time monitoring
- Parameterized queries via command-line arguments

---

## 12. References

- [Anthropic API Documentation](https://docs.anthropic.com/)
- [Claude Model Cards](https://www.anthropic.com/claude)
- [Python Multiprocessing](https://docs.python.org/3/library/multiprocessing.html)
- [RotatingFileHandler](https://docs.python.org/3/library/logging.handlers.html#rotatingfilehandler)
