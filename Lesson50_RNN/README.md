# RNN Word Prediction

**Author:** Yair Levi

## See result analysing later below


A Python package that builds a complete RNN pipeline for next-word prediction:
vocabulary → embedding → biased template sentence generation → train/test split → LSTM training → evaluation.

---

## Requirements

- Python 3.10+
- WSL (Ubuntu) recommended
- CUDA-capable GPU optional (falls back to CPU)

---

## Setup

```bash
# From the project root (RNN/)
python3 -m venv ../../venv
source ../../venv/bin/activate
pip install -r requirements.txt
```

> **Note:** If you change vocabulary or sentence generation parameters, delete `data/` before rerunning to avoid stale cache conflicts.
> ```bash
> rm -rf data/
> python main.py
> ```

---

## Usage

### Full Pipeline (all tasks)

```bash
python main.py
```

### Skip vocabulary/sentence generation (reuse saved data)

```bash
python main.py --skip-vocab
```

### Custom parameters

```bash
python main.py \
  --num-sentences 50000 \
  --epochs 30 \
  --hidden-size 128 \
  --num-layers 1 \
  --lr 0.0005 \
  --batch-size 128 \
  --patience 5 \
  --weight-decay 0.0001
```

---

## CLI Reference

| Flag | Default | Description |
|------|---------|-------------|
| `--skip-vocab` | False | Skip Task 1; load existing `data/` files |
| `--vocab-size` | 1000 | Upper cap on vocabulary size (actual size = category union ~48 words) |
| `--num-sentences` | 100000 | Number of template sentences to generate |
| `--max-sent-len` | 5 | Maximum words per sentence |
| `--train-ratio` | 0.8 | Fraction of data used for training |
| `--embed-dim` | 64 | Word embedding dimensionality |
| `--hidden-size` | 128 | LSTM hidden state size |
| `--num-layers` | 1 | Number of LSTM layers |
| `--dropout` | 0.4 | Dropout probability |
| `--lr` | 0.0005 | Adam learning rate |
| `--epochs` | 30 | Max training epochs (early stopping may halt sooner) |
| `--batch-size` | 128 | Mini-batch size |
| `--patience` | 5 | Early-stopping patience (epochs without val improvement) |
| `--weight-decay` | 0.0001 | L2 regularisation coefficient for Adam |
| `--seed` | 42 | Random seed for reproducibility |

---

## How Sentence Generation Works

Sentences are built from **grammatical templates** using six word categories:

| Category | Example words |
|----------|--------------|
| Determiners | the, a, this, my, some, every |
| Nouns | dog, cat, child, bird, rain, wind, fire, river, sun, tree |
| Adjectives | big, small, old, young, fast, slow, hot, cold, loud, quiet |
| Verbs | runs, walks, sleeps, falls, grows, stops, starts, moves, stays, calls |
| Adverbs | fast, slowly, always, never, still, away, back, well, soon, hard |
| Objects | it, them, us, me, you, one, him, her, this, that |

Example templates (last slot = prediction target):

```
[DET, NOUN, VERB]            →  "the dog runs"
[ADJ, NOUN, VERB, ADV]       →  "big dog runs fast"
[DET, ADJ, NOUN, VERB, ADV]  →  "the big dog runs fast"
[NOUN, VERB, OBJ]            →  "dog runs it"
```

A **bias table** (70% strength) makes certain words strongly predict specific followers,
giving the model a genuine learnable signal:

```
"dog"   → verb  "runs"    |  "rain"  → verb  "falls"
"old"   → noun  "tree"    |  "hot"   → noun  "fire"
"runs"  → adverb "fast"   |  "grows" → adverb "slowly"
```

---

## Output Files

| File | Description |
|------|-------------|
| `log/rnn_predictor.log` | Ring buffer: 20 files × 16 MB |
| `data/vocabulary.pkl` | Word list |
| `data/embeddings.pkl` | Word2Vec model + index maps + embedding matrix |
| `data/sentences.pkl` | Generated sentence list |
| `data/train.pkl` | Encoded training split |
| `data/test.pkl` | Encoded test split |
| `data/best_model.pt` | Best model checkpoint (lowest val loss) |

---

## Evaluation Metrics Explained

| Metric | Meaning |
|--------|---------|
| **Top-1 Accuracy** | Model's single best guess is exactly right |
| **Top-5 Accuracy** | Correct word appears in model's top 5 predictions |
| **Perplexity** | Average surprise of the model — lower = more confident and correct |
| **Precision (macro)** | When model predicts a word, how often is it right (averaged over all words) |
| **Recall (macro)** | Of all sentences with a given true word, how often does model find it |
| **F1 (macro)** | Harmonic mean of precision and recall |

---

## Benchmark Results (default parameters, 2026-04-16)

**Pipeline total time:** 301 seconds (CPU only)

### Test Set Summary

```
Sentences tested : 20,000
Top-1 correct    : 11,329  (56.65%)
Top-5 correct    : 14,442  (72.21%)
Perplexity       : 5.72
Precision (macro): 0.2670
Recall (macro)   : 0.3315
F1 (macro)       : 0.2901
```

Random-chance baseline with 10 words per category would give ~10% Top-1.
The model achieves 56.65%, demonstrating it has learned the bias patterns.

### Sample Predictions — Successes

```
Input: 'some young child'       → true: 'calls'    pred: 'calls'   ✓
Input: 'the child runs'         → true: 'fast'     pred: 'fast'    ✓
Input: 'the young cat'          → true: 'sleeps'   pred: 'sleeps'  ✓
Input: 'quiet cat'              → true: 'sleeps'   pred: 'sleeps'  ✓
Input: 'a tree'                 → true: 'grows'    pred: 'grows'   ✓
Input: 'some hot fire'          → true: 'grows'    pred: 'grows'   ✓
Input: 'my quiet cat runs'      → true: 'fast'     pred: 'fast'    ✓
Input: 'this old tree'          → true: 'grows'    pred: 'grows'   ✓
Input: 'old tree'               → true: 'grows'    pred: 'grows'   ✓
Input: 'a hot fire grows'       → true: 'slowly'   pred: 'slowly'  ✓
```

### Sample Predictions — Failures

```
Input: 'river moves'            → true: 'you'      pred: 'away'
Input: 'small cat'              → true: 'calls'    pred: 'sleeps'
Input: 'that bird falls'        → true: 'them'     pred: 'away'
Input: 'fire grows'             → true: 'back'     pred: 'slowly'
Input: 'no dog runs'            → true: 'you'      pred: 'fast'
Input: 'dog runs'               → true: 'me'       pred: 'fast'
Input: 'cat sleeps'             → true: 'them'     pred: 'still'
Input: 'some cold wind moves'   → true: 'soon'     pred: 'away'
Input: 'no young child sleeps'  → true: 'never'    pred: 'still'
Input: 'my fire grows'          → true: 'fast'     pred: 'slowly'
```

**Important note on failures:** Many "failures" are actually linguistically reasonable.
For example:

- `'dog runs' → pred: 'fast'` — "the dog runs fast" is perfectly natural English,
  even though the dataset happened to assign `'me'` as the target.
- `'river moves' → pred: 'away'` — "the river moves away" makes sense;
  the true label `'you'` is arguably less natural.
- `'that bird falls' → pred: 'away'` — "the bird falls away" is plausible;
  `'them'` is a less obvious completion.

This is an inherent limitation of synthetic single-label evaluation: in natural
language, **many words can correctly complete the same sentence**. The model is
penalised for predicting a valid completion that differs from the one the random
generator happened to assign. True language model evaluation accounts for this
with human judgements or perplexity rather than exact-match accuracy.

---

## Confusion Matrix Analysis (top-20 classes, default run)

```
Labels: ['that', 'fast', 'runs', 'sleeps', 'falls', 'grows', 'moves',
         'stays', 'calls', 'slowly', 'still', 'away', 'back', 'soon',
         'it', 'us', 'me', 'you', 'him', 'her']

[[   0   40    0    0    0    0    0    0    0   86   95  144   64   12    0    0    0    0    0    0]
 [   0  827    0    0    0    0    0    0    0   52   54   72   27    7    0    0    0    0    0    0]
 [   0    0  683   36   25   51   51    5   28    0    0    0    0    0    0    0    0    0    0    0]
 [   0    0   27  695   17   46   49    8   22    0    0    0    0    0    0    0    0    0    0    0]
 [   0    0   29   35  540   51   39   20   18    0    0    0    0    0    0    0    0    0    0    0]
 [   0    0   25   30   19  994   59   11   18    0    0    0    0    0    0    0    0    0    0    0]
 [   0    0   35   26   16   34 1216   13   18    0    0    0    0    0    0    0    0    0    0    0]
 [   0    0   26   36   20   41   72  260   18    0    0    0    0    0    0    0    0    0    0    0]
 [   0    0   22   27   29   40   53   17  481    0    0    0    0    0    0    0    0    0    0    0]
 [   0   28    0    0    0    0    0    0    0 1335   48   73   26    6    0    0    0    0    0    0]
 [   0   42    0    0    0    0    0    0    0   60 1230   73   33    8    0    0    0    0    0    0]
 [   0   39    0    0    0    0    0    0    0   64   52 2011   35    7    0    0    0    0    0    0]
 [   0   37    0    0    0    0    0    0    0   60   51   82  878   12    0    0    0    0    0    0]
 [   0   32    0    0    0    0    0    0    0   52   64   93   51  179    0    0    0    0    0    0]
 [   0   48    0    0    0    0    0    0    0   90   86  152   56   11    0    0    0    0    0    0]
 [   0   50    0    0    0    0    0    0    0   99   97  144   50   20    0    0    0    0    0    0]
 [   0   47    0    0    0    0    0    0    0   94  102  139   47   10    0    0    0    0    0    0]
 [   0   53    0    0    0    0    0    0    0   86   87  162   63   15    0    0    0    0    0    0]
 [   0   56    0    0    0    0    0    0    0   91   97  127   66   11    0    0    0    0    0    0]
 [   0   50    0    0    0    0    0    0    0   98   85  162   58   14    0    0    0    0    0    0]]
```

### Confusion Matrix Summary

| Group | Behaviour | Reason |
|-------|-----------|--------|
| Verbs (`runs`, `sleeps`, `falls`, `grows`, `moves`, `stays`, `calls`) | Well learned; predictions stay within verb category | Strong bias triggers + typed template slots |
| Adverbs `slowly`, `still`, `away` | Very well learned; high diagonal counts | Multiple bias triggers each (2+ trigger words) |
| Adverbs `back`, `fast` | Moderately learned | Single or moderate triggers |
| `soon` | Poorly learned (diagonal=179) | Single weak trigger (`stops→soon`), drowned out by `away` |
| Objects (`it`, `us`, `me`, `you`, `him`, `her`) | Never predicted (diagonal=0) | Adverb targets dominate the same template slot position |
| `that` | Never predicted (diagonal=0) | Too few/varied contexts; no dedicated bias trigger |

**Key insight:** The matrix splits cleanly into two non-overlapping blocks — verbs
(rows 2–8) never predict adverbs/objects, and adverbs/objects never predict verbs.
This shows the model has learned **grammatical category** from the template structure,
even when it cannot identify the exact word.

---

## What to Fix Next

1. **Objects are never predicted** — add more bias entries pointing specifically to
   object words (e.g. `"child" → "them"`, `"dog" → "it"`), or create dedicated
   object-slot templates so adverbs and objects no longer compete for the same
   position in a sentence.

2. **`soon` and `that` are lost** — add a second bias trigger for each. `soon` only
   has `"stops" → "soon"`; adding `"calls" → "soon"` would double its training signal.
   `that` needs at least one strong trigger word.

3. **`fast` is over-predicted** — it acts as a default fallback for the adverb/object
   group. Reduce its bias strength from 70% to ~50%, or add stronger competing
   signals for the words it drowns out (`soon`, `never`, `hard`, `well`).

---

## Project Structure

```
RNN/
├── main.py
├── requirements.txt
├── README.md
├── CLAUDE.md
├── planning.md
├── tasks.md
├── log/
├── data/
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

../../venv/   ← virtual environment (two levels up from project root)
```

---

## License

MIT — Yair Levi, 2026
