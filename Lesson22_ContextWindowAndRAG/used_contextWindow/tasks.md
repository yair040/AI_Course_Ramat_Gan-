# Tasks Breakdown
# Context Window Size Impact Testing Program

**Author:** Yair Levi
**Version:** 1.0
**Date:** 2025-12-14

---

## Task Organization

Tasks are organized into phases and numbered sequentially. Each task includes:
- **Task ID:** Unique identifier
- **Description:** What needs to be done
- **Estimated Lines:** Code complexity estimate
- **Dependencies:** Prerequisites
- **Status:** Not Started / In Progress / Completed / Blocked

---

## Phase 1: Project Setup

### Task 1.1: Create Directory Structure
**Status:** Not Started
**Dependencies:** None
**Estimated Time:** 10 minutes

Create the following directories:
```
exercise2_used_context_window/
├── context_window_test/
│   └── (Python files will go here)
├── files/
├── log/
└── (config files at root)
```

**Commands:**
```bash
mkdir -p context_window_test
mkdir -p files
mkdir -p log
```

### Task 1.2: Set Up Virtual Environment
**Status:** Not Started
**Dependencies:** Task 1.1
**Estimated Time:** 5 minutes

**Commands:**
```bash
python3 -m venv venv
source venv/bin/activate  # On WSL/Linux
```

### Task 1.3: Create API Key File
**Status:** Not Started
**Dependencies:** None
**Estimated Time:** 2 minutes

- Obtain Anthropic API key from https://console.anthropic.com/
- Create `api_key.dat` in project root
- Paste API key into file (single line, no extra spaces)
- Ensure file is in `.gitignore`

### Task 1.4: Create requirements.txt
**Status:** Not Started
**Dependencies:** None
**Estimated Time:** 5 minutes

List all required packages with versions.

### Task 1.5: Install Dependencies
**Status:** Not Started
**Dependencies:** Task 1.2, Task 1.4
**Estimated Time:** 5 minutes

**Command:**
```bash
pip install -r requirements.txt
```

---

## Phase 2: Core Module Development

### Task 2.1: Implement config.py
**Status:** Not Started
**Dependencies:** Task 1.1
**Estimated Lines:** 80-100
**Estimated Time:** 20 minutes

**Subtasks:**
- [ ] Define API configuration constants
- [ ] Define document configuration constants
- [ ] Define query configuration constants
- [ ] Define logging configuration constants
- [ ] Define visualization configuration constants
- [ ] Add comments for each section

**Validation:**
- Import config in Python REPL
- Verify all constants are accessible
- Check no typos in constant names

### Task 2.2: Implement logger_setup.py
**Status:** Not Started
**Dependencies:** Task 2.1
**Estimated Lines:** 70-80
**Estimated Time:** 30 minutes

**Subtasks:**
- [ ] Import necessary modules (logging, pathlib, RotatingFileHandler)
- [ ] Implement `setup_logger()` function
- [ ] Create log directory if not exists
- [ ] Configure RotatingFileHandler with ring buffer (20 files × 16MB)
- [ ] Set log format and level
- [ ] Add console handler for user feedback
- [ ] Return configured logger

**Validation:**
- Run logger_setup.py
- Verify log directory created
- Write test log messages
- Check log file created in ./log/
- Verify format is correct

**Test Code:**
```python
from context_window_test import logger_setup

logger = logger_setup.setup_logger()
logger.info("Test INFO message")
logger.warning("Test WARNING message")
logger.error("Test ERROR message")

# Check ./log/app.log exists and contains messages
```

### Task 2.3: Implement document_generator.py
**Status:** Not Started
**Dependencies:** Task 2.1, Task 2.2
**Estimated Lines:** 160-180
**Estimated Time:** 90 minutes

**Subtasks:**
- [ ] Import necessary modules
- [ ] Implement `generate_text_content(word_count)` function
  - [ ] Use Lorem Ipsum or word list
  - [ ] Repeat words to reach target count
  - [ ] Return text string
- [ ] Implement `insert_target_sentence(text, target)` function
  - [ ] Split text into words
  - [ ] Find middle index
  - [ ] Insert target sentence
  - [ ] Rejoin and return
- [ ] Implement `create_document(word_count)` function
  - [ ] Generate text content
  - [ ] Insert target sentence
  - [ ] Construct filename
  - [ ] Write to file in ./files/
  - [ ] Log progress
  - [ ] Return filename
- [ ] Implement `generate_all_documents(word_counts)` function
  - [ ] Create files directory
  - [ ] Use multiprocessing Pool
  - [ ] Generate all documents in parallel
  - [ ] Log completion
  - [ ] Return list of filenames

**Validation:**
- Run document_generator.py standalone
- Check 7 files created in ./files/
- Open each file and verify:
  - Word count is approximately correct (±5%)
  - Target sentence appears once
  - Target sentence is near the middle

**Test Code:**
```python
from context_window_test import document_generator, config

filenames = document_generator.generate_all_documents(config.WORD_COUNTS)
print(f"Generated: {filenames}")

# Manual check: open doc_2000.txt and verify content
```

### Task 2.4: Implement query_processor.py
**Status:** Not Started
**Dependencies:** Task 2.1, Task 2.2
**Estimated Lines:** 180-200
**Estimated Time:** 120 minutes

**Subtasks:**
- [ ] Import necessary modules (anthropic, time, pathlib)
- [ ] Implement `load_api_key()` function
  - [ ] Read from api_key.dat
  - [ ] Validate format
  - [ ] Return key (NEVER log it)
  - [ ] Handle errors gracefully
- [ ] Implement `initialize_client(api_key)` function
  - [ ] Create Anthropic client
  - [ ] Return client instance
- [ ] Implement `load_document(filename)` function
  - [ ] Read file from ./files/
  - [ ] Return text content
- [ ] Implement `count_tokens(client, text)` function
  - [ ] Use client.count_tokens() or tiktoken
  - [ ] Return token count
- [ ] Implement `query_document(client, document_text, query)` function
  - [ ] Start timer
  - [ ] Create API message with document as context
  - [ ] Send query
  - [ ] Stop timer
  - [ ] Extract response text
  - [ ] Return (response_text, elapsed_time)
- [ ] Implement `query_with_retry(client, document_text, query)` function
  - [ ] Wrap query_document with retry logic
  - [ ] Implement exponential backoff
  - [ ] Log retries
  - [ ] Raise exception after max retries
- [ ] Implement `process_document(client, filename, query)` function
  - [ ] Load document
  - [ ] Count tokens
  - [ ] Query with timing
  - [ ] Build results dict
  - [ ] Return results

**Validation:**
- Test with small document first
- Verify API connection works
- Check timing is accurate
- Verify token count is reasonable
- Test retry logic with invalid API key (temporarily)

**Test Code:**
```python
from context_window_test import query_processor, config

api_key = query_processor.load_api_key()
client = query_processor.initialize_client(api_key)

result = query_processor.process_document(client, "doc_2000.txt", config.QUERY_TEXT)
print(result)

# Expected output: dict with token_count, query_time, response, etc.
```

### Task 2.5: Implement accuracy_checker.py
**Status:** Not Started
**Dependencies:** Task 2.1, Task 2.2
**Estimated Lines:** 110-130
**Estimated Time:** 60 minutes

**Subtasks:**
- [ ] Import necessary modules (sentence_transformers or spacy)
- [ ] Implement `load_nlp_model()` function
  - [ ] Load SentenceTransformer model
  - [ ] Cache globally
  - [ ] Return model instance
- [ ] Implement `extract_answer(response)` function
  - [ ] Clean response text
  - [ ] Remove common prefixes
  - [ ] Return cleaned answer
- [ ] Implement `calculate_similarity(response, expected)` function
  - [ ] Load NLP model
  - [ ] Clean both texts
  - [ ] Encode texts
  - [ ] Calculate cosine similarity
  - [ ] Return similarity score (0-1)
- [ ] Implement `check_accuracy(response, expected, threshold)` function
  - [ ] Calculate similarity
  - [ ] Determine accuracy (1 or 0)
  - [ ] Log results
  - [ ] Return (accuracy, similarity_score)
- [ ] Implement `update_results_with_accuracy(results)` function
  - [ ] Call check_accuracy
  - [ ] Update results dict
  - [ ] Return updated dict

**Validation:**
- Test similarity with known examples:
  - "Ben Gurion was the first PM" vs "Ben Gurion was the first Prime Minister" → High similarity
  - "David Ben-Gurion" vs "Ben Gurion" → Medium-high similarity
  - "Netanyahu" vs "Ben Gurion" → Low similarity
- Verify accuracy threshold works correctly

**Test Code:**
```python
from context_window_test import accuracy_checker, config

# Test similarity
response1 = "Ben Gurion was the first Prime Minister of Israel."
response2 = "David Ben-Gurion."
response3 = "I don't know."

sim1 = accuracy_checker.calculate_similarity(response1, config.EXPECTED_ANSWER)
sim2 = accuracy_checker.calculate_similarity(response2, config.EXPECTED_ANSWER)
sim3 = accuracy_checker.calculate_similarity(response3, config.EXPECTED_ANSWER)

print(f"Similarity 1: {sim1}")  # Should be high (> 0.9)
print(f"Similarity 2: {sim2}")  # Should be medium (0.5-0.8)
print(f"Similarity 3: {sim3}")  # Should be low (< 0.3)
```

### Task 2.6: Implement visualization.py
**Status:** Not Started
**Dependencies:** Task 2.1, Task 2.2
**Estimated Lines:** 140-160
**Estimated Time:** 90 minutes

**Subtasks:**
- [ ] Import necessary modules (matplotlib, numpy)
- [ ] Implement `prepare_data(results_list)` function
  - [ ] Extract arrays for tokens, times, accuracies, words
  - [ ] Return dict with data arrays
- [ ] Implement `create_dual_axis_plot(data)` function
  - [ ] Create figure and primary axis
  - [ ] Plot query time on left y-axis (line plot)
  - [ ] Create secondary y-axis
  - [ ] Plot accuracy on right y-axis (scatter plot)
  - [ ] Add labels, title, legend, grid
  - [ ] Return figure
- [ ] Implement `save_graph(fig, filename)` function
  - [ ] Save with configured DPI
  - [ ] Use tight layout
  - [ ] Log save location
- [ ] Implement `print_results_table(results_list)` function
  - [ ] Print formatted table to console
  - [ ] Show all metrics
  - [ ] Calculate and show summary statistics
- [ ] Implement `visualize_results(results_list)` function
  - [ ] Prepare data
  - [ ] Create plot
  - [ ] Save graph
  - [ ] Print table
  - [ ] Close figure

**Validation:**
- Create mock results_list with sample data
- Run visualization
- Check graph file created
- Verify graph looks good (dual axes, proper labels)
- Verify table prints correctly

**Test Code:**
```python
from context_window_test import visualization

# Mock data
mock_results = [
    {"document_name": "doc_2000.txt", "word_count": 2000, "token_count": 2847,
     "query_time": 2.34, "accuracy": 1, "similarity_score": 0.95},
    {"document_name": "doc_5000.txt", "word_count": 5000, "token_count": 7123,
     "query_time": 3.56, "accuracy": 1, "similarity_score": 0.93},
    # ... more entries
]

visualization.visualize_results(mock_results)
# Check results_graph.png created and looks correct
```

### Task 2.7: Implement main.py
**Status:** Not Started
**Dependencies:** Task 2.1-2.6
**Estimated Lines:** 140-160
**Estimated Time:** 60 minutes

**Subtasks:**
- [ ] Import all modules
- [ ] Implement `main()` function
  - [ ] Initialize logging
  - [ ] Load API key and create client
  - [ ] Generate documents
  - [ ] Initialize empty results_list
  - [ ] Loop through documents
    - [ ] Process document (query)
    - [ ] Check accuracy
    - [ ] Append to results_list
    - [ ] Log progress
  - [ ] Visualize results
  - [ ] Log completion
  - [ ] Handle exceptions
- [ ] Add `if __name__ == "__main__"` block

**Validation:**
- Run end-to-end with all 7 documents
- Verify no errors
- Check all files created
- Verify graph generated
- Review logs

### Task 2.8: Implement __init__.py
**Status:** Not Started
**Dependencies:** Task 2.7
**Estimated Lines:** 20-30
**Estimated Time:** 10 minutes

**Subtasks:**
- [ ] Add package docstring
- [ ] Define __version__
- [ ] Define __author__
- [ ] Import main function
- [ ] Define __all__

**Validation:**
- Import package: `import context_window_test`
- Access version: `context_window_test.__version__`
- Call main: `context_window_test.main()`

---

## Phase 3: Testing and Validation

### Task 3.1: Unit Testing - Document Generator
**Status:** Not Started
**Dependencies:** Task 2.3
**Estimated Time:** 30 minutes

**Test Cases:**
- [ ] Verify word count accuracy (±5% tolerance)
- [ ] Verify target sentence appears exactly once
- [ ] Verify target sentence is at middle position (±10% tolerance)
- [ ] Verify all 7 files created
- [ ] Verify file naming convention

### Task 3.2: Unit Testing - Query Processor
**Status:** Not Started
**Dependencies:** Task 2.4
**Estimated Time:** 45 minutes

**Test Cases:**
- [ ] Test API key loading (valid and invalid)
- [ ] Test API client initialization
- [ ] Test document loading
- [ ] Test token counting
- [ ] Test query execution with mock data
- [ ] Test retry logic

### Task 3.3: Unit Testing - Accuracy Checker
**Status:** Not Started
**Dependencies:** Task 2.5
**Estimated Time:** 30 minutes

**Test Cases:**
- [ ] Test similarity with identical texts (should be ~1.0)
- [ ] Test similarity with similar texts (should be > 0.8)
- [ ] Test similarity with different texts (should be < 0.5)
- [ ] Test accuracy determination with threshold
- [ ] Test answer extraction

### Task 3.4: Integration Testing - End-to-End
**Status:** Not Started
**Dependencies:** Task 2.7
**Estimated Time:** 60 minutes

**Test Cases:**
- [ ] Run with 2 documents (small sample)
- [ ] Verify all components work together
- [ ] Check data flows correctly through pipeline
- [ ] Verify results_list structure
- [ ] Check graph generation
- [ ] Verify logging works

### Task 3.5: Full System Test
**Status:** Not Started
**Dependencies:** Task 3.4
**Estimated Time:** 120 minutes (includes API calls)

**Test Cases:**
- [ ] Run complete program with all 7 documents
- [ ] Monitor execution time
- [ ] Verify all API calls succeed
- [ ] Check accuracy results
- [ ] Verify token counts
- [ ] Inspect graph output
- [ ] Review log files
- [ ] Validate log rotation (if enough logs generated)

### Task 3.6: Manual Validation
**Status:** Not Started
**Dependencies:** Task 3.5
**Estimated Time:** 30 minutes

**Validation Steps:**
- [ ] Manually read 2-3 generated documents
- [ ] Verify Claude's responses are reasonable
- [ ] Check if hypothesis holds (accuracy degrades with size)
- [ ] Review graph for trends
- [ ] Verify all metrics make sense

---

## Phase 4: Documentation and Finalization

### Task 4.1: Code Documentation
**Status:** Not Started
**Dependencies:** Task 2.1-2.8
**Estimated Time:** 45 minutes

**Subtasks:**
- [ ] Add docstrings to all functions
- [ ] Add type hints where appropriate
- [ ] Add inline comments for complex logic
- [ ] Ensure code follows PEP 8

### Task 4.2: Create README.md
**Status:** Not Started
**Dependencies:** Task 4.1
**Estimated Time:** 30 minutes

**Content:**
- [ ] Project overview
- [ ] Installation instructions
- [ ] Usage instructions
- [ ] Configuration options
- [ ] Expected output
- [ ] Troubleshooting
- [ ] Author and license

### Task 4.3: Create .gitignore
**Status:** Not Started
**Dependencies:** None
**Estimated Time:** 5 minutes

**Include:**
```
venv/
__pycache__/
*.pyc
*.pyo
*.log
api_key.dat
files/
log/
results_graph.png
.vscode/
.idea/
*.egg-info/
dist/
build/
```

### Task 4.4: Final Review
**Status:** Not Started
**Dependencies:** All previous tasks
**Estimated Time:** 30 minutes

**Review Checklist:**
- [ ] All tasks completed
- [ ] All tests passing
- [ ] Documentation complete
- [ ] No API key exposed
- [ ] Relative paths only
- [ ] Code follows style guidelines
- [ ] No hardcoded values (use config.py)
- [ ] Error handling in place
- [ ] Logging comprehensive

---

## Phase 5: Optional Enhancements

### Task 5.1: Add Command-Line Arguments
**Status:** Not Started
**Dependencies:** Task 2.7
**Estimated Time:** 30 minutes

Use argparse to allow:
- Custom word counts
- Custom query
- Custom output filename
- Verbose mode

### Task 5.2: Export Results to JSON
**Status:** Not Started
**Dependencies:** Task 2.7
**Estimated Time:** 15 minutes

Save results_list to JSON file for further analysis.

### Task 5.3: Add Statistical Analysis
**Status:** Not Started
**Dependencies:** Task 2.6
**Estimated Time:** 60 minutes

Calculate:
- Correlation coefficient (tokens vs accuracy)
- Linear regression
- Confidence intervals

### Task 5.4: Create Test Suite
**Status:** Not Started
**Dependencies:** Task 3.1-3.3
**Estimated Time:** 90 minutes

Use pytest to create automated test suite.

---

## Summary

### Total Estimated Time
- **Phase 1:** ~30 minutes
- **Phase 2:** ~530 minutes (~9 hours)
- **Phase 3:** ~315 minutes (~5 hours)
- **Phase 4:** ~110 minutes (~2 hours)
- **Total:** ~16 hours

### Critical Path
1. Setup environment (Phase 1)
2. Implement core modules (Phase 2)
3. Integration testing (Phase 3)
4. Full system test (Phase 3)
5. Documentation (Phase 4)

### Dependencies Graph
```
Phase 1 (Setup)
    ↓
Task 2.1 (config.py)
    ↓
Task 2.2 (logger_setup.py)
    ↓
Tasks 2.3-2.6 (Parallel: document_generator, query_processor, accuracy_checker, visualization)
    ↓
Task 2.7 (main.py)
    ↓
Task 2.8 (__init__.py)
    ↓
Phase 3 (Testing)
    ↓
Phase 4 (Documentation)
```

---

## Progress Tracking

Use this checklist to track overall progress:

- [ ] **Phase 1:** Project Setup (5 tasks)
- [ ] **Phase 2:** Core Module Development (8 tasks)
- [ ] **Phase 3:** Testing and Validation (6 tasks)
- [ ] **Phase 4:** Documentation and Finalization (4 tasks)
- [ ] **Phase 5:** Optional Enhancements (4 tasks)

**Current Status:** Not Started
**Completion:** 0%

---

## Notes

- Prioritize getting end-to-end flow working before optimization
- Test incrementally (don't wait until everything is done)
- Use logging extensively for debugging
- Keep API costs in mind (test with smaller documents first)
- Document any deviations from plan
- Update this file as tasks are completed
