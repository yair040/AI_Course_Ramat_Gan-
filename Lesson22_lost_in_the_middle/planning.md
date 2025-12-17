# Project Planning Document
# Lost in the Middle - Implementation Plan

**Author:** Yair Levi
**Project:** Context Window Testing Framework
**Date:** 2025-12-10

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture Design](#architecture-design)
3. [Module Breakdown](#module-breakdown)
4. [Implementation Order](#implementation-order)
5. [Data Flow](#data-flow)
6. [Technical Decisions](#technical-decisions)
7. [Risk Management](#risk-management)
8. [Testing Strategy](#testing-strategy)

---

## Project Overview

### Goal
Build a Python framework to test the "Lost in the Middle" hypothesis by measuring Claude Haiku 4.5's ability to retrieve information from different positions within large documents.

### Constraints
- Python files: 150-200 lines maximum
- Platform: WSL with virtual environment
- API: Anthropic Claude Haiku 4.5
- Budget: Cost-optimized (using Haiku model)
- Paths: Relative only, no absolute paths

### Success Metrics
- 30 successful API queries (6 documents × 5 iterations)
- Accurate position tracking and counting
- Clear statistical comparison between positions
- Professional visualization of results

---

## Architecture Design

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Main Program                        │
│                          (main.py)                          │
└────────────────┬────────────────────────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
        ▼                 ▼
┌──────────────┐   ┌──────────────┐
│   Config     │   │   Logger     │
│ (config.py)  │   │  (utils.py)  │
└──────────────┘   └──────────────┘
        │
        ├─────────────┬─────────────┬─────────────┬──────────────┐
        ▼             ▼             ▼             ▼              ▼
┌──────────────┐ ┌──────────┐ ┌─────────┐ ┌──────────┐ ┌────────────┐
│   Document   │ │ Sentence │ │   API   │ │ Analyzer │ │ Visualizer │
│  Generator   │ │ Injector │ │ Tester  │ │          │ │            │
└──────────────┘ └──────────┘ └─────────┘ └──────────┘ └────────────┘
        │             │             │             │              │
        ▼             ▼             ▼             ▼              ▼
   ./files/      ./files/        API Calls    Statistics    ./results/
```

### Package Structure

```
exercise1_lost_in_the_middle/
│
├── __init__.py                    # Package initialization
│
├── main.py                        # Entry point, orchestration
│
├── config.py                      # Configuration constants
│   - Paths
│   - API settings
│   - Experiment parameters
│
├── utils.py                       # Utility functions
│   - Logging setup
│   - Credential loading
│   - Path helpers
│
├── document_generator.py          # Document generation module
│   - generate_document()
│   - save_document()
│   - generate_all_documents()
│
├── sentence_injector.py           # Sentence injection module
│   - inject_sentence()
│   - process_all_documents()
│   - get_injection_position()
│
├── api_tester.py                  # API testing module
│   - load_document()
│   - query_anthropic()
│   - check_answer()
│   - test_document()
│
├── analyzer.py                    # Statistical analysis module
│   - calculate_success_rates()
│   - generate_statistics()
│   - format_results()
│
├── visualizer.py                  # Visualization module
│   - create_bar_chart()
│   - save_visualization()
│
├── api_key.dat                    # API key (secure)
├── token.pickle                   # Token storage (secure)
├── requirements.txt               # Python dependencies
│
├── files/                         # Generated documents
│   ├── doc_1.txt
│   ├── doc_2.txt
│   ├── ...
│   ├── start_doc_1.txt
│   ├── start_doc_2.txt
│   ├── middle_doc_3.txt
│   ├── middle_doc_4.txt
│   ├── end_doc_5.txt
│   └── end_doc_6.txt
│
├── log/                           # Rotating log files
│   ├── app.log
│   ├── app.log.1
│   ├── ...
│   └── app.log.19
│
└── results/                       # Output visualizations
    ├── results_graph.png
    └── statistics.txt
```

---

## Module Breakdown

### 1. config.py (~50-80 lines)
**Purpose:** Central configuration management

**Key Components:**
- Path definitions (relative)
- Experiment parameters (word count, iterations, etc.)
- API model specification
- Logging configuration constants
- Test sentence constant

**Example Structure:**
```python
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
FILES_DIR = BASE_DIR / "files"
LOG_DIR = BASE_DIR / "log"
RESULTS_DIR = BASE_DIR / "results"

# Experiment parameters
DOCUMENT_COUNT = 6
WORD_COUNT_PER_DOCUMENT = 75000
TEST_ITERATIONS = 5
TEST_SENTENCE = "The 6 day war lasted 7 days"
TEST_QUESTION = "How many days did the 6 day war last?"

# API configuration
API_MODEL = "claude-haiku-4-5-20250929"
MAX_TOKENS = 1024

# Logging configuration
LOG_MAX_BYTES = 16 * 1024 * 1024  # 16MB
LOG_BACKUP_COUNT = 19
```

### 2. utils.py (~100-150 lines)
**Purpose:** Shared utility functions

**Key Functions:**
- `setup_logging()` - Configure rotating file handler
- `load_credentials()` - Load API key securely
- `ensure_directories()` - Create required directories
- `get_logger(name)` - Get configured logger instance
- `sanitize_filename(name)` - Clean filename strings

**Critical Features:**
- Ring buffer logging implementation
- Secure credential handling
- Directory creation with error handling

### 3. document_generator.py (~150-200 lines)
**Purpose:** Generate test documents

**Key Functions:**
- `generate_paragraph(word_count)` - Generate single paragraph
- `generate_document(word_count)` - Generate full document
- `save_document(content, filename)` - Write document to file
- `generate_all_documents()` - Generate all 6 base documents
- `count_words(text)` - Verify word count

**Strategy:**
- Use lorem ipsum or generated text
- Ensure coherent sentence structure
- Mix sentence lengths for natural flow
- Validate word count accuracy

**Considerations:**
- Can use `lorem` library or custom generation
- Ensure documents are large enough (~75k words)
- Make text suitable for context testing

### 4. sentence_injector.py (~150-200 lines)
**Purpose:** Inject test sentence into documents

**Key Functions:**
- `split_sentences(text)` - Parse document into sentences
- `inject_at_position(sentences, sentence, position)` - Insert sentence
- `inject_sentence(doc_path, position)` - Main injection function
- `process_all_documents()` - Process all 6 documents
- `validate_injection(doc_path)` - Verify injection success

**Position Logic:**
- **Start:** Random position between sentences 1-5
- **Middle:** Exactly at midpoint (len(sentences) // 2)
- **End:** Random position in last 5 sentences

**File Naming:**
- Original: `doc_1.txt`
- Start: `start_doc_1.txt`
- Middle: `middle_doc_3.txt`
- End: `end_doc_5.txt`

### 5. api_tester.py (~150-200 lines)
**Purpose:** Test documents using Anthropic API

**Key Functions:**
- `create_api_client(api_key)` - Initialize Anthropic client
- `load_document(file_path)` - Read document from file
- `query_document(client, document, question)` - Query API
- `check_answer_correctness(response, target)` - Validate answer
- `test_document(file_path)` - Complete test cycle for one document
- `test_all_documents()` - Test all documents in iteration

**API Implementation:**
- Use Claude Haiku 4.5 model
- Fresh context for each document (no conversation state)
- Error handling for API failures
- Token usage logging

**Answer Validation:**
- Check for "7 days" or "7" + "day" in response
- Optional: Use NLP similarity (nltk/spacy)
- Log validation results
- Return boolean success/failure

### 6. analyzer.py (~100-150 lines)
**Purpose:** Statistical analysis of results

**Key Functions:**
- `calculate_success_rates(counters, iterations)` - Compute percentages
- `generate_statistics(counters)` - Create statistical summary
- `format_results(counters, rates)` - Pretty print results
- `save_statistics(results)` - Export to text file
- `perform_significance_test(counters)` - Optional statistical testing

**Calculations:**
- Success rate per position type
- Total accuracy across all tests
- Standard deviation (if applicable)
- Confidence intervals (optional)

### 7. visualizer.py (~100-150 lines)
**Purpose:** Create visual representation

**Key Functions:**
- `create_bar_chart(counters, iterations)` - Generate bar chart
- `add_labels(bars, values)` - Add value labels to bars
- `save_chart(fig, filename)` - Save to file
- `display_chart(fig)` - Show to user
- `create_summary_table(counters)` - Optional table visualization

**Chart Specifications:**
- X-axis: Position (Start, Middle, End)
- Y-axis: Success rate (0-100%)
- Colors: Distinct for each position
- Labels: Show percentage on bars
- Title: Clear and descriptive
- Save: High DPI (300) PNG format

### 8. main.py (~150-200 lines)
**Purpose:** Program orchestration

**Key Functions:**
- `initialize()` - Setup logging, credentials, directories
- `run_experiment()` - Execute complete experiment
- `run_iteration(iteration_num, counters)` - Single iteration
- `main()` - Entry point

**Execution Flow:**
```python
def main():
    # 1. Initialize
    logger = initialize()

    # 2. Generate documents
    logger.info("Generating base documents...")
    generate_all_documents()

    # 3. Inject sentences
    logger.info("Injecting test sentences...")
    process_all_documents()

    # 4. Run iterations
    counters = {'start': 0, 'middle': 0, 'end': 0}

    for i in range(1, TEST_ITERATIONS + 1):
        logger.info(f"Starting iteration {i}")
        run_iteration(i, counters)

    # 5. Analyze results
    logger.info("Analyzing results...")
    results = generate_statistics(counters)

    # 6. Visualize
    logger.info("Creating visualization...")
    create_bar_chart(counters, TEST_ITERATIONS)

    # 7. Complete
    logger.info("Experiment complete!")
    logger.info(f"Final results: {results}")
```

---

## Implementation Order

### Phase 1: Infrastructure (Critical Foundation)
**Goal:** Set up basic infrastructure

1. Create package structure
   - Create `__init__.py`
   - Set up directory structure

2. Implement `config.py`
   - Define all constants
   - Set up path configuration

3. Implement `utils.py`
   - Logging setup with ring buffer
   - Credential loading
   - Directory creation helpers

4. Test infrastructure
   - Verify logging works
   - Confirm directories are created
   - Test credential loading

**Success Criteria:**
- Logging writes to `./log/` with rotation
- Directories auto-create
- Credentials load without exposing keys

---

### Phase 2: Document Generation (Core Data)
**Goal:** Generate test documents

5. Implement `document_generator.py`
   - Paragraph generation
   - Document assembly
   - File writing
   - Validation

6. Test document generation
   - Generate 1 small document (1000 words)
   - Verify word count
   - Check file creation

7. Generate all 6 full documents
   - Run generation for all documents
   - Verify all files exist in `./files/`
   - Check file sizes are appropriate

**Success Criteria:**
- 6 documents in `./files/` directory
- Each ~75,000 words
- Coherent, readable text

---

### Phase 3: Sentence Injection (Data Preparation)
**Goal:** Inject test sentence at positions

8. Implement `sentence_injector.py`
   - Sentence splitting
   - Position calculation
   - Injection logic
   - File naming and saving

9. Test injection
   - Test on small document first
   - Verify sentence placement
   - Check file naming

10. Process all documents
    - Inject in 2 at start
    - Inject in 2 at middle
    - Inject in 2 at end
    - Verify all 6 processed files exist

**Success Criteria:**
- 6 modified documents with correct prefixes
- Sentence verifiable at correct positions
- Original documents preserved

---

### Phase 4: API Integration (Core Testing)
**Goal:** Query documents via API

11. Implement `api_tester.py`
    - API client setup
    - Document loading
    - Query execution
    - Answer validation

12. Test API integration
    - Test with 1 small document
    - Verify response format
    - Test answer checking logic

13. Test with full documents
    - Run test on 1 full document
    - Monitor token usage
    - Verify logging

**Success Criteria:**
- Successful API connection
- Correct answer validation
- Appropriate error handling

---

### Phase 5: Main Loop (Integration)
**Goal:** Implement complete experiment flow

14. Implement `main.py`
    - Initialization
    - Iteration loop
    - Counter management
    - Error handling

15. Dry run test
    - Run with 1 iteration only
    - Test all 6 documents
    - Verify counters update correctly

16. Full experiment run
    - Execute 5 complete iterations
    - Monitor progress
    - Verify all 30 queries complete

**Success Criteria:**
- 30 successful API queries
- Accurate counter tracking
- Complete logs
- No crashes or errors

---

### Phase 6: Analysis & Visualization (Results)
**Goal:** Present results clearly

17. Implement `analyzer.py`
    - Success rate calculations
    - Statistical summary
    - Result formatting

18. Implement `visualizer.py`
    - Bar chart creation
    - Labels and formatting
    - File saving

19. Generate final output
    - Create visualization
    - Save statistics
    - Generate summary report

**Success Criteria:**
- Clear bar chart showing comparison
- Accurate percentages
- Professional appearance
- Results saved to `./results/`

---

### Phase 7: Polish & Documentation (Finalization)
**Goal:** Clean up and document

20. Code review
    - Check all files are 150-200 lines
    - Verify no absolute paths
    - Confirm no exposed API keys
    - Add missing docstrings

21. Testing
    - Run complete experiment again
    - Verify reproducibility
    - Check edge cases

22. Documentation
    - Update comments
    - Create usage instructions
    - Document any quirks or notes

**Success Criteria:**
- Clean, documented code
- Successful end-to-end run
- All requirements met

---

## Data Flow

### Detailed Data Flow Diagram

```
START
  │
  ├─► [1] document_generator.py
  │    ├─► Generate 6 documents (~75k words each)
  │    └─► Save to ./files/ as doc_1.txt ... doc_6.txt
  │
  ├─► [2] sentence_injector.py
  │    ├─► Load doc_1.txt → Inject at START → Save as start_doc_1.txt
  │    ├─► Load doc_2.txt → Inject at START → Save as start_doc_2.txt
  │    ├─► Load doc_3.txt → Inject at MIDDLE → Save as middle_doc_3.txt
  │    ├─► Load doc_4.txt → Inject at MIDDLE → Save as middle_doc_4.txt
  │    ├─► Load doc_5.txt → Inject at END → Save as end_doc_5.txt
  │    └─► Load doc_6.txt → Inject at END → Save as end_doc_6.txt
  │
  ├─► [3] Main iteration loop (×5)
  │    │
  │    └─► For each of 6 documents:
  │         │
  │         ├─► [4] api_tester.py
  │         │    ├─► Load document from ./files/
  │         │    ├─► Send to Anthropic API (Claude Haiku 4.5)
  │         │    ├─► Query: "How many days did the 6 day war last?"
  │         │    ├─► Receive response
  │         │    ├─► Check answer correctness (NLP similarity)
  │         │    └─► Return True/False
  │         │
  │         └─► Update counters
  │              ├─► If start_doc_X.txt and correct → counters['start'] += 1
  │              ├─► If middle_doc_X.txt and correct → counters['middle'] += 1
  │              └─► If end_doc_X.txt and correct → counters['end'] += 1
  │
  ├─► [5] analyzer.py
  │    ├─► Calculate success rates:
  │    │    ├─► start_rate = counters['start'] / 10 * 100
  │    │    ├─► middle_rate = counters['middle'] / 10 * 100
  │    │    └─► end_rate = counters['end'] / 10 * 100
  │    └─► Generate statistical summary
  │
  ├─► [6] visualizer.py
  │    ├─► Create bar chart (Start vs Middle vs End)
  │    ├─► Add labels and formatting
  │    ├─► Save to ./results/results_graph.png
  │    └─► Display to user
  │
  └─► END
       ├─► Log final results
       └─► Display summary
```

### State Management

**Global Counters:**
```python
counters = {
    'start': 0,    # Successful retrievals from start position
    'middle': 0,   # Successful retrievals from middle position
    'end': 0       # Successful retrievals from end position
}
```

**Tracking:**
- Each counter can range from 0 to 10 (2 documents × 5 iterations)
- Counters updated immediately after each successful query
- Final rates calculated as: (count / 10) × 100%

---

## Technical Decisions

### 1. Text Generation Strategy
**Decision:** Use lorem ipsum library or custom generator

**Rationale:**
- Need ~75,000 words per document
- Text must be coherent enough to not confuse the model
- Don't need perfectly meaningful content
- Speed and simplicity over sophistication

**Implementation:**
```python
# Option A: lorem library
import lorem
text = lorem.text() * 1000  # Generate enough text

# Option B: Custom generation
paragraphs = [generate_paragraph() for _ in range(500)]
text = '\n\n'.join(paragraphs)
```

### 2. NLP Similarity Method
**Decision:** Start simple, enhance if needed

**Approach 1 (Simple):**
```python
def check_answer(response):
    return "7" in response and "day" in response.lower()
```

**Approach 2 (Enhanced):**
```python
from difflib import SequenceMatcher

def check_answer(response, target):
    similarity = SequenceMatcher(None, response.lower(), target.lower()).ratio()
    return similarity >= 0.6
```

**Rationale:**
- Simple approach likely sufficient for clear-cut facts
- Can enhance if getting false positives/negatives

### 3. Multiprocessing Strategy
**Decision:** Parallel processing with caution

**Strategy:**
- Process multiple documents in parallel where safe
- Be mindful of API rate limits
- Use multiprocessing.Pool for document processing
- Keep API calls sequential per document

**Implementation:**
```python
# Parallel document generation (no API calls)
with Pool(processes=6) as pool:
    pool.map(generate_and_save_document, range(6))

# API testing - consider rate limits
# Either: Sequential (safe)
# Or: Parallel with rate limiting
```

### 4. Logging Verbosity
**Decision:** INFO level with key milestones

**What to log:**
- ✅ Program start/end
- ✅ Phase transitions
- ✅ Document generation progress
- ✅ API calls (without keys)
- ✅ Answer validation results
- ✅ Counter updates
- ✅ Errors and warnings
- ❌ Full document contents
- ❌ Excessive debug info

### 5. Error Recovery
**Decision:** Continue on failure, log and report

**Strategy:**
- If single API call fails → Log error, continue, mark as failure
- If document loading fails → Log error, skip document
- If logging fails → Print to console as fallback
- Track and report number of failures in final summary

---

## Risk Management

### Risk 1: API Rate Limiting
**Probability:** Medium
**Impact:** High (blocks entire experiment)

**Mitigation:**
- Use Claude Haiku 4.5 (lower rate limits than Opus)
- Add exponential backoff on rate limit errors
- Consider sequential processing instead of parallel
- Add delays between calls if needed

**Code:**
```python
import time
from anthropic import RateLimitError

def query_with_retry(client, document, question, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.messages.create(...)
        except RateLimitError:
            wait_time = 2 ** attempt
            logger.warning(f"Rate limited, waiting {wait_time}s")
            time.sleep(wait_time)
    raise Exception("Max retries exceeded")
```

### Risk 2: Large Token Costs
**Probability:** Medium
**Impact:** Medium (budget overrun)

**Mitigation:**
- Use Claude Haiku 4.5 (most cost-effective)
- Monitor token usage per call
- Set up cost alerts if possible
- Test with smaller documents first

**Monitoring:**
```python
usage = message.usage
logger.info(f"Tokens used: {usage.input_tokens} in, {usage.output_tokens} out")
```

### Risk 3: NLP Similarity False Negatives
**Probability:** Medium
**Impact:** Medium (incorrect results)

**Mitigation:**
- Start with simple keyword matching
- Manually verify a sample of responses
- Adjust threshold if needed
- Log all responses for post-analysis

**Validation:**
```python
# Log all responses for manual review
logger.info(f"Question: {question}")
logger.info(f"Response: {response}")
logger.info(f"Validated: {is_correct}")
```

### Risk 4: File System Issues
**Probability:** Low
**Impact:** High (program crash)

**Mitigation:**
- Ensure directories exist before writing
- Use try-except for all file operations
- Validate paths before use
- Check disk space

**Code:**
```python
def safe_write(path, content):
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
    except IOError as e:
        logger.error(f"Failed to write {path}: {e}")
        raise
```

### Risk 5: Memory Issues with Large Documents
**Probability:** Low
**Impact:** Medium (slow performance, crashes)

**Mitigation:**
- Process one document at a time
- Clear variables after use
- Don't keep all documents in memory
- Monitor memory usage during testing

---

## Testing Strategy

### Unit Testing
Test individual functions before integration.

**Document Generator:**
```python
def test_generate_document():
    doc = generate_document(word_count=1000)
    assert count_words(doc) == 1000 ± 10
    assert len(doc) > 0
    assert doc.count('.') > 50  # Multiple sentences
```

**Sentence Injector:**
```python
def test_inject_sentence():
    doc = "Sentence 1. Sentence 2. Sentence 3."
    result = inject_sentence(doc, "Test sentence", "middle")
    assert "Test sentence" in result
    assert result.count('.') == doc.count('.') + 1
```

**Answer Checker:**
```python
def test_check_answer():
    correct = "The war lasted 7 days"
    assert check_answer(correct, target=True)

    incorrect = "I don't know"
    assert not check_answer(incorrect, target=True)
```

### Integration Testing
Test complete workflows.

**Small Document End-to-End:**
```python
# Generate 1 small document (1000 words)
# Inject sentence
# Query API
# Validate response
# Check counter updates
```

**Full Workflow (Limited):**
```python
# Run 1 iteration with all 6 documents
# Verify counters
# Check logging
# Validate file outputs
```

### Manual Validation
Human verification of key outputs.

1. Inspect 2-3 generated documents (readability, word count)
2. Verify sentence injection positions manually
3. Review sample API responses
4. Check visualization appearance

### Performance Testing
Measure execution time and resource usage.

- Measure time per document generation
- Measure time per API call
- Monitor total execution time
- Check log file sizes

**Benchmarks:**
- Document generation: < 30 seconds per document
- API call: < 10 seconds per call
- Total experiment: < 10 minutes

---

## Success Checklist

Implementation complete when:

- [ ] All Python files created and under line limit
- [ ] Package structure with `__init__.py` in place
- [ ] Logging configured and writing to `./log/` with rotation
- [ ] Configuration centralized in `config.py`
- [ ] 6 base documents generated (~75k words each)
- [ ] Sentences injected at correct positions
- [ ] API integration working with Claude Haiku 4.5
- [ ] Answer validation logic functioning
- [ ] 30 total API queries executed (5 iterations × 6 documents)
- [ ] Counters tracking accurately
- [ ] Statistical analysis complete
- [ ] Visualization saved to `./results/`
- [ ] No API keys exposed in code or logs
- [ ] All paths are relative
- [ ] Code documented with docstrings
- [ ] Error handling throughout
- [ ] Manual testing completed
- [ ] Ready for full experiment run

---

**Next Step:** Review tasks.md for detailed step-by-step implementation tasks.
