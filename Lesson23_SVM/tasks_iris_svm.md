# Tasks Breakdown
## Iris SVM Classification System

**Author:** Yair Levi  
**Project:** Lesson23_SVM

---

## Task Categories

- 🔵 **Setup** - Environment and structure
- 🟢 **Core** - Essential functionality
- 🟡 **ML** - Machine learning components
- 🟠 **Task** - Task modules
- 🔴 **Integration** - Main program and integration
- 🟣 **Visualization** - Plotting and reporting
- ⚪ **Documentation** - Docs and testing

---

## Phase 1: Setup 🔵

### Task 1.1: Directory Structure
- [ ] Create `iris_classifier/` package directory
- [ ] Create `tasks/` package directory
- [ ] Create `log/` directory
- [ ] Create `results/` directory
- [ ] Add `__init__.py` files to packages

### Task 1.2: Virtual Environment
- [ ] Navigate to `../../` from project root
- [ ] Create venv: `python3 -m venv venv`
- [ ] Activate venv: `source venv/bin/activate`
- [ ] Verify Python version

### Task 1.3: Dependencies
- [ ] Create `requirements.txt`
- [ ] Install packages: `pip install -r requirements.txt`
- [ ] Verify all imports work

### Task 1.4: Initial Files
- [ ] Create all Python file placeholders
- [ ] Add module docstrings
- [ ] Set up basic imports

---

## Phase 2: Core Implementation 🟢

### Task 2.1: config.py
- [ ] Define path constants using `pathlib`
- [ ] Define ML hyperparameters
- [ ] Define logging parameters
- [ ] Create Config class
- [ ] Add validation for paths
- **Lines:** ~50

### Task 2.2: logger_setup.py
- [ ] Import logging and RotatingFileHandler
- [ ] Create log directory if not exists
- [ ] Configure formatter with timestamp
- [ ] Set up RotatingFileHandler (16MB × 20 files)
- [ ] Create get_logger() factory function
- [ ] Test logging to file
- **Lines:** ~60

### Task 2.3: data_loader.py
- [ ] Implement load_iris_data() function
- [ ] Use relative path to iris.csv
- [ ] Validate CSV structure
- [ ] Check for missing values
- [ ] Implement stratified train_test_split
- [ ] Return X_train, X_test, y_train, y_test
- [ ] Add logging for data loading steps
- **Lines:** ~80

### Task 2.4: preprocessor.py
- [ ] Implement StandardScaler wrapper
- [ ] Implement data normalization
- [ ] Handle edge cases (empty data, single sample)
- [ ] Implement label encoding for binary grouping
- [ ] Create group_classes() function for Stage 1
- [ ] Create filter_group_b() function for Stage 2
- [ ] Add logging for preprocessing steps
- **Lines:** ~70

---

## Phase 3: ML Pipeline 🟡

### Task 3.1: svm_trainer.py
- [ ] Import SVC from sklearn
- [ ] Implement train_svm() function
- [ ] Accept kernel, C, gamma parameters
- [ ] Fit model on training data
- [ ] Add training time logging
- [ ] Return trained model
- [ ] Handle convergence warnings
- [ ] Add hyperparameter logging
- **Lines:** ~90

### Task 3.2: evaluator.py
- [ ] Implement predict_and_evaluate() function
- [ ] Calculate accuracy score
- [ ] Calculate precision, recall, F1 (macro avg)
- [ ] Generate confusion matrix
- [ ] Create results dictionary
- [ ] Add logging for evaluation metrics
- [ ] Implement pretty-print for confusion matrix
- [ ] Handle edge cases (empty predictions)
- **Lines:** ~100

---

## Phase 4: Task Modules 🟠

### Task 4.1: task_stage1.py
- [ ] Import required modules
- [ ] Implement run_stage1(iteration_num) function
- [ ] Load data using data_loader
- [ ] Group classes: {0} vs {1,2}
- [ ] Preprocess data
- [ ] Train SVM model
- [ ] Evaluate on test set
- [ ] Store predictions for Stage 2
- [ ] Return results dict with metrics
- [ ] Add comprehensive logging
- **Lines:** ~120

### Task 4.2: task_stage2.py
- [ ] Import required modules
- [ ] Implement run_stage2(iteration_num, stage1_predictions) function
- [ ] Filter only Group B samples (classes 1 & 2)
- [ ] Relabel classes 1→0, 2→1
- [ ] Preprocess filtered data
- [ ] Train SVM model
- [ ] Evaluate on test set
- [ ] Combine with Stage 1 for final predictions
- [ ] Return results dict with metrics
- [ ] Add comprehensive logging
- **Lines:** ~100

### Task 4.3: task_analysis.py
- [ ] Import required modules
- [ ] Implement aggregate_results(all_iterations) function
- [ ] Calculate mean, std, min, max for each metric
- [ ] Calculate overall accuracy across iterations
- [ ] Create statistical summary
- [ ] Call visualizer to generate plots
- [ ] Save summary to JSON/CSV
- [ ] Return aggregated statistics
- [ ] Add logging for analysis steps
- **Lines:** ~110

---

## Phase 5: Main Program 🔴

### Task 5.1: main.py - Basic Structure
- [ ] Import all required modules
- [ ] Set up argument parser (optional)
- [ ] Initialize logger
- [ ] Define run_single_iteration() function
- [ ] Add error handling wrapper
- **Lines:** ~140 total

### Task 5.2: main.py - Iteration Logic
- [ ] Implement iteration execution
- [ ] Call task_stage1
- [ ] Call task_stage2 with stage1 results
- [ ] Collect iteration results
- [ ] Handle and log errors

### Task 5.3: main.py - Multiprocessing
- [ ] Import multiprocessing Pool
- [ ] Determine optimal worker count
- [ ] Wrap iteration in picklable function
- [ ] Execute 5 iterations in parallel
- [ ] Collect all results
- [ ] Handle multiprocessing exceptions

### Task 5.4: main.py - Final Steps
- [ ] Call task_analysis with all results
- [ ] Print summary to console
- [ ] Log completion
- [ ] Clean exit with status code

---

## Phase 6: Visualization 🟣

### Task 6.1: visualizer.py - Setup
- [ ] Import matplotlib, seaborn
- [ ] Configure plot style
- [ ] Create results directory if not exists
- [ ] Implement save_plot() helper function
- **Lines:** ~130 total

### Task 6.2: visualizer.py - Accuracy Plots
- [ ] Implement plot_accuracy_distribution()
- [ ] Create box plot for Stage 1 accuracy
- [ ] Create box plot for Stage 2 accuracy
- [ ] Create box plot for overall accuracy
- [ ] Add mean markers
- [ ] Save to results/accuracy_distribution.png

### Task 6.3: visualizer.py - Confusion Matrix
- [ ] Implement plot_confusion_matrix()
- [ ] Aggregate confusion matrices across iterations
- [ ] Create heatmap with annotations
- [ ] Add proper labels
- [ ] Save to results/confusion_matrix.png

### Task 6.4: visualizer.py - Statistics Plot
- [ ] Implement plot_statistics_summary()
- [ ] Create bar chart with error bars
- [ ] Show mean ± std for each metric
- [ ] Add horizontal line for baseline
- [ ] Save to results/statistics_summary.png

### Task 6.5: statistics.py
- [ ] Implement calculate_statistics() function
- [ ] Calculate mean, std, min, max, median
- [ ] Calculate confidence intervals
- [ ] Format statistical report
- [ ] Return statistics dictionary
- [ ] Add logging
- **Lines:** ~80

---

## Phase 7: Testing & Documentation ⚪

### Task 7.1: Unit Tests
- [ ] Test data_loader with sample data
- [ ] Test preprocessor functions
- [ ] Test SVM training
- [ ] Test evaluator metrics calculation
- [ ] Test grouping logic

### Task 7.2: Integration Tests
- [ ] Test complete Stage 1 pipeline
- [ ] Test complete Stage 2 pipeline
- [ ] Test full single iteration
- [ ] Test result aggregation

### Task 7.3: System Tests
- [ ] Run full 5-iteration cycle
- [ ] Verify all log files created
- [ ] Verify ring buffer works correctly
- [ ] Verify all visualizations generated
- [ ] Check file sizes and counts

### Task 7.4: README.md
- [ ] Write installation instructions
- [ ] Document virtual environment setup
- [ ] Explain how to run the program
- [ ] Describe output files
- [ ] Add troubleshooting section
- [ ] Include example results

### Task 7.5: Final Documentation
- [ ] Review and update Claude.md
- [ ] Complete this tasks.md checklist
- [ ] Add inline code comments
- [ ] Generate API documentation (optional)
- [ ] Create usage examples

---

## Progress Tracking

### Overall Progress
- Phase 1 (Setup): ⬜⬜⬜⬜ 0/4 tasks
- Phase 2 (Core): ⬜⬜⬜⬜ 0/4 tasks
- Phase 3 (ML): ⬜⬜ 0/2 tasks
- Phase 4 (Tasks): ⬜⬜⬜ 0/3 tasks
- Phase 5 (Main): ⬜⬜⬜⬜ 0/4 tasks
- Phase 6 (Viz): ⬜⬜⬜⬜⬜ 0/5 tasks
- Phase 7 (Test): ⬜⬜⬜⬜⬜ 0/5 tasks

**Total: 0/27 major tasks completed**

---

## Critical Path

```
Setup (1.1-1.4)
    ↓
Core (2.1-2.4) → ML (3.1-3.2)
    ↓
Tasks (4.1-4.3)
    ↓
Main (5.1-5.4)
    ↓
Viz (6.1-6.5) + Testing (7.1-7.3)
    ↓
Documentation (7.4-7.5)
```

---

## Notes

### File Size Monitoring
- Keep track of line counts during development
- Refactor if approaching 150 line limit
- Split large functions into smaller helpers

### Common Issues to Watch
- Path separators (use pathlib)
- Multiprocessing on WSL (test early)
- Log file permissions
- CSV encoding (UTF-8)
- Random seed consistency

### Testing Checkpoints
- ✓ After each Phase, run integration test
- ✓ Test with small data first
- ✓ Verify logging output
- ✓ Check memory usage with multiprocessing

---

## Dependencies Checklist

- [ ] numpy >= 1.21.0
- [ ] pandas >= 1.3.0
- [ ] scikit-learn >= 1.0.0
- [ ] matplotlib >= 3.4.0
- [ ] seaborn >= 0.11.0

---

## Completion Criteria

- ✅ All code files created and under 150 lines
- ✅ Virtual environment properly configured
- ✅ All 5 iterations run successfully
- ✅ Logging system works with ring buffer
- ✅ All visualizations generated
- ✅ Results show expected accuracy (>80%)
- ✅ No absolute paths in code
- ✅ Multiprocessing provides performance improvement
- ✅ Documentation complete and accurate
- ✅ Code passes all tests