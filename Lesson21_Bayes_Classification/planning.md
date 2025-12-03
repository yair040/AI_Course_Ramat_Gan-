# Technical Planning Document
## Iris Naive Bayes Classification Project

**Author:** Yair Levi
**Date:** 2025-12-03

---

## 1. Architecture Overview

### 1.1 System Design

```
┌─────────────────────────────────────────────────────────────┐
│                         main.py                              │
│                    (Entry Point & Orchestrator)              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ imports and calls
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   iris_classifier/                           │
│                  (Package Directory)                         │
├─────────────────────────────────────────────────────────────┤
│  __init__.py         - Package initialization                │
│  logger_config.py    - Ring buffer logging setup             │
│  data_loader.py      - Load CSV, split train/test            │
│  naive_bayes_manual.py - Manual NumPy implementation         │
│  naive_bayes_library.py - Scikit-learn implementation        │
│  visualization.py    - Histogram & confusion matrix plots    │
└─────────────────────────────────────────────────────────────┘
                       │
                       │ generates
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                      log/                                    │
│              (Ring Buffer Log Files)                         │
│  iris_classifier_01.log ... iris_classifier_20.log           │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Data Flow

```
iris.csv
   │
   └──> data_loader.py
          │
          ├──> X_train (75%), y_train (75%)
          │      │
          │      ├──> naive_bayes_manual.py (training)
          │      │      │
          │      │      ├──> Calculate P(Ci)
          │      │      ├──> Build 12 histograms
          │      │      └──> visualization.py (show histograms)
          │      │
          │      └──> naive_bayes_library.py (training)
          │             └──> GaussianNB.fit()
          │
          └──> X_test (25%), y_test (25%)
                 │
                 ├──> naive_bayes_manual.py (testing)
                 │      │
                 │      ├──> Calculate P(Ci|X) for each sample
                 │      └──> y_pred_manual
                 │
                 └──> naive_bayes_library.py (testing)
                        └──> GaussianNB.predict() -> y_pred_library

                 ├──> Confusion Matrix (manual)
                 └──> Confusion Matrix (library)
```

---

## 2. Module Specifications

### 2.1 logger_config.py (≈50 lines)

**Purpose:** Configure ring buffer logging system

**Functionality:**
- Create `log/` directory if not exists
- Setup `RotatingFileHandler` with 20 files
- Each file max 16MB (16 * 1024 * 1024 bytes)
- Format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- Level: INFO and above

**Key Classes:**
- Custom handler or use `logging.handlers.RotatingFileHandler`

**Returns:**
- Configured logger instance

---

### 2.2 data_loader.py (≈80 lines)

**Purpose:** Load and preprocess iris dataset

**Functions:**

1. `load_iris_data(file_path='iris.csv')` → DataFrame
   - Read CSV with pandas or numpy
   - Validate structure (4 features + 1 label)
   - Return complete dataset

2. `split_data(data, test_size=0.25, random_state=42)` → tuple
   - Separate features (X) and labels (y)
   - Use sklearn.model_selection.train_test_split
   - Return: (X_train, X_test, y_train, y_test)

3. `get_data()` → dict
   - Main function called by main.py
   - Returns dictionary with all splits and metadata
   - Uses relative path for iris.csv

**Dependencies:**
- numpy, pandas (optional), sklearn.model_selection

---

### 2.3 naive_bayes_manual.py (≈150 lines)

**Purpose:** Manual implementation using NumPy only

**Class:** `ManualNaiveBayes`

**Methods:**

1. `__init__(self, n_bins=10)`
   - Initialize with number of histogram bins
   - Store histograms dictionary
   - Store prior probabilities

2. `fit(self, X_train, y_train)`
   - Calculate P(Ci) for each class
   - Log prior probabilities
   - Build histograms for each class-feature combination
   - Use `np.histogram()` for binning
   - Apply Laplace smoothing (add 1 to empty bins)
   - Store bin edges for later use
   - Return self

3. `_build_histogram(self, feature_data, n_bins)`
   - Create histogram for single feature
   - Return counts and bin edges
   - Apply Laplace smoothing

4. `predict(self, X_test)`
   - For each test sample:
     - For each class:
       - Calculate log(P(Ci))
       - For each feature:
         - Find which bin the value falls into
         - Calculate log(P(Xi|Ci))
       - Sum: log(P(Ci)) + Σ log(P(Xi|Ci))
     - Assign class with max probability
   - Return predictions array

5. `get_histograms()`
   - Return histogram data for visualization
   - Format: {class: {feature: (counts, edges)}}

**Use multiprocessing for histogram building (12 histograms)**

---

### 2.4 naive_bayes_library.py (≈60 lines)

**Purpose:** Scikit-learn implementation

**Class:** `LibraryNaiveBayes`

**Methods:**

1. `__init__(self)`
   - Initialize GaussianNB from sklearn

2. `fit(self, X_train, y_train)`
   - Call model.fit()
   - Log training completion
   - Return self

3. `predict(self, X_test)`
   - Call model.predict()
   - Return predictions

4. `get_model()`
   - Return trained model for inspection

**Dependencies:**
- sklearn.naive_bayes.GaussianNB

---

### 2.5 visualization.py (≈120 lines)

**Purpose:** Create histograms and confusion matrices

**Functions:**

1. `plot_histograms(histogram_data, feature_names, class_names)`
   - Create 4 subplots (2x2 grid)
   - Each subplot shows one feature across all 3 classes
   - Use different colors for each class
   - Add legends, labels, title
   - Use `matplotlib.pyplot`
   - Save to file or display

2. `plot_confusion_matrix(y_true, y_pred, class_names, title, save_path=None)`
   - Use sklearn.metrics.confusion_matrix
   - Create heatmap visualization
   - Add labels and percentages
   - Save or display

3. `display_results(y_test, y_pred_manual, y_pred_library, class_names)`
   - Create side-by-side confusion matrices
   - Print accuracy scores
   - Log comparison metrics

**Use multiprocessing for generating multiple plots if beneficial**

---

### 2.6 main.py (≈100 lines)

**Purpose:** Entry point and orchestration

**Structure:**

```python
def main():
    # 1. Setup logging
    logger = setup_logger()

    # 2. Load and split data
    data = get_data()

    # 3. Train manual implementation
    manual_nb = ManualNaiveBayes()
    manual_nb.fit(data['X_train'], data['y_train'])

    # 4. Train library implementation
    library_nb = LibraryNaiveBayes()
    library_nb.fit(data['X_train'], data['y_train'])

    # 5. Visualize histograms
    histograms = manual_nb.get_histograms()
    plot_histograms(histograms, data['feature_names'], data['class_names'])

    # 6. Test both implementations
    y_pred_manual = manual_nb.predict(data['X_test'])
    y_pred_library = library_nb.predict(data['X_test'])

    # 7. Display results
    display_results(data['y_test'], y_pred_manual, y_pred_library,
                    data['class_names'])

if __name__ == '__main__':
    main()
```

---

### 2.7 __init__.py (≈30 lines)

**Purpose:** Package initialization

**Contents:**
```python
"""
Iris Naive Bayes Classification Package

Author: Yair Levi
"""

from .data_loader import get_data, load_iris_data, split_data
from .naive_bayes_manual import ManualNaiveBayes
from .naive_bayes_library import LibraryNaiveBayes
from .visualization import plot_histograms, plot_confusion_matrix, display_results
from .logger_config import setup_logger

__version__ = '1.0.0'
__author__ = 'Yair Levi'

__all__ = [
    'get_data',
    'load_iris_data',
    'split_data',
    'ManualNaiveBayes',
    'LibraryNaiveBayes',
    'plot_histograms',
    'plot_confusion_matrix',
    'display_results',
    'setup_logger'
]
```

---

## 3. Multiprocessing Strategy

### 3.1 Histogram Building (naive_bayes_manual.py)
- Use `multiprocessing.Pool`
- Parallel generation of 12 histograms (3 classes × 4 features)
- Each worker builds one histogram
- Gather results and organize into dictionary

### 3.2 Prediction (if dataset is large)
- Split test data into chunks
- Process chunks in parallel
- Gather predictions

### 3.3 Implementation Example
```python
from multiprocessing import Pool, cpu_count

def build_single_histogram(args):
    class_id, feature_id, data, n_bins = args
    counts, edges = np.histogram(data, bins=n_bins)
    counts = counts + 1  # Laplace smoothing
    return (class_id, feature_id, counts, edges)

def build_all_histograms_parallel(X, y, n_bins):
    tasks = []
    for class_id in unique_classes:
        for feature_id in range(X.shape[1]):
            data = X[y == class_id, feature_id]
            tasks.append((class_id, feature_id, data, n_bins))

    with Pool(min(cpu_count(), 12)) as pool:
        results = pool.map(build_single_histogram, tasks)

    return organize_results(results)
```

---

## 4. Logging Strategy

### 4.1 Ring Buffer Implementation

```python
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logger(name='iris_classifier'):
    # Create log directory
    log_dir = Path(__file__).parent.parent / 'log'
    log_dir.mkdir(exist_ok=True)

    # Configure rotating handler
    log_file = log_dir / 'iris_classifier.log'
    handler = RotatingFileHandler(
        log_file,
        maxBytes=16 * 1024 * 1024,  # 16MB
        backupCount=19  # Plus 1 main = 20 files
    )

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger
```

### 4.2 Logging Points

1. **data_loader.py:**
   - Data loaded successfully
   - Train/test split completed
   - Data statistics

2. **naive_bayes_manual.py:**
   - Prior probabilities calculated
   - Histogram building started/completed
   - Training completed
   - Prediction started/completed

3. **naive_bayes_library.py:**
   - Training started/completed
   - Prediction completed

4. **visualization.py:**
   - Plots generated
   - Files saved

5. **main.py:**
   - Program started
   - Each phase completion
   - Final results
   - Program completed

---

## 5. Error Handling Strategy

### 5.1 Data Loading
- File not found → log error, provide instructions
- Invalid CSV format → log error, validate structure
- Missing columns → log error, show expected format

### 5.2 Training
- Empty histogram bins → Apply Laplace smoothing automatically
- Zero probabilities → Use log(probability + epsilon)
- Invalid data types → Validate and convert

### 5.3 Prediction
- Out-of-range feature values → Handle bin edge cases
- Log of zero → Add smoothing constant

### 5.4 Visualization
- Display not available → Save to file instead
- Invalid data → Log error with details

---

## 6. Testing Strategy

### 6.1 Unit Tests (Future)
- Test each module independently
- Mock dependencies
- Validate calculations

### 6.2 Integration Tests
- Run full pipeline
- Validate output formats
- Check file creation

### 6.3 Validation
- Compare manual vs library predictions
- Check confusion matrix properties (sum = n_samples)
- Verify prior probabilities sum to 1

---

## 7. Performance Targets

- **Data Loading:** < 1 second
- **Training (manual):** < 10 seconds
- **Training (library):** < 1 second
- **Prediction (manual):** < 5 seconds
- **Prediction (library):** < 1 second
- **Visualization:** < 5 seconds
- **Total Runtime:** < 30 seconds

---

## 8. Dependencies Management

### 8.1 Core Dependencies
- numpy >= 1.21.0
- scikit-learn >= 1.0.0
- matplotlib >= 3.4.0

### 8.2 Optional Dependencies
- pandas >= 1.3.0 (for easier CSV handling)

### 8.3 Standard Library
- logging, multiprocessing, pathlib, sys, os

---

## 9. File Path Strategy

### 9.1 Relative Path Resolution

```python
from pathlib import Path

# Get project root
PROJECT_ROOT = Path(__file__).parent

# Data file
DATA_FILE = PROJECT_ROOT / 'iris.csv'

# Log directory
LOG_DIR = PROJECT_ROOT / 'log'

# Package directory
PACKAGE_DIR = PROJECT_ROOT / 'iris_classifier'
```

### 9.2 Path Validation
- Check file existence before operations
- Create directories if needed
- Use Path objects throughout (not strings)

---

## 10. Deployment Considerations

### 10.1 Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 10.2 Running
```bash
cd /path/to/Bayes_Classification
source venv/bin/activate
python main.py
```

### 10.3 WSL Compatibility
- Use Unix-style paths
- Handle line endings correctly
- Test matplotlib display or use Agg backend

---

## 11. Code Quality Standards

- **PEP 8:** Follow Python style guide
- **Type Hints:** Use where appropriate
- **Docstrings:** All functions and classes
- **Comments:** Explain complex algorithms
- **Line Length:** Max 100 characters (flexible)
- **File Length:** Max 200 lines per file

---

## 12. Success Metrics

1. All modules under 200 lines
2. Logging system functional with 20-file rotation
3. Both methods produce valid predictions
4. Confusion matrices match expected format
5. Histograms clearly visualized
6. Code runs on WSL without errors
7. Relative paths work correctly
8. Multiprocessing improves performance

---

## 13. Future Enhancements

- Command-line arguments for parameters
- Configuration file (YAML/JSON)
- Additional Naive Bayes variants
- Cross-validation support
- Export results to CSV
- Web interface for predictions
- Docker containerization
- CI/CD pipeline
