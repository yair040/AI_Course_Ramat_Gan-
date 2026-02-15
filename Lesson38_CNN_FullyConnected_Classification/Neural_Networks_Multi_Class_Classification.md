**Multi-Class Classification:**

**Fully Connected vs. Convolutional Neural Networks**

*Based on Lecture by Dr. Yoram Segal*

1\. Introduction

This document provides a comprehensive overview of multi-class
classification using neural networks, comparing two fundamental
architectures: Fully Connected (FC) Neural Networks and Convolutional
Neural Networks (CNNs). These networks are essential tools in modern
machine learning, particularly for image classification tasks.

Multi-class classification is the task of categorizing input data into
one of several predefined classes. For example, identifying whether an
image contains a cat, dog, bird, or other animals. While fully connected
networks can perform this task, CNNs have revolutionized image
processing by preserving spatial relationships and reducing
computational complexity.

2\. Fully Connected Neural Networks for Multi-Class Classification

2.1 Training Phase

The training process in a fully connected network involves several key
steps:

1.  **Probability Vector Generation:** The network processes the input
    and generates a probability vector where each element represents the
    likelihood that the input belongs to a particular class.

2.  **One-Hot Encoding:** The true label is converted into a one-hot
    encoded vector. This vector contains all zeros except for a single 1
    at the index corresponding to the correct class. For example, if an
    image is a cat (class 2 out of 5 classes), the vector would be \[0,
    0, 1, 0, 0\].

3.  **Error Calculation:** The error vector is computed by subtracting
    the one-hot encoded vector from the probability vector. The
    magnitude of this error is obtained through the dot product of the
    error vector with itself.

4.  **Backpropagation:** The calculated error is propagated backward
    through the network, adjusting weights to minimize the error in
    future predictions.

**Example: Training Process**

  ----------------------- ----------------------- -----------------------
  **Step**                **Vector**              **Description**

  Network Output          \[0.1, 0.2, 0.6, 0.05,  Probability for each
                          0.05\]                  class

  True Label (Cat)        \[0, 0, 1, 0, 0\]       One-hot encoded vector

  Error Vector            \[0.1, 0.2, -0.4, 0.05, Difference used for
                          0.05\]                  backpropagation
  ----------------------- ----------------------- -----------------------

2.2 Testing Phase

During testing, the trained network evaluates new, unseen data. Two
critical measures are applied to ensure robust classification:

-   **Threshold Application:** Only probabilities exceeding a predefined
    threshold are considered. This prevents misclassification when all
    probabilities are low, avoiding cases where one class is selected
    merely because it\'s slightly higher than others.

-   **Maximum Selection:** After applying the threshold, the class with
    the highest probability is selected. This resolves situations where
    multiple classes exceed the threshold.

2.3 Confusion Matrix

A confusion matrix is a fundamental tool for evaluating classification
performance. It can be constructed during both training (on validation
sets) and testing phases.

**Construction Process:**

-   One axis represents the true (actual) class of each sample

-   The other axis represents the predicted class

-   For each test sample, increment the counter at the intersection of
    its true and predicted class

**Example: 3-Class Confusion Matrix**

  ----------------- --------------- ------------- -------------
                    **Predicted**                 

  **Actual**        **Cat**         **Dog**       **Bird**

  **Cat**           **45**          3             2

  **Dog**           4               **38**        1

  **Bird**          1               2             **42**
  ----------------- --------------- ------------- -------------

***Note:** Diagonal elements (highlighted in green) represent correct
predictions. Off-diagonal elements represent misclassifications.*

2.4 Limitations of Fully Connected Networks for Image Processing

While fully connected networks are versatile, they have significant
drawbacks when applied to image classification:

-   **Loss of Spatial Context:** Images must be flattened into 1D
    vectors for input, destroying the 2D spatial relationships between
    pixels. The network learns patterns based solely on pixel brightness
    probabilities at specific positions in the linear vector.

-   **Lack of Translation Invariance:** FC networks cannot recognize
    objects that have been moved or shifted within an image. Since there
    are no geometric relationships preserved, moving a cat from one
    location to another breaks the learned associations between pixel
    positions and the object identity.

-   **Computational Inefficiency:** FC networks require an enormous
    number of parameters (every pixel connects to every neuron in the
    next layer), leading to excessive memory consumption, slow training,
    and increased risk of overfitting.

-   **Pattern Recognition by Position:** The network builds probability
    vectors of brightness patterns along specific positions in the
    flattened image vector, making it position-dependent rather than
    feature-dependent.

3\. Convolutional Neural Networks (CNNs)

Convolutional Neural Networks represent a specialized architecture
designed specifically for processing grid-like data, particularly
images. CNNs address the fundamental limitations of fully connected
networks by preserving spatial structure and dramatically reducing the
number of parameters.

3.1 Core Principles

CNNs operate on fundamentally different principles compared to fully
connected networks:

-   **Spatial Structure Preservation:** Unlike FC networks, CNNs
    maintain the 2D topology of images, processing pixels in relation to
    their neighbors.

-   **Local Connectivity:** Each neuron connects only to a small region
    of the input (its receptive field), similar to how the human visual
    system processes information.

-   **Parameter Sharing:** The same filter (kernel) scans the entire
    image, using identical weights across all positions. This
    dramatically reduces the number of parameters compared to FC
    networks.

-   **Translation Invariance:** Objects can be recognized regardless of
    their position in the image, as the same features are detected
    everywhere.

-   **Parallel Processing:** Convolution operations are highly
    parallelizable, enabling efficient GPU utilization.

3.2 The Convolution Operation

3.2.1 Basic Concept

A convolution applies a small matrix called a **kernel** (or filter)
that slides across the input image. At each position, the kernel
performs an element-wise multiplication with the overlapping region of
the image, and the results are summed to produce a single output value.

**Example: Simple Convolution Process**

**Input Image (5×5):**

  -------------- -------------- -------------- -------------- --------------
  1              2              3              4              5

  6              7              8              9              10

  11             12             13             14             15

  16             17             18             19             20

  21             22             23             24             25
  -------------- -------------- -------------- -------------- --------------

**Kernel (3×3 Averaging Filter):**

  ----------------------- ----------------------- -----------------------
  1/9                     1/9                     1/9

  1/9                     1/9                     1/9

  1/9                     1/9                     1/9
  ----------------------- ----------------------- -----------------------

**Output Feature Map (3×3):**

*Formula: O = I - K + 1 = 5 - 3 + 1 = 3*

The convolution operation slides the 3×3 kernel across the image,
computing the average of the 9 pixels it covers at each position. This
produces a smaller output image that represents local averages.

3.2.2 Mathematical Definition

**1D Convolution:**

*(f \* g)(t) = Σ f(τ) × g(t - τ)*

Where f is the signal, \* is the convolution operator, and g is the
kernel. Note that in the mathematical definition, the kernel is inverted
(flipped).

**2D Feature Map Output Dimensions:**

*O = I - K + 1*

-   **O:** Output dimension (width or height)

-   **I:** Input dimension

-   **K:** Kernel size

**Example:** A 5×5 input with a 3×3 kernel produces a 3×3 output (5 -
3 + 1 = 3).

3.3 Kernels and Feature Detection

Kernels are the fundamental building blocks of CNNs. Different kernel
weights detect different features or patterns in images.

3.3.1 Common Kernel Types

+-----------------+-----------------+-----------------------------------+
| **Kernel Type** | **Weights**     | **Purpose**                       |
+-----------------+-----------------+-----------------------------------+
| **Vertical Edge | \[-1 0 +1\]     | Detects vertical lines and edges  |
| Detector**      |                 | by identifying horizontal changes |
|                 | \[-1 0 +1\]     | in intensity                      |
|                 |                 |                                   |
|                 | \[-1 0 +1\]     |                                   |
+-----------------+-----------------+-----------------------------------+
| **Horizontal    | \[+1 +1 +1\]    | Detects horizontal lines and      |
| Edge Detector** |                 | edges by identifying vertical     |
|                 | \[ 0 0 0\]      | changes in intensity              |
|                 |                 |                                   |
|                 | \[-1 -1 -1\]    |                                   |
+-----------------+-----------------+-----------------------------------+
| **B             | \[1/9 1/9 1/9\] | Smooths the image by averaging    |
| lur/Averaging** |                 | neighboring pixels, reducing      |
|                 | \[1/9 1/9 1/9\] | noise                             |
|                 |                 |                                   |
|                 | \[1/9 1/9 1/9\] |                                   |
+-----------------+-----------------+-----------------------------------+
| **Sharpen**     | \[ 0 -1 0\]     | Enhances edges and details by     |
|                 |                 | emphasizing differences           |
|                 | \[-1 5 -1\]     |                                   |
|                 |                 |                                   |
|                 | \[ 0 -1 0\]     |                                   |
+-----------------+-----------------+-----------------------------------+
| **Sobel         | \[-1 0 +1\]     | Advanced edge detection with      |
| (Horizontal)**  |                 | emphasis on center pixels         |
|                 | \[-2 0 +2\]     |                                   |
|                 |                 |                                   |
|                 | \[-1 0 +1\]     |                                   |
+-----------------+-----------------+-----------------------------------+

3.3.2 Learning Kernel Weights

Unlike handcrafted kernels, CNNs learn optimal kernel weights through
training:

5.  **Initialize:** Start with random weights for all kernels

6.  **Forward Pass:** Apply kernels to images and compute output

7.  **Backpropagation:** Adjust weights based on classification error

8.  **Optimization:** Through iterative training, kernels learn to
    detect patterns most relevant for classification

Each layer of the network learns different patterns. Early layers detect
simple features like edges and corners, while deeper layers identify
complex patterns like object parts and entire objects.

3.4 Hierarchical Feature Learning

CNNs build a hierarchy of increasingly complex features through multiple
layers:

-   **Layer 1 (Early):** Detects basic features like edges, corners, and
    textures. Operates on small regions with small receptive fields.

-   **Layer 2 (Middle):** Combines basic features into more complex
    patterns like curves, simple shapes, and object parts. Has larger
    receptive fields.

-   **Layer 3+ (Deep):** Recognizes complete objects, faces, and complex
    structures. Has very large receptive fields that capture
    relationships between distant pixels.

**Example:** In a face recognition CNN, layer 1 might detect edges,
layer 2 might identify eye or nose shapes, and layer 3 might recognize
complete faces.

3.5 Feature Maps and Multiple Filters

A single kernel produces a single feature map. To capture various
features, CNNs use multiple kernels in parallel at each layer.

**Example Configuration:**

-   **Input:** 28×28 grayscale image (single channel)

-   **Filters:** 32 different 3×3 kernels applied in parallel

-   **Output:** 32 feature maps, each 26×26 pixels (using O = 28 - 3 + 1
    = 26)

-   **Result:** A tensor of dimensions 26×26×32

Each of the 32 filters learns to detect different features. One might
detect vertical edges, another horizontal edges, another curves, and so
on. The number of kernels defines the depth (number of channels) of the
output.

3.6 Key Architectural Components

3.6.1 Padding

Convolution naturally reduces the spatial dimensions of feature maps.
Padding addresses this issue by adding borders around the input.

  ----------------- -------------------------- --------------------------
  **Strategy**      **Description**            **Formula**

  **Valid Padding** No padding added. Output   O = I - K + 1
                    is smaller than input.     

  **Same Padding**  Add zeros around borders.  O = I
                    Output size equals input   
                    size. Padding width = K/2. 
  ----------------- -------------------------- --------------------------

3.6.2 Stride

Stride controls how many pixels the kernel moves at each step:

-   **Stride = 1:** Kernel moves one pixel at a time (default, preserves
    maximum information)

-   **Stride = 2:** Kernel moves two pixels at a time, reducing output
    size by approximately half

-   **Stride \> 2:** Further dimensionality reduction, though less
    common

Larger strides are an efficient way to reduce spatial dimensions and
computational cost, often used in place of or in combination with
pooling layers.

3.6.3 General Output Dimensions Formula

The complete formula incorporating padding and stride:

*H*out *= ⌊(Hin - K + 2P) / S⌋ + 1*

**Where:**

-   *H*out: Output height (or width)

-   *H*in: Input height (or width)

-   **K:** Kernel size

-   **P:** Padding size

-   **S:** Stride size

-   **⌊ ⌋:** Floor function (round down)

4\. Image Preprocessing for Neural Networks

Proper preprocessing is crucial for effective neural network training
and inference.

4.1 Standard Preprocessing Steps

9.  **Resize:** Convert all images to uniform dimensions. For example,
    resize all images to 224×224 pixels. This ensures consistent input
    dimensions across the dataset.

10. **Normalize:** Scale pixel values to a standard range (typically 0
    to 1). This improves training stability and convergence speed.

11. **Reshape:** For color images, organize data into a tensor with
    dimensions (height × width × channels). For example, a color image
    becomes a tensor of shape (224, 224, 3) where 3 represents RGB
    channels.

4.2 Normalization Strategies

  ----------------- ----------------- ---------------------- ------------------
  **Method**        **Range**         **Formula**            **Use Case**

  **Min-Max         0 to 1            (I - min) / (max -     Default for most
  \[0,1\]**                           min)                   CNNs

  **Min-Max         -1 to 1           2(I-min)/(max-min) - 1 GANs, Tanh
  \[-1,1\]**                                                 activation

  **Z-Score**       Zero-centered     (I - μ) / σ            Standardization,
                                                             when data has
                                                             different scales
  ----------------- ----------------- ---------------------- ------------------

***Note:** For color images, normalization is typically applied
separately to each color channel (R, G, B).*

4.3 Data Augmentation

When training data is limited, augmentation artificially expands the
dataset by creating modified versions of existing images:

-   **Rotation:** Rotate images by various angles (e.g., ±15 degrees)

-   **Translation:** Shift images horizontally and vertically

-   **Flipping:** Mirror images horizontally or vertically

-   **Zooming:** Apply random zoom in/out

-   **Brightness/Contrast:** Adjust lighting conditions

Python libraries such as Keras\' ImageDataGenerator and Albumentations
provide built-in augmentation capabilities, making it easy to apply
these transformations during training.

5\. Mathematical Properties of Convolution

Understanding the mathematical properties of convolution helps explain
why CNNs work so effectively:

12. **Commutativity:** *f \* g = g \* f* --- It doesn\'t matter whether
    the kernel slides over the image or the image slides under the
    kernel; the result is the same.

13. **Associativity:** *(f \* g) \* h = f \* (g \* h)* --- When applying
    multiple kernels sequentially, the order of grouping doesn\'t
    matter.

14. **Linearity:** Convolution operations can be decomposed and
    distributed, enabling efficient computation.

15. **Translation Equivariance:** If the input image shifts, the output
    feature map shifts by the same amount. This is a key advantage over
    fully connected networks, which lack this property.

5.1 Convolution vs. Correlation

In strict mathematical terms, **convolution** involves flipping
(inverting) the kernel before sliding it across the input.
**Correlation** slides the kernel without flipping.

In practice, most deep learning frameworks implement correlation but
call it convolution. Since kernels are learned through backpropagation
(not hand-designed), the distinction becomes irrelevant --- the network
learns appropriate weights regardless of whether the operation is
technically convolution or correlation.

6\. Computational Efficiency and Parameter Count

6.1 Parameter Sharing in CNNs

One of CNN\'s greatest advantages is parameter sharing. All neurons in a
feature map use the **same kernel weights**. This dramatically reduces
the number of parameters compared to fully connected networks.

**Example:** A 3×3 convolutional kernel has only **10 parameters** (9
weights + 1 bias), regardless of the input image size. In contrast, a
fully connected layer connecting a 28×28 image (784 pixels) to just 100
neurons would require **78,400 parameters** (784 × 100).

6.2 GPU Acceleration

Convolution operations are essentially matrix multiplications, which
GPUs are specifically optimized for. Since the same kernel is applied
across the entire image in parallel, CNNs can leverage GPU parallelism
extremely efficiently, resulting in much faster training and inference
compared to fully connected networks.

7\. CNNs vs. Fully Connected Networks: Comparison

  ----------------- -------------------------- --------------------------
  **Aspect**        **Fully Connected**        **Convolutional**

  **Spatial         Lost - images flattened to Preserved - maintains 2D
  Structure**       1D vectors                 relationships

  **Translation     No - moving objects breaks Yes - detects objects
  Invariance**      recognition                anywhere in image

  **Parameters**    Very high - every          Low - weight sharing
                    connection has unique      across image
                    weight                     

  **Training        Slow - many parameters to  Fast - GPU-optimized
  Speed**           update                     parallel operations

  **Overfitting     High - too many parameters Lower - fewer parameters,
  Risk**            for available data         better generalization

  **Memory Usage**  Very high                  Much lower

  **Feature         Position-dependent         Hierarchical features
  Learning**        brightness patterns        (edges → parts → objects)
  ----------------- -------------------------- --------------------------

8\. Conclusion

Convolutional Neural Networks represent a fundamental breakthrough in
image processing and computer vision. By preserving spatial structure,
sharing parameters, and building hierarchical representations, CNNs
overcome the key limitations of fully connected networks.

**Key Takeaways:**

-   Fully connected networks flatten images, losing spatial context and
    requiring enormous parameter counts

-   CNNs preserve 2D structure through local connectivity and maintain
    translation invariance

-   Convolution operations use learnable kernels to detect features at
    multiple scales

-   Parameter sharing dramatically reduces model complexity and training
    time

-   Proper preprocessing (resizing, normalization, augmentation) is
    essential for success

-   CNNs build hierarchical representations from simple features to
    complex objects

These principles have made CNNs the dominant architecture for image
classification, object detection, facial recognition, medical imaging
analysis, and countless other visual recognition tasks. Understanding
these fundamentals provides the foundation for working with modern deep
learning architectures and developing effective computer vision
solutions.

─────────────────────────────────────────────

*Document prepared based on lecture by Dr. Yoram Segal*
