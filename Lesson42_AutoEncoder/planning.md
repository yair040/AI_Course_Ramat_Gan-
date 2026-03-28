# Planning — AutoEncoder Project

**Author:** Yair Levi

---

## Phases

### Phase 0 — Environment Setup
- [ ] Create virtual environment at `../../venv/`
- [ ] Install dependencies from `requirements.txt`
- [ ] Verify WSL Python version ≥ 3.10
- [ ] Confirm `cats/` and `dogs/` folders each contain ~1500 images

### Phase 1 — Package Skeleton
- [ ] Create `autoencoder/__init__.py`
- [ ] Create `autoencoder/config.py` with all hyperparameters
- [ ] Create `autoencoder/logger.py` with ring-buffer handler
- [ ] Create `tasks.py` dispatcher
- [ ] Smoke-test: `python tasks.py --help`

### Phase 2 — Image Preprocessing (Task 1)
- [ ] Implement `dataset.py` (path helpers, image listing)
- [ ] Implement `preprocessing.py` (multiprocessing Pool resize)
- [ ] Create `output/cats_resized/` and `output/dogs_resized/`
- [ ] Validate resized image dimensions
- [ ] Log and print elapsed time

### Phase 3 — Model Definition
- [ ] Implement `Encoder` in `model.py` (dynamic layers from config)
- [ ] Implement `Decoder` in `model.py` (mirrored architecture)
- [ ] Implement `AutoEncoder` combining both
- [ ] Unit test: forward pass with a random tensor

### Phase 4 — Training (Tasks 2 & 3)
- [ ] Implement `train_cats.py` — training loop, loss logging, model save
- [ ] Implement `train_dogs.py` — same for dogs
- [ ] Implement visualization: show N input/output sample pairs
- [ ] Save plots to `output/plots/`
- [ ] Log and print training time

### Phase 5 — Cross-Domain Inference (Tasks 4 & 5)
- [ ] Implement `cross_cats_enc_dogs_dec.py`
  - Load cats encoder + dogs decoder
  - Run on dog samples → plot
  - Run on cat samples → plot
- [ ] Implement `cross_dogs_enc_cats_dec.py`
  - Load dogs encoder + cats decoder
  - Run on cat samples → plot
  - Run on dog samples → plot

### Phase 6 — Integration & QA
- [ ] Run full pipeline: `python tasks.py --task all`
- [ ] Check log files in `log/` directory
- [ ] Verify rotation behavior (no more than 20 files)
- [ ] Review output plots for visual sanity

---

## Risk Register

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| PyTorch not available on WSL CPU | Medium | Fall back to CPU (`config.DEVICE`) |
| Images have inconsistent formats (PNG/JPG/BMP) | High | Use Pillow `.convert("RGB")` before resize |
| Memory overflow with large batch | Medium | Reduce `batch_size` in config |
| Cross-domain outputs look like noise | High (expected) | Document as expected behaviour for very different latent spaces |
| Log directory not writable | Low | Auto-create with `mkdir(parents=True)` |

---

## Timeline Estimate

| Phase | Effort |
|-------|--------|
| 0 — Setup | 0.5 h |
| 1 — Skeleton | 1 h |
| 2 — Preprocessing | 1 h |
| 3 — Model | 1.5 h |
| 4 — Training | 2 h |
| 5 — Cross-domain | 1.5 h |
| 6 — QA | 1 h |
| **Total** | **~8.5 h** |

---

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| Convolutional AutoEncoder (not fully-connected) | Images need spatial feature extraction |
| Separate encoder/decoder weights per species | Enables cross-domain swap without re-training |
| `RotatingFileHandler` for ring buffer | Standard library; 20 files × 16 MB = 320 MB max log size |
| Multiprocessing Pool for resize | PIL resize is CPU-bound; embarrassingly parallel |
| `pathlib.Path` throughout | Cross-platform, WSL-safe, readable |
| Adam optimizer default | Adaptive LR; good default for autoencoders |
| MSE loss default | Standard reconstruction loss; BCE suits binary images; SSIM suits perceptual quality |
