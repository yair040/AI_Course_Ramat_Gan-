# Product Requirements Document (PRD)
## Logistic Regression with Gradient Descent

**Author:** Yair Levi
**Version:** 1.0
**Date:** 2025-11-16
**Platform:** WSL (Windows Subsystem for Linux) with Python Virtual Environment

---

## 1. Executive Summary

This project implements a logistic regression classifier from scratch using the gradient descent algorithm. The program will separate two groups of 3D data points using a sigmoid function, without relying on ML libraries (only NumPy for numerical operations).

---

## 2. Project Goals

- Implement logistic regression algorithm using gradient descent
- Visualize the classification results and training progress
- Demonstrate understanding of ML fundamentals without using scikit-learn
- Provide educational insight into how logistic regression works internally

---

## 3. Technical Requirements

### 3.1 Environment
- **Operating System:** WSL (Windows Subsystem for Linux)
- **Python Version:** 3.8+
- **Virtual Environment:** Required
- **Dependencies:** NumPy, Matplotlib (for visualization), Tkinter (for GUI)

### 3.2 Code Structure
- Modular design with multiple Python files
- Each file should contain 150-200 lines maximum
- Main program orchestrates task execution
- Clear separation of concerns (data generation, training, visualization)

---

## 4. Functional Requirements

### 4.1 Dataset Generation
**Description:** Create synthetic dataset with two distinct classes

**Specifications:**
- **Total samples:** 2000 points (1000 per class)
- **Features per sample:** 3 dimensions (x₀, x₁, x₂)
  - x₀: Bias term, always equals 1
  - x₁: First feature
  - x₂: Second feature
- **Class 0 (Group 1):**
  - Label: y = 0
  - x₁ ∈ [0.1, 0.4] (uniform random)
  - x₂ ∈ [0.1, 0.4] (uniform random)
- **Class 1 (Group 2):**
  - Label: y = 1
  - x₁ ∈ [0.6, 0.9] (uniform random)
  - x₂ ∈ [0.6, 0.9] (uniform random)

**Output Format:**
- Matrix X: shape (2000, 3)
- Vector y: shape (2000,)

### 4.2 Model Initialization
**Description:** Initialize model parameters

**Specifications:**
- **Coefficients (Weights):** β₀, β₁, β₂
  - Initialize randomly in range [-1, 1]
  - These represent the coefficients of the logistic regression model
- **Learning Rate:** η = 0.3
  - Controls the step size in gradient descent

### 4.3 Sigmoid Function
**Description:** Compute probability for each sample

**Mathematical Formula:**
```
p(i) = 1 / (1 + e^(-(β₀ + β₁*x₁ + β₂*x₂)))
```

**Specifications:**
- Input: Feature vector [x₀, x₁, x₂] and coefficients [β₀, β₁, β₂]
- Output: Probability p(i) ∈ [0, 1]
- Apply to all samples to create probability vector p

### 4.4 Gradient Calculation
**Description:** Compute gradient of log-likelihood

**Mathematical Formula:**
```
g = X^T(y - p)
```

**Specifications:**
- X: Dataset matrix (2000, 3) without labels
- X^T: Transpose of X, shape (3, 2000)
- y: Label vector, shape (2000,)
- p: Probability vector, shape (2000,)
- g: Gradient vector, shape (3,) - one value for each β

### 4.5 Gradient Descent Algorithm
**Description:** Iterative optimization to find optimal coefficients

**Algorithm Steps:**
1. **Initialize:** Set β from random values (Section 4.2)
2. **Compute probabilities:** Calculate p(i) for all samples using sigmoid
3. **Calculate error vector:** Compute (y - p)
4. **Compute gradient:** g = X^T(y - p)
5. **Update coefficients:** β_new = β_old + η * g
6. **Check convergence:** Repeat until maximum likelihood or convergence criteria met
7. **Return:** Final β values

**Convergence Criteria:**
- Maximum iterations: 1000
- Or gradient norm < threshold (e.g., 1e-6)
- Or likelihood improvement < threshold

### 4.6 Output Requirements

#### 4.6.1 Final Sigmoid Equation
**Display the trained model equation:**
```
p(x) = 1 / (1 + e^(-(β₀ + β₁*x₁ + β₂*x₂)))
```
With actual numerical values for β₀, β₁, β₂

#### 4.6.2 Results Table
**Content:**
- Original dataset features (x₀, x₁, x₂)
- True labels (y)
- Predicted probabilities (p)
- Binary predictions (0 if p < 0.5, else 1)
- Squared error: (y - p)²

**Statistics:**
- Average error: Σ(y - p)² / (n - 1), where n = 2000
- Display in GUI with table widget
- Consider pagination or scrolling due to 2000 rows

#### 4.6.3 Classification Scatter Plot
**Requirements:**
- 2D scatter plot showing x₁ vs x₂
- Color coding:
  - Class 0: One color (e.g., blue)
  - Class 1: Different color (e.g., green)
- **Misclassification indicators:**
  - Red "X" marker near misclassified points
  - Misclassified = (y ≠ predicted_label)
- Title, axis labels, legend
- Decision boundary visualization (optional enhancement)

#### 4.6.4 Training Progress Plots
**Requirements:**
- Create 2 subplots in one figure:

**Plot 1: Log-Likelihood vs Iteration**
- X-axis: Iteration number
- Y-axis: Log-likelihood value
- Shows convergence behavior

**Plot 2: Average Error vs Iteration**
- X-axis: Iteration number
- Y-axis: Average error = Σ(y - p)² / (n - 1)
- Tracks prediction quality over time

---

## 5. Non-Functional Requirements

### 5.1 Performance
- Dataset generation: < 1 second
- Training: Complete within reasonable time (< 30 seconds)
- Visualization rendering: Smooth and responsive

### 5.2 Usability
- Clear console output showing training progress
- Intuitive GUI with clear visualizations
- Well-formatted tables and plots

### 5.3 Maintainability
- Modular code structure
- Clear function and variable names
- Docstrings for all major functions
- Type hints where appropriate

### 5.4 Code Quality
- PEP 8 compliance
- No file exceeds 200 lines
- Single responsibility principle for each module

---

## 6. Module Structure

### 6.1 main.py
- Entry point of the application
- Orchestrates workflow: data → training → visualization
- Handles command-line arguments if needed

### 6.2 data_generator.py
- Functions for dataset creation
- Random data generation for two classes
- Data validation

### 6.3 logistic_model.py
- Sigmoid function implementation
- Gradient calculation
- Model training (gradient descent loop)
- Prediction functions

### 6.4 visualization.py
- Scatter plot generation
- Training progress plots
- GUI table display

### 6.5 utils.py
- Helper functions
- Error calculations
- Metrics computation
- File I/O if needed

---

## 7. Dependencies

### 7.1 Core Libraries
- **numpy:** Numerical computations, matrix operations
- **matplotlib:** Plotting and visualization
- **tkinter:** GUI for table display (included in Python standard library)

### 7.2 Development Tools
- **pip:** Package management
- **venv:** Virtual environment

---

## 8. Deliverables

1. **Source Code:**
   - main.py
   - data_generator.py
   - logistic_model.py
   - visualization.py
   - utils.py

2. **Documentation:**
   - PRD.md (this document)
   - planning.md (architecture and design)
   - tasks.md (development task breakdown)
   - Claude.md (AI context and instructions)
   - README.md (user guide)

3. **Configuration:**
   - requirements.txt (Python dependencies)
   - .gitignore (if using git)

4. **Output:**
   - Trained model parameters
   - Visualization plots
   - Results table with statistics

---

## 9. Success Criteria

1. **Functional:**
   - Successfully separates two classes with > 95% accuracy
   - Gradient descent converges smoothly
   - All visualizations display correctly

2. **Technical:**
   - Code follows modular structure (< 200 lines per file)
   - Runs in WSL virtual environment without errors
   - Uses only NumPy for calculations (no sklearn)

3. **Educational:**
   - Clear demonstration of gradient descent process
   - Visualizations aid understanding of algorithm behavior
   - Code is readable and well-documented

---

## 10. Future Enhancements (Out of Scope)

- Multi-class classification (> 2 classes)
- Regularization (L1/L2)
- Cross-validation
- ROC curve and AUC metrics
- Interactive parameter tuning
- Save/load trained models
- Support for larger datasets
- Real-world dataset compatibility

---

## 11. Constraints and Assumptions

### Constraints:
- Must use WSL environment
- Cannot use scikit-learn or similar ML libraries
- Each Python file limited to 150-200 lines

### Assumptions:
- User has Python 3.8+ installed in WSL
- User has basic Python knowledge
- X server configured for GUI display in WSL (or WSL2 with WSLg)
- Dataset is linearly separable in feature space

---

## 12. Greek Letter Notation Reference

- **β (Beta):** Model coefficients/weights
  - β₀: Intercept term
  - β₁: Coefficient for x₁
  - β₂: Coefficient for x₂
- **η (Eta):** Learning rate (0.3)
- **Σ (Sigma):** Summation operator

---

## 13. Mathematical Background

**Logistic Regression Model:**
- Predicts probability of binary outcome
- Uses sigmoid function to map linear combination to [0,1]
- Optimized via maximum likelihood estimation

**Gradient Descent:**
- Iterative optimization algorithm
- Moves in direction of steepest ascent (for likelihood)
- Step size controlled by learning rate η

**Log-Likelihood:**
- Objective function to maximize
- Measures how well model explains data
- Gradient points toward better parameters

---

## End of PRD
