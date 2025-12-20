# Claude.md - AI Assistant Guide
# Context Window Size Impact Testing Project

**Project Owner:** Yair Levi
**Last Updated:** 2025-12-14

---

## Project Overview

This project tests the hypothesis that Large Language Models (specifically Claude) experience degraded search accuracy as the context window size increases. The program generates documents of varying sizes (2K-50K words), queries them via the Anthropic API, and measures accuracy and performance.

---

## For AI Assistants Working on This Project

### Key Constraints

1. **File Size:** Each Python file must be 150-200 lines maximum
2. **Security:** NEVER expose the API key from `api_key.dat` in logs or print statements
3. **Paths:** Use ONLY relative paths, never absolute
4. **Environment:** WSL (Linux) compatible, virtual environment
5. **Model:** Use `claude-haiku-4-5-20250929` (Haiku 4.5) to minimize costs

### Critical Components

#### API Key Handling
```python
# CORRECT - Read from file, don't expose
with open("api_key.dat", "r") as f:
    api_key = f.read().strip()

# NEVER log or print the key
logger.info("API key loaded successfully")  # ✓ Good
logger.info(f"API key: {api_key}")          # ✗ BAD - NEVER DO THIS
```

#### Logging Configuration
- **Ring Buffer:** 20 files × 16MB each
- **Location:** `./log/` subfolder
- **Level:** INFO and above
- **Implementation:** Use `RotatingFileHandler` with:
  - `maxBytes=16*1024*1024` (16MB)
  - `backupCount=19` (plus main file = 20 total)

#### Document Structure
The target sentence must be inserted at the **exact middle** of each document:
```
"The first prime minister of Israel was Ben Gurion"
```

Query to ask: `"Who was the first Prime Minister of Israel?"`

Expected answer: `"Ben Gurion was the first Prime Minister of Israel"`

### Package Structure

```
context_window_test/
├── __init__.py              # Package initialization
├── main.py                  # Entry point, orchestrates workflow
├── document_generator.py    # Creates 7 test documents
├── query_processor.py       # Handles API calls and timing
├── accuracy_checker.py      # NLP similarity comparison
├── visualization.py         # Generates graphs
├── logger_setup.py          # Configures logging
└── config.py               # All configuration constants
```

### Implementation Guidelines

#### 1. Module Responsibilities

**main.py** (150-200 lines)
- Import all modules
- Initialize logging
- Create results list
- Call document generator
- Loop through documents and call query processor
- Call visualization
- Print summary

**document_generator.py** (150-200 lines)
- Function to generate text content (random or Lorem ipsum)
- Function to insert target sentence at middle
- Function to create all 7 documents
- Save to `./files/` subfolder

**query_processor.py** (150-200 lines)
- Load API key from file
- Initialize Anthropic client
- Function to load document content
- Function to query Claude with timing
- Function to count tokens
- Return results dict

**accuracy_checker.py** (150-200 lines)
- Load NLP model (sentence-transformers or spaCy)
- Function to calculate similarity score
- Function to determine accuracy (1 or 0)
- Return score and accuracy

**visualization.py** (150-200 lines)
- Function to create dual-axis plot (time + accuracy vs tokens)
- Function to save graph
- Optional: create similarity score plot

**logger_setup.py** (50-100 lines)
- Function to set up RotatingFileHandler
- Configure format and level
- Return logger instance

**config.py** (50-100 lines)
- All constants (API model name, file paths, thresholds, etc.)
- No logic, only configuration

#### 2. Multiprocessing Opportunities

**Document Generation:**
```python
from multiprocessing import Pool

def generate_single_document(word_count):
    # Generate one document
    pass

with Pool(processes=7) as pool:
    pool.map(generate_single_document, WORD_COUNTS)
```

**Note:** API queries should be sequential due to rate limits and to avoid parallel API costs.

#### 3. Error Handling

```python
import time
from anthropic import APIError

def query_with_retry(client, messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.messages.create(...)
            return response
        except APIError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                logger.warning(f"API error, retrying in {wait_time}s: {e}")
                time.sleep(wait_time)
            else:
                logger.error(f"API failed after {max_retries} attempts")
                raise
```

#### 4. Token Counting

Use Anthropic's built-in token counting:
```python
# Count tokens in a message
def count_tokens(client, text):
    return client.count_tokens(text)
```

Or use `tiktoken`:
```python
import tiktoken

def count_tokens(text, model="claude-3-haiku-20240307"):
    # Use appropriate encoding for Claude
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))
```

#### 5. Similarity Checking

**Option A: sentence-transformers (Recommended)**
```python
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_similarity(response, expected):
    emb1 = model.encode(response, convert_to_tensor=True)
    emb2 = model.encode(expected, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(emb1, emb2).item()
    return similarity
```

**Option B: spaCy**
```python
import spacy

nlp = spacy.load("en_core_web_md")

def calculate_similarity(response, expected):
    doc1 = nlp(response)
    doc2 = nlp(expected)
    return doc1.similarity(doc2)
```

---

## Development Workflow

### Phase 1: Setup
1. Create virtual environment
2. Install dependencies from `requirements.txt`
3. Create directory structure
4. Place API key in `api_key.dat`

### Phase 2: Core Development
1. Implement `config.py` with all constants
2. Implement `logger_setup.py` and test logging
3. Implement `document_generator.py` and generate test docs
4. Implement `query_processor.py` with API integration
5. Implement `accuracy_checker.py` with NLP comparison
6. Implement `visualization.py` for graphing

### Phase 3: Integration
1. Implement `main.py` to orchestrate everything
2. Create `__init__.py` to make it a package
3. Test end-to-end flow

### Phase 4: Testing & Validation
1. Verify document generation (word counts, sentence placement)
2. Test API connection with small document
3. Validate similarity calculation
4. Check log rotation
5. Run full test with all 7 documents
6. Verify graph output

---

## Testing Commands

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # WSL/Linux

# Install dependencies
pip install -r requirements.txt

# Run the program
python -m context_window_test

# Or
python context_window_test/main.py

# Check logs
ls -lh log/
tail -f log/app.log
```

---

## Expected Output

### Console Output
```
[INFO] Logging initialized - Ring buffer: 20 files × 16MB
[INFO] Loaded API key successfully
[INFO] Generating 7 documents...
[INFO] Generated doc_2000.txt (2000 words)
[INFO] Generated doc_5000.txt (5000 words)
...
[INFO] Processing doc_2000.txt...
[INFO] Query completed in 2.34s, Tokens: 2847, Accuracy: 1
[INFO] Processing doc_5000.txt...
...
[INFO] All queries completed!
[INFO] Graph saved to results_graph.png

Results Summary:
+---------------+--------------+------------+----------+
| Document      | Tokens       | Time (s)   | Accuracy |
+---------------+--------------+------------+----------+
| doc_2000.txt  | 2,847       | 2.34       | 1        |
| doc_5000.txt  | 7,123       | 3.56       | 1        |
| doc_10000.txt | 14,289      | 5.21       | 1        |
| doc_20000.txt | 28,456      | 8.92       | 1        |
| doc_30000.txt | 42,834      | 12.45      | 0        |
| doc_40000.txt | 57,123      | 15.67      | 0        |
| doc_50000.txt | 71,456      | 19.23      | 0        |
+---------------+--------------+------------+----------+
```

### Files Created
- `./files/doc_*.txt` (7 files)
- `./log/app.log` (and up to 19 backup files)
- `./results_graph.png`

---

## Common Issues & Solutions

### Issue 1: API Key Not Found
**Error:** `FileNotFoundError: api_key.dat`
**Solution:** Ensure `api_key.dat` exists in the project root with valid API key

### Issue 2: Import Errors
**Error:** `ModuleNotFoundError: No module named 'context_window_test'`
**Solution:** Run as package: `python -m context_window_test` or ensure `__init__.py` exists

### Issue 3: Log Directory Not Found
**Error:** `FileNotFoundError: ./log/`
**Solution:** Create directory in code:
```python
import os
os.makedirs(config.LOG_DIR, exist_ok=True)
```

### Issue 4: Rate Limiting
**Error:** `anthropic.RateLimitError`
**Solution:** Add delays between API calls:
```python
time.sleep(2)  # Wait 2 seconds between documents
```

### Issue 5: Token Count Exceeds Model Limit
**Warning:** Large documents may exceed context limits
**Solution:** Monitor token counts, consider using Claude Sonnet if needed (larger context)

---

## Cost Estimation

**Model:** Claude Haiku 4.5
**Pricing (approximate):**
- Input: $0.80 per million tokens
- Output: $4.00 per million tokens

**Expected Usage:**
- 7 documents ranging from ~3K to ~70K tokens
- Total input tokens: ~200K
- Total output tokens: ~300 (short answers)

**Estimated Cost:** $0.17 per run (very affordable)

---

## Dependencies Rationale

| Package | Purpose | Alternative |
|---------|---------|-------------|
| anthropic | API client | None (official) |
| sentence-transformers | NLP similarity | spaCy, sklearn |
| matplotlib | Visualization | plotly, seaborn |
| tiktoken | Token counting | anthropic built-in |
| numpy | Data manipulation | None |
| python-dotenv | (Optional) Env vars | Manual file read |

---

## Security Checklist

- [ ] API key read from file, never hardcoded
- [ ] API key never logged or printed
- [ ] API key file in `.gitignore`
- [ ] No API key in error messages
- [ ] Validate API key format before use
- [ ] Use environment variables as alternative (optional)

---

## Performance Optimization Tips

1. **Multiprocessing:** Use for document generation (I/O bound)
2. **Async:** Consider for API calls if running multiple iterations
3. **Caching:** Cache NLP models (load once)
4. **Memory:** Stream large file reads if memory is constrained
5. **Token Counting:** Use efficient tokenizer (tiktoken is fast)

---

## Research Hypothesis

**Hypothesis:** Claude's ability to retrieve specific facts decreases as context window size increases.

**Expected Results:**
- Small documents (2K-10K words): High accuracy (95-100%)
- Medium documents (20K words): Good accuracy (80-95%)
- Large documents (30K-50K words): Decreased accuracy (50-80%)

**Graph Pattern:**
- Execution time: Linear or slightly exponential increase
- Accuracy: May drop sharply at a threshold size (e.g., 25K words)

**Conclusion:** If accuracy drops, it validates the "lost in the middle" phenomenon documented in LLM research.

---

## Additional Notes for Implementation

- Use `pathlib` for path operations (more robust than `os.path`)
- Add progress bars for user feedback (optional: `tqdm`)
- Consider saving raw results to JSON for later analysis
- Document all functions with docstrings
- Use type hints for better code clarity
- Follow PEP 8 style guidelines

---

## References

- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python)
- [Sentence Transformers](https://www.sbert.net/)
- [Python Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)
- [Multiprocessing Best Practices](https://docs.python.org/3/library/multiprocessing.html#programming-guidelines)
