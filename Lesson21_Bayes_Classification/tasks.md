# Implementation Tasks
## Iris Naive Bayes Classification Project

**Author:** Yair Levi
**Date:** 2025-12-03

---

## Task Breakdown

### Phase 1: Project Setup (30 minutes)

#### Task 1.1: Create Virtual Environment
- [ ] Navigate to project directory in WSL
- [ ] Create virtual environment: `python3 -m venv venv`
- [ ] Activate virtual environment: `source venv/bin/activate`
- [ ] Verify Python version (3.8+)

#### Task 1.2: Create requirements.txt
- [ ] List all dependencies:
  - numpy
  - scikit-learn
  - matplotlib
  - pandas (optional)
- [ ] Specify minimum versions
- [ ] Install dependencies: `pip install -r requirements.txt`

#### Task 1.3: Create Package Structure
- [ ] Create `iris_classifier/` directory
- [ ] Create `iris_classifier/__init__.py`
- [ ] Verify iris.csv exists in project root
- [ ] Create `log/` directory (or let code create it)

#### Task 1.4: Setup Version Control (Optional)
- [ ] Initialize git repository: `git init`
- [ ] Create .gitignore (venv/, log/, __pycache__/, *.pyc)
- [ ] Initial commit with documentation

---

### Phase 2: Logging System (45 minutes)

#### Task 2.1: Implement logger_config.py
- [ ] Import necessary modules (logging, logging.handlers, pathlib)
- [ ] Create `setup_logger()` function
- [ ] Implement log directory creation with relative path
- [ ] Configure RotatingFileHandler:
  - maxBytes = 16 * 1024 * 1024 (16MB)
  - backupCount = 19 (total 20 files)
- [ ] Set formatter with timestamp, name, level, message
- [ ] Set logging level to INFO
- [ ] Test logger independently
- [ ] Verify file size < 200 lines

#### Task 2.2: Test Logging System
- [ ] Create test script to generate logs
- [ ] Verify log files created in `log/` directory
- [ ] Generate enough logs to test rotation
- [ ] Verify 20-file limit
- [ ] Verify oldest file gets overwritten

---

### Phase 3: Data Loading (1 hour)

#### Task 3.1: Implement data_loader.py - Basic Loading
- [ ] Import dependencies (numpy, pandas, sklearn)
- [ ] Import logger
- [ ] Implement `load_iris_data(file_path='iris.csv')`:
  - Use pathlib for relative path
  - Read CSV file
  - Validate structure (5 columns)
  - Validate headers
  - Log success/failure
  - Return DataFrame or numpy array

#### Task 3.2: Implement data_loader.py - Data Splitting
- [ ] Implement `split_data(data, test_size=0.25, random_state=42)`:
  - Separate features (first 4 columns) and labels (last column)
  - Use sklearn.model_selection.train_test_split
  - Log split statistics (train size, test size)
  - Return (X_train, X_test, y_train, y_test)

#### Task 3.3: Implement data_loader.py - Main Function
- [ ] Implement `get_data()`:
  - Call load_iris_data()
  - Call split_data()
  - Extract feature names from headers
  - Extract class names from unique labels
  - Return dictionary with all data
- [ ] Verify file size < 200 lines

#### Task 3.4: Test Data Loading
- [ ] Create standalone test
- [ ] Verify correct split proportions (75/25)
- [ ] Verify labels removed from test features
- [ ] Print sample statistics
- [ ] Verify reproducibility with fixed seed

---

### Phase 4: Manual Naive Bayes Implementation (3 hours)

#### Task 4.1: Setup ManualNaiveBayes Class
- [ ] Create naive_bayes_manual.py
- [ ] Import dependencies (numpy, multiprocessing, logging)
- [ ] Define ManualNaiveBayes class
- [ ] Implement `__init__(self, n_bins=10)`:
  - Initialize instance variables
  - Setup logger

#### Task 4.2: Implement Prior Probability Calculation
- [ ] Implement `fit()` method - Part 1:
  - Get unique classes
  - Count samples per class
  - Calculate P(Ci) = count(class_i) / total
  - Log prior probabilities
  - Store in self.priors dictionary

#### Task 4.3: Implement Histogram Building - Sequential
- [ ] Implement `_build_histogram()` helper method:
  - Use np.histogram() with n_bins
  - Apply Laplace smoothing (+1 to all bins)
  - Return (counts, bin_edges)
- [ ] Implement `fit()` method - Part 2:
  - For each class, for each feature:
    - Extract feature data for that class
    - Build histogram
    - Store in self.histograms[class][feature]

#### Task 4.4: Implement Histogram Building - Parallel
- [ ] Create worker function for multiprocessing
- [ ] Modify `fit()` to use multiprocessing.Pool:
  - Create task list (class, feature, data)
  - Use Pool.map() with 12 tasks
  - Organize results into histogram dictionary
- [ ] Test parallel vs sequential performance

#### Task 4.5: Implement Prediction Method
- [ ] Implement `predict()` method:
  - Initialize predictions array
  - For each test sample:
    - For each class:
      - Start with log(P(Ci))
      - For each feature:
        - Find which bin contains feature value
        - Calculate bin probability
        - Add log(P(Xi|Ci))
      - Store total log probability
    - Assign class with max probability
  - Return predictions array

#### Task 4.6: Implement Helper Methods
- [ ] Implement `get_histograms()` for visualization
- [ ] Implement `_find_bin_index()` helper for prediction
- [ ] Add error handling for edge cases
- [ ] Verify file size < 200 lines

#### Task 4.7: Test Manual Implementation
- [ ] Create standalone test script
- [ ] Load sample data
- [ ] Train model
- [ ] Make predictions
- [ ] Verify predictions are valid class labels
- [ ] Check for any NaN or inf values
- [ ] Test edge cases (values outside histogram range)

---

### Phase 5: Library Naive Bayes Implementation (30 minutes)

#### Task 5.1: Implement LibraryNaiveBayes Class
- [ ] Create naive_bayes_library.py
- [ ] Import sklearn.naive_bayes.GaussianNB
- [ ] Import logging
- [ ] Define LibraryNaiveBayes class

#### Task 5.2: Implement Core Methods
- [ ] Implement `__init__()`:
  - Initialize GaussianNB model
  - Setup logger
- [ ] Implement `fit()`:
  - Call model.fit(X_train, y_train)
  - Log training completion
  - Return self
- [ ] Implement `predict()`:
  - Call model.predict(X_test)
  - Log prediction completion
  - Return predictions
- [ ] Implement `get_model()` for inspection

#### Task 5.3: Test Library Implementation
- [ ] Create standalone test
- [ ] Compare with manual implementation
- [ ] Verify predictions format
- [ ] Verify file size < 200 lines

---

### Phase 6: Visualization (2 hours)

#### Task 6.1: Implement Histogram Plotting
- [ ] Create visualization.py
- [ ] Import matplotlib.pyplot, numpy
- [ ] Configure matplotlib backend (Agg for WSL compatibility)
- [ ] Implement `plot_histograms()`:
  - Create 2x2 subplot figure
  - For each feature (4 features):
    - Get histogram data for all 3 classes
    - Plot overlapping/side-by-side histograms
    - Use different colors for each class
    - Add legend, labels, title
  - Adjust layout
  - Save to file or display
  - Log completion

#### Task 6.2: Implement Confusion Matrix Plotting
- [ ] Implement `plot_confusion_matrix()`:
  - Calculate confusion matrix using sklearn
  - Create heatmap with matplotlib
  - Add value annotations
  - Add row/column labels (class names)
  - Add title
  - Add colorbar
  - Save or display

#### Task 6.3: Implement Results Display
- [ ] Implement `display_results()`:
  - Create figure with 2 subplots (side by side)
  - Plot confusion matrix for manual method
  - Plot confusion matrix for library method
  - Calculate and display accuracy scores
  - Print comparison metrics to console
  - Log results
- [ ] Verify file size < 200 lines

#### Task 6.4: Test Visualization
- [ ] Generate sample predictions
- [ ] Test histogram plotting
- [ ] Test confusion matrix plotting
- [ ] Verify files saved correctly
- [ ] Check plot quality and readability

---

### Phase 7: Package Integration (1 hour)

#### Task 7.1: Complete __init__.py
- [ ] Add package docstring
- [ ] Import all public functions and classes
- [ ] Define __all__ list
- [ ] Add version, author metadata
- [ ] Verify file size < 200 lines

#### Task 7.2: Implement main.py
- [ ] Import from iris_classifier package
- [ ] Implement main() function:
  - Setup logger
  - Load and split data
  - Train manual model
  - Train library model
  - Plot histograms
  - Make predictions (both methods)
  - Display results
  - Handle exceptions
- [ ] Add if __name__ == '__main__' guard
- [ ] Verify file size < 200 lines

#### Task 7.3: Test Package Import
- [ ] Test: `from iris_classifier import ManualNaiveBayes`
- [ ] Test: `from iris_classifier import get_data`
- [ ] Verify all imports work
- [ ] Check for circular dependencies

---

### Phase 8: Integration Testing (1.5 hours)

#### Task 8.1: End-to-End Test
- [ ] Activate virtual environment
- [ ] Run: `python main.py`
- [ ] Verify no errors
- [ ] Check log files created
- [ ] Check plots generated
- [ ] Verify console output

#### Task 8.2: Validate Outputs
- [ ] Verify prior probabilities sum to 1.0
- [ ] Verify confusion matrices:
  - Sum equals number of test samples
  - Values are non-negative integers
- [ ] Compare manual vs library predictions:
  - Should be similar (may not be identical)
  - Both should be reasonable accuracy
- [ ] Check histogram plots:
  - All 4 feature plots present
  - 3 classes per plot
  - Readable labels

#### Task 8.3: Test Edge Cases
- [ ] Test with different random seeds
- [ ] Test with different train/test splits
- [ ] Test with missing iris.csv (error handling)
- [ ] Test log rotation (generate lots of logs)

#### Task 8.4: Performance Testing
- [ ] Measure total runtime
- [ ] Compare multiprocessing vs sequential
- [ ] Check memory usage
- [ ] Verify meets performance targets (< 30 seconds total)

---

### Phase 9: Code Quality & Documentation (1 hour)

#### Task 9.1: Code Review
- [ ] Check all files < 200 lines
- [ ] Verify PEP 8 compliance (or reasonable adherence)
- [ ] Add type hints where helpful
- [ ] Add docstrings to all functions/classes
- [ ] Add comments for complex algorithms
- [ ] Remove debug print statements

#### Task 9.2: Documentation Review
- [ ] Review PRD.md for accuracy
- [ ] Review Claude.md for completeness
- [ ] Review planning.md for accuracy
- [ ] Review tasks.md (this file) - mark completed tasks
- [ ] Add usage examples if needed

#### Task 9.3: Final Checks
- [ ] Verify requirements.txt is complete
- [ ] Verify .gitignore is appropriate
- [ ] Check for hardcoded paths (should be relative)
- [ ] Verify WSL compatibility
- [ ] Test fresh virtual environment install

---

### Phase 10: Delivery (30 minutes)

#### Task 10.1: Package Cleanup
- [ ] Remove __pycache__ directories
- [ ] Remove .pyc files
- [ ] Clear log files for clean delivery
- [ ] Verify only source files remain

#### Task 10.2: Create README (Optional)
- [ ] Create README.md with quick start
- [ ] Add installation instructions
- [ ] Add usage examples
- [ ] Link to Claude.md for details

#### Task 10.3: Final Verification
- [ ] Fresh clone/copy to test directory
- [ ] Fresh virtual environment
- [ ] Install requirements
- [ ] Run main.py
- [ ] Verify complete success

#### Task 10.4: Submission Preparation
- [ ] Zip/tar project directory
- [ ] Include all documentation
- [ ] Include all source code
- [ ] Include iris.csv
- [ ] Exclude venv/, log/, __pycache__/

---

## Estimated Time Breakdown

| Phase | Tasks | Estimated Time |
|-------|-------|----------------|
| 1. Project Setup | 1.1-1.4 | 30 min |
| 2. Logging System | 2.1-2.2 | 45 min |
| 3. Data Loading | 3.1-3.4 | 1 hour |
| 4. Manual Naive Bayes | 4.1-4.7 | 3 hours |
| 5. Library Naive Bayes | 5.1-5.3 | 30 min |
| 6. Visualization | 6.1-6.4 | 2 hours |
| 7. Package Integration | 7.1-7.3 | 1 hour |
| 8. Integration Testing | 8.1-8.4 | 1.5 hours |
| 9. Code Quality | 9.1-9.3 | 1 hour |
| 10. Delivery | 10.1-10.4 | 30 min |
| **Total** | | **~11.5 hours** |

---

## Critical Path

1. Logging System (needed by all modules)
2. Data Loading (needed by both implementations)
3. Manual Implementation (longest, most complex)
4. Library Implementation (quick, validates manual)
5. Visualization (depends on both implementations)
6. Integration (final assembly)

---

## Dependencies Between Tasks

```
1.1-1.3 (Setup) → 2.1 (Logging) → 3.1 (Data Loading)
                                  ↓
                     ┌────────────┴────────────┐
                     ↓                         ↓
                  4.1 (Manual)             5.1 (Library)
                     ↓                         ↓
                     └────────────┬────────────┘
                                  ↓
                            6.1 (Visualization)
                                  ↓
                            7.2 (Integration)
                                  ↓
                            8.1 (Testing)
```

---

## Risk Mitigation

| Risk | Task | Mitigation |
|------|------|------------|
| Histogram bins all zero | 4.3 | Implement Laplace smoothing |
| Log of zero | 4.5 | Add epsilon or use smoothing |
| File size exceeds 200 lines | All | Refactor into helper functions |
| Multiprocessing overhead | 4.4 | Profile and compare with sequential |
| WSL display issues | 6.1 | Use Agg backend, save to files |
| Path issues | All | Use pathlib throughout |

---

## Testing Checklist

- [ ] All modules import successfully
- [ ] Logging creates 20-file ring buffer
- [ ] Data splits correctly (75/25)
- [ ] Manual implementation trains without errors
- [ ] Library implementation trains without errors
- [ ] Histograms display all 3 classes per feature
- [ ] Predictions are valid class labels
- [ ] Confusion matrices are valid (sum = n_test)
- [ ] Manual and library results are comparable
- [ ] All file sizes < 200 lines
- [ ] All paths are relative
- [ ] Works in fresh virtual environment on WSL

---

## Success Criteria

- [ ] Complete documentation (PRD, Claude, planning, tasks)
- [ ] Working package structure
- [ ] Both implementations produce results
- [ ] Visualizations generated
- [ ] Logging system functional
- [ ] All code < 200 lines per file
- [ ] Relative paths throughout
- [ ] Multiprocessing implemented
- [ ] Runs successfully on WSL
- [ ] Reproducible results

---

## Notes

- Keep functions small and focused
- Log all significant operations
- Handle errors gracefully
- Use meaningful variable names
- Comment complex algorithms (especially manual Naive Bayes)
- Test incrementally (don't wait until the end)
