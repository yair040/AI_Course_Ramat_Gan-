# Tasks — LSTM Signal Filter

**Author:** Yair Levi  
**Version:** 1.1.0

Each task maps directly to the numbered steps in the PRD.

---

## Task 1 — Generate 4 Sine Signals
**File:** `signals.py::generate_signals(cfg)`  
**Input:** Config (freqs, amplitude, phase, duration, sample_rate)  
**Output:** `(t, signals)` — continuous time axis + dict `{freq: np.ndarray}`  
**Formula:** `y(t) = A·sin(2πft + φ)`  
**Timing:** `perf_counter` logged at INFO level  

## Task 2 — Plot Continuous Signals
**File:** `signals.py::plot_signals(t, signals)`  
**Output:** 5-panel figure: 4 signals + normalised composite (÷4)  
**Saves to:** `plots/task2_continuous.png`  
**Result:** Clean sine waves clearly visible at 1, 3, 5, 7 Hz; composite shows complex interference pattern.

## Task 3 — Sample Signals at 1 kHz
**File:** `sampling.py::sample_signals(cfg)`  
**Output:** `(t_samp, sampled)` — discrete time axis + dict `{freq: np.ndarray}`  
**Multiprocessing:** Each signal sampled in a separate process via `Pool.map`  
**Result:** 10 000 samples per signal; 4 arrays of shape (10000,)  

## Task 4 — Plot Sampled Signals
**File:** `sampling.py::plot_sampled(t_samp, sampled)`  
**Output:** Stem plot, first 0.5 s shown for readability  
**Saves to:** `plots/task4_sampled.png`  
**Note:** `use_line_collection` argument removed (deprecated in matplotlib 3.7+)

## Task 5 — Add Noise to Sampled Signals
**File:** `noise.py::add_noise(t_samp, sampled, cfg, rng)`  
**Noise model:** Per sample:
  - `dA ~ Uniform(−amp_noise, +amp_noise)` (default ±0.2)
  - `dφ ~ Uniform(−phase_noise, +phase_noise)` (default ±π/5)
  - `y_noisy(t) = (A + dA)·sin(2πft + φ + dφ)`
**Output:** Dict `{freq: noisy_array}` same shape as `sampled`

## Task 6 — Plot Noisy Signals
**File:** `noise.py::plot_noisy(t_samp, noisy, sampled)`  
**Output:** Each panel: noisy (blue) vs clean (orange dashed); composite panel (red)  
**Saves to:** `plots/task6_noisy.png`  
**Result:** Noise clearly visible; clean signal shape still recognisable beneath noise.

## Task 7 — Define Dataset Schema
**File:** `dataset.py` (module docstring)  

| Column | Shape | Contents |
|--------|-------|----------|
| filter_vec | (4,) | One-hot: which frequency to extract |
| input_win | (prefix+window,) | Noisy composite with warm-up prefix |
| clean_label | (window,) | Clean target signal at same position |

## Task 8 — Build Dataset
**File:** `dataset.py::build_dataset(cfg, sampled, noisy)`  
**Process:**
1. Stack clean arrays: `(n_signals, T)`, noisy arrays: `(n_signals, T)`
2. Compute noisy composite: `sum(noisy_arrays) / n_signals` → `(T,)`
3. For each row: pick random signal index and random start position
4. Slice `prefix+window` samples from composite as input
5. Slice `window` samples from clean target as label
6. Parallelise via `Pool.map` (one chunk per CPU core)  

**Saves to:** `data/dataset.pkl` as `(filters, input_wins, clean_labels)`  
**v1.1 change:** Each input window now includes 200 warm-up prefix samples before the 100-sample prediction window.

## Task 9 — Train / Test Split
**File:** `train.py::split_dataset(filters, input_wins, clean_labels, cfg)`  
**Uses:** `sklearn.model_selection.train_test_split` with fixed seed  
**Result:** 6 400 training rows, 1 600 test rows (80/20)

## Task 10 — Build LSTM Network
**File:** `model.py::LSTMFilter`  

**Architecture:**
```
Input A: filter_vec (4,)
  → filter_embed MLP (4 → 2H → H, Tanh)
  → h0_proj (H → layers×H) → LSTM h₀
  → c0_proj (H → layers×H) → LSTM c₀
  → expanded to (prefix+window) steps → concatenated with signal

Input B: noisy composite (prefix+window,)
  → unsqueeze → (prefix+window, 1)
  → concat with filter expansion → (prefix+window, 1+H)
  → LSTM(input=1+H, hidden=H, layers=L, dropout=0.2)
  → take last `window` outputs → (window, H)
  → output_head MLP (H → H → 1) → (window,)
```

**Key design:** Filter initialises h₀ and c₀ so the LSTM begins already tuned to the target frequency, not just at zero state.

## Task 11 — Train Network
**File:** `train.py::train(model, ...)`  
**Loss:** `nn.MSELoss`  
**Optimiser:** Adam (lr=1e-3)  
**Scheduler:** ReduceLROnPlateau (factor=0.5, patience=8)  
**Gradient clipping:** max_norm=1.0  
**Logs:** per-epoch train loss and val loss  
**Note:** `verbose` argument removed from scheduler (deprecated in PyTorch 2.4+)

## Task 12 — Test Network
**File:** `train.py::evaluate(model, ...)`  
**Loads:** Best checkpoint from `checkpoints/best_model.pt`  
**Metrics:** MSE, MAE, R² (sklearn)  
**Returns:** `(metrics_dict, predictions_array)`

## Task 13 — CLI Parameters
**File:** `config.py::parse_args()`  
**All flags:** layers, amp-noise, phase-noise, freqs, sample-rate, duration, records, epochs, batch-size, hidden-size, window, prefix, seed  
**Returns:** Typed `Config` dataclass with computed properties `n_samples` and `n_signals`

## Task 14 — Visualise Results
**File:** `visualise.py`  

| Function | Output | Saves to |
|----------|--------|----------|
| `plot_loss_curve(history)` | Train + val MSE per epoch | `plots/task14_loss.png` |
| `print_metrics(metrics)` | MSE, MAE, R² table to stdout | — |
| `plot_samples(noisy, preds, labels, n=5)` | 5-panel comparison plot | `plots/task14_samples.png` |

**Loss curve observations (v1.1 run):**
- Rapid descent epoch 1–15 (0.41 → 0.06)
- Temporary spike at epoch ~30 and ~78 (LR scheduler steps)
- Smooth convergence to near-zero MSE by epoch 100
- Train and validation track closely — no overfitting

**Sample prediction observations (v1.1 run):**
- Predicted signal closely follows clean label across all test examples
- No start-of-window divergence (warm-up prefix eliminates transient)
- Noisy composite successfully separated into target frequency

---

## Cross-Cutting Concerns

| Concern | Implementation |
|---------|---------------|
| Timing | `time.perf_counter()` at start/end of every task function; logged at INFO |
| Logging | `logger = logging.getLogger(__name__)` in every module; ring buffer in `log/` |
| Reproducibility | `np.random.seed(cfg.seed)`, `torch.manual_seed(cfg.seed)` in `main.py` |
| WSL safety | `matplotlib.use("Agg")` at top of all plot modules; no `plt.show()` |
| Output dirs | `main.py::ensure_dirs()` creates `log/`, `plots/`, `data/`, `checkpoints/` |
| File length | All modules ≤ 150 lines |
