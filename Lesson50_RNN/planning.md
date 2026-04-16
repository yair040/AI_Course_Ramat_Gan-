# planning.md — RNN Word Prediction Project Plan

**Author:** Yair Levi
**Date:** 2026

---

## Goal

Build a Python package that demonstrates a complete RNN pipeline:
vocabulary → embedding → biased template sentence generation → train/test split → LSTM training → evaluation with benchmarks.

---

## Design Evolution

The project went through three iterations of the dataset strategy before reaching
good results. Understanding this evolution is important for future changes.

### Iteration 1 — NLTK random word sampling (failed)
- Sampled 10,000 words at random from NLTK's 235k-word dictionary.
- Result: words like `paleostriatum`, `fifteenfold`, `axhammered` — obscure, rare.
- Model collapsed to predicting 2 words (`irony`, `theaters`).
- Top-1 accuracy: **0.01%**, Perplexity: **10,091**.
- Root cause: vocabulary/sentence mismatch + 10k vocab too large for random sentences.

### Iteration 2 — Common words + uniform templates (partial improvement)
- Switched to `wordfreq` frequency-ranked words and grammatical templates.
- Result: model still collapsed to `sky` and `name` for nearly all predictions.
- Top-1 accuracy: **2.96%**, Perplexity: **41.3**.
- Root cause: template word categories (~50 words each) too large; no co-occurrence
  signal between words — input didn't constrain output at all.

### Iteration 3 — Small categories + word-pair biases (current, working)
- 10 words per category; BIAS_TABLE gives 70% probability of specific word pairs.
- Top-1 accuracy: **56.65%**, Perplexity: **5.72**.
- The model now genuinely learns that `"dog"` predicts `"runs"`, `"old"` predicts `"tree"` etc.

---

## Phases

### Phase 0 — Environment Setup
- Create virtual environment at `../../venv` (relative to project root).
- Install dependencies from `requirements.txt`.
- Verify CUDA availability (fall back to CPU gracefully).
- Initialize `log/` and `data/` directories automatically on first run.

### Phase 1 — Dataset Preparation (skippable with `--skip-vocab`)

**1a. Vocabulary**
- Vocabulary is the union of all word categories defined in `sentence_builder.py`.
- ~48 unique words across 6 categories: Determiners, Nouns, Adjectives, Verbs, Adverbs, Objects.
- `--vocab-size` acts as an upper cap only; the full category union is always used.
- Persist to `data/vocabulary.pkl`.

**1b. Tokenization & Embedding**
- Train a Word2Vec model (`gensim`) on the vocabulary.
- Build word↔index maps (index 0 = `<PAD>`).
- Build a pre-trained embedding matrix for the LSTM.
- Persist all to `data/embeddings.pkl`.

**1c. Sentence Generation** *(multiprocessing)*
- Build M sentences from grammatical templates (default M = 100,000).
- Each template maps slots to word categories; last slot = prediction target.
- A BIAS_TABLE (70% strength) makes preceding words strongly predict specific followers.
- `multiprocessing.Pool` with `spawn` context splits work across CPU cores.
- Progress shown via `tqdm`.
- Persist to `data/sentences.pkl`.

### Phase 2 — Data Split
- Encode sentences (words → integer indices).
- Shuffle with fixed seed for reproducibility.
- Split 80% training / 20% testing (default).
- Persist to `data/train.pkl` and `data/test.pkl`.

### Phase 3 — RNN Model Definition
- Architecture: Embedding (pre-trained) → LSTM → Dropout → Linear → LogSoftmax.
- Default: 1 LSTM layer, hidden size 128, dropout 0.4.
- All hyperparameters exposed via CLI.

### Phase 4 — Training
- Adam optimizer with L2 weight decay (default 1e-4).
- NLLLoss criterion.
- `ReduceLROnPlateau` scheduler: halves LR when val loss stalls for 2 epochs.
- Early stopping with configurable patience (default 5 epochs).
- Per-epoch tqdm progress bars with live loss display.
- Best checkpoint saved to `data/best_model.pt`.

### Phase 5 — Evaluation
- Load best checkpoint before evaluating.
- Feed test sentences with last word removed; predict missing word.
- Metrics computed and logged:
  - Top-1 and Top-5 accuracy (with absolute counts)
  - Perplexity
  - Precision / Recall / F1 (macro-averaged)
  - Confusion matrix (top-20 most frequent classes)
- Sample successes and failures printed (10 each).

---

## Vocabulary & Sentence Design

### Word Categories (10 words each)

| Category | Words |
|----------|-------|
| Determiners | the, a, this, that, my, your, some, every, no, each |
| Nouns | dog, cat, child, bird, rain, wind, fire, river, sun, tree |
| Adjectives | big, small, old, young, fast, slow, hot, cold, loud, quiet |
| Verbs | runs, walks, sleeps, falls, grows, stops, starts, moves, stays, calls |
| Adverbs | fast, slowly, always, never, still, away, back, well, soon, hard |
| Objects | it, them, us, me, you, one, him, her, this, that |

### Bias Table (selected entries, 70% strength)

| Trigger | Category | Preferred word |
|---------|----------|----------------|
| dog | VERB | runs |
| cat | VERB | sleeps |
| rain | VERB | falls |
| old | NOUN | tree |
| hot | NOUN | fire |
| runs | ADV | fast |
| grows | ADV | slowly |
| falls | ADV | away |

---

## Known Limitations & Next Steps

| Issue | Status | Suggested Fix |
|-------|--------|---------------|
| Object words never predicted | Open | Add object-specific templates; strengthen object bias triggers |
| `soon` poorly predicted | Open | Add a second bias trigger word for `soon` |
| `that` never predicted | Open | Add at least one strong bias trigger |
| `fast` over-predicted as default | Open | Reduce bias strength for `fast` to ~50% |
| Multi-label fairness | By design | Many sentences have multiple valid completions; exact-match accuracy underestimates true model quality |

---

## Risk & Mitigation

| Risk | Mitigation |
|------|------------|
| Stale `data/` cache after vocab change | Always `rm -rf data/` before rerunning after category changes |
| Overfitting (val loss rises from epoch 1) | Early stopping + ReduceLROnPlateau + weight decay |
| Multiprocessing on WSL | `spawn` context used explicitly in `sentence_builder.py` |
| PyTorch API deprecations | `verbose` removed from `ReduceLROnPlateau`; `_to_long()` helper avoids `torch.tensor(tensor)` warning |

---

## Directory Layout

```
RNN/                         ← project root
├── main.py
├── requirements.txt
├── README.md
├── CLAUDE.md
├── planning.md
├── tasks.md
├── log/                     ← ring-buffer log (20 × 16 MB)
├── data/
│   ├── vocabulary.pkl
│   ├── embeddings.pkl
│   ├── sentences.pkl
│   ├── train.pkl
│   ├── test.pkl
│   └── best_model.pt
└── rnn_predictor/
    ├── __init__.py
    ├── config.py
    ├── logger_setup.py
    ├── vocab.py
    ├── tokenizer.py
    ├── sentence_builder.py
    ├── data_splitter.py
    ├── rnn_model.py
    ├── trainer.py
    └── evaluator.py

../../venv/                  ← virtual environment (two levels up)
```

---

## Actual Run Times (default parameters, CPU only)

| Phase | Actual Duration |
|-------|----------------|
| 1 — Dataset | ~2 min |
| 2 — Split | < 5 sec |
| 3 — Model build | < 5 sec |
| 4 — Training | ~4 min (early stopping at ~7 epochs) |
| 5 — Evaluation | ~1 sec |
| **Total** | **~301 seconds** |
