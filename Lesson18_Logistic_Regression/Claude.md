# Claude.md - AI Assistant Context
## Logistic Regression Project

**Author:** Yair Levi
**Purpose:** Guide Claude Code when assisting with this project

---

## Project Overview

This is an educational implementation of **Logistic Regression using Gradient Descent** algorithm. The project demonstrates binary classification from scratch using only NumPy for calculations (no scikit-learn or ML libraries).

**Key Characteristics:**
- Binary classification (2 classes)
- 3D feature space (x₀=1, x₁, x₂)
- 2000 synthetic data points
- Custom gradient descent implementation
- Visualization of results and training progress

---

## Important Constraints

### 1. Library Restrictions
**CRITICAL:** Do NOT use:
- scikit-learn (sklearn)
- TensorFlow, PyTorch, JAX
- Scipy optimization functions
- Any pre-built ML libraries

**ALLOWED:**
- NumPy (for numerical operations)
- Matplotlib (for plotting)
- Tkinter (for GUI tables)

### 2. Code Structure
- **Each Python file must be 150-200 lines maximum**
- Modular design with clear separation of concerns
- Main program orchestrates task execution

### 3. Mathematical Implementation
- All calculations must be implemented manually using NumPy
- Follow the specific formulas provided in PRD.md
- No shortcuts using built-in ML functions

---

## Mathematical Formulas (Reference)

### Sigmoid Function
```
p(i) = 1 / (1 + e^(-(β₀ + β₁*x₁ + β₂*x₂)))
```

### Gradient Calculation
```
g = X^T(y - p)
```
Where:
- X is the feature matrix (2000, 3)
- X^T is the transpose (3, 2000)
- y is labels vector (2000,)
- p is probabilities vector (2000,)
- g is gradient vector (3,)

### Parameter Update
```
β_new = β_old + η * g
```
Where η = 0.3 (learning rate)

### Average Error
```
Average Error = Σ(y - p)² / (n - 1)
```
Where n = 2000 (number of samples)

### Log-Likelihood
```
LL = Σ[y*log(p) + (1-y)*log(1-p)]
```

---

## Module Responsibilities

### data_generator.py (100-130 lines)
**Purpose:** Generate synthetic dataset

**Key Functions:**
- `generate_class_data()`: Create data for one class
- `generate_dataset()`: Create complete 2-class dataset
- `validate_dataset()`: Check data integrity
- `get_dataset_statistics()`: Calculate dataset stats

**Output:**
- X: (2000, 3) array with features
- y: (2000,) array with labels (0 or 1)

---

### logistic_model.py (180-200 lines)
**Purpose:** Core machine learning logic

**Key Functions:**
- `sigmoid(z)`: Compute sigmoid function
- `initialize_beta()`: Random initialization of β in [-1, 1]
- `compute_probabilities(X, beta)`: Calculate p(i) for all samples
- `compute_gradient(X, y, p)`: Calculate g = X^T(y-p)
- `compute_log_likelihood(y, p)`: Calculate log-likelihood
- `train_model(X, y, ...)`: Main gradient descent loop
- `predict(X, beta)`: Make predictions on data

**Critical Details:**
- Clip probabilities to avoid log(0): `np.clip(p, 1e-15, 1-1e-15)`
- Use vectorized NumPy operations (no Python loops for calculations)
- Track history during training (log-likelihood, errors, beta values)

---

### visualization.py (150-180 lines)
**Purpose:** Display results

**Key Functions:**
- `plot_classification_results()`: Scatter plot with:
  - Class 0 in blue
  - Class 1 in green
  - Red X markers for misclassifications
- `plot_training_progress()`: Dual subplot:
  - Log-likelihood vs iteration
  - Average error vs iteration
- `display_results_table()`: Tkinter GUI showing:
  - All samples with features, labels, predictions, errors
  - Average error at bottom
  - Scrollable interface

**GUI Consideration:**
- WSL may require X server for GUI
- Test with WSL2 WSLg (built-in GUI support)
- Provide fallback to save plots if GUI fails

---

### utils.py (100-130 lines)
**Purpose:** Helper functions

**Key Functions:**
- `calculate_average_error(y, p)`: Compute average squared error
- `calculate_accuracy(y_true, y_pred)`: Compute classification accuracy
- `format_equation(beta)`: Format sigmoid equation with β values
- `print_training_status()`: Console output during training

---

### main.py (120-150 lines)
**Purpose:** Orchestrate entire workflow

**Execution Flow:**
1. Generate dataset
2. Train model (gradient descent)
3. Make predictions
4. Calculate metrics
5. Display results (console + visualizations)

---

## Dataset Specifications

### Class 0 (1000 samples)
- Label: y = 0
- x₀: 1 (always)
- x₁: Uniform random in [0.1, 0.4]
- x₂: Uniform random in [0.1, 0.4]

### Class 1 (1000 samples)
- Label: y = 1
- x₀: 1 (always)
- x₁: Uniform random in [0.6, 0.9]
- x₂: Uniform random in [0.6, 0.9]

**Note:** Classes are spatially separated for clear linear separability.

---

## Training Parameters

- **Learning Rate (η):** 0.3
- **Max Iterations:** 1000
- **Convergence Tolerance:** 1e-6 (gradient norm)
- **Initial β:** Random in [-1, 1]

---

## Expected Behavior

### Convergence
- Model should converge within 100-500 iterations
- Log-likelihood should increase monotonically
- Average error should decrease over iterations
- Final accuracy should be > 95% (classes are well-separated)

### Final Output
1. **Console:**
   - Training progress (optional)
   - Final β values
   - Sigmoid equation with numerical values
   - Accuracy and average error

2. **Visualizations:**
   - Scatter plot showing classification
   - Training progress plots
   - GUI table with all results

---

## Common Issues & Solutions

### Issue 1: Overflow in Sigmoid
**Problem:** `exp(-z)` overflows for large |z|
**Solution:** Clip z values before exponential
```python
z = np.clip(z, -500, 500)
```

### Issue 2: Log of Zero
**Problem:** `log(0)` or `log(1)` causes NaN
**Solution:** Clip probabilities
```python
p = np.clip(p, 1e-15, 1 - 1e-15)
```

### Issue 3: GUI Not Displaying in WSL
**Problem:** Tkinter/matplotlib GUI doesn't show
**Solution:**
- Use WSL2 with WSLg (automatic GUI support)
- Or install X server (VcXsrv, Xming)
- Set DISPLAY environment variable
- Fallback: Save plots to files

### Issue 4: File Exceeds 200 Lines
**Problem:** Module getting too long
**Solution:**
- Extract helper functions
- Move constants to separate section
- Simplify complex functions
- Consider splitting into sub-modules if necessary

### Issue 5: Slow Convergence
**Problem:** Model takes too many iterations
**Solution:**
- Check learning rate (should be 0.3)
- Verify gradient calculation
- Check for bugs in update rule
- Ensure proper matrix dimensions

---

## Testing Checklist

When assisting with this project, ensure:

1. **Correctness:**
   - [ ] Sigmoid function outputs values in [0, 1]
   - [ ] Gradient has shape (3,)
   - [ ] Beta update increases log-likelihood
   - [ ] Matrix dimensions match specifications

2. **Functionality:**
   - [ ] Dataset has correct shape (2000, 3) and (2000,)
   - [ ] Training converges
   - [ ] Predictions have correct shape and values
   - [ ] Visualizations display properly

3. **Code Quality:**
   - [ ] Each file < 200 lines
   - [ ] No sklearn or ML libraries used
   - [ ] Clear docstrings and comments
   - [ ] Type hints where appropriate
   - [ ] PEP 8 compliant

4. **Performance:**
   - [ ] Uses vectorized NumPy operations
   - [ ] No unnecessary Python loops
   - [ ] Completes in < 30 seconds

---

## When Helping with Code

### DO:
- ✅ Use NumPy for all numerical operations
- ✅ Implement formulas exactly as specified in PRD
- ✅ Keep functions focused and modular
- ✅ Add comprehensive docstrings
- ✅ Validate input dimensions
- ✅ Handle edge cases (overflow, log(0), etc.)
- ✅ Use Greek letters in comments and output (β, η)
- ✅ Test each function independently

### DON'T:
- ❌ Use scikit-learn or similar ML libraries
- ❌ Import scipy.optimize or pre-built optimizers
- ❌ Skip input validation
- ❌ Use Python loops for vectorizable operations
- ❌ Make files longer than 200 lines
- ❌ Ignore numerical stability issues
- ❌ Forget to transpose matrices correctly

---

## Development Workflow

### Phase 1: Implementation
1. Start with data_generator.py
2. Test data generation independently
3. Implement logistic_model.py step by step
4. Test each function (sigmoid, gradient, etc.)
5. Implement training loop
6. Test convergence on small dataset

### Phase 2: Visualization
1. Implement plotting functions
2. Test with sample data
3. Implement GUI table
4. Test GUI in WSL environment

### Phase 3: Integration
1. Implement main.py
2. Connect all modules
3. End-to-end testing
4. Debug any issues

### Phase 4: Polish
1. Add documentation
2. Verify line counts
3. Code review and refactor
4. Final testing

---

## Debugging Tips

### Matrix Dimension Errors
Print shapes at each step:
```python
print(f"X shape: {X.shape}")
print(f"beta shape: {beta.shape}")
print(f"z shape: {z.shape}")
print(f"g shape: {g.shape}")
```

### Convergence Issues
Track gradient norm:
```python
print(f"Iteration {i}, Gradient norm: {np.linalg.norm(g)}")
```

### Numerical Issues
Check for NaN or Inf:
```python
assert not np.isnan(p).any(), "NaN in probabilities"
assert not np.isinf(p).any(), "Inf in probabilities"
```

---

## Greek Letters for Display

Use Unicode characters for output:
- β (Beta): `\u03B2` or type directly
- η (Eta): `\u03B7`
- Σ (Sigma): `\u03A3`

Example:
```python
print(f"β₀ = {beta[0]:.4f}")
print(f"β₁ = {beta[1]:.4f}")
print(f"β₂ = {beta[2]:.4f}")
print(f"Learning rate η = {learning_rate}")
```

---

## File Structure Reference

```
logistic_regression/
├── main.py                 # Entry point (~140 lines)
├── data_generator.py       # Dataset creation (~120 lines)
├── logistic_model.py       # ML core (~190 lines)
├── visualization.py        # Plots & GUI (~170 lines)
├── utils.py               # Helpers (~120 lines)
├── requirements.txt       # Dependencies
├── PRD.md                 # Requirements doc
├── planning.md            # Architecture doc
├── tasks.md              # Task breakdown
├── Claude.md             # This file
└── README.md             # User guide
```

---

## Quick Reference: Key Equations

| Component | Formula | Notes |
|-----------|---------|-------|
| Sigmoid | p = 1/(1+e^(-z)) | z = X @ β |
| Gradient | g = X^T(y-p) | Shape (3,) |
| Update | β = β + η*g | η = 0.3 |
| Log-likelihood | Σ[y*log(p) + (1-y)*log(1-p)] | Maximize |
| Avg Error | Σ(y-p)²/(n-1) | Minimize |

---

## Success Criteria

The project is successful when:
1. Model converges reliably (< 1000 iterations)
2. Achieves > 95% accuracy on the dataset
3. All visualizations display correctly
4. Code is modular and well-documented
5. Each file is within line limit (< 200 lines)
6. Uses only NumPy for calculations
7. Runs smoothly in WSL virtual environment

---

## Questions to Ask User

If unclear about implementation:
1. "Should we shuffle the dataset after generation?"
2. "Do you want command-line arguments for parameters?"
3. "Should we save plots to files as well as displaying them?"
4. "Do you want logging to a file or just console output?"
5. "Should we implement early stopping if converged?"

---

## Environment Setup Commands

```bash
# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run program
python main.py

# Deactivate when done
deactivate
```

---

## Final Notes

This project is **educational** - the goal is to understand logistic regression from first principles. The implementation should be:
- **Clear:** Easy to understand and follow
- **Correct:** Mathematically accurate
- **Complete:** All requirements met
- **Clean:** Well-organized and documented

The constraints (no ML libraries, line limits, specific formulas) are intentional to ensure deep understanding of the algorithm.

---

## End of Claude.md
