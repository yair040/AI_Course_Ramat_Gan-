# Product Requirements Document (PRD)
## AutoEncoder Image Processing — Cats & Dogs

**Author:** Yair Levi  
**Project:** AutoEncoder  
**Location:** `C:\Users\yair0\AI_continue\Lesson42_AutoEncoder\AutoEncoder\`  
**Platform:** Python on WSL (Windows Subsystem for Linux) in a virtual environment  

---

## 1. Overview

This project implements a configurable Convolutional AutoEncoder in Python that trains on grayscale or RGB images of cats and dogs. The program is structured as a Python package, invoked via a task runner, and supports rich hyperparameter control. Cross-domain experiments (cats encoder → dogs decoder, and vice versa) visualize how latent spaces transfer across domains.

---

## 2. Goals

| # | Goal |
|---|------|
| G1 | Resize all images to a consistent resolution suitable for the encoder input |
| G2 | Train a cats AutoEncoder and evaluate reconstruction quality |
| G3 | Train a dogs AutoEncoder and evaluate reconstruction quality |
| G4 | Perform cross-domain inference: cats encoder + dogs decoder |
| G5 | Perform cross-domain inference: dogs encoder + cats decoder |
| G6 | Log every step with a rotating ring-buffer log strategy |
| G7 | Expose all key settings as hyperparameters |

---

## 3. Scope

### In Scope
- Image preprocessing (resize, normalize)
- Convolutional AutoEncoder training (separate for cats and dogs)
- Cross-domain encoder/decoder merging
- Sample visualization (input vs reconstruction)
- Hyperparameter configuration via a config file or CLI
- Rotating file logging (20 files × 16 MB)
- Multiprocessing for image preprocessing
- Execution time measurement for each task

### Out of Scope
- Web or REST API interface
- GPU cluster scheduling
- Real-time inference server
- Deployment / containerization

---

## 4. Directory Structure

```
AutoEncoder/                      ← project root (current folder)
├── autoencoder/                  ← Python package
│   ├── __init__.py
│   ├── config.py                 ← hyperparameters & settings
│   ├── preprocessing.py          ← Task 1: image resizing
│   ├── train_cats.py             ← Task 2: cats autoencoder
│   ├── train_dogs.py             ← Task 3: dogs autoencoder
│   ├── cross_cats_enc_dogs_dec.py← Task 4: cats-enc + dogs-dec
│   ├── cross_dogs_enc_cats_dec.py← Task 5: dogs-enc + cats-dec
│   ├── model.py                  ← shared AutoEncoder model definition
│   ├── dataset.py                ← dataset loader utilities
│   └── logger.py                 ← ring-buffer logging setup
├── tasks.py                      ← main task dispatcher
├── requirements.txt
├── Claude.md
├── planning.md
├── tasks.md
├── PRD.md
├── log/                          ← rotating log files (auto-created)
├── cats/                         ← 1500 cat images (input)
├── dogs/                         ← 1500 dog images (input)
└── output/                       ← resized images, saved models, plots
    ├── cats_resized/
    ├── dogs_resized/
    ├── models/
    └── plots/
```

Virtual environment location: `../../venv/` (relative to project root)

---

## 5. Hyperparameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `image_size` | Target (H, W) for resizing input images | `(128, 128)` |
| `code_size` | Bottleneck (latent) dimension | `128` |
| `num_layers` | Number of conv layers in encoder (mirrored in decoder) | `3` |
| `nodes_per_layer` | Base channel count; halved each encoder layer | `64` |
| `loss_function` | `mse`, `bce`, or `ssim` | `mse` |
| `epochs` | Training epochs | `30` |
| `batch_size` | Mini-batch size | `32` |
| `learning_rate` | Adam optimizer LR | `1e-3` |
| `num_workers` | Multiprocessing workers for DataLoader & preprocessing | `4` |
| `sample_count` | Number of samples shown per visualization | `8` |

All hyperparameters are defined in `autoencoder/config.py` and can be overridden via environment variables or CLI flags passed to `tasks.py`.

---

## 6. Tasks

### Task 1 — Preprocess Images
- Resize all images in `cats/` and `dogs/` to `image_size`
- Save resized images to `output/cats_resized/` and `output/dogs_resized/`
- Use multiprocessing (Pool) for parallel resizing
- Log start, progress (every 100 images), and completion
- Report wall-clock time

### Task 2 — Train Cats AutoEncoder
- Load resized cats images
- Instantiate `AutoEncoder` model with configured hyperparameters
- Train for `epochs` epochs, logging loss per epoch
- Save model to `output/models/cats_autoencoder.pth`
- Display `sample_count` input/reconstruction pairs as a matplotlib figure
- Report training time

### Task 3 — Train Dogs AutoEncoder
- Same as Task 2 but for dogs images
- Save model to `output/models/dogs_autoencoder.pth`

### Task 4 — Cats Encoder + Dogs Decoder
- Load cats encoder weights from Task 2
- Load dogs decoder weights from Task 3
- Run inference on a sample of dogs images → show input vs. output
- Run inference on a sample of cats images → show input vs. output
- Save visualization plots to `output/plots/`

### Task 5 — Dogs Encoder + Cats Decoder
- Load dogs encoder weights from Task 3
- Load cats decoder weights from Task 2
- Run inference on a sample of cats images → show input vs. output
- Run inference on a sample of dogs images → show input vs. output
- Save visualization plots to `output/plots/`

---

## 7. Logging Requirements

| Requirement | Value |
|-------------|-------|
| Minimum level | `INFO` |
| Strategy | Ring buffer |
| Max files | 20 |
| Max file size | 16 MB |
| Rotation | When last file is full, overwrite first file (circular) |
| Log directory | `log/` (relative to project root) |
| Format | `%(asctime)s [%(levelname)s] %(name)s: %(message)s` |

Implementation: Python `logging.handlers.RotatingFileHandler` with `maxBytes=16*1024*1024` and `backupCount=19` achieves the 20-file ring buffer behavior.

---

## 8. Non-Functional Requirements

| Area | Requirement |
|------|-------------|
| Performance | Preprocessing must use multiprocessing |
| Portability | All paths relative; no hard-coded absolute paths |
| Modularity | Each Python file ≤ 150 lines |
| Packaging | Valid Python package with `__init__.py` |
| Reproducibility | Random seed configurable via `config.py` |
| Platform | WSL Ubuntu with Python 3.10+ |

---

## 9. Dependencies (requirements.txt)

| Package | Purpose |
|---------|---------|
| `torch` | Deep learning framework |
| `torchvision` | Image transforms & datasets |
| `Pillow` | Image I/O and resizing |
| `matplotlib` | Visualization |
| `numpy` | Array operations |
| `tqdm` | Progress bars |

---

## 10. Acceptance Criteria

- [ ] All 5 tasks run end-to-end without errors
- [ ] Resized images match configured `image_size`
- [ ] Both autoencoders produce visually recognizable reconstructions
- [ ] Cross-domain outputs show meaningful (if imperfect) reconstructions
- [ ] Log directory contains rotating log files
- [ ] Execution times are logged and printed for each task
- [ ] No absolute paths appear anywhere in the codebase
