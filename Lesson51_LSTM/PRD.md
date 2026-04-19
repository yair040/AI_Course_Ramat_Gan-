# Product Requirements Document (PRD)
## LSTM Signal Filter — Python Package

**Author:** Yair Levi  
**Project Path:** `C:\Users\yair0\Documents\AI_continue\Lesson51_LSTM\LSTM\`  
**Environment:** WSL Ubuntu, Python Virtual Environment  
**Version:** 1.1.0  
**Last Updated:** 2026-04-19

---

## 1. Overview

A Python package that trains a dual-input LSTM neural network to extract a single clean sine-wave signal from a noisy four-frequency composite. The user supplies a one-hot filter vector that identifies the target frequency; the network receives the noisy composite and outputs the denoised target signal. All heavy computation is parallelised; all runs are fully logged with a ring-buffer file handler.

---

## 2. Goals

| # | Goal | Status |
|---|------|--------|
| G1 | Generate four pure sine signals, visualise them, sample at 1 kHz | ✅ Done |
| G2 | Add independent amplitude and phase noise; visualise | ✅ Done |
| G3 | Build an 8 000-row dataset and split it 80/20 | ✅ Done |
| G4 | Train a filter-conditioned LSTM to extract a chosen frequency from the noisy composite | ✅ Done |
| G5 | Evaluate: MSE, MAE, R²; plot loss curve and sample predictions | ✅ Done |
| G6 | Expose all key hyper-parameters as CLI options | ✅ Done |
| G7 | Ring-buffer logging (20 files × 16 MB) in `log/` subfolder | ✅ Done |
| G8 | Report elapsed time for every numbered task | ✅ Done |

---

## 3. Functional Requirements

### 3.1 Signal Generation (Tasks 1–2)
- Four sine signals: `y(t) = A·sin(2πft + φ)` with A=1, φ=0, f ∈ {1, 3, 5, 7} Hz (configurable)
- Time axis: 10 000 points over [0, 10 s]
- Plot all four signals + their normalised composite (sum ÷ 4) → `plots/task2_continuous.png`

### 3.2 Sampling (Tasks 3–4)
- Default sample rate: 1 kHz, duration: 10 s → 10 000 samples per signal
- Sampling parallelised across CPU cores via `multiprocessing.Pool`
- Plot sampled signals + composite (first 0.5 s shown) → `plots/task4_sampled.png`

### 3.3 Noise (Tasks 5–6)
- Per-sample amplitude noise: `dA ~ Uniform(−0.2, +0.2)`
- Per-sample phase noise: `dφ ~ Uniform(−π/5, +π/5)`
- Noisy signal: `y_noisy(t) = (A + dA)·sin(2πft + φ + dφ)`
- Plot noisy vs clean per signal + noisy composite → `plots/task6_noisy.png`

### 3.4 Dataset Schema (Tasks 7–8)

| Column | Shape | Contents |
|--------|-------|----------|
| Filter vector | (4,) | One-hot: which frequency to extract. e.g. `[0,1,0,0]` = 3 Hz |
| Input window | (prefix+window,) | Consecutive samples from the **noisy composite**. First `prefix` samples are warm-up context; last `window` samples are the prediction target region |
| Clean label | (window,) | Samples of the **clean** target signal at the same position as the last `window` input samples |

- Default: 8 000 rows, prefix=200, window=100
- Dataset pickled to `data/dataset.pkl`
- Generation parallelised via `multiprocessing.Pool`

### 3.5 Train / Test Split (Task 9)
- 80% training / 20% testing, random shuffle with fixed seed

### 3.6 LSTM Network Architecture (Task 10)

**Filter-conditioned dual-input LSTM:**

```
filter_vec (4,)
    │
    ▼
filter_embed (MLP: 4 → 2H → H, Tanh)
    │
    ├──► h0_proj (H → num_layers × H)  ──► initialises LSTM h₀
    ├──► c0_proj (H → num_layers × H)  ──► initialises LSTM c₀
    │
    └──► repeated across time ──┐
                                │
noisy_composite (prefix+W,)     │
    │                           │
    ▼                           ▼
[sample_t, f_emb_t]  ──► LSTM(input=1+H, hidden=H, layers=L)
                                │
                         last W outputs (after prefix)
                                │
                         output_head (MLP: H → H → 1)
                                │
                         prediction (W,)
```

- Loss: MSE between prediction and clean label
- The filter embedding initialises both h₀ and c₀ so the network begins in a state already tuned to the target frequency
- The filter embedding is also concatenated at every time step as a constant conditioning signal

### 3.7 Training & Testing (Tasks 11–12)
- Optimiser: Adam (lr=1e-3)
- Scheduler: ReduceLROnPlateau (factor=0.5, patience=8 epochs)
- Gradient clipping: max norm = 1.0
- Best checkpoint saved to `checkpoints/best_model.pt`
- Test metrics: MSE, MAE, R²

### 3.8 CLI Parameters (Task 13)

| Flag | Default | Description |
|------|---------|-------------|
| `--layers` | 2 | Number of LSTM layers |
| `--amp-noise` | 0.2 | Amplitude noise ± |
| `--phase-noise` | π/5 ≈ 0.628 | Phase noise ± (rad) |
| `--freqs` | 1 3 5 7 | Signal frequencies (Hz), space-separated |
| `--sample-rate` | 1000 | Sampling frequency (Hz) |
| `--duration` | 10 | Sample duration (s) |
| `--records` | 8000 | Dataset rows |
| `--epochs` | 150 | Training epochs |
| `--batch-size` | 64 | Batch size |
| `--hidden-size` | 128 | LSTM hidden units |
| `--window` | 100 | Prediction window (samples) |
| `--prefix` | 200 | Warm-up context samples before prediction window |
| `--seed` | 42 | Random seed |

### 3.9 Visualisation (Task 14)
- Loss curve (train vs. validation MSE per epoch) → `plots/task14_loss.png`
- Evaluation metrics table printed to stdout
- 5-panel sample plot: noisy composite / predicted / clean label → `plots/task14_samples.png`

---

## 4. Non-Functional Requirements

| Category | Requirement |
|----------|-------------|
| Performance | Multiprocessing for dataset generation and signal sampling |
| Logging | `RotatingFileHandler`, 20 backups × 16 MB = ~320 MB ring buffer, in `log/` |
| Code style | ≤ 150 lines per Python file, single responsibility per module |
| Paths | All relative; venv at `../../venv` relative to `LSTM/` |
| Package | `__init__.py` present; importable as `lstm_filter` |
| Reproducibility | `np.random.seed` and `torch.manual_seed` set from `--seed` |
| WSL compatibility | `matplotlib.use("Agg")` avoids X-display errors; plots saved to file |

---

## 5. File Structure

```
LSTM/
├── __init__.py
├── main.py              # Entry point; orchestrates all 14 tasks
├── config.py            # CLI parsing; Config dataclass
├── logger_setup.py      # Ring-buffer rotating logger
├── signals.py           # Tasks 1–2
├── sampling.py          # Tasks 3–4
├── noise.py             # Tasks 5–6
├── dataset.py           # Tasks 7–8
├── model.py             # Task 10: LSTMFilter
├── train.py             # Tasks 9, 11–12
├── visualise.py         # Task 14
├── requirements.txt
├── PRD.md
├── README.md
├── Claude.md
├── planning.md
├── tasks.md
├── log/                 # Auto-created: ring-buffer log files
├── plots/               # Auto-created: PNG output figures
├── data/                # Auto-created: dataset.pkl
└── checkpoints/         # Auto-created: best_model.pt
```

---

## 6. Design Decisions & Lessons Learned

| Decision | Rationale |
|----------|-----------|
| Window = 100 samples (not 10) | 10 samples (10 ms) covers < 1% of the 1 Hz period — insufficient for frequency identification. 100 ms covers meaningful fractions of all four periods. |
| 200-sample warm-up prefix | LSTM hidden state needs time to settle. Without prefix, the first ~30 predictions are inaccurate (transient response). Prefix eliminates this artefact. |
| Filter initialises h₀ and c₀ | Stronger conditioning than merely concatenating the filter at the output. The LSTM starts with its memory already tuned to the target frequency. |
| hidden_size = 128 | Provides sufficient capacity to distinguish 4 frequency patterns; 64 was too small. |
| epochs = 150 with ReduceLROnPlateau | Allows full convergence; scheduler prevents getting stuck at local minima after plateau. |
| Gradient clipping (max_norm=1.0) | Prevents exploding gradients common in deep LSTM with long sequences. |

---

## 7. Milestones

| Milestone | Deliverable | Status |
|-----------|-------------|--------|
| M1 | Documentation suite | ✅ |
| M2 | Package skeleton + logger + config | ✅ |
| M3 | Signal / sampling / noise modules | ✅ |
| M4 | Dataset builder with parallel generation | ✅ |
| M5 | LSTM model + training loop | ✅ |
| M6 | Evaluation + visualisation | ✅ |
| M7 | End-to-end integration + warm-up prefix fix | ✅ |
