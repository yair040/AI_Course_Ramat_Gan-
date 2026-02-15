# Multi-Class Classification: Fully Connected vs. Convolutional Neural Networks

**Based on Lecture by Dr. Yoram Segal**

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Fully Connected Neural Networks](#2-fully-connected-neural-networks-for-multi-class-classification)
3. [Convolutional Neural Networks (CNNs)](#3-convolutional-neural-networks-cnns)
4. [Image Preprocessing](#4-image-preprocessing-for-neural-networks)
5. [Mathematical Properties](#5-mathematical-properties-of-convolution)
6. [Computational Efficiency](#6-computational-efficiency-and-parameter-count)
7. [Comparison](#7-cnns-vs-fully-connected-networks-comparison)
8. [Conclusion](#8-conclusion)

---

## 1. Introduction

This document provides a comprehensive overview of **multi-class classification** using neural networks, comparing two fundamental architectures:

- **Fully Connected (FC) Neural Networks**
- **Convolutional Neural Networks (CNNs)**

These networks are essential tools in modern machine learning, particularly for image classification tasks.

### What is Multi-Class Classification?

Multi-class classification is the task of categorizing input data into one of several predefined classes. For example:
- Identifying whether an image contains a **cat**, **dog**, **bird**, or other animals
- Recognizing handwritten digits (0-9)
- Classifying medical images into different disease categories

While fully connected networks can perform this task, **CNNs have revolutionized image processing** by preserving spatial relationships and reducing computational complexity.

---

## 2. Fully Connected Neural Networks for Multi-Class Classification

### 2.1 Training Phase

The training process in a fully connected network involves several key steps:

#### Step-by-Step Process:

1. **Probability Vector Generation**
   - The network processes the input and generates a probability vector
   - Each element represents the likelihood that the input belongs to a particular class

2. **One-Hot Encoding**
   - The true label is converted into a one-hot encoded vector
   - This vector contains all zeros except for a single 1 at the correct class index
   - **Example**: If an image is a cat (class 2 out of 5 classes), the vector would be `[0, 0, 1, 0, 0]`

3. **Error Calculation**
   - Error vector = Probability vector - One-hot encoded vector
   - Error magnitude = Dot product of error vector with itself

4. **Backpropagation**
   - The calculated error propagates backward through the network
   - Weights are adjusted to minimize the error in future predictions

#### Training Example

| Step | Vector | Description |
|------|--------|-------------|
| **Network Output** | `[0.1, 0.2, 0.6, 0.05, 0.05]` | Probability for each class |
| **True Label (Cat)** | `[0, 0, 1, 0, 0]` | One-hot encoded vector |
| **Error Vector** | `[0.1, 0.2, -0.4, 0.05, 0.05]` | Difference used for backpropagation |

---

### 2.2 Testing Phase

During testing, the trained network evaluates new, unseen data. Two critical measures ensure robust classification:

#### 🎯 Threshold Application
- Only probabilities exceeding a predefined threshold are considered
- **Purpose**: Prevents misclassification when all probabilities are low
- **Prevents**: Cases where one class is selected merely because it's slightly higher than others

#### 🎯 Maximum Selection
- After applying the threshold, select the class with the highest probability
- **Purpose**: Resolves situations where multiple classes exceed the threshold

---

### 2.3 Confusion Matrix

A confusion matrix is a fundamental tool for evaluating classification performance.

#### Construction Process:
- ✓ One axis represents the **true (actual)** class of each sample
- ✓ The other axis represents the **predicted** class
- ✓ For each test sample, increment the counter at the intersection

#### Example: 3-Class Confusion Matrix

|  | **Predicted →** | Cat | Dog | Bird |
|---|---|---|---|---|
| **Actual ↓** | | | | |
| **Cat** | | **45** ✓ | 3 | 2 |
| **Dog** | | 4 | **38** ✓ | 1 |
| **Bird** | | 1 | 2 | **42** ✓ |

> **Note**: Diagonal elements (✓) represent correct predictions. Off-diagonal elements represent misclassifications.

#### Key Metrics from Confusion Matrix:
- **Accuracy** = (45 + 38 + 42) / 143 = 87.4%
- **Precision for Cat** = 45 / (45 + 4 + 1) = 90%
- **Recall for Cat** = 45 / (45 + 3 + 2) = 90%

---

### 2.4 Limitations of Fully Connected Networks for Image Processing

While FC networks are versatile, they have significant drawbacks for image classification:

#### ❌ Loss of Spatial Context
- Images must be **flattened** into 1D vectors for input
- This destroys the 2D spatial relationships between pixels
- The network learns patterns based solely on pixel brightness at specific positions

#### ❌ Lack of Translation Invariance
- FC networks cannot recognize objects that have been moved or shifted
- Moving a cat from one location breaks learned associations
- No geometric relationships are preserved

#### ❌ Computational Inefficiency
- Enormous number of parameters (every pixel connects to every neuron)
- Leads to:
  - Excessive memory consumption
  - Slow training
  - Increased risk of overfitting

#### ❌ Position-Dependent Pattern Recognition
- Builds probability vectors of brightness patterns along specific positions
- Makes recognition position-dependent rather than feature-dependent

---

## 3. Convolutional Neural Networks (CNNs)

CNNs represent a specialized architecture designed specifically for processing grid-like data, particularly images.

### 3.1 Core Principles

CNNs address the fundamental limitations of fully connected networks:

#### ✅ Spatial Structure Preservation
- Maintains the 2D topology of images
- Processes pixels in relation to their neighbors
- Similar to how the human visual system works

#### ✅ Local Connectivity
- Each neuron connects only to a small region (receptive field)
- Inspired by biological visual processing

#### ✅ Parameter Sharing
- **Same filter (kernel) scans the entire image**
- Uses identical weights across all positions
- Dramatically reduces parameter count

#### ✅ Translation Invariance
- Objects recognized regardless of position in image
- Same features detected everywhere

#### ✅ Parallel Processing
- Convolution operations are highly parallelizable
- Enables efficient GPU utilization

---

### 3.2 The Convolution Operation

#### 3.2.1 Basic Concept

A convolution applies a small matrix called a **kernel** (or filter) that slides across the input image.

**Process**:
1. Kernel overlaps a region of the image
2. Element-wise multiplication of kernel with overlapping region
3. Sum all products to produce single output value
4. Slide kernel to next position and repeat

#### Simple Example: Averaging Filter

**Input Image (5×5)**:
```
┌────────────────────┐
│  1   2   3   4   5 │
│  6   7   8   9  10 │
│ 11  12  13  14  15 │
│ 16  17  18  19  20 │
│ 21  22  23  24  25 │
└────────────────────┘
```

**Kernel (3×3 Averaging Filter)**:
```
┌─────────────────┐
│ 1/9  1/9  1/9  │
│ 1/9  1/9  1/9  │
│ 1/9  1/9  1/9  │
└─────────────────┘
```

**Output Feature Map (3×3)**:
- Formula: `O = I - K + 1 = 5 - 3 + 1 = 3`
- The kernel slides across the image, computing local averages

---

#### 3.2.2 Mathematical Definition

**1D Convolution**:
```
(f ∗ g)(t) = Σ f(τ) × g(t - τ)
```
- `f` = signal
- `∗` = convolution operator
- `g` = kernel (inverted in mathematical definition)

**2D Feature Map Output Dimensions**:
```
O = I - K + 1
```

Where:
- **O** = Output dimension (width or height)
- **I** = Input dimension
- **K** = Kernel size

**Example**: A 5×5 input with a 3×3 kernel produces a 3×3 output:
```
5 - 3 + 1 = 3
```

---

### 3.3 Kernels and Feature Detection

Kernels are the fundamental building blocks of CNNs. Different kernel weights detect different features.

#### 3.3.1 Common Kernel Types

| Kernel Type | Weights | Purpose |
|-------------|---------|---------|
| **Vertical Edge Detector** | `[-1  0  +1]`<br>`[-1  0  +1]`<br>`[-1  0  +1]` | Detects vertical lines by identifying horizontal intensity changes |
| **Horizontal Edge Detector** | `[+1  +1  +1]`<br>`[ 0   0   0]`<br>`[-1  -1  -1]` | Detects horizontal lines by identifying vertical intensity changes |
| **Blur/Averaging** | `[1/9  1/9  1/9]`<br>`[1/9  1/9  1/9]`<br>`[1/9  1/9  1/9]` | Smooths image by averaging neighboring pixels |
| **Sharpen** | `[ 0  -1   0]`<br>`[-1   5  -1]`<br>`[ 0  -1   0]` | Enhances edges and details |
| **Sobel (Horizontal)** | `[-1   0  +1]`<br>`[-2   0  +2]`<br>`[-1   0  +1]` | Advanced edge detection with center emphasis |

#### Visualizing Edge Detection

**Example**: Vertical edge detector on an image with a black rectangle:

```
Original Image:           After Vertical Edge Kernel:
┌──────────────┐         ┌──────────────┐
│ ⬜⬜⬜⬜⬜⬜ │         │ 0  0  0  0  0 │
│ ⬜⬜⬛⬛⬜⬜ │    →    │ 0  0 [2] 0  0 │  ← Left edge detected
│ ⬜⬜⬛⬛⬜⬜ │         │ 0  0 [2] 0  0 │
│ ⬜⬜⬜⬜⬜⬜ │         │ 0  0  0  0  0 │
└──────────────┘         └──────────────┘
                         (Only vertical edges highlighted)
```

---

#### 3.3.2 Learning Kernel Weights

Unlike handcrafted kernels, CNNs **learn optimal kernel weights** through training:

1. **Initialize**: Start with random weights for all kernels
2. **Forward Pass**: Apply kernels to images and compute output
3. **Backpropagation**: Adjust weights based on classification error
4. **Optimization**: Kernels learn to detect patterns most relevant for classification

**Hierarchical Learning**:
- **Early layers**: Detect simple features (edges, corners, textures)
- **Middle layers**: Combine features into patterns (curves, shapes, object parts)
- **Deep layers**: Recognize complete objects, faces, complex structures

---

### 3.4 Hierarchical Feature Learning

CNNs build a hierarchy of increasingly complex features:

```
┌─────────────────────────────────────────────────────────┐
│                    LAYER HIERARCHY                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Layer 1 (Early)  →  Layer 2 (Middle)  →  Layer 3+ (Deep)│
│                                                          │
│  ┌─────────┐         ┌──────────┐         ┌──────────┐ │
│  │ Edges   │    →    │ Shapes   │    →    │ Objects  │ │
│  │ Corners │         │ Curves   │         │ Faces    │ │
│  │ Textures│         │ Parts    │         │ Complex  │ │
│  └─────────┘         └──────────┘         └──────────┘ │
│                                                          │
│  Small receptive    Medium receptive    Large receptive │
│  fields             fields              fields           │
└─────────────────────────────────────────────────────────┘
```

**Example**: Face recognition CNN
- **Layer 1**: Detects edges
- **Layer 2**: Identifies eye or nose shapes
- **Layer 3**: Recognizes complete faces

---

### 3.5 Feature Maps and Multiple Filters

A single kernel produces a single feature map. To capture various features, CNNs use **multiple kernels in parallel**.

#### Example Configuration:

```
Input:  28×28 grayscale image (single channel)
         ↓
Filters: 32 different 3×3 kernels (applied in parallel)
         ↓
Output: 32 feature maps, each 26×26 pixels
         (O = 28 - 3 + 1 = 26)
         ↓
Result: Tensor of dimensions 26×26×32
```

**Visualization**:
```
┌──────────┐
│  Input   │
│  28×28×1 │
└────┬─────┘
     │
     ├─→ [Kernel 1] → Feature Map 1 (26×26) → Vertical edges
     ├─→ [Kernel 2] → Feature Map 2 (26×26) → Horizontal edges
     ├─→ [Kernel 3] → Feature Map 3 (26×26) → Curves
     │     ...
     └─→ [Kernel 32] → Feature Map 32 (26×26) → Complex patterns
          │
          ↓
     Output: 26×26×32 tensor
```

Each of the 32 filters learns to detect different features. The **number of kernels defines the depth** (number of channels) of the output.

---

### 3.6 Key Architectural Components

#### 3.6.1 Padding

Convolution naturally reduces spatial dimensions. **Padding** addresses this by adding borders around the input.

| Strategy | Description | Formula |
|----------|-------------|---------|
| **Valid Padding** | No padding added. Output is smaller than input. | `O = I - K + 1` |
| **Same Padding** | Add zeros around borders. Output size = Input size.<br>Padding width = K/2 | `O = I` |

**Visual Example**:

Without Padding (Valid):
```
┌───────┐
│ Image │  5×5  →  [3×3 Kernel]  →  3×3 output
└───────┘
```

With Padding (Same):
```
┌─────────────┐
│ 0 0 0 0 0 0 │
│ 0 ┌───────┐ 0 │
│ 0 │ Image │ 0 │  7×7  →  [3×3 Kernel]  →  5×5 output
│ 0 └───────┘ 0 │
│ 0 0 0 0 0 0 │
└─────────────┘
```

---

#### 3.6.2 Stride

Stride controls how many pixels the kernel moves at each step.

- **Stride = 1**: Kernel moves one pixel at a time (default, maximum information)
- **Stride = 2**: Kernel moves two pixels, reducing output size by ~half
- **Stride > 2**: Further dimensionality reduction

**Visualization**:

Stride = 1:
```
Step 1: [■■■]□□□    Step 2: □[■■■]□□    Step 3: □□[■■■]□
```

Stride = 2:
```
Step 1: [■■■]□□□    Step 2: □□[■■■]□    (skips middle position)
```

---

#### 3.6.3 General Output Dimensions Formula

The complete formula incorporating padding and stride:

```
Hₒᵤₜ = ⌊(Hᵢₙ - K + 2P) / S⌋ + 1
```

Where:
- **Hₒᵤₜ** = Output height (or width)
- **Hᵢₙ** = Input height (or width)
- **K** = Kernel size
- **P** = Padding size
- **S** = Stride size
- **⌊ ⌋** = Floor function (round down)

**Examples**:

| Input Size | Kernel | Padding | Stride | Output Size | Calculation |
|------------|--------|---------|--------|-------------|-------------|
| 28×28 | 3×3 | 0 | 1 | 26×26 | ⌊(28-3+0)/1⌋+1 = 26 |
| 28×28 | 3×3 | 1 | 1 | 28×28 | ⌊(28-3+2)/1⌋+1 = 28 |
| 28×28 | 3×3 | 0 | 2 | 13×13 | ⌊(28-3+0)/2⌋+1 = 13 |

---

## 4. Image Preprocessing for Neural Networks

Proper preprocessing is crucial for effective neural network training and inference.

### 4.1 Standard Preprocessing Steps

#### 1️⃣ Resize
- Convert all images to **uniform dimensions**
- Example: Resize all images to 224×224 pixels
- Ensures consistent input dimensions across dataset

#### 2️⃣ Normalize
- Scale pixel values to a standard range (typically 0 to 1)
- Improves training stability and convergence speed
- Original range: 0-255 → Normalized range: 0-1

#### 3️⃣ Reshape
- For color images, organize data into a tensor
- Format: (height × width × channels)
- Example: Color image → (224, 224, 3) where 3 = RGB channels

---

### 4.2 Normalization Strategies

| Method | Range | Formula | Use Case |
|--------|-------|---------|----------|
| **Min-Max [0,1]** | 0 to 1 | `(I - min) / (max - min)` | Default for most CNNs |
| **Min-Max [-1,1]** | -1 to 1 | `2(I - min) / (max - min) - 1` | GANs, Tanh activation |
| **Z-Score** | Zero-centered | `(I - μ) / σ` | Standardization, different scales |

Where:
- **I** = Pixel intensity value
- **min** / **max** = Minimum/maximum value in data
- **μ** = Mean
- **σ** = Standard deviation

> **Note**: For color images, normalization is typically applied **separately to each color channel** (R, G, B).

#### Normalization Example:

Original pixel value: 200 (range 0-255)

**Min-Max [0,1]**:
```
(200 - 0) / (255 - 0) = 0.784
```

**Min-Max [-1,1]**:
```
2 × (200 - 0) / (255 - 0) - 1 = 0.569
```

---

### 4.3 Data Augmentation

When training data is limited, augmentation artificially expands the dataset by creating modified versions of existing images.

#### Common Augmentation Techniques:

| Technique | Description | Example |
|-----------|-------------|---------|
| 🔄 **Rotation** | Rotate images by various angles | ±15°, ±30° |
| ↔️ **Translation** | Shift images horizontally/vertically | ±10% of dimensions |
| 🪞 **Flipping** | Mirror images | Horizontal, Vertical |
| 🔍 **Zooming** | Random zoom in/out | 80%-120% |
| 💡 **Brightness/Contrast** | Adjust lighting conditions | ±20% brightness |

**Visual Example**:

```
Original:        Rotated:       Flipped:       Zoomed:
┌─────────┐     ┌─────────┐    ┌─────────┐    ┌─────────┐
│  🐱    │     │    🐱   │    │    🐱  │    │   🐱   │
│         │  →  │   ↻     │ →  │  ⟷      │ →  │  ⤢     │
│         │     │         │    │         │    │         │
└─────────┘     └─────────┘    └─────────┘    └─────────┘
```

**Python Libraries**:
- `Keras ImageDataGenerator`
- `Albumentations`
- `torchvision.transforms`

---

## 5. Mathematical Properties of Convolution

Understanding these properties explains why CNNs work so effectively:

### Key Properties:

#### 1. Commutativity
```
f ∗ g = g ∗ f
```
- Doesn't matter if kernel slides over image or image slides under kernel
- Result is the same

#### 2. Associativity
```
(f ∗ g) ∗ h = f ∗ (g ∗ h)
```
- When applying multiple kernels sequentially
- Order of grouping doesn't matter

#### 3. Linearity
- Convolution operations can be decomposed and distributed
- Enables efficient computation

#### 4. Translation Equivariance
- **If input shifts → output shifts by same amount**
- Key advantage over fully connected networks
- Enables translation invariance

---

### 5.1 Convolution vs. Correlation

| Operation | Kernel Processing | Mathematical Definition |
|-----------|-------------------|------------------------|
| **Convolution** | Flips kernel before sliding | `(f ∗ g)(t) = Σ f(τ)g(t-τ)` |
| **Correlation** | Slides kernel without flipping | `(f ⋆ g)(t) = Σ f(τ)g(t+τ)` |

> **In Practice**: Most deep learning frameworks implement **correlation** but call it "convolution". Since kernels are learned (not hand-designed), the distinction is irrelevant—the network learns appropriate weights regardless.

---

## 6. Computational Efficiency and Parameter Count

### 6.1 Parameter Sharing in CNNs

One of CNN's greatest advantages: **All neurons in a feature map use the same kernel weights.**

#### Comparison Example:

**CNN (3×3 kernel)**:
- Parameters: **10** (9 weights + 1 bias)
- Independent of input image size!

**Fully Connected (28×28 image to 100 neurons)**:
- Parameters: **78,400** (784 × 100)
- Grows with input size

```
┌────────────────────────────────────────┐
│          Parameter Efficiency          │
├────────────────────────────────────────┤
│                                        │
│  CNN:        10 parameters    ✓✓✓     │
│  FC:     78,400 parameters    ❌❌❌    │
│                                        │
│  Reduction: 99.99%                     │
└────────────────────────────────────────┘
```

---

### 6.2 GPU Acceleration

**Convolution = Matrix Multiplication**

- GPUs are specifically optimized for matrix operations
- Same kernel applied across entire image **in parallel**
- CNNs leverage GPU parallelism extremely efficiently
- Result: Much faster training and inference vs. FC networks

**Speed Comparison** (typical):
```
Training Time (same dataset):
┌────────────────────────────────┐
│ FC Network:  ████████████  12h │
│ CNN:         ███            3h │
└────────────────────────────────┘
```

---

## 7. CNNs vs. Fully Connected Networks: Comparison

| Aspect | Fully Connected | Convolutional |
|--------|----------------|---------------|
| **Spatial Structure** | ❌ Lost - images flattened to 1D | ✅ Preserved - maintains 2D relationships |
| **Translation Invariance** | ❌ No - moving objects breaks recognition | ✅ Yes - detects objects anywhere |
| **Parameters** | ❌ Very high - every connection unique | ✅ Low - weight sharing |
| **Training Speed** | ❌ Slow - many parameters | ✅ Fast - GPU-optimized parallel ops |
| **Overfitting Risk** | ❌ High - too many parameters | ✅ Lower - fewer parameters |
| **Memory Usage** | ❌ Very high | ✅ Much lower |
| **Feature Learning** | ❌ Position-dependent brightness | ✅ Hierarchical features (edges→parts→objects) |

### Visual Comparison:

**Fully Connected Approach**:
```
Image → [Flatten] → [784 nodes] → [Hidden Layers] → [Output]
        Lost 2D      Position      Every pixel
        structure    dependent     connected
```

**CNN Approach**:
```
Image → [Conv1] → [Conv2] → [Conv3] → [FC] → [Output]
        Edges      Shapes     Objects   Classify
        ↓          ↓          ↓
        Preserved  Hierarchy  Translation
        structure  of features invariant
```

---

## 8. Conclusion

Convolutional Neural Networks represent a fundamental breakthrough in image processing and computer vision. By preserving spatial structure, sharing parameters, and building hierarchical representations, CNNs overcome the key limitations of fully connected networks.

### 🎯 Key Takeaways:

✅ **Fully connected networks** flatten images, losing spatial context and requiring enormous parameter counts

✅ **CNNs preserve 2D structure** through local connectivity and maintain translation invariance

✅ **Convolution operations** use learnable kernels to detect features at multiple scales

✅ **Parameter sharing** dramatically reduces model complexity and training time

✅ **Proper preprocessing** (resizing, normalization, augmentation) is essential for success

✅ **CNNs build hierarchical representations** from simple features to complex objects

---

### Why CNNs Dominate Computer Vision:

```
┌─────────────────────────────────────────────────┐
│                                                 │
│  Image Classification  ✓                        │
│  Object Detection      ✓                        │
│  Facial Recognition    ✓                        │
│  Medical Imaging       ✓                        │
│  Autonomous Vehicles   ✓                        │
│  Video Analysis        ✓                        │
│                                                 │
└─────────────────────────────────────────────────┘
```

These principles have made CNNs the dominant architecture for countless visual recognition tasks. Understanding these fundamentals provides the foundation for working with modern deep learning architectures and developing effective computer vision solutions.

---

### 📚 Further Study Topics:

- Advanced CNN architectures (ResNet, VGG, Inception)
- Pooling layers and their role
- Batch normalization and dropout
- Transfer learning and pre-trained models
- Object detection (YOLO, Faster R-CNN)
- Semantic segmentation (U-Net, FCN)

---

<div align="center">

**Document prepared based on lecture by Dr. Yoram Segal**

*Multi-Class Classification with Neural Networks*

</div>
