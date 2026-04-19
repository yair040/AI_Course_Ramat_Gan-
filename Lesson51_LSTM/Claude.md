# Claude.md — AI Assistant Context

## Project
LSTM Signal Filter — `lstm_filter` Python package  
**Author:** Yair Levi  
**Version:** 1.1.0

## Purpose of This File
Provides full context so Claude (or any LLM assistant) can continue work on this project knowing all past design decisions, bugs fixed, and current architecture.

---

## Current Architecture (v1.1.0)

### Dataset Schema
```
filters:      (N, 4)              — one-hot filter vectors
input_wins:   (N, prefix+window)  — noisy composite with warm-up prefix
clean_labels: (N, window)         — clean target signal (label)
```

### Model: LSTMFilter (`model.py`)
```
filter_vec (4,)
    │
    ▼
filter_embed: Linear(4→2H) → Tanh → Linear(2H→H) → Tanh
    │
    ├──► h0_proj: Linear(H → layers×H)  — initialises LSTM h₀
    ├──► c0_proj: Linear(H → layers×H)  — initialises LSTM c₀
    │
    └──► expanded across (prefix+window) steps
         concatenated with noisy composite samples
                 │
                 ▼
         LSTM(input=1+H, hidden=H, layers=L, dropout=0.2)
                 │
         only last `window` outputs used
                 │
         output_head: Linear(H→H) → ReLU → Linear(H→1)
                 │
         prediction: (window,)
```

### Training Config (Defaults)
```python
FREQS        = [1, 3, 5, 7]   # Hz
AMPLITUDE    = 1.0
PHASE        = 0.0
SAMPLE_RATE  = 1000            # Hz
DURATION     = 10              # seconds
AMP_NOISE    = 0.2             # uniform ±
PHASE_NOISE  = math.pi / 5    # uniform ±
N_RECORDS    = 8000
WINDOW       = 100             # prediction samples per row
PREFIX       = 200             # warm-up samples before window
LSTM_LAYERS  = 2
HIDDEN_SIZE  = 128
EPOCHS       = 150
BATCH_SIZE   = 64
LEARNING_RATE = 1e-3
```

---

## Architecture Decisions

### Why filter initialises h₀ and c₀?
Simply concatenating the filter vector to the LSTM output is weak — it doesn't affect how the LSTM reads the signal. Initialising h₀ and c₀ from the filter embedding makes the LSTM start with its recurrent memory already biased toward the target frequency. It's the same principle as conditioning in sequence-to-sequence models. The filter is *also* concatenated at every time step for a constant reminder.

### Why prefix = 200 samples?
An LSTM has a transient response just like a real digital filter. During the first 20–40 time steps the hidden state is still settling, producing inaccurate outputs. The 200-sample prefix (200 ms) lets the LSTM fully settle before any prediction is required. Only the last `window` outputs are passed to the output head.

### Why window = 100?
At 1 kHz, 10 samples = 10 ms, which is < 1% of the 1 Hz period. The LSTM cannot identify frequency from such a short segment. 100 ms covers: 0.1 cycles @ 1Hz, 0.3 @ 3Hz, 0.5 @ 5Hz, 0.7 @ 7Hz — enough shape for frequency discrimination.

### Why hidden_size = 128?
64 was too small — the network learned to predict a smoothed mean rather than the actual waveform shape. 128 provides sufficient capacity without overfitting on 8 000 rows.

### Why multiprocessing for dataset generation?
Dataset rows are independent — each is a random draw from the signal arrays. `Pool.map` splits the 8 000 rows across workers (one per signal frequency), reducing wall time roughly 4×.

### Why ring-buffer logger?
Long training runs are verbose. 20 × 16 MB = ~320 MB of history before overwrite. Enough to diagnose a failed overnight run without filling disk.

---

## Bugs Fixed (Chronological)

| Bug | Symptom | Fix |
|-----|---------|-----|
| `use_line_collection` TypeError | `sampling.py` crashed on matplotlib 3.7+ | Removed deprecated argument |
| `verbose` TypeError | `train.py` crashed on PyTorch 2.4+ | Removed `verbose=False` from `ReduceLROnPlateau` |
| Venv not executable on WSL | `pip` crashed with "cannot execute" | Recreate venv from inside WSL with `python3 -m venv` |
| Predicted signal tracks composite mean, not clean signal | 10-sample window + no strong filter conditioning | Window→100, filter-conditioned h₀/c₀, hidden→128 |
| Start-of-window divergence | LSTM transient / warm-up lag | Added 200-sample prefix; output head applied only after prefix |

---

## Conventions

| Convention | Rule |
|------------|------|
| Paths | Always relative; never hard-coded absolute paths |
| Logging | `logger = logging.getLogger(__name__)` in every module |
| Timing | `time.perf_counter()` at start and end of every numbered task |
| Random seed | Set `np.random.seed(cfg.seed)` and `torch.manual_seed(cfg.seed)` in `main.py` |
| Backend | `matplotlib.use("Agg")` at top of every plotting module |
| File length | ≤ 150 lines per `.py` file |

---

## Environment

```
OS:      WSL Ubuntu
Python:  3.12
venv:    ../../venv  (relative to LSTM/)
Activate: source ../../venv/bin/activate
Run:      python3 main.py [--flags]
```

---

## How to Extend

| Goal | Where to change |
|------|----------------|
| Add a new frequency | Pass `--freqs 1 3 5 7 9`; n_signals auto-updates |
| Change noise distribution | Edit `noise.py::add_noise()` |
| Swap LSTM for GRU | Replace `nn.LSTM` with `nn.GRU` in `model.py`; remove cell state `c₀` |
| Swap for Transformer | Replace `model.py` entirely; keep `train.py` interface unchanged |
| Add new evaluation metric | Add to `visualise.py::print_metrics()` |
| Longer warm-up | Increase `--prefix` (e.g. 400 for better 1 Hz settling) |
