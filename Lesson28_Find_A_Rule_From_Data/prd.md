# Product Requirements Document (PRD)

## Title
**Finds a Rule from Data**

## Author
Yair Levi

## Target Environment
Google Colab (Python 3.x)

## Project Type
Demo / Educational

---

## 1. Purpose

The purpose of this project is to demonstrate how a **machine can discover a mathematical rule from known input–output data**, using a **neuron-based model implemented with Keras**, evaluated **scalar-by-scalar**, and trained via **backpropagation**.

The discovered rule corresponds to the known **Celsius → Fahrenheit** transformation.

---

## 2. Problem Definition

### 2.1 Known Data (Fixed, No Noise)

**Input (Celsius):**
```python
celsius_q = np.array([-40, -10, 0, 8, 15, 22, 38], dtype=float)
```

**Output (Fahrenheit):**
```python
fahrenheit_a = np.array([-40, 14, 32, 46.4, 59, 71.6, 100], dtype=float)
```

- Data is **known ahead of time**
- No noise injection
- No data augmentation
- Each training step evaluates **a single scalar input → scalar output**

---

## 3. Conceptual Model

### 3.1 Neuron Definition

- Neurons follow the **deep learning abstraction**
- **No activation functions** are allowed
- Neurons perform **pure linear transformations**

Mathematical form:
```
y = w · x + b
```

Multi-neuron models are compositions of such linear neurons.

---

## 4. Learning & Optimization

### 4.1 Backpropagation

- **Backpropagation is mandatory**
- Implemented via **Keras**
- Optimizer: **Adam**
- Learning rate: **0.1**
- Epochs: **500**
- Loss is computed using Mean Squared Error (MSE)

This setup ensures transparent gradient-based learning without nonlinear activations.

---

## 5. Metrics

### 5.1 Primary Metric

**Mean Squared Error (MSE)**
```
MSE = mean((y_true - y_pred)²)
```

Used for:
- Training
- Model comparison
- Convergence evaluation

### 5.2 Post-Training Test Error

After training, the model must be tested on an **unseen scalar input**:

```text
Input: 100°C
Expected Output: 212°F
```

The following must be calculated and printed:
```
absolute_error = |predicted - 212|
```

---

## 6. Tasks

### Task A — Single Neuron Rule Discovery

**Objective:**  
Discover the rule using **one linear neuron**.

**Requirements:**
- Keras `Dense(1)` layer
- Adam optimizer (lr = 0.1)
- 500 epochs

**Outputs:**
- Printed learned equation (w, b)
- MSE training curve
- Neuron diagram including:
  - Input
  - Weight
  - Bias
  - Output
- Prediction for 100°C and absolute error

---

### Task B — Multi-Neuron Rule Discovery

**Objective:**  
Discover the same rule using **more than one linear neuron**.

**Requirements:**
- At least one hidden linear layer
- Adam optimizer (lr = 0.1)
- 500 epochs

**Outputs:**
- Printed effective learned equation
- MSE training curve
- Neuron network diagram including:
  - Input
  - Hidden neurons
  - Weights
  - Biases
  - Output
- Prediction for 100°C and absolute error

---

## 7. Visualization Requirements

### 7.1 Error Visualization

- Plot **MSE vs Epochs** using Keras training history
- One plot per task

### 7.2 Neuron Network Visualization

- After training, draw the neuron network for **each task**
- Diagrams must include:
  - Inputs
  - Outputs
  - Weights
  - Biases
- Visualization can be schematic and Matplotlib-based

---

## 8. Implementation Constraints

- Use **functions**, not task-specific files
- Use **Keras** for model definition and training
- Code must be readable and educational
- No activation functions
- No noise
- No external data

---

## 9. Logging

- Logging level: **INFO**
- Ring buffer logging:
  - 20 files
  - 16 MB per file
  - Circular overwrite
- Logs stored under `log/` directory

---

## 10. Success Criteria

- Correct Celsius → Fahrenheit rule learned
- MSE converges near zero
- Learned equations are printed
- Network diagrams are shown
- 100°C test produces low absolute error
- Runs end-to-end in Google Colab

---

## 11. Explicit Non-Goals

- No classification
- No activation functions
- No noise injection
- No production hardening
