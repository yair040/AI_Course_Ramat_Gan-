# Planning Document
## Logistic Regression Implementation

**Author:** Yair Levi
**Date:** 2025-11-16
**Project:** Gradient Descent Logistic Regression

---

## 1. Architecture Overview

### 1.1 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                       main.py                           │
│            (Orchestrator & Entry Point)                 │
└────────────┬────────────────────────────────────────────┘
             │
             ├──────────────┬──────────────┬──────────────┬──────────────┐
             │              │              │              │              │
             ▼              ▼              ▼              ▼              ▼
    ┌────────────┐  ┌──────────────┐ ┌──────────┐ ┌─────────────┐ ┌────────┐
    │   data_    │  │  logistic_   │ │  visual_ │ │   utils.py  │ │ config │
    │ generator  │  │   model.py   │ │ ization  │ │  (helpers)  │ │  (opt) │
    │   .py      │  │   (core ML)  │ │   .py    │ │             │ │        │
    └────────────┘  └──────────────┘ └──────────┘ └─────────────┘ └────────┘
```

### 1.2 Data Flow

```
1. [Generate Data] → Dataset (X, y)
                      ↓
2. [Initialize Model] → Random β values
                      ↓
3. [Training Loop] → Compute p → Calculate gradient → Update β
                      ↓
4. [Predictions] → Final p values & classifications
                      ↓
5. [Visualize] → Plots & GUI Tables
```

---

## 2. Module Design

### 2.1 main.py (Entry Point)
**Responsibilities:**
- Parse command-line arguments (optional)
- Initialize all components
- Execute workflow in correct order
- Handle high-level error management

**Key Functions:**
```python
def main():
    """Main execution function"""
    # 1. Generate dataset
    # 2. Initialize model
    # 3. Train model
    # 4. Generate predictions
    # 5. Calculate metrics
    # 6. Visualize results

def parse_arguments():
    """Parse CLI arguments (optional)"""

def print_summary(beta, metrics):
    """Print training summary to console"""
```

**Estimated Lines:** 120-150

---

### 2.2 data_generator.py
**Responsibilities:**
- Generate synthetic dataset
- Ensure data quality and correctness
- Provide data statistics

**Key Functions:**
```python
def generate_dataset(n_samples_per_class=1000, random_seed=None):
    """
    Generate two-class dataset

    Returns:
        X (np.ndarray): Features matrix (2000, 3)
        y (np.ndarray): Labels vector (2000,)
    """

def generate_class_data(n_samples, x1_range, x2_range):
    """Generate data for single class"""

def validate_dataset(X, y):
    """Validate dataset properties"""

def get_dataset_statistics(X, y):
    """Calculate dataset statistics"""
```

**Estimated Lines:** 100-130

---

### 2.3 logistic_model.py
**Responsibilities:**
- Implement sigmoid function
- Calculate gradients
- Train model using gradient descent
- Make predictions

**Key Functions:**
```python
def sigmoid(z):
    """
    Compute sigmoid function
    z = β₀ + β₁*x₁ + β₂*x₂

    Args:
        z (np.ndarray): Linear combination

    Returns:
        np.ndarray: Probabilities in [0, 1]
    """

def compute_probabilities(X, beta):
    """
    Compute p(i) for all samples

    Args:
        X (np.ndarray): Features (n, 3)
        beta (np.ndarray): Coefficients (3,)

    Returns:
        np.ndarray: Probabilities (n,)
    """

def compute_gradient(X, y, p):
    """
    Compute gradient: g = X^T(y - p)

    Args:
        X (np.ndarray): Features (n, 3)
        y (np.ndarray): Labels (n,)
        p (np.ndarray): Probabilities (n,)

    Returns:
        np.ndarray: Gradient (3,)
    """

def compute_log_likelihood(y, p):
    """
    Compute log-likelihood
    LL = Σ[y*log(p) + (1-y)*log(1-p)]
    """

def train_model(X, y, learning_rate=0.3, max_iterations=1000, tolerance=1e-6):
    """
    Train logistic regression using gradient descent

    Args:
        X: Features matrix
        y: Labels vector
        learning_rate: η (eta)
        max_iterations: Max training iterations
        tolerance: Convergence threshold

    Returns:
        beta: Final coefficients
        history: Training history (likelihood, errors)
    """

def predict(X, beta, threshold=0.5):
    """
    Make binary predictions

    Returns:
        predictions: Binary labels (0 or 1)
        probabilities: Predicted probabilities
    """

def initialize_beta(random_seed=None):
    """Initialize β₀, β₁, β₂ randomly in [-1, 1]"""
```

**Estimated Lines:** 180-200

---

### 2.4 visualization.py
**Responsibilities:**
- Create scatter plots with classifications
- Generate training progress plots
- Display results table in GUI

**Key Functions:**
```python
def plot_classification_results(X, y, predictions, beta):
    """
    Create scatter plot with:
    - Two classes in different colors
    - Red X for misclassifications
    - Decision boundary (optional)
    """

def plot_training_progress(history):
    """
    Create dual subplot:
    - Log-likelihood vs iteration
    - Average error vs iteration
    """

def display_results_table(X, y, predictions, probabilities):
    """
    Display results in GUI table using tkinter
    Shows: x₀, x₁, x₂, y, prediction, error
    Include pagination for 2000 rows
    """

def plot_decision_boundary(X, beta, ax):
    """
    Plot decision boundary line (optional enhancement)
    Line where β₀ + β₁*x₁ + β₂*x₂ = 0
    """

def show_all_plots():
    """Display all matplotlib figures"""
```

**Estimated Lines:** 150-180

---

### 2.5 utils.py
**Responsibilities:**
- Helper functions
- Metrics calculations
- Error handling utilities

**Key Functions:**
```python
def calculate_average_error(y, p, n):
    """
    Calculate average error: Σ(y - p)² / (n - 1)

    Args:
        y: True labels
        p: Predicted probabilities
        n: Number of samples

    Returns:
        float: Average error
    """

def calculate_accuracy(y_true, y_pred):
    """Calculate classification accuracy"""

def format_equation(beta):
    """
    Format sigmoid equation for display
    Returns: "p(x) = 1 / (1 + e^-(β₀ + β₁*x₁ + β₂*x₂))"
    """

def save_results(filepath, data):
    """Save results to file (optional)"""

def load_results(filepath):
    """Load results from file (optional)"""

def print_training_status(iteration, likelihood, error):
    """Print formatted training progress"""
```

**Estimated Lines:** 100-130

---

## 3. Data Structures

### 3.1 Core Data Types

```python
# Features Matrix
X: np.ndarray
    shape: (2000, 3)
    dtype: float64
    columns: [x₀, x₁, x₂]
    x₀ = 1 (bias term)

# Labels Vector
y: np.ndarray
    shape: (2000,)
    dtype: int or float
    values: 0 or 1

# Coefficients Vector
beta: np.ndarray
    shape: (3,)
    dtype: float64
    elements: [β₀, β₁, β₂]

# Probabilities Vector
p: np.ndarray
    shape: (2000,)
    dtype: float64
    range: [0, 1]

# Predictions Vector
predictions: np.ndarray
    shape: (2000,)
    dtype: int
    values: 0 or 1

# Training History
history: dict
    {
        'iterations': List[int],
        'log_likelihood': List[float],
        'average_error': List[float],
        'beta_values': List[np.ndarray]
    }
```

---

## 4. Algorithm Implementation Details

### 4.1 Gradient Descent Pseudocode

```
INPUT: X (features), y (labels), η (learning rate)
OUTPUT: β (optimal coefficients), history (training log)

1. INITIALIZE:
   β ← random values in [-1, 1]
   history ← empty dict
   iteration ← 0

2. REPEAT until convergence or max_iterations:
   a. Compute linear combination: z = X @ β
   b. Compute probabilities: p = sigmoid(z)
   c. Compute gradient: g = X.T @ (y - p)
   d. Update parameters: β = β + η * g
   e. Compute log-likelihood: LL = Σ[y*log(p) + (1-y)*log(1-p)]
   f. Compute average error: err = Σ(y - p)² / (n - 1)
   g. Store in history: iteration, LL, err, β
   h. iteration ← iteration + 1

   i. CHECK convergence:
      IF |g| < tolerance OR iteration >= max_iterations:
         BREAK

3. RETURN β, history
```

### 4.2 Matrix Dimensions Check

```
Operation: g = X^T(y - p)

X:     (2000, 3)
X^T:   (3, 2000)
y:     (2000,)
p:     (2000,)
(y-p): (2000,)

X^T @ (y-p): (3, 2000) @ (2000,) = (3,)
Result g:    (3,) ✓ Correct
```

---

## 5. Error Handling Strategy

### 5.1 Input Validation
- Check X dimensions: must be (n, 3)
- Check y dimensions: must be (n,)
- Check y values: must be 0 or 1
- Check β dimensions: must be (3,)

### 5.2 Numerical Stability
- Clip probabilities: avoid log(0)
  ```python
  p = np.clip(p, 1e-15, 1 - 1e-15)
  ```
- Check for NaN or Inf values
- Handle overflow in exponential

### 5.3 Convergence Issues
- Warning if not converged after max iterations
- Track gradient norm
- Option to increase max_iterations

---

## 6. Testing Strategy

### 6.1 Unit Tests
- Test sigmoid function with known values
- Test gradient calculation with small dataset
- Test data generation ranges and sizes
- Test error calculations

### 6.2 Integration Tests
- Test full pipeline with small dataset
- Verify convergence behavior
- Check visualization generation

### 6.3 Validation
- Manually verify on simple linearly separable data
- Check that likelihood increases over iterations
- Verify error decreases over iterations

---

## 7. Performance Considerations

### 7.1 Optimization Opportunities
- Use vectorized NumPy operations (no loops)
- Pre-allocate arrays for history
- Batch matrix operations

### 7.2 Expected Performance
- Data generation: < 0.1s
- Training (1000 iterations): < 5s
- Visualization: < 2s
- Total runtime: < 10s

---

## 8. Development Workflow

### Phase 1: Core Implementation (Days 1-2)
1. Set up virtual environment
2. Implement data_generator.py
3. Implement logistic_model.py core functions
4. Test training loop with small dataset

### Phase 2: Training & Metrics (Day 3)
1. Implement full training loop
2. Add convergence detection
3. Implement metrics in utils.py
4. Test on full 2000-sample dataset

### Phase 3: Visualization (Day 4)
1. Implement scatter plot
2. Implement training progress plots
3. Implement GUI table display
4. Polish visualizations

### Phase 4: Integration & Testing (Day 5)
1. Integrate all modules in main.py
2. End-to-end testing
3. Bug fixes and refinements
4. Documentation updates

---

## 9. Configuration Parameters

```python
# Dataset Configuration
N_SAMPLES_PER_CLASS = 1000
CLASS_0_X1_RANGE = (0.1, 0.4)
CLASS_0_X2_RANGE = (0.1, 0.4)
CLASS_1_X1_RANGE = (0.6, 0.9)
CLASS_1_X2_RANGE = (0.6, 0.9)

# Model Configuration
LEARNING_RATE = 0.3  # η
MAX_ITERATIONS = 1000
CONVERGENCE_TOLERANCE = 1e-6
BETA_INIT_RANGE = (-1, 1)

# Visualization Configuration
FIGURE_SIZE = (12, 5)
DPI = 100
CLASS_0_COLOR = 'blue'
CLASS_1_COLOR = 'green'
MISCLASS_MARKER = 'rx'
```

---

## 10. File Structure

```
logistic_regression/
│
├── main.py                    # Entry point
├── data_generator.py          # Dataset creation
├── logistic_model.py          # Core ML logic
├── visualization.py           # Plots and GUI
├── utils.py                   # Helper functions
│
├── requirements.txt           # Dependencies
├── PRD.md                     # Product requirements
├── planning.md               # This file
├── tasks.md                  # Task breakdown
├── Claude.md                 # AI assistant context
├── README.md                 # User guide (to be created)
│
├── venv/                     # Virtual environment (not in repo)
├── .gitignore               # Git ignore rules (optional)
│
└── output/                  # Results directory (optional)
    ├── plots/
    └── logs/
```

---

## 11. Dependencies Rationale

### NumPy
- Matrix operations (X^T, matrix multiplication)
- Random number generation
- Mathematical functions (exp, log)
- Array operations

### Matplotlib
- Scatter plots for classification results
- Line plots for training progress
- Subplot management
- Customizable visualizations

### Tkinter
- Native Python GUI toolkit
- Table/treeview widgets for data display
- Cross-platform compatibility
- No additional installation needed

---

## 12. Risk Analysis

### Risk 1: Non-Convergence
**Probability:** Medium
**Impact:** High
**Mitigation:**
- Use proven learning rate (0.3)
- Implement convergence checks
- Add maximum iteration limit
- Provide diagnostic output

### Risk 2: GUI Display in WSL
**Probability:** Medium
**Impact:** Medium
**Mitigation:**
- Ensure X server is configured
- Test with WSL2 WSLg
- Provide fallback to save plots as images
- Document GUI setup steps

### Risk 3: Numerical Instability
**Probability:** Low
**Impact:** Medium
**Mitigation:**
- Clip probabilities before log
- Use numerically stable sigmoid
- Check for NaN/Inf values
- Add error handling

### Risk 4: File Size Exceeding 200 Lines
**Probability:** Low
**Impact:** Low
**Mitigation:**
- Plan modular design upfront
- Extract helper functions
- Keep functions focused
- Regular refactoring

---

## 13. Success Metrics

1. **Code Quality:**
   - All files < 200 lines ✓
   - No pylint warnings ✓
   - Clear documentation ✓

2. **Functionality:**
   - Convergence within 1000 iterations ✓
   - Accuracy > 95% on dataset ✓
   - All visualizations working ✓

3. **Performance:**
   - Total runtime < 30 seconds ✓
   - Smooth GUI rendering ✓

4. **User Experience:**
   - Clear console output ✓
   - Intuitive visualizations ✓
   - Easy to run and understand ✓

---

## End of Planning Document
