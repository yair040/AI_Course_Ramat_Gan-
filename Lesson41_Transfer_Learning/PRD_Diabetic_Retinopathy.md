# Product Requirements Document
## Diabetic Retinopathy Risk Assessment System
### AI-Powered Eye Image Classification using Transfer Learning

**Author:** Yair Levi
**Version:** 1.0
**Platform:** Google Colab · **Framework:** PyTorch · **Model:** ResNet-50

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Dataset Description](#2-dataset-description)
3. [System Architecture](#3-system-architecture)
4. [Preprocessing Requirements](#4-preprocessing-requirements)
5. [Model Architecture](#5-model-architecture)
6. [Training Experiments](#6-training-experiments)
7. [Evaluation & Metrics](#7-evaluation--metrics)
8. [Performance Timing](#8-performance-timing)
9. [Google Colab Notebook Structure](#9-google-colab-notebook-structure)
10. [Google Drive Storage Management](#10-google-drive-storage-management)
11. [Acceptance Criteria](#11-acceptance-criteria)
12. [Risks and Mitigations](#12-risks-and-mitigations)
13. [Glossary](#13-glossary)

---

## 1. Project Overview

Diabetic Retinopathy (DR) is one of the leading causes of blindness worldwide. Early detection through automated analysis of retinal fundus images can dramatically improve patient outcomes by enabling timely medical intervention. This project delivers an end-to-end deep learning pipeline on Google Colab that classifies retinal images into five severity levels of diabetic retinopathy.

The system leverages Transfer Learning with a ResNet-50 backbone pre-trained on ImageNet, applies domain-specific preprocessing and data augmentation, and provides comprehensive performance evaluation across three training strategies of increasing complexity.

### 1.1 Project Goals

- Automate the classification of retinal fundus images into DR severity levels.
- Achieve high diagnostic accuracy suitable for clinical decision support.
- Provide a reproducible, well-documented Google Colab notebook.
- Measure and report performance at every pipeline stage.
- Enable user control over model hyper-parameters and training strategies.

### 1.2 Stakeholders

| Stakeholder | Role | Interest |
|---|---|---|
| Yair Levi | Author / Developer | Deliver working classification system |
| Ophthalmologists | Clinical Users | Accurate early diagnosis aid |
| Data Scientists | Technical Reviewers | Model performance & reproducibility |

---

## 2. Dataset Description

The dataset is sourced from the Kaggle APTOS 2019 Blindness Detection competition. It consists of high-resolution retinal fundus photographs captured under varying imaging conditions. Each image is labeled by a clinician with a severity score from 0 to 4.

- **Source:** https://www.kaggle.com/competitions/aptos2019-blindness-detection/data
- **Storage:** Google Drive under the folder `Diabetic_Retinopathy/`
- **Images:** PNG files located at `Diabetic_Retinopathy/images/`
- **Labels:** CSV file at `Diabetic_Retinopathy/labels.csv`

### 2.1 Label File Structure (labels.csv)

| Column | Description |
|---|---|
| `id_code` | Image filename without the `.png` extension (e.g., `000c1434d8d7`) |
| `diagnosis` | Severity class integer: 0, 1, 2, 3, or 4 |

### 2.2 Class Definitions

| Class | Label | Clinical Description |
|---|---|---|
| 0 | No DR | No signs of diabetic retinopathy. Healthy retina. |
| 1 | Mild | Microaneurysms only. Earliest detectable stage. |
| 2 | Moderate | More than just microaneurysms. Some vision threat. |
| 3 | Severe | Extensive hemorrhages. High risk of progression. |
| 4 | Proliferative DR | New abnormal blood vessel growth. Sight-threatening. |

### 2.3 Class Distribution (Original Dataset)

| Class | Count | Target (Balanced) | Action Required |
|---|---|---|---|
| 0 (No DR) | 1,806 | ~1,000 | Downsample (remove ~806) |
| 1 (Mild) | 371 | ~1,000 | Augment (generate ~629) |
| 2 (Moderate) | 1,000 | ~1,000 | Keep as is |
| 3 (Severe) | 194 | ~1,000 | Augment (generate ~806) |
| 4 (Proliferative) | 1,180 | ~1,000 | Downsample (remove ~180) |

---

## 3. System Architecture

### 3.1 Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| Runtime | Google Colab (GPU) | Cloud-based training environment |
| Language | Python 3.x | Primary programming language |
| Deep Learning | PyTorch | Model definition & training |
| Base Model | ResNet-50 (ImageNet) | Transfer learning backbone |
| Image Processing | PIL / OpenCV | Preprocessing pipeline |
| Data Handling | Pandas / NumPy | Dataset management |
| Visualization | Matplotlib / Seaborn | Metrics & sample display |
| Metrics | Scikit-learn | Confusion matrix, precision, recall |
| Storage | Google Drive | Dataset & model persistence |

### 3.2 High-Level Pipeline

1. Mount Google Drive and validate dataset access.
2. Display one sample image per category for visual sanity check.
3. Balance preprocessing: downsample over-represented classes, augment under-represented classes.
4. Resolution preprocessing: resize all images to 224×224 pixels.
5. Split dataset: 80% training, 20% test.
6. Load ResNet-50 with ImageNet weights.
7. Run Experiment 1: Evaluate pre-trained model with no fine-tuning.
8. Run Experiment 2: Fine-tune last fully-connected layer only.
9. Run Experiment 3: Unfreeze deeper layers and fine-tune.
10. Report and compare metrics across all experiments.

---

## 4. Preprocessing Requirements

### 4.1 Preprocessing Order and Rationale

Preprocessing is performed in the following order for optimal speed and memory efficiency on Google Colab:

1. **Balance Preprocessing FIRST** — Balancing is performed on the original full-resolution images. By reducing the dataset size before resizing, we minimize the total number of resize operations and avoid storing augmented high-resolution images in memory unnecessarily.

2. **Resolution Decrease SECOND** — After balancing, all selected/generated images are resized to 224×224. Working on a smaller, balanced set means this step is faster and the resulting dataset has a predictable, manageable footprint.

### 4.2 Balance Image Preprocessing

#### 4.2.1 Downsampling (Classes 0 and 4)

- Class 0: Randomly select 1,000 images from 1,806. Discard the rest.
- Class 4: Randomly select 1,000 images from 1,180. Discard the rest.
- Use a fixed random seed for reproducibility.

#### 4.2.2 Augmentation (Classes 1 and 3)

- Class 1 (371 images): Generate ~629 additional images to reach ~1,000.
- Class 3 (194 images): Generate ~806 additional images to reach ~1,000.
- Class 2 (1,000 images): No action required.

Augmentation transforms to apply (randomly combined per generated image):

- Horizontal flip
- Vertical flip
- Random rotation (up to ±15 degrees)
- Brightness and contrast jitter (±10%)
- Gaussian blur (optional, mild)

### 4.3 Decrease Resolution Preprocessing

- Target resolution: **224×224 pixels** (required input size for ResNet-50).
- Resize using high-quality Lanczos resampling.
- Apply normalization using ImageNet mean and std: `mean=[0.485, 0.456, 0.406]`, `std=[0.229, 0.224, 0.225]`.
- All timing measurements are recorded and displayed for both preprocessing steps.

---

## 5. Model Architecture

### 5.1 Base Model: ResNet-50

ResNet-50 is a 50-layer deep residual network pre-trained on 1.28 million ImageNet images across 1,000 categories. Its residual connections address the vanishing gradient problem, enabling effective training of deep networks. The final fully-connected layer is replaced to output 5 classes instead of 1,000.

| Property | Value |
|---|---|
| Architecture | ResNet-50 |
| Pre-training | ImageNet (1.28M images, 1,000 classes) |
| Input size | 224 × 224 × 3 (RGB) |
| Output classes | 5 (DR severity levels 0–4) |
| Optimizer | Adam |
| Loss function | Cross-Entropy Loss |
| Batch Normalization | User-configurable (on/off via parameter) |

**Custom classification head:**
```
Linear(2048 → 512) → [BatchNorm1d(512)] → ReLU → Dropout(0.5) → Linear(512 → 5)
```
`BatchNorm1d` is included only when `USE_BATCH_NORM = True`.

### 5.2 User-Configurable Parameters

| Parameter | Default | Description |
|---|---|---|
| `USE_BATCH_NORM` | `True` | Enable/disable batch normalization layers |
| `LEARNING_RATE` | `1e-4` | Adam optimizer learning rate (Experiment 2) |
| `LR_EXP3` | `1e-5` | Reduced learning rate for Experiment 3 |
| `BATCH_SIZE` | `32` | Training mini-batch size |
| `NUM_EPOCHS` | `10` | Number of training epochs per experiment |
| `RANDOM_SEED` | `42` | Seed for reproducibility |
| `UNFREEZE_LAYERS` | `['layer4', 'fc']` | ResNet block(s) to unfreeze in Experiment 3 |

---

## 6. Training Experiments

### 6.1 Experiment 1: Zero-Shot Evaluation (No Training)

**Purpose:** Establish a baseline by evaluating the pre-trained ResNet-50 with its original ImageNet weights and a randomly initialized classification head. This measures how well the generic feature representations transfer to retinal image classification without any domain adaptation.

- Load ResNet-50 with ImageNet weights.
- Replace the final FC layer with a 5-class output layer (randomly initialized).
- Run inference on the full test set (20% split) without any gradient updates.
- Record all evaluation metrics.

### 6.2 Experiment 2: Fine-Tune Last FC Layer Only

**Purpose:** Freeze all convolutional layers and train only the new 5-class fully-connected layer. This is the fastest fine-tuning approach and often achieves strong results by adapting the classification head while preserving the learned feature extractor.

- Freeze all layers: set `requires_grad = False` for all parameters.
- Unfreeze the final FC layer: set `requires_grad = True` for `fc` parameters.
- Train for `NUM_EPOCHS` epochs using Adam optimizer.
- Evaluate on test set and compare to Experiment 1.
- Save model checkpoint to Google Drive.

### 6.3 Experiment 3: Partial Unfreeze (Deeper Layers)

**Purpose:** Allow gradient flow through deeper convolutional blocks (e.g., `layer4` of ResNet-50), enabling domain-specific feature adaptation. This typically improves accuracy at the cost of longer training time and risk of overfitting.

- Starting from Experiment 2 model weights (warm start).
- Unfreeze the configured `UNFREEZE_LAYERS` (default: `layer4` and the `fc` layer).
- Train with a lower learning rate (`LR_EXP3`) to prevent catastrophic forgetting.
- Evaluate on test set and compare to both previous experiments.
- Save model to Google Drive if sufficient disk space is available (checked automatically).

**ResNet-50 layer structure:**
```
conv1 → bn1 → relu → maxpool → layer1 → layer2 → layer3 → layer4 → avgpool → fc
```

---

## 7. Evaluation & Metrics

### 7.1 Performance Metrics

All three experiments report the following metrics on the test set:

| Metric | Description |
|---|---|
| Overall Accuracy | Fraction of correctly classified images across all 5 classes |
| Precision (per class) | TP / (TP + FP) — how many predicted positives are correct |
| Recall (per class) | TP / (TP + FN) — how many actual positives are captured |
| F1-Score (per class) | Harmonic mean of precision and recall |
| Macro F1 | Unweighted average F1 across all classes |
| Confusion Matrix | 5×5 matrix visualizing true vs. predicted class distributions |
| Classification Report | Full `sklearn.classification_report` output |

### 7.2 Comparative Analysis

After all three experiments complete, a side-by-side comparison table and bar charts are displayed, showing accuracy, macro F1, and training time for each experiment. This enables clear identification of the best-performing strategy.

### 7.3 Visual Outputs

- One sample image from each of the 5 categories displayed for human comparison.
- Confusion matrix heatmap (Seaborn) for each experiment.
- Training loss and accuracy curves (Experiments 2 and 3).
- Per-class precision/recall bar chart.
- Comparative summary table across all three experiments.

---

## 8. Performance Timing

The elapsed time is recorded and displayed for every major pipeline stage to support performance profiling and reproducibility reporting. Timing is implemented using Python's `time` module with clear formatted output.

| Stage | Measurement |
|---|---|
| Balance Preprocessing | Wall-clock time for downsample + augmentation |
| Resolution Preprocessing | Wall-clock time for all image resizes |
| Dataset Split | Time to build train/test DataLoaders |
| Experiment 1 Inference | Total inference time on test set |
| Experiment 2 Training | Total training + evaluation time |
| Experiment 3 Training | Total training + evaluation time |

---

## 9. Google Colab Notebook Structure

The notebook is organized into clearly labeled sections. Each code cell is preceded by a Markdown cell with a human-readable explanation of the purpose, expected inputs, and outputs of that section.

| Section | Title | Description |
|---|---|---|
| 1 | Setup & Imports | Install libraries, import modules, set config parameters |
| 2 | Mount Google Drive | Connect to Drive and verify dataset paths |
| 3 | Load Labels | Parse `labels.csv` and display class distribution |
| 4 | Visual Sample Display | Show one image per category for visual comparison |
| 5 | Balance Preprocessing | Downsample and augment to ~1,000 per class |
| 6 | Resolution Preprocessing | Resize all images to 224×224 |
| 7 | Dataset Split & DataLoaders | 80/20 split, normalization, PyTorch DataLoaders |
| 8 | Model Setup | Load ResNet-50, modify FC layer, batch norm config |
| 9 | Experiment 1: Zero-Shot | Evaluate without training; report baseline metrics |
| 10 | Experiment 2: FC Fine-Tune | Train last layer; evaluate; save model |
| 11 | Experiment 3: Deep Fine-Tune | Unfreeze deeper layers; train; compare; save model |
| 12 | Results Comparison | Side-by-side table and charts across all experiments |

---

## 10. Google Drive Storage Management

All persistent artifacts are saved to Google Drive. Before saving Experiment 3, available disk space is checked automatically. If insufficient space is detected (less than 500 MB free), the save is skipped with a warning.

| Artifact | Path |
|---|---|
| Experiment 2 model | `/Diabetic_Retinopathy/models/exp2_fc_finetune.pth` |
| Experiment 3 model | `/Diabetic_Retinopathy/models/exp3_deep_finetune.pth` *(conditional)* |
| Preprocessed image cache | `/Diabetic_Retinopathy/preprocessed/` *(optional)* |

---

## 11. Acceptance Criteria

| Requirement | Criterion |
|---|---|
| Dataset loads correctly | All 5 classes detected; label CSV parsed without error |
| Balanced dataset | Each class has 950–1,050 images after preprocessing |
| Resolution preprocessing | All images are exactly 224×224 after resize |
| Timing displayed | Elapsed time shown for all 6 timed stages |
| Sample images shown | Exactly 1 image per class displayed with label |
| Experiment 1 runs | Metrics computed without any training |
| Experiment 2 trains | Model saved; accuracy improves over Experiment 1 |
| Experiment 3 trains | Model saved if space available; results reported |
| Batch norm control | `USE_BATCH_NORM` flag correctly enables/disables BN |
| All metrics reported | Confusion matrix, accuracy, precision, recall, F1 per experiment |

---

## 12. Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Colab session timeout | Loss of preprocessed data | Save preprocessed cache to Drive after each step |
| GPU memory (OOM) | Training crash | Configurable batch size; clear cache between experiments |
| Class imbalance (residual) | Biased predictions | Balanced dataset + class-weighted metrics reported |
| Google Drive space | Model save failure | Auto-check space before saving Experiment 3 |
| Augmentation overfitting | Poor generalization | Mild augmentation transforms; validation monitoring |

---

## 13. Glossary

| Term | Definition |
|---|---|
| DR | Diabetic Retinopathy — eye disease caused by diabetes damaging retinal blood vessels |
| Transfer Learning | Reusing a model trained on one task as the starting point for a model on a different task |
| ResNet-50 | 50-layer Residual Network with skip connections; pre-trained on ImageNet |
| Fine-Tuning | Continuing training of a pre-trained model on a new dataset |
| Augmentation | Generating new training images via transformations (flip, rotate, etc.) |
| Batch Normalization | Technique normalizing layer inputs during training to stabilize learning |
| Adam | Adaptive Moment Estimation — gradient-based optimizer combining RMSProp and momentum |
| Confusion Matrix | Table showing predicted vs. actual class counts; visualizes classification errors |
| Macro F1 | Unweighted average of per-class F1 scores; treats all classes equally |

---

*Document prepared by Yair Levi · Diabetic Retinopathy Risk Assessment · Version 1.0*
