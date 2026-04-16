# tasks.md — Development Task Checklist

**Author:** Yair Levi

---

## Setup Tasks

- [x] **T-00** Create `../../venv` virtual environment
  `python3 -m venv ../../venv`
- [x] **T-01** Activate venv and install requirements
  `source ../../venv/bin/activate && pip install -r requirements.txt`
- [x] **T-02** Verify package imports (`python -c "import rnn_predictor"`)
- [x] **T-03** `log/` and `data/` directories auto-created at runtime

---

## Implementation Tasks

### Package Infrastructure
- [x] **T-10** `rnn_predictor/__init__.py` — NLTK auto-download, version string
- [x] **T-11** `rnn_predictor/config.py` — dataclass with all defaults (updated: smaller vocab, early stopping, weight decay)
- [x] **T-12** `rnn_predictor/logger_setup.py` — ring-buffer `RotatingFileHandler` (20 × 16 MB)

### Task 1 — Dataset
- [x] **T-20** `rnn_predictor/vocab.py` — vocabulary from `sentence_builder.ALL_WORDS` (single source of truth)
- [x] **T-21** `rnn_predictor/tokenizer.py` — Word2Vec embedding training + index maps
- [x] **T-22** `rnn_predictor/sentence_builder.py` — biased template generation with multiprocessing

### Task 2 — Split
- [x] **T-30** `rnn_predictor/data_splitter.py` — encode + shuffle + 80/20 split + persist

### Task 3 — Model
- [x] **T-40** `rnn_predictor/rnn_model.py` — LSTM model (Embedding → LSTM → Dropout → Linear → LogSoftmax)

### Task 4 — Training
- [x] **T-50** `rnn_predictor/trainer.py` — training loop, early stopping, LR scheduling, checkpointing

### Task 5 — Evaluation
- [x] **T-60** `rnn_predictor/evaluator.py` — accuracy counts, confusion matrix, F1, perplexity, sample display

### Entry Point
- [x] **T-70** `main.py` — argparse CLI (all params including `--patience`, `--weight-decay`), task orchestration

---

## Testing Tasks

- [x] **T-80** Full pipeline end-to-end with defaults — completed, 301s, Top-1=56.65%
- [x] **T-81** `--skip-vocab` reuse of saved data — verified working
- [x] **T-82** Smoke test with small values — verified working
- [x] **T-83** Log files appear in `log/` — verified
- [x] **T-84** Ring-buffer rotation — verified (RotatingFileHandler)
- [x] **T-85** Multiprocessing in WSL with `spawn` context — verified working
- [x] **T-86** Model checkpoint save/reload before evaluation — verified

---

## Bug Fixes Applied

- [x] **T-B01** Fixed `torch.tensor(tensor)` UserWarning → `_to_long()` helper using `.clone().detach()`
- [x] **T-B02** Fixed `ReduceLROnPlateau(verbose=...)` TypeError (removed in PyTorch 2.4)
- [x] **T-B03** Fixed vocabulary/sentence mismatch — `vocab.py` now imports `ALL_WORDS` from `sentence_builder.py`
- [x] **T-B04** Fixed model collapse (predicting only 2 words) — reduced category sizes to 10 words each
- [x] **T-B05** Added `--patience` and `--weight-decay` CLI flags (were wired internally but not exposed)
- [x] **T-B06** Added `tqdm` progress bars to training (per-batch + per-epoch) and sentence generation
- [x] **T-B07** Added sentence tested/succeeded counts to evaluator log output
- [x] **T-B08** Added sample success/failure display in evaluator (10 each)

---

## Open Improvement Tasks

- [ ] **T-I01** Objects never predicted — add object-specific template slots or stronger bias triggers
- [ ] **T-I02** `soon` poorly predicted (diagonal=179) — add second bias trigger
- [ ] **T-I03** `that` never predicted (diagonal=0) — add at least one bias trigger
- [ ] **T-I04** `fast` over-predicted as default fallback — reduce bias strength to ~50%
- [ ] **T-I05** Multi-label evaluation — consider Top-K or human-plausibility metrics instead of exact-match only
- [ ] **T-I06** Try real text corpus (NLTK Brown) for genuine co-occurrence patterns
- [ ] **T-I07** Add GPU timing benchmarks alongside CPU results

---

## Documentation Tasks

- [x] **T-90** `README.md` — usage, CLI reference, benchmark results, confusion matrix analysis
- [x] **T-91** Inline docstrings on all public functions
- [x] **T-92** `planning.md` — updated with design evolution, known limitations, actual run times
- [x] **T-93** `tasks.md` — updated with completed/open status

---

## Status Legend

| Symbol | Meaning |
|--------|---------|
| `[ ]` | Not started |
| `[~]` | In progress |
| `[x]` | Complete |
| `[!]` | Blocked |
