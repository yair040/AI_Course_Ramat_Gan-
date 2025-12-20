# Product Requirements Document (PRD)
# Lost in the Middle - Context Window Testing

**Author:** Yair Levi
**Version:** 1.0
**Date:** 2025-12-10
**Project:** Lost in the Middle Hypothesis Testing

---

## 1. Executive Summary

This project implements a Python-based testing framework to validate the "Lost in the Middle" hypothesis - the theory that Large Language Models (LLMs) have lower accuracy in retrieving information from the middle portions of long documents compared to information at the beginning or end.

The program will systematically test this hypothesis by:
- Generating large text documents (~75,000 words each)
- Injecting a specific factual statement at different positions (start, middle, end)
- Querying the LLM through the Anthropic API
- Measuring retrieval accuracy across different document positions
- Performing statistical analysis over multiple iterations
- Visualizing results graphically

---

## 2. Project Objectives

### Primary Objective
Measure and compare the accuracy of information retrieval from different positions within large context windows using Claude Haiku 4.5.

### Secondary Objectives
- Establish a reusable testing framework for context window experiments
- Generate statistically significant data (5 iterations minimum)
- Provide clear visualization of results
- Maintain cost efficiency using Claude Haiku 4.5
- Implement robust logging for analysis and debugging

---

## 3. Technical Requirements

### 3.1 Environment
- **Platform:** WSL (Windows Subsystem for Linux)
- **Python Version:** 3.8+
- **Environment:** Virtual environment (venv)
- **Package Structure:** Proper Python package with `__init__.py`

### 3.2 Code Standards
- Maximum file length: 150-200 lines per Python file
- Use relative paths (no absolute paths)
- Modular design with separate task functions
- PEP 8 compliance

### 3.3 Performance
- Use multiprocessing where applicable for parallel operations
- Efficient file handling for large documents
- Optimized API calls to minimize token usage

### 3.4 Logging
- **Level:** INFO and above
- **Format:** Ring buffer with 20 rotating files
- **File Size:** Maximum 16MB per file
- **Location:** `./log/` subfolder
- **Behavior:** Circular overwrite when buffer is full

### 3.5 API Integration
- **Provider:** Anthropic API
- **Model:** Claude Haiku 4.5 (cost-optimized)
- **Authentication:** API key from `api_key.dat` and `token.pickle`
- **Security:** No API key exposure in code or logs
- **Context Management:** Fresh context window for each document test

---

## 4. Functional Requirements

### 4.1 Document Generation Module
**Function:** Generate test documents

**Specifications:**
- Create 6 text documents
- Each document: ~75,000 words
- Output location: `./files/` subfolder
- Format: Plain text (.txt)
- Content: Coherent text suitable for context testing

### 4.2 Sentence Injection Module
**Function:** Inject test sentence into documents

**Test Sentence:** "The 6 day war lasted 7 days"

**Position Distribution:**
- **2 documents:** Start position (prefix: `start_`)
  - Insert between sentences 1-5
- **2 documents:** End position (prefix: `end_`)
  - Insert between last 5 sentences
- **2 documents:** Middle position (prefix: `middle_`)
  - Insert at document midpoint

**Output:** Modified documents saved with appropriate prefixes

### 4.3 Testing Module
**Function:** Execute retrieval tests

**Process per document:**
1. Load document into Anthropic API context window
2. Submit query: "How many days did the 6 day war last?"
3. Capture response
4. Validate response using NLP similarity comparison
5. Update success counter for document type

**Validation:**
- Compare API response to target: "The 6 day war lasted 7 days"
- Use NLP library for similarity matching
- Threshold: TBD based on testing

### 4.4 Statistical Analysis Module
**Function:** Aggregate and analyze results

**Execution:**
- Run complete test cycle (all 6 documents) 5 times
- Maintain global counters:
  - `start_success_count` (integer)
  - `middle_success_count` (integer)
  - `end_success_count` (integer)
- Calculate success rates per position type
- Perform statistical significance testing

### 4.5 Visualization Module
**Function:** Display results graphically

**Requirements:**
- Bar chart comparing success rates by position
- Clear labels and legend
- Save as image file
- Display summary statistics

---

## 5. Data Flow

```
Main Program
    ↓
[1] Document Generation
    ↓ (6 documents)
[2] Sentence Injection
    ↓ (6 modified documents: 2×start, 2×middle, 2×end)
[3] Testing Loop (×5 iterations)
    ↓
    For each document:
        - Load to API
        - Query
        - Validate response
        - Update counters
    ↓
[4] Statistical Analysis
    ↓
[5] Visualization & Report
    ↓
Results displayed and saved
```

---

## 6. File Structure

```
exercise1_lost_in_the_middle/
├── __init__.py
├── main.py                    # Entry point
├── document_generator.py      # Module 4.1
├── sentence_injector.py       # Module 4.2
├── api_tester.py             # Module 4.3
├── analyzer.py               # Module 4.4
├── visualizer.py             # Module 4.5
├── config.py                 # Configuration and constants
├── utils.py                  # Utility functions
├── api_key.dat              # API key (not in git)
├── token.pickle             # Token storage (not in git)
├── requirements.txt         # Python dependencies
├── files/                   # Generated documents
│   ├── document_1.txt
│   ├── start_document_1.txt
│   ├── ...
├── log/                     # Log files (ring buffer)
│   ├── app.log
│   ├── app.log.1
│   ├── ...
├── results/                 # Output visualizations
│   └── results_graph.png
├── PRD.md                   # This document
├── Claude.md                # Claude-specific instructions
├── planning.md              # Project planning
└── tasks.md                 # Task breakdown
```

---

## 7. Dependencies

### Core Libraries
- `anthropic` - Anthropic API client
- `nltk` or `spacy` - NLP for similarity comparison
- `matplotlib` or `plotly` - Data visualization
- `logging` - Built-in logging with rotating file handler

### Supporting Libraries
- `json` - Credential management
- `pickle` - Token storage
- `multiprocessing` - Parallel processing
- `pathlib` - Path manipulation
- `typing` - Type hints

---

## 8. Security Requirements

- API keys must not be hardcoded
- Use environment variables or secure file storage
- Add `api_key.dat` and `token.pickle` to `.gitignore`
- Sanitize logs to prevent credential leakage
- Validate file paths to prevent directory traversal

---

## 9. Testing & Validation

### Unit Testing
- Test document generation (word count, format)
- Test sentence injection (position accuracy)
- Test API integration (mock responses)
- Test similarity matching (known pairs)

### Integration Testing
- End-to-end test with small documents
- Verify counter increments
- Validate data flow

### Statistical Validation
- Ensure 5 iterations complete successfully
- Verify counter accuracy
- Check visualization output

---

## 10. Success Criteria

1. **Functionality:** All 6 documents generated and processed correctly
2. **Accuracy:** NLP similarity matching correctly identifies valid responses
3. **Statistics:** Complete 5 full test iterations (30 total API calls)
4. **Visualization:** Clear graphical representation of results
5. **Logging:** Complete logs with no errors or missing entries
6. **Performance:** Completion within reasonable time frame
7. **Cost:** Efficient token usage with Claude Haiku 4.5

---

## 11. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| API rate limiting | Test delays | Implement exponential backoff |
| Large token costs | Budget overrun | Use Claude Haiku 4.5, monitor usage |
| NLP similarity false negatives | Inaccurate results | Tune threshold, manual validation |
| Document generation quality | Invalid tests | Validate document coherence |
| File system issues | Program crash | Robust error handling, path validation |

---

## 12. Future Enhancements

- Support for multiple LLM models (comparison testing)
- Configurable document sizes and iteration counts
- Additional position testing (quartiles)
- Web dashboard for real-time monitoring
- Export results to CSV/JSON for further analysis
- Automated statistical significance testing

---

## 13. Acceptance Criteria

- [ ] All 6 documents generated with ~75,000 words each
- [ ] Sentence correctly injected at specified positions
- [ ] All 30 API queries execute successfully (6 docs × 5 iterations)
- [ ] Counters accurately track success rates
- [ ] Statistical analysis shows clear comparison
- [ ] Visualization saved and displays correctly
- [ ] Logs maintain ring buffer (20 files × 16MB)
- [ ] No API key exposure in code or logs
- [ ] Code follows 150-200 line limit per file
- [ ] Package structure with proper `__init__.py`

---

## 14. Glossary

- **Lost in the Middle:** Hypothesis that LLMs have reduced accuracy for information in the middle of long contexts
- **Context Window:** The amount of text that can be processed in a single API call
- **Ring Buffer:** Circular logging system that overwrites oldest files when full
- **NLP Similarity:** Natural Language Processing technique to measure semantic similarity between texts

---

**Document Status:** Draft for Review
**Next Steps:** Create planning.md, tasks.md, and Claude.md
