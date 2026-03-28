# Tasks — AutoEncoder Project

**Author:** Yair Levi

---

## Task Overview

| # | Name | Module | CLI |
|---|------|--------|-----|
| 1 | Preprocess Images | `autoencoder/preprocessing.py` | `python tasks.py --task 1` |
| 2 | Train Cats AutoEncoder | `autoencoder/train_cats.py` | `python tasks.py --task 2` |
| 3 | Train Dogs AutoEncoder | `autoencoder/train_dogs.py` | `python tasks.py --task 3` |
| 4 | Cats Enc + Dogs Dec | `autoencoder/cross_cats_enc_dogs_dec.py` | `python tasks.py --task 4` |
| 5 | Dogs Enc + Cats Dec | `autoencoder/cross_dogs_enc_cats_dec.py` | `python tasks.py --task 5` |
| all | Run All Tasks | `tasks.py` | `python tasks.py --task all` |

---

## Task 1 — Preprocess Images

**Goal:** Resize all cats and dogs images to the configured `image_size`.

**Steps:**
1. Read all image file paths from `cats/` and `dogs/`
2. Spawn a multiprocessing Pool
3. Each worker: open image → convert to RGB → resize → save to `output/cats_resized/` or `output/dogs_resized/`
4. Log counts and elapsed time

**Inputs:** `cats/*.jpg` (or png/jpeg), `dogs/*.jpg`  
**Outputs:** `output/cats_resized/*.jpg`, `output/dogs_resized/*.jpg`  
**Timing:** Wall-clock from start to finish of all workers  

**Status:** ⬜ Not started

---

## Task 2 — Train Cats AutoEncoder

**Goal:** Train an AutoEncoder on cats images and visualize reconstructions.

**Steps:**
1. Load resized cats images from `output/cats_resized/`
2. Build `AutoEncoder(config)` model
3. Train for `config.EPOCHS` epochs using `config.LOSS_FUNCTION`
4. Log epoch loss (INFO level)
5. Save model to `output/models/cats_autoencoder.pth`
6. Display `config.SAMPLE_COUNT` input/output pairs
7. Save plot to `output/plots/cats_reconstruction.png`
8. Log and print training time

**Inputs:** `output/cats_resized/`  
**Outputs:** `output/models/cats_autoencoder.pth`, `output/plots/cats_reconstruction.png`  
**Timing:** Training loop wall-clock time  

**Status:** ⬜ Not started

---

## Task 3 — Train Dogs AutoEncoder

**Goal:** Same as Task 2 but for dogs.

**Steps:**
1. Load resized dogs images from `output/dogs_resized/`
2. Build `AutoEncoder(config)` model
3. Train and save to `output/models/dogs_autoencoder.pth`
4. Save plot to `output/plots/dogs_reconstruction.png`
5. Log and print training time

**Inputs:** `output/dogs_resized/`  
**Outputs:** `output/models/dogs_autoencoder.pth`, `output/plots/dogs_reconstruction.png`  
**Timing:** Training loop wall-clock time  

**Status:** ⬜ Not started

---

## Task 4 — Cats Encoder + Dogs Decoder

**Goal:** Merge the encoder from the cats model with the decoder from the dogs model and run cross-domain inference.

**Steps:**
1. Load `Encoder` weights from `output/models/cats_autoencoder.pth`
2. Load `Decoder` weights from `output/models/dogs_autoencoder.pth`
3. Combine into a hybrid forward pass (no re-training)
4. Run inference on `config.SAMPLE_COUNT` dogs images → save plot
5. Run inference on `config.SAMPLE_COUNT` cats images → save plot
6. Save plots to `output/plots/task4_dogs_input.png` and `output/plots/task4_cats_input.png`

**Prerequisite:** Tasks 2 and 3 must be complete  
**Status:** ⬜ Not started

---

## Task 5 — Dogs Encoder + Cats Decoder

**Goal:** Merge the encoder from the dogs model with the decoder from the cats model.

**Steps:**
1. Load `Encoder` weights from `output/models/dogs_autoencoder.pth`
2. Load `Decoder` weights from `output/models/cats_autoencoder.pth`
3. Combine into a hybrid forward pass (no re-training)
4. Run inference on `config.SAMPLE_COUNT` cats images → save plot
5. Run inference on `config.SAMPLE_COUNT` dogs images → save plot
6. Save plots to `output/plots/task5_cats_input.png` and `output/plots/task5_dogs_input.png`

**Prerequisite:** Tasks 2 and 3 must be complete  
**Status:** ⬜ Not started

---

## Hyperparameter Tuning Guide

| Symptom | Try |
|---------|-----|
| Reconstruction too blurry | Increase `code_size`, add more layers |
| Model overfits (train loss << val loss) | Decrease `code_size`, reduce `num_layers` |
| Training too slow | Reduce `image_size`, `batch_size`, `epochs` |
| Cross-domain output is pure noise | Try a larger `code_size` to capture more general features |
| Loss NaN | Lower `learning_rate`, check image normalization |

---

## Status Legend

| Symbol | Meaning |
|--------|---------|
| ⬜ | Not started |
| 🔄 | In progress |
| ✅ | Complete |
| ❌ | Blocked |
