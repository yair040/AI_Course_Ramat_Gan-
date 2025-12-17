# Claude Implementation Guide
# Lost in the Middle - Context Window Testing

**Target Model:** Claude Code
**Author:** Yair Levi
**Purpose:** Implementation instructions for Claude AI assistant

---

## Overview

This document provides specific instructions for Claude AI to implement the "Lost in the Middle" hypothesis testing framework. Read the PRD.md for complete requirements and planning.md for the implementation strategy.

---

## Pre-Implementation Checklist

Before starting implementation, ensure:
- [ ] PRD.md has been read and understood
- [ ] planning.md has been reviewed
- [ ] tasks.md task breakdown is clear
- [ ] Working directory confirmed: `exercise1_lost_in_the_middle/`
- [ ] Python virtual environment will be used
- [ ] WSL environment is available

---

## Implementation Priorities

### Phase 1: Foundation (High Priority)
1. Create package structure with `__init__.py`
2. Set up logging infrastructure with ring buffer
3. Create configuration management (config.py)
4. Implement credential loading securely
5. Create utility functions

### Phase 2: Core Functionality (High Priority)
6. Document generation module
7. Sentence injection module
8. Anthropic API integration
9. NLP similarity comparison

### Phase 3: Testing & Analysis (Medium Priority)
10. Main program flow with iteration logic
11. Statistical analysis module
12. Result visualization

### Phase 4: Polish (Lower Priority)
13. Error handling and edge cases
14. Performance optimization
15. Documentation and comments

---

## Critical Implementation Rules

### Code Structure
- **MAXIMUM 150-200 lines per file** - strictly enforce
- If a module exceeds limit, split into logical submodules
- Use clear function names and docstrings
- Keep functions focused and single-purpose

### Path Management
- **ONLY use relative paths** - never absolute paths
- Use `pathlib.Path` for cross-platform compatibility
- All paths relative to project root
- Example:
  ```python
  from pathlib import Path

  BASE_DIR = Path(__file__).parent
  FILES_DIR = BASE_DIR / "files"
  LOG_DIR = BASE_DIR / "log"
  ```

### Logging Configuration
This is **CRITICAL** - implement exactly as specified:

```python
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Configuration
LOG_DIR = Path(__file__).parent / "log"
LOG_DIR.mkdir(exist_ok=True)

# Ring buffer: 20 files × 16MB = 320MB total
MAX_BYTES = 16 * 1024 * 1024  # 16MB
BACKUP_COUNT = 19  # 20 files total (1 current + 19 backups)

# Setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(
    LOG_DIR / "app.log",
    maxBytes=MAX_BYTES,
    backupCount=BACKUP_COUNT
)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
```

### API Security
**CRITICAL:** Never expose API keys

```python
from pathlib import Path

def load_credentials():
    """Load API credentials securely."""
    api_key_file = Path(__file__).parent / "api_key.dat"

    if not api_key_file.exists():
        raise FileNotFoundError("api_key.dat not found")

    with open(api_key_file, 'r', encoding='utf-8') as f:
        api_key = f.read().strip()

    # Never log the actual key
    logger.info("API key loaded successfully")
    return api_key
```

**Do NOT:**
- Print API keys
- Log API keys
- Include keys in error messages
- Store keys in code

### Anthropic API Usage
Use Claude Haiku 4.5 for cost efficiency:

```python
import anthropic

client = anthropic.Anthropic(api_key=api_key)

def query_document(document_text: str, question: str) -> str:
    """Query document using Anthropic API with fresh context."""

    logger.info(f"Querying document (length: {len(document_text)} chars)")

    message = client.messages.create(
        model="claude-haiku-4-5-20250929",  # Haiku 4.5
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Here is a document:

{document_text}

Question: {question}

Please provide a direct answer."""
            }
        ]
    )

    response = message.content[0].text
    logger.info(f"Received response: {response[:100]}...")

    return response
```

### Document Generation
Create coherent text documents:

```python
def generate_document(word_count: int = 75000) -> str:
    """Generate a coherent text document.

    Args:
        word_count: Target number of words (default: 75,000)

    Returns:
        Generated text as string
    """
    # Strategy: Use lorem ipsum or generate paragraphs
    # Ensure natural sentence structure
    # Each paragraph should be 100-200 words
    # Mix sentence lengths for natural flow

    pass  # Implementation here
```

### Sentence Injection
Precise position control:

```python
def inject_sentence(
    document: str,
    sentence: str,
    position: str
) -> str:
    """Inject sentence at specified position.

    Args:
        document: Original document text
        sentence: Sentence to inject
        position: 'start', 'middle', or 'end'

    Returns:
        Modified document
    """
    sentences = document.split('. ')

    if position == 'start':
        # Insert between sentences 1-5
        insert_idx = random.randint(1, 5)
    elif position == 'end':
        # Insert between last 5 sentences
        insert_idx = len(sentences) - random.randint(1, 5)
    elif position == 'middle':
        # Insert at midpoint
        insert_idx = len(sentences) // 2
    else:
        raise ValueError(f"Invalid position: {position}")

    sentences.insert(insert_idx, sentence)
    return '. '.join(sentences)
```

### NLP Similarity Comparison
Use semantic similarity:

```python
from difflib import SequenceMatcher

def check_answer_similarity(response: str, target: str) -> bool:
    """Check if response matches target using similarity.

    Args:
        response: API response text
        target: Expected answer

    Returns:
        True if similar enough, False otherwise
    """
    # Method 1: Simple string matching
    response_lower = response.lower()

    # Check for key facts: "7 days" in response
    if "7" in response and "day" in response_lower:
        logger.info("Answer contains correct information")
        return True

    # Method 2: Sequence similarity
    similarity = SequenceMatcher(None, response_lower, target.lower()).ratio()
    threshold = 0.6

    logger.info(f"Similarity score: {similarity:.2f}")
    return similarity >= threshold
```

### Main Program Structure

```python
def main():
    """Main program execution."""

    logger.info("=" * 60)
    logger.info("Starting Lost in the Middle experiment")
    logger.info("=" * 60)

    # Global counters
    counters = {
        'start': 0,
        'middle': 0,
        'end': 0
    }

    total_iterations = 5

    # Step 1: Generate documents
    logger.info("Step 1: Generating documents")
    generate_base_documents(count=6)

    # Step 2: Inject sentences
    logger.info("Step 2: Injecting test sentences")
    inject_test_sentences()

    # Step 3-6: Testing loop
    for iteration in range(1, total_iterations + 1):
        logger.info(f"Starting iteration {iteration}/{total_iterations}")

        for doc_file in get_test_documents():
            result = test_document(doc_file)
            if result:
                position_type = get_position_type(doc_file)
                counters[position_type] += 1

        logger.info(f"Iteration {iteration} complete. Counters: {counters}")

    # Step 7: Visualization
    logger.info("Step 7: Generating results visualization")
    visualize_results(counters, total_iterations)

    logger.info("Experiment complete!")
    logger.info(f"Final results: {counters}")
```

---

## Multiprocessing Strategy

Since we have 6 documents and independent tests, parallelize where possible:

```python
from multiprocessing import Pool, Manager

def test_all_documents_parallel(iteration: int, counters: dict):
    """Test all documents in parallel."""

    doc_files = get_test_documents()

    # Use multiprocessing pool
    with Pool(processes=min(6, os.cpu_count())) as pool:
        results = pool.map(test_document, doc_files)

    # Update counters
    for doc_file, result in zip(doc_files, results):
        if result:
            position_type = get_position_type(doc_file)
            counters[position_type] += 1
```

**Note:** Be cautious with API rate limits when using multiprocessing.

---

## Visualization Requirements

Create clear, professional visualization:

```python
import matplotlib.pyplot as plt

def visualize_results(counters: dict, iterations: int):
    """Create bar chart of results."""

    positions = ['Start', 'Middle', 'End']
    successes = [counters['start'], counters['middle'], counters['end']]

    # Each position tested: 2 documents × 5 iterations = 10 times
    total_tests_per_position = 2 * iterations
    success_rates = [s / total_tests_per_position * 100 for s in successes]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(positions, success_rates, color=['#2ecc71', '#e74c3c', '#3498db'])

    plt.ylabel('Success Rate (%)')
    plt.xlabel('Sentence Position')
    plt.title('Lost in the Middle: Information Retrieval Accuracy by Position')
    plt.ylim(0, 100)

    # Add value labels on bars
    for bar, rate in zip(bars, success_rates):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{rate:.1f}%',
                ha='center', va='bottom')

    # Save
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)

    plt.savefig(results_dir / "results_graph.png", dpi=300, bbox_inches='tight')
    plt.show()

    logger.info(f"Visualization saved to {results_dir / 'results_graph.png'}")
```

---

## Testing & Validation

Before final run:
1. Test with small documents (1000 words) first
2. Test with 1 iteration before full 5
3. Verify logging works correctly
4. Check file structure is created properly
5. Validate API integration with one test call
6. Confirm similarity matching works

---

## Error Handling

Be defensive and log everything:

```python
try:
    result = api_call(document)
except anthropic.APIError as e:
    logger.error(f"API error: {e}")
    return None
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    return None
```

---

## Performance Considerations

1. **Token Optimization:**
   - Don't send unnecessary whitespace
   - Use efficient prompt structure
   - Monitor token usage per call

2. **File I/O:**
   - Use context managers (`with` statements)
   - Don't keep files open unnecessarily
   - Buffer large file operations

3. **Memory:**
   - Don't load all documents simultaneously
   - Process one at a time if memory constrained
   - Clean up large variables when done

---

## Deliverables Checklist

When implementation is complete, verify:
- [ ] All Python files are 150-200 lines maximum
- [ ] Package has proper `__init__.py`
- [ ] Logging creates ring buffer in `./log/`
- [ ] 6 documents generated in `./files/` (~75k words each)
- [ ] Sentences injected correctly (2 start, 2 middle, 2 end)
- [ ] API integration works with Claude Haiku 4.5
- [ ] No API keys exposed anywhere
- [ ] 5 iterations complete (30 total tests)
- [ ] Counters track correctly
- [ ] Visualization saved to `./results/`
- [ ] All relative paths work correctly
- [ ] requirements.txt lists all dependencies
- [ ] Code is clean and documented

---

## Troubleshooting Guide

### Issue: Import errors
- Ensure `__init__.py` exists
- Verify virtual environment is activated
- Check all dependencies in requirements.txt

### Issue: API authentication fails
- Verify api_key.dat exists and is valid
- Check API key format
- Ensure no whitespace in key

### Issue: Logging not working
- Verify `./log/` directory exists
- Check file permissions
- Confirm RotatingFileHandler setup

### Issue: Documents too small/large
- Adjust word count in generation
- Verify counting logic
- Check for sentence boundary issues

---

## Next Steps After Implementation

1. Run initial test with small documents
2. Verify logging and file structure
3. Run full experiment (5 iterations)
4. Analyze results
5. Document findings
6. Consider additional experiments

---

**Remember:** Follow the planning.md and tasks.md for step-by-step implementation order. Start with infrastructure, then core functionality, then testing and analysis.
