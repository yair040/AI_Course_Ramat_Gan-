# Network Architecture Planning
# Perceptron Gates Implementation

**Author:** Yair Levi
**Date:** 2025-12-30

## 1. Neural Network Architecture Design

### 1.1 AND Gate Network

**Minimum Architecture:**
```
Input Layer: 2 neurons (x1, x2)
   ↓
Hidden Layer: NONE (linearly separable)
   ↓
Output Layer: 1 neuron (output)
```

**Rationale:**
- AND gate is linearly separable
- Single perceptron can learn the decision boundary
- Activation function: Sigmoid (for binary classification)

**Architecture Details:**
- **Input:** (2,) shape
- **Dense Layer 1:** 1 neuron, sigmoid activation
- **Total Parameters:** 3 (2 weights + 1 bias)

**Mathematical Model:**
```
output = σ(w1*x1 + w2*x2 + b)
where σ is sigmoid function
```

### 1.2 XOR Gate Network

**Minimum Architecture:**
```
Input Layer: 2 neurons (x1, x2)
   ↓
Hidden Layer: 2 neurons (minimum for XOR)
   ↓
Output Layer: 1 neuron (output)
```

**Rationale:**
- XOR is NOT linearly separable
- Requires at least 2 hidden neurons to create non-linear decision boundary
- Activation functions:
  - Hidden layer: ReLU or Sigmoid
  - Output layer: Sigmoid

**Architecture Details:**
- **Input:** (2,) shape
- **Dense Layer 1 (Hidden):** 2 neurons, sigmoid activation
- **Dense Layer 2 (Output):** 1 neuron, sigmoid activation
- **Total Parameters:** 9 (2→2: 6 params, 2→1: 3 params)

**Mathematical Model:**
```
h1 = σ(w11*x1 + w12*x2 + b1)
h2 = σ(w21*x1 + w22*x2 + b2)
output = σ(w31*h1 + w32*h2 + b3)
```

## 2. Dataset Design

### 2.1 Truth Tables

**AND Gate:**
| x1 | x2 | output |
|----|-------|--------|
| 0  | 0     | 0      |
| 0  | 1     | 0      |
| 1  | 0     | 0      |
| 1  | 1     | 1      |

**XOR Gate:**
| x1 | x2 | output |
|----|-------|--------|
| 0  | 0     | 0      |
| 0  | 1     | 1      |
| 1  | 0     | 1      |
| 1  | 1     | 0      |

### 2.2 Noise Generation Strategy

**Requirements:**
- 15% noise amplitude
- Positive noise only (move points closer to 1.0)
- 600 samples per gate

**Implementation:**
```python
# Base truth table points (4 unique combinations)
# Replicate each 150 times to get 600 samples
# Add noise: value + random(0, 0.15)
# Clip to valid range [0, 1]
```

**Noise Distribution:**
- Uniform random: [0, 0.15]
- Applied to both inputs and outputs
- Creates realistic "fuzzy" boundaries
- Simulates real-world sensor noise

## 3. Training Strategy

### 3.1 Loss Function
- **Function:** Mean Squared Error (MSE)
- **Formula:** `L = (1/n) * Σ(y_true - y_pred)²`
- **Reason:** Suitable for regression-like continuous outputs

### 3.2 Optimizer
- **Optimizer:** Adam
- **Learning Rate:** Default (0.001)
- **Reason:** Adaptive learning, good convergence

### 3.3 Training Parameters
```python
epochs = 500
batch_size = 32
validation_split = 0.2
```

### 3.4 Expected Convergence
- **AND Gate:** Fast convergence (< 100 epochs)
- **XOR Gate:** Slower convergence (200-400 epochs)

## 4. Visualization Plan

### 4.1 Network Architecture Diagrams

**Tools:** matplotlib with custom drawing or networkx

**AND Gate Visualization:**
```
[x1] ──w1──┐
           ├──> [σ] ──> [output]
[x2] ──w2──┘
      b────┘
```

**XOR Gate Visualization:**
```
        ┌──w11──> [h1] ──w31──┐
[x1] ───┤                      ├──> [σ] ──> [output]
        └──w12──┐              │
                ├──> [h2] ──w32┘
[x2] ───────────┘
```

### 4.2 Data Point Clouds

**2D Scatter Plots:**
- X-axis: x1 input
- Y-axis: x2 input
- Color: output value (0=blue, 1=red)
- Show decision boundary after training

### 4.3 Training History

**Plots:**
- Loss vs Epochs
- Accuracy vs Epochs
- Separate plots for training and validation

## 5. Module Structure

### 5.1 File Organization
```
perceptron_gates/
├── __init__.py
├── logger_config.py      (~50 lines)
├── dataset_generator.py  (~120 lines)
├── models.py             (~80 lines)
├── trainer.py            (~130 lines)
├── visualizer.py         (~145 lines)
├── main.py               (~100 lines)
└── log/                  (created at runtime)
```

### 5.2 Module Dependencies
```
main.py
  ├── logger_config.py
  ├── dataset_generator.py
  ├── models.py
  │    └── keras
  ├── trainer.py
  │    └── models.py
  └── visualizer.py
       └── matplotlib
```

## 6. Multiprocessing Strategy

**Parallelizable Tasks:**
1. Dataset generation (AND and XOR in parallel)
2. Model training (AND and XOR in parallel)
3. Visualization generation (multiple plots in parallel)

**Implementation:**
- Use `multiprocessing.Pool`
- Process count: 2 (for 2 gates)
- Shared results via Queue or file system

## 7. Logging Strategy

### 7.1 Ring Buffer Configuration
```python
max_files = 20
max_bytes = 16 * 1024 * 1024  # 16 MB
log_dir = "./log/"
format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

### 7.2 Log Levels
- INFO: Training progress, dataset creation
- WARNING: Convergence issues
- ERROR: File I/O errors, model failures
- DEBUG: Detailed parameter tracking (optional)

## 8. Success Metrics

**Quantitative:**
- AND accuracy: > 95%
- XOR accuracy: > 95%
- Training time: < 5 min total
- All files < 150 lines

**Qualitative:**
- Clear visualizations
- Comprehensive logs
- Clean code structure
- Proper error handling

## 9. Implementation Order

1. Logger configuration (foundation)
2. Dataset generator (data ready)
3. Models definition (architecture)
4. Trainer (core functionality)
5. Visualizer (outputs)
6. Main orchestrator (integration)
7. Testing and validation
