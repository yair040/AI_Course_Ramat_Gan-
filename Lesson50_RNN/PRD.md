# Product Requirements Document (PRD)
## RNN Word Prediction Package

**Author:** Yair Levi  
**Version:** 1.0  
**Date:** 2025  
**Platform:** Python 3.10+, WSL (Ubuntu), Virtual Environment

---

## 1. Executive Summary

This document specifies a Python package (`rnn_predictor`) that demonstrates an end-to-end Recurrent Neural Network pipeline for next-word prediction. The system samples English words, generates synthetic short sentences, trains an LSTM-based RNN, and evaluates prediction quality using standard NLP benchmarks.

---

## 2. Objectives

1. Provide a complete, runnable RNN pipeline from raw word data to evaluated model.
2. Allow users to skip the expensive dataset-preparation phase if data already exists.
3. Keep each source file ≤ 150 lines and all paths relative.
4. Leverage multiprocessing for CPU-bound sentence generation.
5. Emit structured, ring-buffered logs for monitoring and debugging.

---

## 3. Functional Requirements

### 3.1 Task 1 — Dataset Preparation (skippable)

#### 3.1a Vocabulary Sampling
- **FR-101**: The system SHALL sample N words at random from the NLTK English words corpus (default N = 10,000).
- **FR-102**: N SHALL be user-configurable via `--vocab-size` CLI argument.
- **FR-103**: The sampled vocabulary SHALL be persisted to `data/vocabulary.pkl`.

#### 3.1b Tokenization & Embedding
- **FR-111**: Each vocabulary word SHALL be tokenized.
- **FR-112**: A Word2Vec model SHALL be trained on the vocabulary to produce dense embedding vectors.
- **FR-113**: Embedding dimensionality SHALL default to 100 and be user-configurable via `--embed-dim`.
- **FR-114**: The embedding model SHALL be persisted to `data/embeddings.pkl`.

#### 3.1c Sentence Generation
- **FR-121**: The system SHALL generate M short sentences from the vocabulary (default M = 100,000).
- **FR-122**: Each sentence SHALL contain at most W words (default W = 5).
- **FR-123**: M and W SHALL be user-configurable via `--num-sentences` and `--max-sent-len`.
- **FR-124**: Sentence generation SHALL use `multiprocessing.Pool` to utilise all available CPU cores.
- **FR-125**: Generated sentences SHALL be persisted to `data/sentences.pkl`.
- **FR-126**: Elapsed time for Task 1 SHALL be logged and printed.

### 3.2 Task 2 — Train/Test Split

- **FR-201**: The system SHALL split sentences into a training set (default 80%) and a test set (default 20%).
- **FR-202**: The split ratio SHALL be user-configurable via `--train-ratio`.
- **FR-203**: Shuffling SHALL use a seeded random generator (default seed = 42, configurable via `--seed`).
- **FR-204**: Splits SHALL be persisted to `data/train.pkl` and `data/test.pkl`.
- **FR-205**: Elapsed time for Task 2 SHALL be logged and printed.

### 3.3 Task 3 — RNN Model Construction

- **FR-301**: The model SHALL be an LSTM-based sequence model.
- **FR-302**: Architecture: Embedding → LSTM → Dropout → Linear → LogSoftmax.
- **FR-303**: All hyperparameters SHALL have documented defaults and be user-configurable (see Section 6).
- **FR-304**: The model SHALL be defined in `rnn_predictor/rnn_model.py` (≤ 150 lines).

### 3.4 Task 4 — Training

- **FR-401**: Training SHALL use the Adam optimizer with NLLLoss.
- **FR-402**: Loss per epoch SHALL be logged at INFO level.
- **FR-403**: The best checkpoint (lowest validation loss) SHALL be saved to `data/best_model.pt`.
- **FR-404**: Elapsed time for Task 4 SHALL be logged and printed.

### 3.5 Task 5 — Evaluation

- **FR-501**: The system SHALL feed test sentences with the last word removed to the model and predict the missing word.
- **FR-502**: The following metrics SHALL be computed and logged:
  - Top-1 Accuracy (exact match)
  - Top-5 Accuracy (correct word in top 5 predictions)
  - Confusion Matrix (top-K most frequent predicted classes)
  - Precision, Recall, F1 (macro-averaged via scikit-learn)
  - Perplexity
- **FR-503**: Elapsed time for Task 5 SHALL be logged and printed.

### 3.6 Skip Mode

- **FR-601**: The CLI flag `--skip-vocab` SHALL cause the program to skip Task 1 and load data from `data/vocabulary.pkl`, `data/embeddings.pkl`, and `data/sentences.pkl`.
- **FR-602**: If `--skip-vocab` is set but required pickle files are missing, the system SHALL exit with a clear error message.

---

## 4. Non-Functional Requirements

### 4.1 Code Quality
- **NFR-101**: Each Python source file SHALL contain no more than 150 lines (including imports and docstrings).
- **NFR-102**: All public functions and classes SHALL have docstrings.
- **NFR-103**: The project SHALL be structured as an installable Python package with `__init__.py`.

### 4.2 Paths
- **NFR-201**: All file I/O SHALL use relative paths via `pathlib.Path`.
- **NFR-202**: No hardcoded absolute paths SHALL appear anywhere in the codebase.
- **NFR-203**: The virtual environment SHALL be located at `../../venv` relative to the project root.

### 4.3 Logging
- **NFR-301**: Logging SHALL use Python's standard `logging` module.
- **NFR-302**: Minimum log level SHALL be INFO.
- **NFR-303**: Log output SHALL use a `RotatingFileHandler` with:
  - `maxBytes = 16 * 1024 * 1024` (16 MB per file)
  - `backupCount = 19` (20 files total: 1 active + 19 rotated)
  - Files stored in the `log/` subdirectory relative to the project root.
- **NFR-304**: When the 20th file fills, the oldest file SHALL be overwritten (standard `RotatingFileHandler` behaviour).
- **NFR-305**: Log format SHALL include timestamp, level, module name, and message.

### 4.4 Performance
- **NFR-401**: Sentence generation SHALL use Python `multiprocessing` (not threading) to maximise CPU utilisation.
- **NFR-402**: Each major task SHALL report elapsed wall-clock time using `time.perf_counter()`.

### 4.5 Reproducibility
- **NFR-501**: A global random seed SHALL be accepted via `--seed` and applied to Python `random`, `numpy`, and `torch`.

---

## 5. System Architecture

```
main.py
  └─ parse CLI args
  └─ setup logger
  └─ if not --skip-vocab:
       └─ vocab.py        → Task 1a
       └─ tokenizer.py    → Task 1b
       └─ sentence_builder.py (multiprocessing) → Task 1c
  └─ data_splitter.py    → Task 2
  └─ rnn_model.py        → Task 3
  └─ trainer.py          → Task 4
  └─ evaluator.py        → Task 5
```

---

## 6. Configuration Defaults

| Parameter | Default | CLI Flag |
|-----------|---------|----------|
| Vocabulary size | 10,000 | `--vocab-size` |
| Sentences | 100,000 | `--num-sentences` |
| Max sentence length | 5 words | `--max-sent-len` |
| Train ratio | 0.8 | `--train-ratio` |
| Embedding dim | 100 | `--embed-dim` |
| Hidden size | 256 | `--hidden-size` |
| LSTM layers | 2 | `--num-layers` |
| Dropout | 0.3 | `--dropout` |
| Learning rate | 0.001 | `--lr` |
| Epochs | 10 | `--epochs` |
| Batch size | 64 | `--batch-size` |
| Random seed | 42 | `--seed` |

---

## 7. File Inventory

| File | Purpose | Max Lines |
|------|---------|-----------|
| `main.py` | CLI entry point, task orchestration | 150 |
| `rnn_predictor/__init__.py` | Package init, NLTK downloads | 30 |
| `rnn_predictor/config.py` | Config dataclass | 60 |
| `rnn_predictor/logger_setup.py` | Ring-buffer logging setup | 50 |
| `rnn_predictor/vocab.py` | Task 1a: word sampling | 60 |
| `rnn_predictor/tokenizer.py` | Task 1b: tokenization + Word2Vec | 80 |
| `rnn_predictor/sentence_builder.py` | Task 1c: sentence generation | 80 |
| `rnn_predictor/data_splitter.py` | Task 2: train/test split | 60 |
| `rnn_predictor/rnn_model.py` | Task 3: LSTM model | 80 |
| `rnn_predictor/trainer.py` | Task 4: training loop | 150 |
| `rnn_predictor/evaluator.py` | Task 5: benchmarks | 150 |

---

## 8. Acceptance Criteria

1. Running `python main.py` with no arguments completes all 5 tasks without error.
2. Running `python main.py --skip-vocab` after a full run reuses saved data and completes Tasks 2–5.
3. Log files appear in `log/` with the naming pattern `rnn_predictor.log`, `rnn_predictor.log.1`, …
4. All 5 evaluation metrics are printed and logged.
5. No source file exceeds 150 lines.
6. No absolute paths appear in any source file.
