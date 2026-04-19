# Planning — LSTM Signal Filter

**Author:** Yair Levi  
**Version:** 1.1.0

---

## Phase 0 — Repository Bootstrap ✅
- [x] Create folder structure inside `LSTM/`
- [x] Write `requirements.txt`
- [x] Write documentation files (PRD, README, Claude.md, planning.md, tasks.md)
- [x] Set up `logger_setup.py` (ring buffer, 20 × 16 MB, `log/` subfolder)
- [x] Set up `config.py` (argparse with all CLI flags + Config dataclass)
- [x] Write `__init__.py`

## Phase 1 — Signal Processing (Tasks 1–6) ✅
- [x] `signals.py` — pure sine generation + matplotlib plot (Tasks 1–2)
- [x] `sampling.py` — discrete sampling via multiprocessing + plot (Tasks 3–4)
  - Fix: removed deprecated `use_line_collection=True` from `stem()` (matplotlib 3.7+)
- [x] `noise.py` — per-sample amplitude and phase noise injection + plot (Tasks 5–6)

All plots save to `plots/` using `Agg` backend (WSL-safe).

## Phase 2 — Dataset (Tasks 7–8) ✅
- [x] `dataset.py`
  - One-hot filter column (4-d)
  - Input window: `prefix + window` samples from noisy composite
  - Clean label: `window` samples from clean target signal (same position)
  - Parallel generation via `multiprocessing.Pool`
  - Pickled to `data/dataset.pkl`
  - **v1.1:** Added 200-sample warm-up prefix to eliminate LSTM transient

## Phase 3 — Model (Tasks 10–12) ✅
- [x] `model.py` — filter-conditioned LSTM (`LSTMFilter`, PyTorch)
  - **v1.0:** Simple concatenation of filter at each step — insufficient
  - **v1.1:** Filter initialises h₀ and c₀; also concatenated per step — correct
  - Output head applied only to last `window` steps (after prefix)
- [x] `train.py`
  - 80/20 split (Task 9)
  - Adam optimiser + ReduceLROnPlateau scheduler + gradient clipping
  - Per-epoch loss logging; best checkpoint to `checkpoints/`
  - Metrics: MSE, MAE, R²
  - Fix: removed deprecated `verbose=False` from scheduler (PyTorch 2.4+)

## Phase 4 — Visualisation (Task 14) ✅
- [x] `visualise.py`
  - Loss curve (train + validation per epoch) → `plots/task14_loss.png`
  - Metrics table to stdout
  - 5-panel sample plot (noisy composite / predicted / clean) → `plots/task14_samples.png`

## Phase 5 — Integration & Polish ✅
- [x] `main.py` wires all tasks with `perf_counter` timing
- [x] WSL venv issue resolved (must create from inside WSL)
- [x] All documents updated to v1.1.0
- [x] README extended with plot images and explanations

---

## Iteration Log

| Version | Change | Reason |
|---------|--------|--------|
| v1.0.0 | Initial release: window=10, hidden=64, epochs=50 | Baseline |
| v1.0.1 | Fix `use_line_collection` in `sampling.py` | Matplotlib 3.7 compatibility |
| v1.0.2 | Fix `verbose` in `ReduceLROnPlateau` | PyTorch 2.4 compatibility |
| v1.1.0 | Window 10→100, hidden 64→128, epochs 50→150, filter-conditioned h₀/c₀, 200-sample prefix | Poor prediction quality: smoothed mean instead of target signal; start-of-window divergence |

---

## Risk Register

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| PyTorch API changes break training code | Low | Pin versions in `requirements.txt` |
| Multiprocessing overhead on WSL | Low | Pool size = min(n_signals, cpu_count−1) |
| Memory blow-up with large dataset | Low | Store as float32 numpy arrays (~300 MB for 8000×300) |
| matplotlib X-display errors on WSL | Mitigated | `matplotlib.use("Agg")` at top of all plot modules |
| LSTM transient at window start | Fixed | 200-sample prefix warm-up |
| Network predicts mean instead of signal | Fixed | filter-conditioned h₀/c₀, window=100, hidden=128 |

---

## Dependencies

| Library | Version | Reason |
|---------|---------|--------|
| `numpy` | ≥1.24 | Signal math, array operations |
| `matplotlib` | ≥3.7 | All plots |
| `torch` | ≥2.0 | LSTM model and training |
| `scikit-learn` | ≥1.3 | Train/test split, R² metric |
| `tqdm` | ≥4.65 | Progress bars in training loop |
