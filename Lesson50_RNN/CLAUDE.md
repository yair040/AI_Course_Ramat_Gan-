# CLAUDE.md — Project Intelligence for RNN Word Prediction

**Author:** Yair Levi
**Project:** RNN Word Prediction Package
**Location:** `C:\Users\yair0\AI_continue\Lesson50_RNN\RNN\` (WSL path)

---

## Architecture Overview

Python package (`rnn_predictor/`) with `main.py` entry point dispatching to task modules.
Each module ≤ 150 lines. Virtual environment at `../../venv` relative to project root.

```
RNN/
├── main.py                   # CLI entry point, task dispatch, elapsed time
├── requirements.txt
├── README.md
├── CLAUDE.md
├── planning.md
├── tasks.md
├── log/                      # Ring-buffer logs (20 × 16 MB)
├── data/                     # Persisted datasets and model checkpoint
└── rnn_predictor/
    ├── __init__.py            # Package init, NLTK auto-download
    ├── config.py              # All defaults and user-tunable parameters
    ├── logger_setup.py        # Ring-buffer RotatingFileHandler
    ├── vocab.py               # Task 1a: imports ALL_WORDS from sentence_builder
    ├── tokenizer.py           # Task 1b: Word2Vec training + index maps
    ├── sentence_builder.py    # Task 1c: biased template generation (multiprocessing)
    ├── data_splitter.py       # Task 2: encode + shuffle + 80/20 split
    ├── rnn_model.py           # Task 3: LSTM model definition
    ├── trainer.py             # Task 4: training loop + early stopping
    └── evaluator.py           # Task 5: metrics + samples + confusion matrix
```

---

## Critical Design Decisions

### Vocabulary = sentence_builder.ALL_WORDS (single source of truth)
`vocab.py` does NOT sample from any external corpus. It imports `ALL_WORDS` directly
from `sentence_builder.py`. This guarantees every word in every generated sentence
is always in the vocabulary. Breaking this coupling will cause unknown-word filtering
to remove most training data.

### Biased Templates (the key to learning signal)
Sentences are generated from grammatical templates with a BIAS_TABLE (70% strength).
Without the bias, input words give zero information about the target word and the
model collapses. The bias creates genuine co-occurrence patterns the model can learn.
Categories have exactly 10 words each — large enough for variety, small enough that
each word appears thousands of times as a training target.

### Early Stopping + ReduceLROnPlateau
Without early stopping, val loss rises from epoch 1 (the model memorises training).
`patience=5` halts training when val loss stops improving. `ReduceLROnPlateau` halves
the LR when val loss stalls for 2 consecutive epochs.

### Multiprocessing with `spawn`
WSL requires `spawn` start method for multiprocessing. Worker functions (`_generate_chunk`,
`_pick`) must be top-level module functions (not lambdas or nested) to be picklable.

### Logging
Ring buffer: `RotatingFileHandler(maxBytes=16*1024*1024, backupCount=19)` — 20 files total.
Files in `log/` subdirectory. Both file and console handlers at INFO level.
`verbose` parameter removed from `ReduceLROnPlateau` (deprecated in PyTorch 2.4+).

### torch.tensor(tensor) warning
Avoided by `_to_long()` helper in `trainer.py`:
```python
def _to_long(y_batch, device):
    if isinstance(y_batch, torch.Tensor):
        return y_batch.clone().detach().to(dtype=torch.long, device=device)
    return torch.tensor(y_batch, dtype=torch.long, device=device)
```
`evaluator.py` imports and reuses this same helper.

---

## Parameter Defaults (current, all overridable via CLI)

| Parameter | Default | CLI flag | Notes |
|-----------|---------|----------|-------|
| Vocabulary size | ~48 (cap=1000) | `--vocab-size` | Cap only; actual = ALL_WORDS |
| Number of sentences | 100,000 | `--num-sentences` | |
| Max words per sentence | 5 | `--max-sent-len` | |
| Train/test split | 80/20 | `--train-ratio` | |
| Embedding dim | 64 | `--embed-dim` | |
| LSTM hidden size | 128 | `--hidden-size` | |
| LSTM layers | 1 | `--num-layers` | 1 layer generalises better on synthetic data |
| Dropout | 0.4 | `--dropout` | |
| Learning rate | 0.0005 | `--lr` | |
| Max epochs | 30 | `--epochs` | Early stopping usually halts sooner |
| Batch size | 128 | `--batch-size` | |
| Early stopping patience | 5 | `--patience` | |
| Weight decay (L2) | 1e-4 | `--weight-decay` | |
| Random seed | 42 | `--seed` | |

---

## Benchmark Results (2026-04-16, default params, CPU only)

| Metric | Value |
|--------|-------|
| Top-1 accuracy | 56.65% |
| Top-5 accuracy | 72.21% |
| Perplexity | 5.72 |
| Precision (macro) | 0.267 |
| Recall (macro) | 0.332 |
| F1 (macro) | 0.290 |
| Total pipeline time | 301 seconds |

---

## Coding Rules

1. Every file ≤ 150 lines (imports + docstring count).
2. No absolute paths — use `pathlib` relative to `__file__` or project root.
3. All public functions have docstrings.
4. Log at `INFO` minimum; `DEBUG` for loop internals.
5. Wrap each task in `time.perf_counter()` and log elapsed time.
6. `if __name__ == "__main__":` guard in `main.py`.
7. Multiprocessing workers must be top-level functions (picklable).
8. Use `_to_long()` helper instead of `torch.tensor()` on existing tensors.
9. Never use `verbose=` in `ReduceLROnPlateau` (removed in PyTorch 2.4).

---

## Known Issues & Open Work

| Issue | File | Priority |
|-------|------|----------|
| Objects never predicted | sentence_builder.py, BIAS_TABLE | High |
| `soon`, `that` never predicted | BIAS_TABLE | Medium |
| `fast` over-predicted as fallback | BIAS_TABLE | Medium |
| Multi-label evaluation unfairness | evaluator.py | Low |
