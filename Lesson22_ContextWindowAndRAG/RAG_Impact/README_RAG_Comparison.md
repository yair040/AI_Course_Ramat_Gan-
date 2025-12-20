# Context Window vs RAG Performance Comparison

**Author:** Yair Levi
**Version:** 1.0
**Date:** 2025-12-15
**Platform:** WSL (Linux)

---

## Overview

This project empirically compares two document retrieval methods for querying information from 20 PDF documents:

1. **Context Window Method**: Loading all documents into Claude's context window
2. **RAG Method**: Using Retrieval Augmented Generation to load only the top 3 most relevant chunks

The program measures response time, token usage, cost, and answer quality across 5 iterations per method (10 total queries).

### Research Question

**"Is RAG faster and more cost-effective than full context loading for multi-document queries?"**

---

## Expected Results

Based on the hypothesis:
- **Response Time**: RAG should be 5-10× faster
- **Token Usage**: RAG should use ~98% fewer input tokens
- **Cost**: RAG should be ~98% cheaper
- **Answer Quality**: Both methods should produce similar, correct answers

---

## Project Structure

```
context_window_vs_rag/
├── __init__.py                  # Package initialization
├── main.py                      # Entry point and orchestration
├── config.py                    # Configuration constants
├── logger_setup.py              # Ring buffer logging (20 files × 16MB)
├── pdf_loader.py                # PDF reading with multiprocessing
├── context_window_method.py     # Full context implementation
├── rag_method.py                # RAG pipeline (chunk + embed + retrieve)
├── query_processor.py           # API calls with timing and retry logic
├── results_analyzer.py          # Statistical analysis and comparison
└── visualization.py             # Generate comparison graphs

Project Root:
├── docs/                        # 20 PDF documents
├── log/                         # Ring buffer logs (auto-created)
├── results/                     # Results JSON (auto-created)
├── api_key.dat                  # Anthropic API key (NEVER commit!)
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore file
├── PRD.md                       # Product Requirements Document
├── CLAUDE.md                    # AI Assistant Guide
├── planning.md                  # Development Plan
├── tasks.md                     # Detailed Task Breakdown
└── README.md                    # This file
```

---

## Prerequisites

### System Requirements

- **OS**: WSL (Windows Subsystem for Linux) or Linux
- **Python**: 3.8 or higher
- **RAM**: 4 GB minimum, 8 GB recommended
- **Disk**: 10 GB free space
- **CPU**: Multi-core recommended for multiprocessing

### Required Files

1. **API Key**: `api_key.dat` containing valid Anthropic API key
2. **PDF Documents**: 20 PDF files in `./docs/` directory

---

## Installation

### 1. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate (WSL/Linux)
source venv/bin/activate
```

### 2. Install System Dependencies (WSL/Ubuntu)

```bash
sudo apt-get update
sudo apt-get install python3-dev build-essential libpoppler-cpp-dev
```

### 3. Install Python Packages

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

**Note**: Installation may take 10-15 minutes due to PyTorch size (~2-3 GB download).

### 4. Verify Installation

```bash
python -c "import anthropic; import pdfplumber; import chromadb; print('✓ All imports successful')"
```

### 5. Setup API Key

Create `api_key.dat` in project root:

```bash
echo "sk-ant-your-api-key-here" > api_key.dat
```

**Security Warning**: Never commit `api_key.dat` to git! It should be in `.gitignore`.

### 6. Verify PDFs

```bash
ls -l docs/*.pdf | wc -l
# Should output: 20
```

---

## Usage

### Basic Usage

```bash
# Run the full comparison
python -m context_window_vs_rag
```

### What It Does

1. **Setup Phase**:
   - Initializes logging (ring buffer: 20 files × 16MB)
   - Loads API key from `api_key.dat`
   - Loads 20 PDF documents using multiprocessing

2. **Context Window Method** (5 iterations):
   - Concatenates all 20 PDFs into single context
   - Queries Claude: "What are the side effects of taking calcium carbonate?"
   - Measures response time, token usage, cost
   - Repeats 5 times with 2-second delays

3. **RAG Method** (5 iterations):
   - Chunks all documents (500 words per chunk, 50-word overlap)
   - Generates embeddings using sentence-transformers
   - Builds vector database (ChromaDB)
   - For each query:
     - Retrieves top 3 most relevant chunks
     - Queries Claude with only these chunks
     - Measures response time, token usage, cost

4. **Analysis**:
   - Calculates statistics (mean, std, min, max)
   - Compares both methods
   - Calculates savings percentages
   - Computes answer similarity

5. **Visualization**:
   - Generates 4 comparison graphs (PNG files)

6. **Output**:
   - Prints summary report to console
   - Saves raw results to `results.json`
   - Saves graphs: `response_time_comparison.png`, `token_usage_comparison.png`, etc.

---

## Expected Output

### Console Output

```
INFO: Starting Context Window vs RAG comparison...
INFO: API key loaded successfully
INFO: Loading PDFs from ./docs/...
INFO: Loaded 20 documents (total: 234,567 words)

==================================================
CONTEXT WINDOW METHOD (5 iterations)
==================================================
INFO: Iteration 1/5: Query time 12.34s, Tokens: 145632/87
INFO: Iteration 2/5: Query time 11.89s, Tokens: 145632/92
INFO: Iteration 3/5: Query time 13.01s, Tokens: 145632/85
INFO: Iteration 4/5: Query time 12.67s, Tokens: 145632/88
INFO: Iteration 5/5: Query time 12.45s, Tokens: 145632/90

==================================================
RAG METHOD (5 iterations)
==================================================
INFO: Building vector database...
INFO: Generated 1,234 chunks from 20 documents
INFO: Vector database built successfully
INFO: Iteration 1/5: Query time 2.15s, Tokens: 1842/91
INFO: Iteration 2/5: Query time 2.08s, Tokens: 1856/89
INFO: Iteration 3/5: Query time 2.23s, Tokens: 1831/93
INFO: Iteration 4/5: Query time 2.11s, Tokens: 1849/90
INFO: Iteration 5/5: Query time 2.18s, Tokens: 1838/92

==================================================
RESULTS SUMMARY
==================================================

Context Window Method:
  Response Time: 12.47 ± 0.42s (range: 11.89 - 13.01s)
  Input Tokens:  145,632 ± 0
  Output Tokens: 88 ± 3
  Cost per Query: $0.117
  Total Cost (5 queries): $0.585

RAG Method:
  Response Time: 2.15 ± 0.06s (range: 2.08 - 2.23s)
  Input Tokens:  1,843 ± 10
  Output Tokens: 91 ± 2
  Cost per Query: $0.0015
  Total Cost (5 queries): $0.0075

Comparison:
  Time Savings: 82.8% (RAG is 5.8× faster)
  Token Savings: 98.7% (RAG uses 98.7% fewer input tokens)
  Cost Savings: 98.7% (RAG is 78× cheaper)
  Answer Similarity: 0.93 (highly consistent answers)

INFO: Graphs saved successfully
INFO: Results saved to results.json
```

### Generated Files

1. **Graphs** (PNG, 300 DPI):
   - `response_time_comparison.png` - Bar chart comparing response times
   - `token_usage_comparison.png` - Grouped bar chart (input/output tokens)
   - `cost_comparison.png` - Bar chart comparing costs
   - `iterations_timeline.png` - Line plot showing time across iterations

2. **Results** (JSON):
   - `results.json` - Raw data from all 10 queries

3. **Logs** (Ring buffer):
   - `log/app.log` - Current log file
   - `log/app.log.1` through `log/app.log.19` - Backup log files

---

## Configuration

All settings can be modified in `context_window_vs_rag/config.py`:

### Key Settings

```python
# API Settings
MODEL_NAME = "claude-haiku-4-5-20250929"  # Haiku 4.5 for cost savings
MAX_TOKENS = 1024
MAX_RETRIES = 3

# RAG Settings
CHUNK_SIZE = 500          # Words per chunk
CHUNK_OVERLAP = 50        # Word overlap between chunks
TOP_K_CHUNKS = 3          # Number of chunks to retrieve
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Fast and efficient

# Test Settings
ITERATIONS = 5            # Queries per method
QUERY = "What are the side effects of taking calcium carbonate?"

# Logging
LOG_MAX_BYTES = 16 * 1024 * 1024  # 16MB per file
LOG_BACKUP_COUNT = 19              # 20 total files
```

### Tuning RAG Performance

To optimize RAG performance, experiment with:
- `CHUNK_SIZE`: Try 300, 500, or 700 words
- `CHUNK_OVERLAP`: Try 25, 50, or 100 words
- `TOP_K_CHUNKS`: Try 2, 3, or 5 chunks
- `EMBEDDING_MODEL`: Try different models (e.g., "all-mpnet-base-v2" for better quality)

---

## Cost Estimation

### Pricing (Claude Haiku 4.5)

- **Input**: $0.80 per million tokens
- **Output**: $4.00 per million tokens

### Expected Costs

| Method | Input Tokens | Output Tokens | Cost per Query | Total (5 queries) |
|--------|--------------|---------------|----------------|-------------------|
| Context Window | ~150,000 | ~90 | $0.12 | $0.60 |
| RAG | ~2,000 | ~90 | $0.002 | $0.01 |
| **Total** | - | - | - | **~$0.61** |

**Very affordable for testing!**

---

## Troubleshooting

### Issue 1: API Key Not Found

**Error**: `FileNotFoundError: api_key.dat`

**Solution**:
```bash
echo "sk-ant-your-actual-key" > api_key.dat
```

### Issue 2: PDF Files Not Found

**Error**: `No PDF files found in ./docs/`

**Solution**:
```bash
# Verify PDFs exist
ls -l docs/*.pdf

# Create docs directory if needed
mkdir -p docs
```

### Issue 3: Import Error (anthropic)

**Error**: `ModuleNotFoundError: No module named 'anthropic'`

**Solution**:
```bash
# Verify virtual environment is activated
which python  # Should show venv path

# Reinstall requirements
pip install -r requirements.txt
```

### Issue 4: ChromaDB Installation Failed

**Error**: ChromaDB installation fails

**Solution**:
```bash
# Try installing without cache
pip install chromadb --no-cache-dir

# Or use alternative vector database (FAISS)
pip install faiss-cpu
# Then modify rag_method.py to use FAISS instead
```

### Issue 5: PyTorch Installation Failed

**Error**: Torch installation fails or is very slow

**Solution**:
```bash
# Install CPU-only version (faster, smaller)
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Issue 6: PDFs Not Readable

**Error**: `Failed to load PDF: ...`

**Solution**:
- Verify PDFs are not corrupted: Open manually
- Check PDF format: Should be readable PDFs (not scanned images)
- Install system dependencies: `sudo apt-get install libpoppler-cpp-dev`

### Issue 7: API Rate Limiting

**Error**: `anthropic.RateLimitError: 429`

**Solution**:
- Program already has 2-second delays between requests
- If still rate-limited, increase `RETRY_DELAY` in config.py
- Check your Anthropic account rate limits

### Issue 8: Context Exceeds Token Limit

**Error**: `Token count exceeds model limit`

**Solution**:
- 20 PDFs may exceed Haiku's 200K token context limit
- Options:
  1. Use Claude Sonnet (400K tokens): Change `MODEL_NAME` in config.py
  2. Reduce number of PDFs
  3. Truncate documents

---

## Testing

### Quick Test (2 PDFs, 2 iterations)

To test quickly with reduced scale:

1. Edit `config.py`:
```python
ITERATIONS = 2  # Instead of 5
```

2. Temporarily move 18 PDFs out of `./docs/`:
```bash
mkdir temp_pdfs
mv docs/doc_{3..20}.pdf temp_pdfs/  # Keep only 2 PDFs
```

3. Run test:
```bash
python -m context_window_vs_rag
```

4. Restore PDFs:
```bash
mv temp_pdfs/* docs/
rmdir temp_pdfs
```

### Verify Results

1. **Check Answers**: Read `results.json` and verify answers are relevant
2. **Check Graphs**: Open PNG files and verify data accuracy
3. **Check Logs**: Inspect `log/app.log` for any warnings or errors
4. **Verify Calculations**: Manually verify token counts and costs

---

## API Key Security

### Critical Security Rules

1. ✅ **DO**: Store key in `api_key.dat` (not committed to git)
2. ✅ **DO**: Validate key format before use
3. ✅ **DO**: Log "API key loaded successfully" (not the key itself)
4. ❌ **DON'T**: Print or log the actual API key
5. ❌ **DON'T**: Include key in error messages
6. ❌ **DON'T**: Commit `api_key.dat` to version control

### Verify Security

```bash
# Check .gitignore includes api_key.dat
grep "api_key.dat" .gitignore

# Check logs don't contain key
grep -i "sk-ant-" log/app.log  # Should return nothing
```

---

## Development

### Adding New Visualizations

1. Add function to `visualization.py`:
```python
def plot_new_metric(cw_stats, rag_stats):
    # Your plotting code
    plt.savefig("new_metric.png", dpi=300)
```

2. Call from `generate_all_graphs()`:
```python
def generate_all_graphs(cw_results, rag_results):
    # ... existing plots ...
    plot_new_metric(cw_stats, rag_stats)
```

### Adding New Queries

Modify `config.py`:
```python
QUERIES = [
    "What are the side effects of taking calcium carbonate?",
    "What is the recommended dosage?",
    "What are the drug interactions?"
]
```

Then update `main.py` to iterate through queries.

### Using Different Embedding Models

Modify `config.py`:
```python
# Faster but lower quality
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Slower but higher quality
EMBEDDING_MODEL = "all-mpnet-base-v2"

# Best quality (largest)
EMBEDDING_MODEL = "multi-qa-mpnet-base-cos-v1"
```

---

## Contributing

This is a research project. If you'd like to extend it:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## License

MIT License - See LICENSE file for details

---

## References

- [Anthropic API Documentation](https://docs.anthropic.com/)
- [Claude Models](https://www.anthropic.com/claude)
- [Sentence Transformers](https://www.sbert.net/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [PDFPlumber](https://github.com/jsvine/pdfplumber)
- [RAG Overview](https://python.langchain.com/docs/use_cases/question_answering/)

---

## FAQ

### Q: Can I use a different Claude model?

**A**: Yes, change `MODEL_NAME` in `config.py`. Options:
- `claude-haiku-4-5-20250929` (fastest, cheapest)
- `claude-sonnet-4-5-20250929` (balanced)
- `claude-opus-4-5-20251101` (highest quality)

### Q: How long does it take to run?

**A**: Approximately:
- Setup (PDF loading, embeddings): 1-2 minutes
- Context Window queries (5×): 1-2 minutes
- RAG queries (5×): 30-60 seconds
- Analysis and visualization: 10-20 seconds
- **Total**: ~5 minutes

### Q: Can I use a different vector database?

**A**: Yes, ChromaDB can be replaced with:
- FAISS (Facebook AI Similarity Search)
- Pinecone (cloud-based)
- Weaviate (open source)
- Qdrant (high-performance)

Modify `rag_method.py` accordingly.

### Q: What if my PDFs are very large?

**A**: If total tokens exceed model limits:
1. Use Claude Sonnet (400K context) or Opus (200K)
2. Reduce number of PDFs
3. Truncate document content
4. Increase chunking (smaller chunks)

### Q: How accurate is RAG?

**A**: RAG accuracy depends on:
- Chunk size (affects context captured)
- Top K (number of chunks retrieved)
- Embedding model quality
- Query relevance to documents

Typical accuracy: 85-95% compared to full context

---

## Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review the logs in `./log/app.log`
3. Consult the [PRD.md](PRD.md) and [CLAUDE.md](CLAUDE.md) documents

---

**Project Status**: ✅ Ready for Use
**Last Updated**: 2025-12-15
**Author**: Yair Levi
