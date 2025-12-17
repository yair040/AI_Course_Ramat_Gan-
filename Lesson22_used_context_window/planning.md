# Implementation Planning Document
# Context Window Size Impact Testing Program

**Author:** Yair Levi
**Version:** 1.0
**Date:** 2025-12-14

---

## 1. Architecture Overview

### 1.1 System Design

```
┌─────────────────────────────────────────────────────────┐
│                      main.py                            │
│  (Orchestration Layer - Entry Point)                   │
└──────────┬──────────────────────────────────────────────┘
           │
           ├──> logger_setup.py (Initialize Logging)
           │
           ├──> document_generator.py (Create Test Docs)
           │    └──> files/doc_*.txt
           │
           ├──> query_processor.py (API Calls)
           │    ├──> Load API Key
           │    ├──> Query Claude
           │    └──> Measure Time & Tokens
           │
           ├──> accuracy_checker.py (NLP Validation)
           │    └──> Calculate Similarity
           │
           └──> visualization.py (Generate Graphs)
                └──> results_graph.png
```

### 1.2 Data Flow

```
[Config] ──> [Main] ──> [Doc Generator] ──> [Files Created]
                │
                ├──> [Query Processor] ──> [Anthropic API] ──> [Response]
                │                                                    │
                │                                                    v
                └──> [Accuracy Checker] <────────────────────[Compare]
                                │
                                v
                        [Results List Updated]
                                │
                                v
                        [Visualization] ──> [Graph Output]
```

---

## 2. Module Specifications

### 2.1 config.py

**Purpose:** Centralized configuration
**Lines:** ~80 lines
**Dependencies:** None

**Content:**
```python
# API Configuration
API_KEY_FILE = "api_key.dat"
MODEL_NAME = "claude-haiku-4-5-20250929"
MAX_TOKENS_RESPONSE = 4096
API_MAX_RETRIES = 3
API_RETRY_DELAY = 2  # seconds

# Document Configuration
WORD_COUNTS = [2000, 5000, 10000, 20000, 30000, 40000, 50000]
TARGET_SENTENCE = "The first prime minister of Israel was Ben Gurion"
FILES_DIR = "./files"
DOC_NAME_PREFIX = "doc_"
DOC_EXTENSION = ".txt"

# Query Configuration
QUERY_TEXT = "Who was the first Prime Minister of Israel?"
EXPECTED_ANSWER = "Ben Gurion was the first Prime Minister of Israel"
SIMILARITY_THRESHOLD = 0.85

# Logging Configuration
LOG_DIR = "./log"
LOG_FILENAME = "app.log"
LOG_FILE_SIZE = 16 * 1024 * 1024  # 16MB
LOG_FILE_COUNT = 20
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Visualization Configuration
OUTPUT_GRAPH = "results_graph.png"
GRAPH_TITLE = "Context Window Size Impact on Query Performance"
GRAPH_DPI = 300
GRAPH_FIGSIZE = (12, 8)

# Text Generation Configuration
LOREM_IPSUM_BASE = "Lorem ipsum dolor sit amet..."  # Base text for padding
RANDOM_SEED = 42  # For reproducibility
```

### 2.2 logger_setup.py

**Purpose:** Configure logging with ring buffer
**Lines:** ~70 lines
**Dependencies:** logging, pathlib, config

**Functions:**
1. `setup_logger() -> logging.Logger`
   - Create log directory if not exists
   - Configure RotatingFileHandler
   - Set format and level
   - Return configured logger

**Implementation Details:**
```python
from logging.handlers import RotatingFileHandler
import logging
from pathlib import Path
import config

def setup_logger():
    """
    Set up rotating file handler with ring buffer.
    Returns configured logger.
    """
    # Create log directory
    log_path = Path(config.LOG_DIR)
    log_path.mkdir(exist_ok=True)

    # Create logger
    logger = logging.getLogger("context_window_test")
    logger.setLevel(getattr(logging, config.LOG_LEVEL))

    # Create rotating file handler
    log_file = log_path / config.LOG_FILENAME
    handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=config.LOG_FILE_SIZE,
        backupCount=config.LOG_FILE_COUNT - 1  # 19 backups + 1 main = 20 total
    )

    # Set formatter
    formatter = logging.Formatter(config.LOG_FORMAT)
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)

    # Also add console handler for user feedback
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
```

### 2.3 document_generator.py

**Purpose:** Generate test documents with target sentence
**Lines:** ~180 lines
**Dependencies:** pathlib, config, logging, multiprocessing

**Functions:**
1. `generate_text_content(word_count: int) -> str`
   - Generate or repeat Lorem Ipsum text
   - Return text with approximately `word_count` words

2. `insert_target_sentence(text: str, target: str) -> str`
   - Split text at middle
   - Insert target sentence
   - Return combined text

3. `create_document(word_count: int) -> str`
   - Generate text content
   - Insert target sentence at middle
   - Save to file
   - Return filename

4. `generate_all_documents(word_counts: list) -> list`
   - Create files directory
   - Use multiprocessing to generate documents in parallel
   - Return list of filenames

**Implementation Strategy:**
- Use `multiprocessing.Pool` with 4-7 processes
- Each process generates one document
- Use Lorem Ipsum or random word generation
- Validate word count accuracy (±5% tolerance)

**Pseudocode:**
```python
def generate_text_content(word_count):
    lorem_base = "Lorem ipsum dolor sit..."
    words = lorem_base.split()

    # Repeat words to reach word_count
    full_text = []
    while len(full_text) < word_count:
        full_text.extend(words)

    return " ".join(full_text[:word_count])

def insert_target_sentence(text, target):
    words = text.split()
    mid_index = len(words) // 2
    words.insert(mid_index, target)
    return " ".join(words)

def create_document(word_count):
    text = generate_text_content(word_count)
    text = insert_target_sentence(text, config.TARGET_SENTENCE)

    filename = f"{config.DOC_NAME_PREFIX}{word_count}{config.DOC_EXTENSION}"
    filepath = Path(config.FILES_DIR) / filename

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)

    return filename

def generate_all_documents(word_counts):
    Path(config.FILES_DIR).mkdir(exist_ok=True)

    with Pool(processes=min(len(word_counts), 7)) as pool:
        filenames = pool.map(create_document, word_counts)

    return filenames
```

### 2.4 query_processor.py

**Purpose:** Handle API communication and timing
**Lines:** ~190 lines
**Dependencies:** anthropic, time, pathlib, config, logging

**Functions:**
1. `load_api_key() -> str`
   - Read API key from file
   - Validate format
   - Return key (never log it!)

2. `initialize_client(api_key: str) -> Anthropic`
   - Create Anthropic client
   - Return client instance

3. `load_document(filename: str) -> str`
   - Read document content from files directory
   - Return text content

4. `count_tokens(client: Anthropic, text: str) -> int`
   - Count tokens in text
   - Use client.count_tokens() if available
   - Otherwise use tiktoken
   - Return token count

5. `query_document(client: Anthropic, document_text: str, query: str) -> tuple`
   - Start timer
   - Create message with document as context
   - Send query to API
   - Stop timer
   - Return (response_text, elapsed_time)

6. `query_with_retry(client: Anthropic, document_text: str, query: str) -> tuple`
   - Wrapper with retry logic
   - Exponential backoff
   - Return result or raise exception

7. `process_document(client: Anthropic, filename: str, query: str) -> dict`
   - Main function to process one document
   - Load document
   - Count tokens
   - Query with timing
   - Return results dict

**Implementation Details:**
```python
def load_api_key():
    try:
        with open(config.API_KEY_FILE, "r") as f:
            api_key = f.read().strip()

        if not api_key or len(api_key) < 20:
            raise ValueError("Invalid API key format")

        logger.info("API key loaded successfully")
        return api_key
    except FileNotFoundError:
        logger.error(f"API key file not found: {config.API_KEY_FILE}")
        raise
    except Exception as e:
        logger.error(f"Error loading API key: {e}")
        raise

def query_document(client, document_text, query):
    start_time = time.time()

    try:
        message = client.messages.create(
            model=config.MODEL_NAME,
            max_tokens=config.MAX_TOKENS_RESPONSE,
            messages=[
                {
                    "role": "user",
                    "content": f"Document:\n{document_text}\n\nQuestion: {query}"
                }
            ]
        )

        end_time = time.time()
        elapsed_time = end_time - start_time

        response_text = message.content[0].text
        return (response_text, elapsed_time)

    except Exception as e:
        logger.error(f"Error querying document: {e}")
        raise

def process_document(client, filename, query):
    logger.info(f"Processing {filename}...")

    # Load document
    filepath = Path(config.FILES_DIR) / filename
    with open(filepath, "r", encoding="utf-8") as f:
        document_text = f.read()

    # Count tokens
    token_count = count_tokens(client, document_text)

    # Query with timing
    response_text, query_time = query_with_retry(client, document_text, query)

    # Extract word count from filename
    word_count = int(filename.split("_")[1].split(".")[0])

    return {
        "document_name": filename,
        "word_count": word_count,
        "token_count": token_count,
        "query_time": query_time,
        "response": response_text,
        "accuracy": None,  # To be filled by accuracy checker
        "similarity_score": None
    }
```

### 2.5 accuracy_checker.py

**Purpose:** Calculate semantic similarity and determine accuracy
**Lines:** ~120 lines
**Dependencies:** sentence_transformers (or spacy), config, logging

**Functions:**
1. `load_nlp_model() -> SentenceTransformer`
   - Load pre-trained model
   - Cache for reuse
   - Return model instance

2. `calculate_similarity(response: str, expected: str) -> float`
   - Encode both texts
   - Calculate cosine similarity
   - Return similarity score (0-1)

3. `extract_answer(response: str) -> str`
   - Clean and extract main answer from response
   - Handle various response formats
   - Return cleaned answer

4. `check_accuracy(response: str, expected: str, threshold: float) -> tuple`
   - Calculate similarity
   - Determine if accuracy = 1 or 0
   - Return (accuracy, similarity_score)

5. `update_results_with_accuracy(results: dict) -> dict`
   - Take results dict from query_processor
   - Check accuracy
   - Update dict with accuracy and similarity_score
   - Return updated dict

**Implementation Details:**
```python
from sentence_transformers import SentenceTransformer, util
import config
import logging

logger = logging.getLogger("context_window_test")

# Global model cache
_nlp_model = None

def load_nlp_model():
    global _nlp_model
    if _nlp_model is None:
        logger.info("Loading NLP model for similarity checking...")
        _nlp_model = SentenceTransformer('all-MiniLM-L6-v2')
        logger.info("NLP model loaded successfully")
    return _nlp_model

def calculate_similarity(response, expected):
    model = load_nlp_model()

    # Clean texts
    response_clean = extract_answer(response)
    expected_clean = expected.strip()

    # Encode
    emb1 = model.encode(response_clean, convert_to_tensor=True)
    emb2 = model.encode(expected_clean, convert_to_tensor=True)

    # Calculate similarity
    similarity = util.pytorch_cos_sim(emb1, emb2).item()

    return similarity

def extract_answer(response):
    # Remove common prefixes
    response = response.strip()
    prefixes = ["The answer is", "According to the document", "Based on"]

    for prefix in prefixes:
        if response.startswith(prefix):
            response = response[len(prefix):].strip()

    return response

def check_accuracy(response, expected, threshold):
    similarity = calculate_similarity(response, expected)
    accuracy = 1 if similarity >= threshold else 0

    logger.info(f"Similarity: {similarity:.4f}, Accuracy: {accuracy}")

    return (accuracy, similarity)

def update_results_with_accuracy(results):
    accuracy, similarity = check_accuracy(
        results["response"],
        config.EXPECTED_ANSWER,
        config.SIMILARITY_THRESHOLD
    )

    results["accuracy"] = accuracy
    results["similarity_score"] = similarity

    return results
```

### 2.6 visualization.py

**Purpose:** Generate graphs from results
**Lines:** ~150 lines
**Dependencies:** matplotlib, numpy, config, logging

**Functions:**
1. `prepare_data(results_list: list) -> dict`
   - Extract data arrays from results
   - Return dict with x, y data

2. `create_dual_axis_plot(data: dict) -> Figure`
   - Create figure with two y-axes
   - Plot time and accuracy vs tokens
   - Return figure

3. `save_graph(fig: Figure, filename: str)`
   - Save figure to file
   - Use configured DPI and format

4. `print_results_table(results_list: list)`
   - Print formatted table to console
   - Show all metrics

5. `visualize_results(results_list: list)`
   - Main function
   - Prepare data
   - Create plot
   - Save graph
   - Print table

**Implementation Details:**
```python
import matplotlib.pyplot as plt
import numpy as np
import config
import logging

logger = logging.getLogger("context_window_test")

def prepare_data(results_list):
    token_counts = [r["token_count"] for r in results_list]
    query_times = [r["query_time"] for r in results_list]
    accuracies = [r["accuracy"] for r in results_list]
    word_counts = [r["word_count"] for r in results_list]

    return {
        "tokens": token_counts,
        "times": query_times,
        "accuracies": accuracies,
        "words": word_counts
    }

def create_dual_axis_plot(data):
    fig, ax1 = plt.subplots(figsize=config.GRAPH_FIGSIZE)

    # Plot query time on left y-axis
    color = 'tab:blue'
    ax1.set_xlabel('Token Count', fontsize=12)
    ax1.set_ylabel('Query Time (seconds)', color=color, fontsize=12)
    ax1.plot(data["tokens"], data["times"], color=color, marker='o',
             linewidth=2, markersize=8, label='Query Time')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, alpha=0.3)

    # Create second y-axis for accuracy
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Accuracy (0 or 1)', color=color, fontsize=12)
    ax2.scatter(data["tokens"], data["accuracies"], color=color,
                s=150, marker='s', label='Accuracy', zorder=5)
    ax2.set_ylim(-0.1, 1.1)
    ax2.tick_params(axis='y', labelcolor=color)

    # Title and legend
    plt.title(config.GRAPH_TITLE, fontsize=14, fontweight='bold')

    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    plt.tight_layout()
    return fig

def print_results_table(results_list):
    print("\n" + "="*70)
    print("RESULTS SUMMARY")
    print("="*70)
    print(f"{'Document':<18} {'Tokens':>10} {'Time (s)':>10} {'Accuracy':>10} {'Similarity':>10}")
    print("-"*70)

    for result in results_list:
        print(f"{result['document_name']:<18} "
              f"{result['token_count']:>10,} "
              f"{result['query_time']:>10.2f} "
              f"{result['accuracy']:>10} "
              f"{result['similarity_score']:>10.4f}")

    print("="*70)

    # Calculate summary statistics
    total_time = sum(r["query_time"] for r in results_list)
    avg_accuracy = sum(r["accuracy"] for r in results_list) / len(results_list)

    print(f"\nTotal Time: {total_time:.2f}s")
    print(f"Average Accuracy: {avg_accuracy:.2%}")
    print("="*70 + "\n")

def visualize_results(results_list):
    logger.info("Generating visualization...")

    # Prepare data
    data = prepare_data(results_list)

    # Create plot
    fig = create_dual_axis_plot(data)

    # Save
    fig.savefig(config.OUTPUT_GRAPH, dpi=config.GRAPH_DPI, bbox_inches='tight')
    logger.info(f"Graph saved to {config.OUTPUT_GRAPH}")

    # Print table
    print_results_table(results_list)

    plt.close(fig)
```

### 2.7 main.py

**Purpose:** Orchestrate entire workflow
**Lines:** ~150 lines
**Dependencies:** All modules, logging

**Functions:**
1. `main()`
   - Initialize logging
   - Load API key and create client
   - Generate documents
   - Initialize results list
   - Loop through documents
   - Process each document
   - Visualize results
   - Handle errors

**Workflow:**
```python
import logging
from pathlib import Path
import config
import logger_setup
import document_generator
import query_processor
import accuracy_checker
import visualization

def main():
    # 1. Initialize logging
    logger = logger_setup.setup_logger()
    logger.info("="*50)
    logger.info("Context Window Size Impact Test - Starting")
    logger.info("="*50)

    try:
        # 2. Load API key and initialize client
        api_key = query_processor.load_api_key()
        client = query_processor.initialize_client(api_key)
        logger.info("Anthropic client initialized")

        # 3. Generate documents
        logger.info(f"Generating {len(config.WORD_COUNTS)} documents...")
        filenames = document_generator.generate_all_documents(config.WORD_COUNTS)
        logger.info(f"Documents generated: {filenames}")

        # 4. Initialize results list
        results_list = []

        # 5. Process each document
        for filename in filenames:
            # Query document
            result = query_processor.process_document(
                client,
                filename,
                config.QUERY_TEXT
            )

            # Check accuracy
            result = accuracy_checker.update_results_with_accuracy(result)

            # Add to results
            results_list.append(result)

            logger.info(f"Completed {filename}: "
                       f"Tokens={result['token_count']}, "
                       f"Time={result['query_time']:.2f}s, "
                       f"Accuracy={result['accuracy']}")

        # 6. Visualize results
        visualization.visualize_results(results_list)

        logger.info("="*50)
        logger.info("Test completed successfully!")
        logger.info("="*50)

    except Exception as e:
        logger.error(f"Error in main execution: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
```

### 2.8 __init__.py

**Purpose:** Package initialization
**Lines:** ~30 lines
**Dependencies:** None

**Content:**
```python
"""
Context Window Size Impact Testing Package

Tests the hypothesis that LLM search accuracy degrades with increasing
context window size.

Author: Yair Levi
"""

__version__ = "1.0.0"
__author__ = "Yair Levi"

# Import main function for easy access
from .main import main

__all__ = ["main"]
```

---

## 3. Implementation Sequence

### Phase 1: Foundation (Day 1)
1. Create directory structure
2. Implement `config.py` ✓
3. Implement `logger_setup.py` ✓
4. Test logging functionality
5. Create `__init__.py` ✓

### Phase 2: Document Generation (Day 1-2)
6. Implement `document_generator.py` ✓
7. Test document generation
8. Verify sentence placement
9. Validate word counts

### Phase 3: API Integration (Day 2)
10. Implement `query_processor.py` ✓
11. Test API connection with small document
12. Implement retry logic
13. Test token counting

### Phase 4: Accuracy Checking (Day 2-3)
14. Implement `accuracy_checker.py` ✓
15. Test similarity calculation
16. Calibrate threshold

### Phase 5: Visualization (Day 3)
17. Implement `visualization.py` ✓
18. Test graph generation
19. Refine visual appearance

### Phase 6: Integration (Day 3-4)
20. Implement `main.py` ✓
21. End-to-end testing
22. Fix bugs and optimize

### Phase 7: Validation (Day 4)
23. Run full test suite
24. Validate results
25. Document findings

---

## 4. Testing Strategy

### 4.1 Unit Tests
- **document_generator:** Verify word counts, sentence placement
- **query_processor:** Mock API calls, test timing
- **accuracy_checker:** Test similarity with known examples
- **logger_setup:** Verify log rotation

### 4.2 Integration Tests
- End-to-end with 2 documents
- API connectivity
- Error handling

### 4.3 Validation Tests
- Manual inspection of generated documents
- Visual graph inspection
- Log file verification

---

## 5. Error Handling Strategy

### 5.1 API Errors
- Retry with exponential backoff
- Log all API errors
- Graceful degradation (skip document if fails after retries)

### 5.2 File Errors
- Create directories if not exist
- Validate file paths
- Handle permission errors

### 5.3 NLP Errors
- Fallback to simpler similarity method
- Log model loading errors
- Provide default similarity if error

---

## 6. Performance Optimization

### 6.1 Multiprocessing
- Document generation: 7 parallel processes
- API calls: Sequential (to avoid rate limits and costs)

### 6.2 Caching
- NLP model: Load once, reuse
- API client: Create once

### 6.3 Memory Management
- Stream large file reads if needed
- Clear intermediate variables

---

## 7. Security Considerations

1. **API Key:**
   - Never log or print
   - Read-only access from file
   - Validate before use

2. **File Permissions:**
   - Restrict log file access
   - Use secure file operations

3. **Input Validation:**
   - Validate file paths
   - Sanitize API responses

---

## 8. Monitoring and Logging

### Log Levels
- **INFO:** Normal operation, progress updates
- **WARNING:** Non-critical issues, retries
- **ERROR:** Failed operations, exceptions
- **CRITICAL:** System failures

### Key Events to Log
- Application start/stop
- API key loaded
- Document generation progress
- Each query execution
- Accuracy results
- Graph saved
- Errors and exceptions

---

## 9. Deployment Checklist

- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Directory structure created
- [ ] API key file placed
- [ ] Logging tested
- [ ] Document generation tested
- [ ] API connectivity tested
- [ ] Full end-to-end test completed
- [ ] Results validated
- [ ] Documentation complete

---

## 10. Future Enhancements

1. **Multi-model comparison** (Haiku vs Sonnet vs Opus)
2. **Different query types** (factual, reasoning, math)
3. **Statistical analysis** (p-values, confidence intervals)
4. **CSV export** for further analysis
5. **Command-line arguments** for customization
6. **Web dashboard** for real-time monitoring
7. **Automated testing suite**
8. **Performance profiling**
