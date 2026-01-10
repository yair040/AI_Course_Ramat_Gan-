# The Discrete Update Algorithm

## Solving the AND Gate with a Perceptron

**Author:** Yair Levi

---

## Overview

This document demonstrates how a perceptron can learn to solve the AND gate logic function using the discrete update algorithm. The perceptron iteratively adjusts its weights until it correctly classifies all input combinations.

## AND Gate Truth Table

| X0 | X1 | X2 | Output |
|----|----|----|--------|
| 1  | 0  | 0  | 0      |
| 1  | 0  | 1  | 0      |
| 1  | 1  | 0  | 0      |
| 1  | 1  | 1  | 1      |

*Note: X0 is always 1 (bias term)*

## Perceptron Model

The perceptron computes its output as:

```
Output = W0*X0 + W1*X1 + W2*X2
```

Since X0 = 1:

```
Output = W0 + W1*X1 + W2*X2
```

The activation function used is the **Sign()** function, which outputs:
- Positive values → 1
- Zero or negative values → 0

## Training Process

### Initial Weights
Starting with random weights: **W = [3, -2, 5]**

### Training Summary

The perceptron undergoes **8 epochs** of training, processing all 4 input combinations in each epoch. During training, weights are adjusted whenever the perceptron's output doesn't match the expected output.

**Weight Update Rules:**
- When output should be 0 but Y > 0: Decrease weights
- When output should be 1 but Y ≤ 0: Increase weights

### Convergence

After 8 epochs (32 total iterations), the perceptron converges to:

**Final Weights: W = [-3, 2, 2]**

- W0 = -3 (bias)
- W1 = 2
- W2 = 2

At this point, all four input patterns are correctly classified.

## Decision Boundary

The separation line between the two classes is found by setting the output to 0:

```
0 = W0 + W1*X1 + W2*X2
X2 = -(W1/W2)*X1 - (W0/W2)
X2 = -X1 + 1.5
```

This line passes through the points **(0, 1.5)** and **(1.5, 0)**.

### Classification Rule
- **Below the line:** Output = 0
- **Above the line:** Output = 1

The AND gate requires both X1 AND X2 to be 1 for a positive output, which the learned decision boundary correctly captures.

## Visualization

```
X2
 │
1.5 ●────────
 │   ╲
 │    ╲
 │     ╲ 
1│      ╲ (1,1) [Output=1]
 │       ╲
 │        ●
 │
 └─────────● X1
          1.5
```

Points (0,0), (0,1), and (1,0) fall below the line (Output = 0)  
Point (1,1) falls above the line (Output = 1)

## Key Insights

1. The perceptron successfully learns a linear decision boundary to separate the AND gate outputs
2. The discrete update algorithm iteratively refines weights until convergence
3. The AND gate is **linearly separable**, making it solvable by a single-layer perceptron
4. Training required 8 epochs to achieve perfect classification

---

## Implementation Notes

This example demonstrates the fundamental learning capability of perceptrons for linearly separable problems. The discrete update algorithm (also known as the perceptron learning rule) guarantees convergence for such problems.