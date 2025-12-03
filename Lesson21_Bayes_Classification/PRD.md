# Product Requirements Document (PRD)
## Iris Flower Classification using Naive Bayes Algorithm

**Author:** Yair Levi
**Date:** 2025-12-03
**Version:** 1.0

---

## 1. Project Overview

This project implements a Naive Bayes classifier for the Iris flower dataset. The implementation includes both a manual implementation using NumPy and a library-based implementation, allowing for comparison and educational purposes.

## 2. Technical Requirements

### 2.1 Environment
- **Platform:** WSL (Windows Subsystem for Linux)
- **Python Version:** 3.8+
- **Virtual Environment:** Required
- **Package Structure:** Python package with `__init__.py`

### 2.2 Code Organization
- Each Python file: Maximum 150-200 lines
- Use relative paths (no absolute paths)
- Modular task-based architecture
- Main program calls individual tasks

### 2.3 Performance
- Use multiprocessing where applicable
- Efficient data processing with NumPy

### 2.4 Logging
- **Level:** INFO and above
- **Format:** Ring buffer with 20 log files
- **File Size:** Maximum 16MB per file
- **Rotation:** When the 20th file is full, overwrite the first file
- **Location:** `log/` subfolder (relative path)

---

## 3. Functional Requirements

### 3.1 Dataset
- **Source:** `iris.csv` file
- **Structure:**
  - 4 feature columns: sepal length, sepal width, petal length, petal width
  - 1 label column: class (setosa, versicolor, virginica)
  - First row: Header with column names

### 3.2 Data Preprocessing
1. **Dataset Split:**
   - 75% training data
   - 25% test data
   - Random selection with fixed seed for reproducibility
   - Remove labels from test set for prediction

### 3.3 Training Phase

#### 3.3.1 Manual Implementation (Method 1)
**Requirements:**
- Use only NumPy library (no ML libraries)
- Calculate prior probabilities P(Ci) for each class:
  - Count flowers in each class
  - Divide by total number of Iris flowers
  - Display P(Ci) for all three classes

- **Histogram Generation:**
  - For each class (3 classes):
    - For each feature Xi (4 features):
      - Build histogram of feature values
      - If any bin is empty, set bin count to 1 (Laplace smoothing)
  - Total: 12 histograms (3 classes × 4 features)

- **Visualization:**
  - Create 4 graphs (one per feature)
  - Each graph shows histograms for all 3 classes
  - Allows comparison across classes for same feature

#### 3.3.2 Library Implementation (Method 2)
- Use scikit-learn's Naive Bayes classifier
- Use same training set as Method 1
- No re-randomization of data split

### 3.4 Testing Phase

#### 3.4.1 Manual Implementation (Method 1)
**Process for each test sample:**
1. For each feature Xi in the sample:
   - Locate value in histogram bin (from training)
   - Calculate P(Xi|Ci) for each class:
     - P(Xi|Ci) = bin_area / total_histogram_area
   - Do this for all 3 classes

2. Apply logarithmic Naive Bayes formula:
   ```
   P(Ci|X) = log(P(Ci)) + Σ log(P(Xi|Ci))
   ```
   Where the sum is over all 4 features

3. Assign class with highest P(Ci|X) as prediction

#### 3.4.2 Library Implementation (Method 2)
- Use trained scikit-learn model
- Use same test set as Method 1
- No re-randomization

### 3.5 Evaluation
- Generate confusion matrix for both methods
- Display comparison of results
- Calculate accuracy metrics

---

## 4. Deliverables

### 4.1 Documentation Files
- `PRD.md` - This document
- `Claude.md` - Project overview and usage guide
- `planning.md` - Technical architecture and design decisions
- `tasks.md` - Implementation task breakdown

### 4.2 Code Files
- `requirements.txt` - Python dependencies
- `__init__.py` - Package initialization
- `main.py` - Entry point and task orchestration
- `data_loader.py` - Data loading and preprocessing
- `naive_bayes_manual.py` - Manual implementation
- `naive_bayes_library.py` - Library-based implementation
- `visualization.py` - Histogram and result visualization
- `logger_config.py` - Logging configuration

### 4.3 Output
- Training metrics and prior probabilities
- 4 histogram graphs (feature comparison across classes)
- Confusion matrices for both methods
- Log files in `log/` directory

---

## 5. Success Criteria

1. Successful 75/25 train-test split
2. Manual implementation produces valid predictions
3. Library implementation produces valid predictions
4. Confusion matrices generated for both methods
5. All histograms properly visualized
6. Logging system operational with ring buffer
7. Code modularity: no file exceeds 200 lines
8. Relative paths used throughout
9. Multiprocessing implemented where beneficial

---

## 6. Constraints

- No external ML libraries for manual implementation (NumPy only)
- Must work in WSL environment
- Must use virtual environment
- File size limits enforced
- Logging ring buffer must work correctly

---

## 7. Future Enhancements (Out of Scope)

- Cross-validation
- Hyperparameter tuning
- Additional classification algorithms
- Real-time classification API
- GUI interface

---

## 8. Dependencies

- NumPy (numerical computations)
- scikit-learn (library-based implementation)
- matplotlib (visualization)
- pandas (optional, for data handling)
- Standard library: logging, multiprocessing, pathlib

---

## 9. Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Empty histogram bins | High | Implement Laplace smoothing (add 1 to empty bins) |
| Log of zero probability | High | Use Laplace smoothing, check for zeros before log |
| File path issues on WSL | Medium | Use pathlib with relative paths |
| Memory issues with logging | Medium | Proper ring buffer implementation with size limits |
| Histogram bin selection | Medium | Use appropriate binning strategy (e.g., Sturges' rule) |

---

## 10. Acceptance Criteria

- [ ] All documentation files created
- [ ] Package structure properly initialized
- [ ] Data correctly split 75/25
- [ ] Manual Naive Bayes produces predictions
- [ ] Library Naive Bayes produces predictions
- [ ] Both confusion matrices displayed
- [ ] Histograms properly visualized
- [ ] Logging system works with ring buffer
- [ ] No file exceeds 200 lines
- [ ] All paths are relative
- [ ] Code runs successfully in WSL virtual environment
