# Task Breakdown
# Lost in the Middle - Implementation Tasks

**Author:** Yair Levi
**Project:** Context Window Testing Framework
**Purpose:** Step-by-step implementation checklist

---

## How to Use This Document

- Tasks are organized by phase
- Each task has a checkbox for tracking progress
- Dependencies are noted where applicable
- Estimated complexity provided (S/M/L)
- Follow tasks in order for best results

---

## Phase 1: Infrastructure Setup

### Task 1.1: Create Package Structure
**Complexity:** S | **Time:** 5 min | **Dependencies:** None

- [ ] Create `__init__.py` in project root
- [ ] Add package docstring to `__init__.py`
- [ ] Test import: `python -c "import exercise1_lost_in_the_middle"`

**Files to create:**
- `__init__.py`

**Success criteria:**
- Package imports without errors

---

### Task 1.2: Create Configuration Module
**Complexity:** M | **Time:** 15 min | **Dependencies:** None

- [ ] Create `config.py`
- [ ] Define base paths (using `pathlib.Path`)
- [ ] Set experiment parameters (document count, word count, iterations)
- [ ] Define API configuration constants
- [ ] Define logging configuration constants
- [ ] Add test sentence and question constants
- [ ] Verify all paths are relative

**Files to create:**
- `config.py`

**Success criteria:**
- All constants defined
- No absolute paths
- File under 200 lines

**Code template:**
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

---

### Task 1.3: Create Utility Module
**Complexity:** L | **Time:** 30 min | **Dependencies:** 1.2

- [ ] Create `utils.py`
- [ ] Implement `setup_logging()` function with RotatingFileHandler
- [ ] Implement `load_credentials()` function
- [ ] Implement `ensure_directories()` function
- [ ] Implement `get_logger(name)` function
- [ ] Add input validation and error handling
- [ ] Verify no API key exposure in logs

**Files to create:**
- `utils.py`

**Success criteria:**
- Logging creates ring buffer (20 files × 16MB)
- Credentials load securely
- Directories auto-create
- File under 200 lines

**Key functions:**
```python
def setup_logging()
def load_credentials()
def ensure_directories()
def get_logger(name)
```

---

### Task 1.4: Test Infrastructure
**Complexity:** S | **Time:** 10 min | **Dependencies:** 1.1, 1.2, 1.3

- [ ] Create test script to verify infrastructure
- [ ] Test logging writes to `./log/` directory
- [ ] Test directory creation
- [ ] Test credential loading (if api_key.dat exists)
- [ ] Verify log rotation works

**Commands:**
```python
# Test script
from utils import setup_logging, ensure_directories, get_logger
from config import LOG_DIR, FILES_DIR, RESULTS_DIR

ensure_directories()
setup_logging()
logger = get_logger(__name__)

logger.info("Test log message")
logger.warning("Test warning")
logger.error("Test error")

print(f"Logs created in: {LOG_DIR}")
print(f"Files directory: {FILES_DIR}")
print(f"Results directory: {RESULTS_DIR}")
```

**Success criteria:**
- Logs appear in `./log/app.log`
- All directories exist
- No errors

---

## Phase 2: Document Generation

### Task 2.1: Create Document Generator Module (Part 1)
**Complexity:** M | **Time:** 20 min | **Dependencies:** 1.2, 1.3

- [ ] Create `document_generator.py`
- [ ] Import necessary libraries
- [ ] Implement `generate_paragraph(word_count)` function
- [ ] Implement `count_words(text)` function
- [ ] Add logging statements

**Files to create:**
- `document_generator.py`

**Functions to implement:**
```python
def generate_paragraph(word_count: int = 150) -> str:
    """Generate a paragraph with approximately word_count words."""
    pass

def count_words(text: str) -> int:
    """Count words in text."""
    pass
```

---

### Task 2.2: Create Document Generator Module (Part 2)
**Complexity:** M | **Time:** 20 min | **Dependencies:** 2.1

- [ ] Implement `generate_document(word_count)` function
- [ ] Implement `save_document(content, filename)` function
- [ ] Add validation for word count accuracy
- [ ] Test with small document (1000 words)

**Functions to implement:**
```python
def generate_document(word_count: int = 75000) -> str:
    """Generate a full document with specified word count."""
    pass

def save_document(content: str, filename: str) -> None:
    """Save document to files directory."""
    pass
```

**Test:**
```python
doc = generate_document(word_count=1000)
print(f"Generated {count_words(doc)} words")
save_document(doc, "test_doc.txt")
```

---

### Task 2.3: Create Document Generator Module (Part 3)
**Complexity:** M | **Time:** 20 min | **Dependencies:** 2.2

- [ ] Implement `generate_all_documents()` function
- [ ] Add progress logging
- [ ] Implement error handling
- [ ] Ensure file is under 200 lines

**Functions to implement:**
```python
def generate_all_documents() -> None:
    """Generate all base documents for the experiment."""
    pass
```

**Success criteria:**
- Function generates 6 documents
- Each saved with naming: `doc_1.txt`, `doc_2.txt`, etc.
- Progress logged
- File under 200 lines

---

### Task 2.4: Test Document Generation
**Complexity:** M | **Time:** 30 min | **Dependencies:** 2.3

- [ ] Run `generate_all_documents()`
- [ ] Verify 6 files created in `./files/`
- [ ] Check word count for each document (~75,000 ± 1000)
- [ ] Inspect 1-2 documents manually for quality
- [ ] Verify logging captured process

**Verification commands:**
```bash
ls -lh ./files/
wc -w ./files/doc_*.txt
```

**Success criteria:**
- 6 documents in `./files/`
- Each ~75,000 words
- Text is coherent and readable

---

## Phase 3: Sentence Injection

### Task 3.1: Create Sentence Injector Module (Part 1)
**Complexity:** M | **Time:** 20 min | **Dependencies:** 1.2, 1.3

- [ ] Create `sentence_injector.py`
- [ ] Import necessary libraries
- [ ] Implement `split_sentences(text)` function
- [ ] Implement `calculate_position(sentences, position_type)` function
- [ ] Add logging

**Files to create:**
- `sentence_injector.py`

**Functions to implement:**
```python
def split_sentences(text: str) -> List[str]:
    """Split text into sentences."""
    pass

def calculate_position(sentences: List[str], position_type: str) -> int:
    """Calculate injection position index.

    Args:
        sentences: List of sentences
        position_type: 'start', 'middle', or 'end'

    Returns:
        Index where sentence should be inserted
    """
    pass
```

---

### Task 3.2: Create Sentence Injector Module (Part 2)
**Complexity:** M | **Time:** 20 min | **Dependencies:** 3.1

- [ ] Implement `inject_sentence(doc_path, sentence, position)` function
- [ ] Implement `get_output_filename(doc_path, position)` function
- [ ] Test with small document

**Functions to implement:**
```python
def inject_sentence(doc_path: Path, sentence: str, position: str) -> Path:
    """Inject sentence into document at specified position.

    Returns path to new file.
    """
    pass

def get_output_filename(doc_path: Path, position: str) -> Path:
    """Generate output filename with position prefix."""
    pass
```

**Test:**
```python
test_doc = FILES_DIR / "doc_1.txt"
result = inject_sentence(test_doc, TEST_SENTENCE, "middle")
print(f"Created: {result}")
```

---

### Task 3.3: Create Sentence Injector Module (Part 3)
**Complexity:** M | **Time:** 20 min | **Dependencies:** 3.2

- [ ] Implement `process_all_documents()` function
- [ ] Implement position distribution logic (2 start, 2 middle, 2 end)
- [ ] Add validation function
- [ ] Ensure file under 200 lines

**Functions to implement:**
```python
def process_all_documents() -> None:
    """Process all base documents and inject test sentence.

    Distribution:
    - doc_1.txt, doc_2.txt → start position
    - doc_3.txt, doc_4.txt → middle position
    - doc_5.txt, doc_6.txt → end position
    """
    pass

def validate_injection(doc_path: Path) -> bool:
    """Verify test sentence is in document."""
    pass
```

---

### Task 3.4: Test Sentence Injection
**Complexity:** M | **Time:** 30 min | **Dependencies:** 3.3

- [ ] Run `process_all_documents()`
- [ ] Verify 6 modified files created
- [ ] Check filenames have correct prefixes
- [ ] Manually verify sentence placement in 2-3 files
- [ ] Verify original documents unchanged

**Verification:**
```bash
ls -lh ./files/start_*
ls -lh ./files/middle_*
ls -lh ./files/end_*

# Manually check sentence location
grep -n "6 day war" ./files/start_doc_1.txt
grep -n "6 day war" ./files/middle_doc_3.txt
grep -n "6 day war" ./files/end_doc_5.txt
```

**Success criteria:**
- 6 new files with prefixes: `start_`, `middle_`, `end_`
- Sentence verifiable at correct positions
- Original files intact

---

## Phase 4: API Integration

### Task 4.1: Create API Tester Module (Part 1)
**Complexity:** M | **Time:** 20 min | **Dependencies:** 1.2, 1.3

- [ ] Create `api_tester.py`
- [ ] Import Anthropic library
- [ ] Implement `create_api_client(api_key)` function
- [ ] Implement `load_document(file_path)` function
- [ ] Add error handling for missing credentials

**Files to create:**
- `api_tester.py`

**Functions to implement:**
```python
def create_api_client(api_key: str):
    """Create Anthropic API client."""
    pass

def load_document(file_path: Path) -> str:
    """Load document from file."""
    pass
```

---

### Task 4.2: Create API Tester Module (Part 2)
**Complexity:** L | **Time:** 30 min | **Dependencies:** 4.1

- [ ] Implement `query_document(client, document, question)` function
- [ ] Add retry logic for rate limits
- [ ] Log token usage
- [ ] Ensure no API key in logs

**Functions to implement:**
```python
def query_document(client, document: str, question: str) -> str:
    """Query document using Anthropic API.

    Args:
        client: Anthropic client
        document: Full document text
        question: Question to ask

    Returns:
        API response text
    """
    pass
```

**Implementation notes:**
- Use `claude-haiku-4-5-20250929` model
- Set `max_tokens=1024`
- Log response length (not full response)
- Handle API errors gracefully

---

### Task 4.3: Create API Tester Module (Part 3)
**Complexity:** M | **Time:** 25 min | **Dependencies:** 4.2

- [ ] Implement `check_answer_correctness(response, target)` function
- [ ] Use simple keyword matching or NLP similarity
- [ ] Log validation results
- [ ] Test with known correct/incorrect answers

**Functions to implement:**
```python
def check_answer_correctness(response: str, target: str) -> bool:
    """Check if response contains correct answer.

    Args:
        response: API response
        target: Expected answer (TEST_SENTENCE)

    Returns:
        True if correct, False otherwise
    """
    pass
```

**Validation logic:**
```python
# Simple approach
if "7" in response and "day" in response.lower():
    return True

# Or NLP similarity
from difflib import SequenceMatcher
similarity = SequenceMatcher(None, response.lower(), target.lower()).ratio()
return similarity >= 0.6
```

---

### Task 4.4: Create API Tester Module (Part 4)
**Complexity:** M | **Time:** 20 min | **Dependencies:** 4.3

- [ ] Implement `test_document(file_path)` function
- [ ] Implement `get_position_type(file_path)` helper function
- [ ] Add comprehensive error handling
- [ ] Ensure file under 200 lines

**Functions to implement:**
```python
def test_document(file_path: Path) -> bool:
    """Complete test cycle for one document.

    Returns True if answer was correct, False otherwise.
    """
    pass

def get_position_type(file_path: Path) -> str:
    """Extract position type from filename.

    Returns: 'start', 'middle', or 'end'
    """
    pass
```

---

### Task 4.5: Test API Integration
**Complexity:** M | **Time:** 20 min | **Dependencies:** 4.4

- [ ] Ensure `api_key.dat` exists with valid API key
- [ ] Test with 1 small document first
- [ ] Test with 1 full document
- [ ] Verify response format
- [ ] Test answer validation logic
- [ ] Monitor token usage

**Test script:**
```python
from api_tester import test_document
from config import FILES_DIR

# Test with one document
test_file = FILES_DIR / "start_doc_1.txt"
result = test_document(test_file)
print(f"Test result: {result}")
```

**Success criteria:**
- Successful API connection
- Response received and validated
- Appropriate logging
- No exposed API keys

---

## Phase 5: Main Program Flow

### Task 5.1: Create Main Module (Part 1)
**Complexity:** M | **Time:** 20 min | **Dependencies:** All previous

- [ ] Create `main.py`
- [ ] Import all modules
- [ ] Implement `initialize()` function
- [ ] Implement `run_iteration(iteration_num, counters)` function
- [ ] Add logging for each phase

**Files to create:**
- `main.py`

**Functions to implement:**
```python
def initialize() -> logging.Logger:
    """Initialize program infrastructure.

    Returns configured logger.
    """
    pass

def run_iteration(iteration_num: int, counters: dict) -> None:
    """Run one complete iteration.

    Args:
        iteration_num: Current iteration number
        counters: Dictionary of success counters
    """
    pass
```

---

### Task 5.2: Create Main Module (Part 2)
**Complexity:** M | **Time:** 20 min | **Dependencies:** 5.1

- [ ] Implement `run_experiment()` function
- [ ] Add counter initialization
- [ ] Implement iteration loop
- [ ] Add progress logging

**Functions to implement:**
```python
def run_experiment() -> dict:
    """Run complete experiment.

    Returns dictionary of final counters.
    """
    counters = {'start': 0, 'middle': 0, 'end': 0}

    for i in range(1, TEST_ITERATIONS + 1):
        logger.info(f"Starting iteration {i}/{TEST_ITERATIONS}")
        run_iteration(i, counters)
        logger.info(f"Iteration {i} complete. Counters: {counters}")

    return counters
```

---

### Task 5.3: Create Main Module (Part 3)
**Complexity:** M | **Time:** 20 min | **Dependencies:** 5.2

- [ ] Implement `main()` function
- [ ] Add exception handling
- [ ] Add final summary logging
- [ ] Add `if __name__ == "__main__":` block
- [ ] Ensure file under 200 lines

**Implementation:**
```python
def main():
    """Main entry point."""
    try:
        # Initialize
        logger = initialize()
        logger.info("="*60)
        logger.info("Starting Lost in the Middle experiment")
        logger.info("="*60)

        # Generate documents (if not exists)
        if not documents_exist():
            logger.info("Generating base documents...")
            generate_all_documents()

            logger.info("Injecting test sentences...")
            process_all_documents()

        # Run experiment
        logger.info("Starting experiment iterations...")
        counters = run_experiment()

        # Results handled in Phase 6

        logger.info("="*60)
        logger.info("Experiment complete!")
        logger.info(f"Final counters: {counters}")
        logger.info("="*60)

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
```

---

### Task 5.4: Dry Run Test
**Complexity:** M | **Time:** 15 min | **Dependencies:** 5.3

- [ ] Modify `TEST_ITERATIONS` to 1 temporarily
- [ ] Run main program
- [ ] Verify all 6 documents tested
- [ ] Check counters update correctly
- [ ] Review logs for issues
- [ ] Revert `TEST_ITERATIONS` to 5

**Commands:**
```bash
# Run dry run
python main.py

# Check results
cat ./log/app.log | tail -50
```

**Success criteria:**
- Program completes without errors
- 6 documents tested
- Counters show results
- Logs are detailed

---

### Task 5.5: Full Experiment Run
**Complexity:** L | **Time:** 30 min | **Dependencies:** 5.4

- [ ] Ensure `TEST_ITERATIONS = 5` in config
- [ ] Run full experiment: `python main.py`
- [ ] Monitor progress (30 total API calls)
- [ ] Verify completion
- [ ] Check final counters

**Success criteria:**
- 30 API calls complete (6 docs × 5 iterations)
- All counters populated
- No errors in logs
- Logs show all iterations

---

## Phase 6: Analysis & Visualization

### Task 6.1: Create Analyzer Module
**Complexity:** M | **Time:** 25 min | **Dependencies:** 1.2, 1.3

- [ ] Create `analyzer.py`
- [ ] Implement `calculate_success_rates(counters, iterations)` function
- [ ] Implement `generate_statistics(counters)` function
- [ ] Implement `format_results(counters, rates)` function
- [ ] Implement `save_statistics(results, filename)` function
- [ ] Ensure file under 200 lines

**Files to create:**
- `analyzer.py`

**Functions to implement:**
```python
def calculate_success_rates(counters: dict, iterations: int) -> dict:
    """Calculate success rate percentages."""
    pass

def generate_statistics(counters: dict) -> dict:
    """Generate statistical summary."""
    pass

def format_results(counters: dict, rates: dict) -> str:
    """Format results as readable string."""
    pass

def save_statistics(results: str, filename: str) -> None:
    """Save statistics to file."""
    pass
```

**Calculation:**
```python
# Each position: 2 documents × 5 iterations = 10 tests
tests_per_position = 2 * iterations
rate = (counters[position] / tests_per_position) * 100
```

---

### Task 6.2: Create Visualizer Module
**Complexity:** M | **Time:** 30 min | **Dependencies:** 1.2, 1.3

- [ ] Create `visualizer.py`
- [ ] Import matplotlib/plotly
- [ ] Implement `create_bar_chart(counters, iterations)` function
- [ ] Implement `save_chart(fig, filename)` function
- [ ] Add labels, colors, and formatting
- [ ] Ensure file under 200 lines

**Files to create:**
- `visualizer.py`

**Functions to implement:**
```python
def create_bar_chart(counters: dict, iterations: int):
    """Create bar chart visualization.

    Returns matplotlib figure.
    """
    pass

def save_chart(fig, filename: str) -> None:
    """Save chart to results directory."""
    pass
```

**Chart requirements:**
- X-axis: Start, Middle, End
- Y-axis: Success rate (0-100%)
- Colors: Distinct for each bar
- Labels: Show percentage on bars
- Title: Clear and descriptive
- Save: 300 DPI PNG

---

### Task 6.3: Integrate Analysis into Main
**Complexity:** S | **Time:** 15 min | **Dependencies:** 6.1, 6.2, 5.3

- [ ] Update `main.py` to call analyzer
- [ ] Update `main.py` to call visualizer
- [ ] Add analysis logging
- [ ] Test integration

**Add to main():**
```python
# After run_experiment()
logger.info("Analyzing results...")
results = generate_statistics(counters)
formatted = format_results(counters, calculate_success_rates(counters, TEST_ITERATIONS))
logger.info(f"\n{formatted}")
save_statistics(formatted, "statistics.txt")

logger.info("Creating visualization...")
fig = create_bar_chart(counters, TEST_ITERATIONS)
save_chart(fig, "results_graph.png")
```

---

### Task 6.4: Test Analysis and Visualization
**Complexity:** S | **Time:** 15 min | **Dependencies:** 6.3

- [ ] Run full experiment again
- [ ] Verify statistics file created in `./results/`
- [ ] Verify graph saved in `./results/`
- [ ] Open and inspect graph
- [ ] Verify accuracy of calculations

**Success criteria:**
- `./results/statistics.txt` exists
- `./results/results_graph.png` exists
- Graph shows clear comparison
- Percentages are accurate

---

## Phase 7: Final Polish

### Task 7.1: Code Review
**Complexity:** M | **Time:** 30 min | **Dependencies:** All

- [ ] Check all files are 150-200 lines max
- [ ] Verify no absolute paths anywhere
- [ ] Confirm no exposed API keys
- [ ] Check all imports are used
- [ ] Verify all functions have docstrings
- [ ] Check error handling in all modules
- [ ] Review logging statements

**Files to review:**
- [ ] `__init__.py`
- [ ] `config.py`
- [ ] `utils.py`
- [ ] `document_generator.py`
- [ ] `sentence_injector.py`
- [ ] `api_tester.py`
- [ ] `analyzer.py`
- [ ] `visualizer.py`
- [ ] `main.py`

---

### Task 7.2: Test Edge Cases
**Complexity:** M | **Time:** 30 min | **Dependencies:** 7.1

- [ ] Test with missing `api_key.dat`
- [ ] Test with invalid API key
- [ ] Test with existing documents (should skip generation)
- [ ] Test with missing directories (should auto-create)
- [ ] Test log rotation (create many log entries)

**Success criteria:**
- Graceful error handling
- Appropriate error messages
- No crashes

---

### Task 7.3: Create requirements.txt
**Complexity:** S | **Time:** 10 min | **Dependencies:** All

- [ ] List all Python dependencies
- [ ] Include version numbers where important
- [ ] Test installation in fresh virtual environment

**See separate task below for requirements.txt content**

---

### Task 7.4: Final Documentation
**Complexity:** M | **Time:** 20 min | **Dependencies:** 7.3

- [ ] Review all docstrings
- [ ] Add inline comments where code is complex
- [ ] Create usage instructions (README or comments in main.py)
- [ ] Document any known issues or limitations

---

### Task 7.5: Final Full Test
**Complexity:** L | **Time:** 30 min | **Dependencies:** All

- [ ] Create fresh virtual environment
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Run complete experiment
- [ ] Verify all outputs
- [ ] Check logs
- [ ] Review results

**Commands:**
```bash
# Fresh environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install
pip install -r requirements.txt

# Run
python main.py

# Verify outputs
ls -R ./files/
ls -R ./log/
ls -R ./results/
```

**Success criteria:**
- Program runs start to finish
- All 30 API calls succeed
- Results are accurate
- Visualization looks professional
- No errors in logs

---

## requirements.txt Content

Create `requirements.txt` with the following dependencies:

```
anthropic>=0.39.0
matplotlib>=3.7.0
lorem>=0.1.1
pathlib>=1.0.1
```

Optional additions (if used):
```
spacy>=3.7.0
nltk>=3.8.0
plotly>=5.18.0
```

---

## Completion Checklist

### All Tasks Complete When:

**Documentation:**
- [x] PRD.md created
- [x] Claude.md created
- [x] planning.md created
- [x] tasks.md created (this file)
- [ ] requirements.txt created

**Code Files:**
- [ ] `__init__.py` created
- [ ] `config.py` created and configured
- [ ] `utils.py` created with all functions
- [ ] `document_generator.py` created and tested
- [ ] `sentence_injector.py` created and tested
- [ ] `api_tester.py` created and tested
- [ ] `analyzer.py` created
- [ ] `visualizer.py` created
- [ ] `main.py` created and tested

**Testing:**
- [ ] Infrastructure tested
- [ ] Document generation tested
- [ ] Sentence injection tested
- [ ] API integration tested
- [ ] Full experiment run successful (5 iterations)
- [ ] Analysis and visualization verified
- [ ] Edge cases tested

**Outputs:**
- [ ] 6 base documents in `./files/`
- [ ] 6 modified documents in `./files/`
- [ ] Logs in `./log/` with rotation
- [ ] Statistics in `./results/statistics.txt`
- [ ] Graph in `./results/results_graph.png`

**Quality:**
- [ ] All files under 200 lines
- [ ] All paths are relative
- [ ] No API keys exposed
- [ ] All functions documented
- [ ] Error handling throughout
- [ ] Code follows best practices

---

**Ready for Execution!**

Start with Phase 1, Task 1.1 and work through sequentially. Good luck!
