# Development Tasks
## Logistic Regression Project

**Author:** Yair Levi
**Date:** 2025-11-16

---

## Task Overview

This document breaks down the development into manageable tasks, organized by module and priority.

---

## Phase 1: Environment Setup

### Task 1.1: Virtual Environment Setup ⚙️
**Priority:** HIGH
**Estimated Time:** 15 minutes

**Steps:**
1. Open WSL terminal
2. Navigate to project directory
3. Create virtual environment:
   ```bash
   python3 -m venv venv
   ```
4. Activate virtual environment:
   ```bash
   source venv/bin/activate
   ```
5. Verify activation (should show `(venv)` prefix)

**Acceptance Criteria:**
- Virtual environment created successfully
- Can activate/deactivate venv
- Python executable points to venv

---

### Task 1.2: Install Dependencies 📦
**Priority:** HIGH
**Estimated Time:** 10 minutes

**Steps:**
1. Ensure venv is activated
2. Create requirements.txt (see separate task)
3. Install packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Verify installations:
   ```bash
   pip list
   ```

**Acceptance Criteria:**
- NumPy installed successfully
- Matplotlib installed successfully
- All dependencies available for import

---

## Phase 2: Data Generation Module

### Task 2.1: Create data_generator.py Structure 📄
**Priority:** HIGH
**Estimated Time:** 20 minutes

**Steps:**
1. Create file: `data_generator.py`
2. Add file docstring
3. Import numpy
4. Define module constants:
   ```python
   N_SAMPLES_PER_CLASS = 1000
   CLASS_0_RANGES = {'x1': (0.1, 0.4), 'x2': (0.1, 0.4)}
   CLASS_1_RANGES = {'x1': (0.6, 0.9), 'x2': (0.6, 0.9)}
   ```

**Acceptance Criteria:**
- File created with proper structure
- Imports work correctly
- Constants defined

---

### Task 2.2: Implement generate_class_data() Function
**Priority:** HIGH
**Estimated Time:** 25 minutes

**Steps:**
1. Create function signature:
   ```python
   def generate_class_data(n_samples, x1_range, x2_range, random_seed=None)
   ```
2. Set random seed if provided
3. Generate x₁ values using `np.random.uniform()`
4. Generate x₂ values using `np.random.uniform()`
5. Create x₀ column (all ones)
6. Stack into (n_samples, 3) array
7. Add docstring and type hints
8. Add input validation

**Acceptance Criteria:**
- Returns array of shape (n_samples, 3)
- x₀ column is all 1s
- x₁ values within specified range
- x₂ values within specified range
- Reproducible with random_seed

**Test:**
```python
data = generate_class_data(10, (0.1, 0.4), (0.1, 0.4), random_seed=42)
assert data.shape == (10, 3)
assert np.all(data[:, 0] == 1)
assert np.all((data[:, 1] >= 0.1) & (data[:, 1] <= 0.4))
```

---

### Task 2.3: Implement generate_dataset() Function
**Priority:** HIGH
**Estimated Time:** 30 minutes

**Steps:**
1. Create function signature:
   ```python
   def generate_dataset(n_samples_per_class=1000, random_seed=None)
   ```
2. Generate Class 0 data using generate_class_data()
3. Generate Class 1 data using generate_class_data()
4. Create labels: y₀ = 0, y₁ = 1
5. Concatenate X matrices vertically
6. Concatenate y vectors
7. Optionally shuffle data
8. Add docstring with return types
9. Add validation

**Acceptance Criteria:**
- Returns X (2000, 3) and y (2000,)
- First 1000 samples have y=0
- Last 1000 samples have y=1
- Data ranges correct for each class
- Reproducible results

**Test:**
```python
X, y = generate_dataset(n_samples_per_class=1000, random_seed=42)
assert X.shape == (2000, 3)
assert y.shape == (2000,)
assert np.sum(y == 0) == 1000
assert np.sum(y == 1) == 1000
```

---

### Task 2.4: Implement Dataset Validation & Statistics
**Priority:** MEDIUM
**Estimated Time:** 20 minutes

**Steps:**
1. Create `validate_dataset(X, y)` function
   - Check shapes
   - Check value ranges
   - Check for NaN/Inf
2. Create `get_dataset_statistics(X, y)` function
   - Mean, std per feature
   - Class distribution
   - Feature ranges

**Acceptance Criteria:**
- Validation catches malformed data
- Statistics provide useful insights
- Functions have clear output format

---

## Phase 3: Logistic Model Module

### Task 3.1: Create logistic_model.py Structure 📄
**Priority:** HIGH
**Estimated Time:** 15 minutes

**Steps:**
1. Create file: `logistic_model.py`
2. Add file docstring explaining logistic regression
3. Import numpy
4. Define constants:
   ```python
   LEARNING_RATE = 0.3
   MAX_ITERATIONS = 1000
   TOLERANCE = 1e-6
   ```

**Acceptance Criteria:**
- File structure ready
- Constants defined

---

### Task 3.2: Implement sigmoid() Function
**Priority:** HIGH
**Estimated Time:** 20 minutes

**Steps:**
1. Create function:
   ```python
   def sigmoid(z):
       """Compute sigmoid: 1 / (1 + exp(-z))"""
   ```
2. Implement using NumPy:
   ```python
   return 1 / (1 + np.exp(-z))
   ```
3. Handle numerical overflow:
   - Clip z to prevent overflow
   - Use np.clip(z, -500, 500)
4. Add docstring and examples
5. Add type hints

**Acceptance Criteria:**
- Returns values in [0, 1]
- Handles large positive/negative inputs
- Vectorized (works on arrays)

**Test:**
```python
assert sigmoid(0) == 0.5
assert sigmoid(100) > 0.99
assert sigmoid(-100) < 0.01
assert sigmoid(np.array([0, 1])).shape == (2,)
```

---

### Task 3.3: Implement initialize_beta() Function
**Priority:** HIGH
**Estimated Time:** 15 minutes

**Steps:**
1. Create function:
   ```python
   def initialize_beta(random_seed=None)
   ```
2. Set random seed if provided
3. Generate 3 random values in [-1, 1]
4. Return as NumPy array

**Acceptance Criteria:**
- Returns array of shape (3,)
- Values in range [-1, 1]
- Reproducible with seed

**Test:**
```python
beta = initialize_beta(random_seed=42)
assert beta.shape == (3,)
assert np.all(beta >= -1) and np.all(beta <= 1)
```

---

### Task 3.4: Implement compute_probabilities() Function
**Priority:** HIGH
**Estimated Time:** 25 minutes

**Steps:**
1. Create function:
   ```python
   def compute_probabilities(X, beta)
   ```
2. Compute linear combination: z = X @ beta
3. Apply sigmoid: p = sigmoid(z)
4. Clip probabilities for numerical stability
5. Add docstring and validation

**Acceptance Criteria:**
- Returns array of shape (n,)
- All values in (0, 1)
- Correct matrix multiplication

**Test:**
```python
X = np.array([[1, 0.2, 0.3], [1, 0.8, 0.7]])
beta = np.array([0, 1, 1])
p = compute_probabilities(X, beta)
assert p.shape == (2,)
assert np.all((p > 0) & (p < 1))
```

---

### Task 3.5: Implement compute_gradient() Function
**Priority:** HIGH
**Estimated Time:** 25 minutes

**Steps:**
1. Create function:
   ```python
   def compute_gradient(X, y, p)
   ```
2. Compute error: error = y - p
3. Compute gradient: g = X.T @ error
4. Verify dimensions: (3, 2000) @ (2000,) = (3,)
5. Add docstring with mathematical formula

**Acceptance Criteria:**
- Returns array of shape (3,)
- Correct matrix transpose and multiplication
- Numerically correct

**Test:**
```python
X = np.array([[1, 0.2, 0.3], [1, 0.8, 0.7]])
y = np.array([0, 1])
p = np.array([0.4, 0.6])
g = compute_gradient(X, y, p)
assert g.shape == (3,)
```

---

### Task 3.6: Implement compute_log_likelihood() Function
**Priority:** MEDIUM
**Estimated Time:** 25 minutes

**Steps:**
1. Create function:
   ```python
   def compute_log_likelihood(y, p)
   ```
2. Clip probabilities: avoid log(0)
   ```python
   p_clipped = np.clip(p, 1e-15, 1 - 1e-15)
   ```
3. Compute:
   ```python
   ll = np.sum(y * np.log(p_clipped) + (1 - y) * np.log(1 - p_clipped))
   ```
4. Return log-likelihood value

**Acceptance Criteria:**
- Returns scalar value
- Handles edge cases (p=0, p=1)
- Increases as model improves

**Test:**
```python
y = np.array([0, 1, 1])
p = np.array([0.1, 0.9, 0.8])
ll = compute_log_likelihood(y, p)
assert isinstance(ll, (float, np.floating))
```

---

### Task 3.7: Implement train_model() Function (Core)
**Priority:** HIGH
**Estimated Time:** 60 minutes

**Steps:**
1. Create function signature with all parameters
2. Initialize β using initialize_beta()
3. Create history dictionary
4. Implement training loop:
   ```python
   for iteration in range(max_iterations):
       # Compute probabilities
       # Compute gradient
       # Update beta
       # Compute log-likelihood
       # Compute error
       # Store history
       # Check convergence
   ```
5. Add convergence check:
   - Gradient norm < tolerance
   - Or max iterations reached
6. Return β and history

**Acceptance Criteria:**
- Converges on test data
- Returns correct β and history
- History contains all required fields
- Respects max_iterations

**Test:**
```python
X, y = generate_dataset(n_samples_per_class=100, random_seed=42)
beta, history = train_model(X, y, max_iterations=100)
assert beta.shape == (3,)
assert 'log_likelihood' in history
assert len(history['log_likelihood']) <= 100
```

---

### Task 3.8: Implement predict() Function
**Priority:** HIGH
**Estimated Time:** 20 minutes

**Steps:**
1. Create function:
   ```python
   def predict(X, beta, threshold=0.5)
   ```
2. Compute probabilities
3. Apply threshold:
   ```python
   predictions = (probabilities >= threshold).astype(int)
   ```
4. Return both predictions and probabilities

**Acceptance Criteria:**
- Returns predictions (0 or 1) and probabilities
- Correct shapes
- Applies threshold correctly

---

## Phase 4: Utilities Module

### Task 4.1: Create utils.py Structure 📄
**Priority:** MEDIUM
**Estimated Time:** 15 minutes

**Steps:**
1. Create file: `utils.py`
2. Add file docstring
3. Import necessary libraries

---

### Task 4.2: Implement calculate_average_error() Function
**Priority:** HIGH
**Estimated Time:** 20 minutes

**Steps:**
1. Create function:
   ```python
   def calculate_average_error(y, p)
   ```
2. Compute squared errors: (y - p)²
3. Sum and divide by (n - 1)
4. Return average error

**Acceptance Criteria:**
- Correct formula implementation
- Returns scalar value
- Handles edge cases

**Test:**
```python
y = np.array([0, 1, 1, 0])
p = np.array([0.1, 0.9, 0.8, 0.2])
avg_err = calculate_average_error(y, p)
assert isinstance(avg_err, (float, np.floating))
assert avg_err >= 0
```

---

### Task 4.3: Implement calculate_accuracy() Function
**Priority:** MEDIUM
**Estimated Time:** 15 minutes

**Steps:**
1. Create function to compute accuracy
2. Compare predictions with true labels
3. Return percentage correct

---

### Task 4.4: Implement format_equation() Function
**Priority:** MEDIUM
**Estimated Time:** 20 minutes

**Steps:**
1. Create function that takes β
2. Format string with Greek letters
3. Return formatted equation string

**Example Output:**
```
p(x) = 1 / (1 + e^-(β₀ + β₁*x₁ + β₂*x₂))
p(x) = 1 / (1 + e^-(0.523 + 2.145*x₁ + 1.876*x₂))
```

---

### Task 4.5: Implement print_training_status() Function
**Priority:** LOW
**Estimated Time:** 15 minutes

**Steps:**
1. Create function for console output
2. Format iteration, likelihood, error
3. Use print with proper formatting

---

## Phase 5: Visualization Module

### Task 5.1: Create visualization.py Structure 📄
**Priority:** HIGH
**Estimated Time:** 15 minutes

**Steps:**
1. Create file: `visualization.py`
2. Import matplotlib.pyplot, numpy
3. Import tkinter
4. Define visualization constants (colors, sizes)

---

### Task 5.2: Implement plot_classification_results() Function
**Priority:** HIGH
**Estimated Time:** 45 minutes

**Steps:**
1. Create function:
   ```python
   def plot_classification_results(X, y, predictions, beta)
   ```
2. Create figure and axis
3. Extract x₁ and x₂ (columns 1 and 2)
4. Create boolean masks for classes
5. Plot Class 0 points (blue)
6. Plot Class 1 points (green)
7. Identify misclassifications: y != predictions
8. Plot red X markers for misclassified points
9. Add title, labels, legend
10. Add grid for readability

**Acceptance Criteria:**
- Two classes clearly distinguished by color
- Misclassifications marked with red X
- Clear labels and legend
- Professional appearance

---

### Task 5.3: Implement plot_training_progress() Function
**Priority:** HIGH
**Estimated Time:** 40 minutes

**Steps:**
1. Create function that takes history dict
2. Create figure with 2 subplots (1 row, 2 cols)
3. **Subplot 1: Log-Likelihood vs Iteration**
   - Plot iterations on x-axis
   - Plot log-likelihood on y-axis
   - Add title, labels, grid
4. **Subplot 2: Average Error vs Iteration**
   - Plot iterations on x-axis
   - Plot average error on y-axis
   - Add title, labels, grid
5. Adjust layout: `plt.tight_layout()`

**Acceptance Criteria:**
- Two subplots side by side
- Clear trends visible
- Proper labels and titles
- Professional formatting

---

### Task 5.4: Implement display_results_table() Function
**Priority:** MEDIUM
**Estimated Time:** 50 minutes

**Steps:**
1. Create function using tkinter
2. Create root window
3. Create Treeview widget with columns:
   - x₀, x₁, x₂, y (true), prediction, error
4. Add scrollbars (vertical and horizontal)
5. Populate with data (2000 rows)
6. Add summary row with average error
7. Configure column widths
8. Add title label
9. Center window on screen

**Acceptance Criteria:**
- All 2000 rows displayed
- Scrolling works smoothly
- Columns properly aligned
- Summary statistics shown
- Window is user-friendly

---

### Task 5.5: Implement show_all_plots() Function
**Priority:** LOW
**Estimated Time:** 10 minutes

**Steps:**
1. Create simple function
2. Call `plt.show()` to display all figures

---

### Task 5.6: (Optional) Implement plot_decision_boundary()
**Priority:** LOW
**Estimated Time:** 30 minutes

**Steps:**
1. Calculate decision boundary line
2. Line equation: β₀ + β₁*x₁ + β₂*x₂ = 0
3. Solve for x₂: x₂ = -(β₀ + β₁*x₁) / β₂
4. Plot line on scatter plot
5. Add to legend

---

## Phase 6: Main Program

### Task 6.1: Create main.py Structure 📄
**Priority:** HIGH
**Estimated Time:** 20 minutes

**Steps:**
1. Create file: `main.py`
2. Add shebang: `#!/usr/bin/env python3`
3. Add file docstring
4. Import all modules
5. Define main() function
6. Add if `__name__ == "__main__"` block

---

### Task 6.2: Implement main() Function
**Priority:** HIGH
**Estimated Time:** 45 minutes

**Steps:**
1. **Step 1: Generate Dataset**
   ```python
   print("Generating dataset...")
   X, y = generate_dataset()
   print(f"Dataset created: {X.shape}")
   ```

2. **Step 2: Initialize Model**
   ```python
   print("Initializing model...")
   # Model initialized in train_model
   ```

3. **Step 3: Train Model**
   ```python
   print("Training model...")
   beta, history = train_model(X, y, learning_rate=0.3)
   print(f"Training complete. Final β: {beta}")
   ```

4. **Step 4: Make Predictions**
   ```python
   print("Making predictions...")
   predictions, probabilities = predict(X, beta)
   ```

5. **Step 5: Calculate Metrics**
   ```python
   avg_error = calculate_average_error(y, probabilities)
   accuracy = calculate_accuracy(y, predictions)
   print(f"Average Error: {avg_error:.6f}")
   print(f"Accuracy: {accuracy:.2%}")
   ```

6. **Step 6: Display Results**
   ```python
   print("\nFinal Sigmoid Equation:")
   print(format_equation(beta))
   ```

7. **Step 7: Create Visualizations**
   ```python
   print("\nGenerating visualizations...")
   plot_classification_results(X, y, predictions, beta)
   plot_training_progress(history)
   display_results_table(X, y, predictions, probabilities)
   show_all_plots()
   ```

**Acceptance Criteria:**
- All steps execute in order
- Clear console output
- Error handling for each step
- Visualizations appear correctly

---

### Task 6.3: Add Error Handling and Logging
**Priority:** MEDIUM
**Estimated Time:** 30 minutes

**Steps:**
1. Wrap main steps in try-except blocks
2. Add meaningful error messages
3. Handle keyboard interrupts gracefully
4. Optional: Add logging module

---

### Task 6.4: (Optional) Add Command-Line Arguments
**Priority:** LOW
**Estimated Time:** 25 minutes

**Steps:**
1. Import argparse
2. Add arguments:
   - `--samples`: Number of samples per class
   - `--learning-rate`: Learning rate
   - `--max-iterations`: Max training iterations
   - `--seed`: Random seed
3. Parse and use in main()

---

## Phase 7: Documentation & Testing

### Task 7.1: Create README.md 📖
**Priority:** MEDIUM
**Estimated Time:** 30 minutes

**Sections:**
1. Project overview
2. Installation instructions
3. Usage guide
4. Expected output
5. Mathematical background
6. Troubleshooting (GUI in WSL)

---

### Task 7.2: Add Docstrings to All Functions
**Priority:** HIGH
**Estimated Time:** 45 minutes

**Steps:**
1. Review each function
2. Add comprehensive docstrings with:
   - Description
   - Args with types
   - Returns with types
   - Examples (where helpful)

---

### Task 7.3: Manual Testing
**Priority:** HIGH
**Estimated Time:** 30 minutes

**Test Cases:**
1. Run with default parameters
2. Run with different random seeds
3. Test with small dataset (debugging)
4. Verify convergence behavior
5. Check all visualizations
6. Test GUI table scrolling

---

### Task 7.4: Verify Line Counts
**Priority:** MEDIUM
**Estimated Time:** 15 minutes

**Steps:**
1. Check each file:
   ```bash
   wc -l *.py
   ```
2. Ensure no file exceeds 200 lines
3. Refactor if necessary

---

## Phase 8: Polish & Deployment

### Task 8.1: Code Review & Refactoring
**Priority:** MEDIUM
**Estimated Time:** 45 minutes

**Steps:**
1. Review code for clarity
2. Check for repeated code
3. Ensure consistent naming
4. Verify PEP 8 compliance

---

### Task 8.2: Performance Optimization
**Priority:** LOW
**Estimated Time:** 30 minutes

**Steps:**
1. Profile code execution
2. Optimize bottlenecks
3. Ensure vectorized operations

---

### Task 8.3: Final Testing & Validation
**Priority:** HIGH
**Estimated Time:** 30 minutes

**Steps:**
1. Fresh virtual environment test
2. Run complete pipeline
3. Verify all outputs
4. Document any issues

---

## Summary of Tasks

**Total Estimated Time:** ~16-18 hours

### By Priority:
- **HIGH:** 18 tasks (~10 hours)
- **MEDIUM:** 9 tasks (~4 hours)
- **LOW:** 5 tasks (~2 hours)

### By Phase:
- Phase 1 (Setup): 25 min
- Phase 2 (Data): 1.5 hours
- Phase 3 (Model): 3.5 hours
- Phase 4 (Utils): 1.5 hours
- Phase 5 (Visualization): 3 hours
- Phase 6 (Main): 2 hours
- Phase 7 (Documentation): 2 hours
- Phase 8 (Polish): 2 hours

---

## Dependencies Between Tasks

```
1.1 → 1.2 → All other tasks
2.1 → 2.2 → 2.3 → 2.4
3.1 → 3.2 → 3.3 → 3.4 → 3.5 → 3.6 → 3.7 → 3.8
4.1 → 4.2, 4.3, 4.4, 4.5
5.1 → 5.2, 5.3, 5.4, 5.5
6.1 → 6.2 (requires all Phase 2-5 complete) → 6.3, 6.4
7.1, 7.2, 7.3, 7.4 (after Phase 6)
8.1, 8.2, 8.3 (after Phase 7)
```

---

## Quick Start Checklist

- [ ] Set up virtual environment
- [ ] Install dependencies
- [ ] Implement data_generator.py
- [ ] Implement logistic_model.py
- [ ] Implement utils.py
- [ ] Implement visualization.py
- [ ] Implement main.py
- [ ] Test end-to-end
- [ ] Create documentation
- [ ] Final validation

---

## End of Tasks Document
