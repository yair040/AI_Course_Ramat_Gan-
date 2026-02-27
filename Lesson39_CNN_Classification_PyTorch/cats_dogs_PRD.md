# Product Requirements Document
# Cat vs. Dog Image Classifier
### CNN Binary Classification with PyTorch — Google Colab Notebook

---

| Field | Value |
|---|---|
| **Author** | Yair Levi |
| **Version** | 1.0 |
| **Date** | February 2026 |
| **Platform** | Google Colab (Python 3.x + PyTorch) |
| **Status** | Draft |
| **Classification** | Internal / Educational |

---

## Table of Contents

1. [Overview](#1-overview)
2. [Objectives](#2-objectives)
3. [Scope](#3-scope)
4. [Data Requirements](#4-data-requirements)
5. [Preprocessing Pipeline](#5-preprocessing-pipeline)
6. [Network Architecture (CNN)](#6-network-architecture-cnn)
7. [Training (Fit)](#7-training-fit)
8. [Test and Evaluation](#8-test-and-evaluation)
9. [Improvement Experiments](#9-improvement-experiments)
10. [Functional Requirements](#10-functional-requirements)
11. [Non-Functional Requirements](#11-non-functional-requirements)
12. [Deliverables](#12-deliverables)
13. [Glossary](#13-glossary)

---

## 1. Overview

This document defines the requirements, architecture, and implementation plan for a binary image classification system that distinguishes between photographs of cats and dogs. The solution is built using PyTorch and is designed to run as an interactive notebook in Google Colab, making it accessible without requiring a local GPU or complex environment setup.

The project covers the complete machine learning pipeline: data loading and exploration, preprocessing, CNN model design, training, evaluation, and iterative improvement. Each step is annotated with explanatory comments so the notebook serves as both a working program and an educational resource.

---

## 2. Objectives

- Build a CNN-based binary classifier in PyTorch that accurately identifies whether an input image contains a cat or a dog.
- Provide a fully runnable Google Colab notebook with step-by-step explanations before each code section.
- Demonstrate the complete ML workflow: data ingestion, preprocessing, model design, training, evaluation, and improvement.
- Allow the user to control key hyperparameters (number of layers, neurons per layer, number of kernels, learning rate, epochs).
- Visualize training progress, model performance, and failure analysis through graphs and confusion matrices.

---

## 3. Scope

### 3.1 In Scope

- Loading 1,500 cat images and 1,500 dog images from local folders (`./cats`, `./dogs`).
- Visualization of sample images from both classes.
- Preprocessing pipeline: resize, normalize, one-hot encode labels.
- CNN architecture definition with configurable parameters.
- Training with Adam optimizer and Cross-Entropy loss.
- Evaluation on a held-out test set with confusion matrix, accuracy, and sample predictions.
- Manual improvement experiments: deeper network, wider network, modified kernels.

### 3.2 Out of Scope

- Real-time webcam classification.
- Multi-class classification beyond cats and dogs.
- Model deployment or serving as an API.
- Data augmentation beyond basic resizing and normalization (unless added as an improvement).

---

## 4. Data Requirements

### 4.1 Dataset

Source: Images randomly sampled from the Kaggle Dogs vs. Cats dataset and stored locally.

| Field | Value |
|---|---|
| **Cats folder** | `./cats/` — 1,500 JPEG/PNG images of cats |
| **Dogs folder** | `./dogs/` — 1,500 JPEG/PNG images of dogs |
| **Image type** | Color (RGB), varying resolutions |
| **Total images** | 3,000 (1,500 per class) |

### 4.2 Train / Validation Split

The split is performed randomly at load time using PyTorch's `Subset` and `random_split` utilities.

| Split | Size |
|---|---|
| **Training set** | 1,000 cat images + 1,000 dog images = 2,000 total |
| **Validation / Test set** | 500 cat images + 500 dog images = 1,000 total |
| **Split ratio** | ~67% training, ~33% test per class |
| **Random seed** | Configurable (default: 42) for reproducibility |

### 4.3 Sample Visualization

Before training, the notebook displays a grid of sample images (e.g., 5 cats and 5 dogs) drawn randomly from the full dataset, using Matplotlib. This helps the user visually inspect data quality and class variety.

---

## 5. Preprocessing Pipeline

All preprocessing transforms are defined as a `torchvision.transforms.Compose` pipeline and applied at data-load time via PyTorch's `ImageFolder` and `DataLoader`.

### 5.1 Resize

All images are resized to **150 × 150 pixels**. This provides enough spatial resolution for a CNN to learn discriminative features while keeping training computationally feasible on Colab's free GPU tier.

```
Transform: transforms.Resize((150, 150))
```

### 5.2 Normalization

Pixel values are first converted to floating-point tensors in the range `[0, 1]` by `transforms.ToTensor()`. They are then further normalized to have zero mean and unit variance using the ImageNet statistics (`mean=[0.485, 0.456, 0.406]`, `std=[0.229, 0.224, 0.225]`).

Normalization is important because: (a) it accelerates gradient descent convergence by ensuring all input features share the same scale, and (b) it reduces the risk of vanishing or exploding gradients in the early convolutional layers.

```
Transform: transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
```

### 5.3 Labels and One-Hot Encoding

Labels are derived automatically from the folder structure: images inside `./cats` receive label `0` and images inside `./dogs` receive label `1`. PyTorch's `ImageFolder` handles this mapping.

For the Cross-Entropy loss function used in this project, PyTorch's `nn.CrossEntropyLoss` internally combines a `LogSoftmax` and `NLLLoss` and expects raw integer class indices (not explicit one-hot vectors). However, one-hot representations are constructed and shown in the notebook for educational purposes, demonstrating what the target distribution looks like from the network's perspective.

---

## 6. Network Architecture (CNN)

The classifier is a Convolutional Neural Network (CNN) that processes 150×150 color images and outputs a 2-element probability vector (cat probability, dog probability).

### 6.1 Architecture Overview

The network is composed of three stages: (1) Feature Extraction via stacked convolution + pooling blocks, (2) Flattening to a 1-D feature vector, and (3) Classification via fully-connected layers.

| Stage | Layer Type | Output Shape | Description |
|---|---|---|---|
| Input | Input Image | 3 × 150 × 150 | RGB color image normalized to [0,1] |
| Block 1 | Conv2d(3→32, 3×3) | 32 × 148 × 148 | 32 kernels, learn low-level edges/colors |
| Block 1 | ReLU | 32 × 148 × 148 | Non-linear activation, removes negatives |
| Block 1 | MaxPool2d(2×2) | 32 × 74 × 74 | Halves spatial dims, keeps dominant features |
| Block 2 | Conv2d(32→64, 3×3) | 64 × 72 × 72 | 64 kernels, learn mid-level textures/shapes |
| Block 2 | ReLU | 64 × 72 × 72 | Non-linear activation |
| Block 2 | MaxPool2d(2×2) | 64 × 36 × 36 | Spatial downsampling |
| Block 3 | Conv2d(64→128, 3×3) | 128 × 34 × 34 | 128 kernels, learn high-level part detectors |
| Block 3 | ReLU | 128 × 34 × 34 | Non-linear activation |
| Block 3 | MaxPool2d(2×2) | 128 × 17 × 17 | Spatial downsampling |
| Flatten | Flatten | 36,992 | Reshape to 1-D for FC layers |
| FC 1 | Linear(36992→512) | 512 | First fully-connected classification layer |
| FC 1 | ReLU | 512 | Non-linear activation |
| FC 1 | Dropout(0.5) | 512 | Regularization to reduce overfitting |
| FC 2 (Output) | Linear(512→2) | 2 | Two logits: P(cat) and P(dog) |
| Output | Softmax | 2 | Convert logits to probabilities summing to 1 |

> **Note on MaxPooling:** A `MaxPool2d(2×2)` layer is placed after **every** convolutional layer. This halves the spatial dimensions at each stage (150 → 74 → 36 → 17 → 8 for a 4-block network), keeping memory and compute manageable while providing spatial translation invariance.

### 6.2 Configurable Hyperparameters

All architectural parameters are exposed as Python variables at the top of the notebook cell:

| Parameter | Default | Description |
|---|---|---|
| `KERNELS` | `[32, 64, 128]` | Number of filters per Conv block |
| `KERNEL_SIZE` | `3` | Spatial size of each convolutional filter |
| `FC_UNITS` | `512` | Neurons in the hidden fully-connected layer |
| `FC_LAYERS` | `1` | Number of hidden FC layers before output |
| `DROPOUT_RATE` | `0.5` | Dropout probability (0 = disabled) |
| `LEARNING_RATE` | `0.001` | Adam optimizer learning rate |
| `BATCH_SIZE` | `32` | Images per gradient update |
| `NUM_EPOCHS` | `20` | Full passes over the training set |

### 6.3 Activation Functions

- **Hidden layers (Conv + FC):** `ReLU` — `f(x) = max(0, x)`. Provides non-linearity while avoiding the vanishing gradient problem common with sigmoid/tanh.
- **Output layer:** `Softmax` — converts raw logits to a probability distribution over 2 classes. The class with the higher probability is the predicted label.

### 6.4 Loss Function

**Cross-Entropy Loss** (`nn.CrossEntropyLoss`) measures the difference between the predicted probability distribution and the true one-hot label distribution:

```
L = −Σ yᵢ · log(pᵢ)
```

where `yᵢ` is the true label (0 or 1) and `pᵢ` is the predicted probability for class `i`. A lower loss means the predicted probabilities are closer to the ground truth. PyTorch's `CrossEntropyLoss` internally applies `LogSoftmax` before computing the loss, so Softmax is applied only during inference for display purposes.

---

## 7. Training (Fit)

### 7.1 Optimization

The model is trained using the **Adam** (Adaptive Moment Estimation) optimizer, which combines the benefits of momentum and adaptive learning rates. Adam is preferred over vanilla SGD for deep CNNs because it converges faster and requires less manual learning rate tuning.

| Parameter | Value |
|---|---|
| **Optimizer** | Adam |
| **Learning rate** | 0.001 (user-configurable) |
| **Beta1 / Beta2** | 0.9 / 0.999 (Adam defaults) |
| **Weight decay** | 1e-4 (L2 regularization) |
| **Batch size** | 32 images per gradient update step |

**Backpropagation** is used to compute gradients of the loss with respect to all model parameters. For each mini-batch:
1. Forward pass computes predictions and loss.
2. `loss.backward()` computes gradients via the chain rule.
3. `optimizer.step()` updates weights in the direction that reduces the loss.

### 7.2 Training Curves

After each epoch, the notebook logs and plots:

- Training loss (Cross-Entropy) per epoch
- Validation loss per epoch
- Training accuracy per epoch
- Validation accuracy per epoch

These four curves are plotted side-by-side in a 2-panel Matplotlib figure, allowing the user to visually monitor convergence, detect overfitting (diverging train vs. val loss), and decide when to stop training.

### 7.3 Model Summary

After the architecture is defined, `torchsummary.summary(model, (3, 150, 150))` is called to print the layer-by-layer summary, including output shape and number of trainable parameters at each stage. This is equivalent to Keras `model.summary()`.

---

## 8. Test and Evaluation

### 8.1 Sample Predictions

After training, the notebook displays a 2×5 grid of test images with their true labels and predicted labels. Correct predictions are shown in **green**; incorrect predictions are shown in **red**. This provides immediate qualitative feedback on the model's performance.

### 8.2 Test Accuracy

The model is evaluated on the full test set (500 cats + 500 dogs). The notebook reports overall accuracy, precision, recall, and F1-score for each class using `sklearn.metrics.classification_report`.

### 8.3 Confusion Matrix

A 2×2 confusion matrix is drawn using `seaborn.heatmap`:

| True \ Predicted | Predicted Cat | Predicted Dog |
|---|---|---|
| **True Cat** | TP (True Positive) | FN (False Negative) |
| **True Dog** | FP (False Positive) | TN (True Negative) |

### 8.4 Error Analysis

Misclassified images are displayed in a dedicated cell. For each error, the notebook prints the image, true label, predicted label, and the model's confidence (Softmax probability). Common failure cases include:

- Ambiguous pose or partial occlusion of the animal.
- Unusual backgrounds that dominate the feature maps.
- Small subject size where the animal occupies only a fraction of the 150×150 frame.
- Images with mixed content (e.g., a person holding a cat).

These failure cases illustrate why accuracy is never 100% even for a well-trained model and motivate the improvement experiments in Section 9.

---

## 9. Improvement Experiments

After the baseline model is trained and evaluated, three manual improvement experiments are conducted. Each experiment changes one architectural dimension and compares the resulting confusion matrix and accuracy to the baseline.

### Experiment A — Deeper Network

Add one additional Conv+Pool block (4 blocks total, kernels `[32, 64, 128, 256]`). A deeper network can learn more abstract feature hierarchies but risks overfitting on a small dataset.

- **Change:** 4 Conv+MaxPool blocks instead of 3
- **Expected:** Slightly higher accuracy if well-regularized; risk of overfitting with only 2,000 training images

### Experiment B — Wider Network

Double the number of kernels in each conv block (`[64, 128, 256]`) and double the FC layer width (1,024 neurons). A wider network has more representational capacity per layer.

- **Change:** Kernels `[64, 128, 256]`, FC units = 1,024
- **Expected:** Marginally better accuracy at the cost of significantly more parameters and longer training time

### Experiment C — Fewer Kernels

Reduce the kernel counts to `[16, 32, 64]` and FC units to 256. This is a more compact model that trains faster.

- **Change:** Kernels `[16, 32, 64]`, FC units = 256
- **Expected:** Slightly lower accuracy but faster convergence, illustrating the accuracy-efficiency trade-off

Each experiment follows the same pipeline: re-define the model, train for the same number of epochs, plot training curves, and show the confusion matrix. A final comparison table summarizes test accuracy across all configurations.

---

## 10. Functional Requirements

| ID | Requirement |
|---|---|
| **FR-01** | The notebook shall load images from `./cats` and `./dogs` folders on the user's Google Drive. |
| **FR-02** | The notebook shall display sample images before training. |
| **FR-03** | The notebook shall resize all images to 150×150 pixels. |
| **FR-04** | The notebook shall normalize pixel values using ImageNet statistics. |
| **FR-05** | The notebook shall assign labels from folder names and demonstrate one-hot encoding. |
| **FR-06** | The notebook shall split data: 1,000 train + 500 test per class. |
| **FR-07** | The user shall be able to configure hyperparameters via clearly labeled variables. |
| **FR-08** | The notebook shall print a model summary (layer shapes, parameter counts). |
| **FR-09** | The notebook shall plot training/validation loss and accuracy curves. |
| **FR-10** | The notebook shall evaluate the model on the test set and report accuracy. |
| **FR-11** | The notebook shall display a 2×2 confusion matrix. |
| **FR-12** | The notebook shall display misclassified images with explanation. |
| **FR-13** | The notebook shall include at least 3 improvement experiments with comparative results. |

---

## 11. Non-Functional Requirements

- **Platform:** Google Colab (Python 3.x, PyTorch ≥ 2.0, torchvision ≥ 0.15).
- **GPU:** The notebook should run on Colab's free T4 GPU. Each training run should complete in under 30 minutes for 20 epochs.
- **Reproducibility:** A fixed random seed (default 42) ensures consistent train/test splits and weight initializations.
- **Readability:** Every code section is preceded by a Markdown cell explaining what it does and why, suitable for students learning deep learning.
- **Modularity:** The model class, data loading, training loop, and evaluation are in separate cells to allow independent re-execution.

---

## 12. Deliverables

1. `cats_dogs_classifier.ipynb` — The fully annotated Google Colab notebook.
2. `cats_dogs_PRD.md` — This PRD document (Markdown).
3. `cats_dogs_PRD.docx` — This PRD document (Word).
4. `README.md` — Setup instructions and project overview.

---

## 13. Glossary

| Term | Definition |
|---|---|
| **CNN** | Convolutional Neural Network — a deep learning architecture specialized for image data. |
| **Kernel / Filter** | A small learnable weight matrix that slides over the image to detect features. |
| **MaxPooling** | A down-sampling operation that keeps the maximum value in each local window. Placed after every Conv layer in this project. |
| **ReLU** | Rectified Linear Unit — activation function `f(x) = max(0, x)`. |
| **Softmax** | Converts a vector of raw scores (logits) into probabilities that sum to 1. |
| **Cross-Entropy** | A loss function for classification measuring KL-divergence between predicted and true distributions. |
| **Adam** | An adaptive gradient optimization algorithm combining momentum and RMSProp. |
| **Backpropagation** | Algorithm for computing gradients of the loss w.r.t. all model parameters via the chain rule. |
| **One-Hot Encoding** | Representing a class label as a binary vector with a 1 at the class index and 0 elsewhere. |
| **Confusion Matrix** | A table showing TP, FP, FN, TN counts for a classifier. |
| **Overfitting** | When a model learns training data too well and fails to generalize to unseen data. |
| **Dropout** | A regularization technique that randomly zeroes neurons during training to prevent overfitting. |

---

*Document prepared by Yair Levi — February 2026 — Version 1.0*
