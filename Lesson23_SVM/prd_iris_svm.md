# Product Requirements Document (PRD)
## Iris Dataset Multi-Class SVM Classification

**Author:** Yair Levi  
**Version:** 1.0  
**Date:** December 2025

---

## 1. Overview

### 1.1 Purpose
Develop a Python program that classifies the Iris dataset using Support Vector Machine (SVM) through a hierarchical binary classification approach.

### 1.2 Scope
The program will:
- Load and process the Iris dataset (3 classes)
- Implement hierarchical SVM classification strategy
- Perform statistical analysis over multiple iterations
- Generate comprehensive results and visualizations

---

## 2. Technical Requirements

### 2.1 Environment
- **Platform:** WSL (Windows Subsystem for Linux)
- **Python Version:** 3.8+
- **Virtual Environment:** Located at `../../venv/` relative to project root
- **Working Directory:** `C:\Users\yair0\AI_continue\Lesson23\Lesson23_SVM`

### 2.2 Code Structure
- **Package Structure:** Proper Python package with `__init__.py`
- **File Size Limit:** Maximum 150 lines per Python file
- **Path Handling:** All paths must be relative
- **Modularity:** Main program calls task modules

### 2.3 Performance
- **Multiprocessing:** Utilize when possible for parallel execution
- **Memory Management:** Efficient handling of dataset and models

### 2.4 Logging
- **Level:** INFO and above
- **Format:** Ring buffer with 20 files
- **File Size:** Maximum 16MB per file
- **Behavior:** Circular overwrite when buffer full
- **Location:** `./log/` subfolder

---

## 3. Functional Requirements

### 3.1 Data Processing
- **Input:** `./iris.csv` (Iris dataset with 3 classes)
- **Split:** 75% training, 25% testing
- **Validation:** Data integrity checks

### 3.2 Classification Strategy

#### Stage 1: First Binary Split
1. Divide 3 classes into 2 groups:
   - Group A: 1 class
   - Group B: 2 classes
2. Train SVM to classify Group A vs Group B
3. Test classification accuracy

#### Stage 2: Second Binary Split
1. Extract Group B samples (2 classes)
2. Train SVM to classify between these 2 classes
3. Test classification accuracy

### 3.3 Statistical Analysis
- **Iterations:** Run complete classification 5 times
- **Metrics:** 
  - Accuracy per stage
  - Confusion matrices
  - Precision, Recall, F1-score
- **Aggregation:** Mean, standard deviation, min, max

### 3.4 Visualization
Generate plots showing:
- Accuracy distribution across iterations
- Confusion matrices (aggregated)
- Classification boundaries (if 2D projection)
- Performance comparison between stages

---

## 4. Deliverables

### 4.1 Code Files
- Main program entry point
- Task modules (data loading, preprocessing, training, evaluation)
- Utility modules (logging, visualization)
- Package initialization files

### 4.2 Configuration Files
- `requirements.txt` - Python dependencies
- Package setup configuration

### 4.3 Documentation
- `Claude.md` - Claude AI interaction notes
- `planning.md` - Development planning and architecture
- `tasks.md` - Task breakdown and progress tracking
- `README.md` - User guide and setup instructions

### 4.4 Output
- Log files in `./log/` directory
- Result visualizations (PNG/PDF)
- Summary statistics (CSV/JSON)

---

## 5. Dependencies

### 5.1 Core Libraries
- `numpy` - Numerical computations
- `pandas` - Data manipulation
- `scikit-learn` - SVM and ML utilities
- `matplotlib` - Visualization
- `seaborn` - Statistical visualizations

### 5.2 Standard Libraries
- `logging` - Logging infrastructure
- `multiprocessing` - Parallel processing
- `pathlib` - Path handling
- `json` - Data serialization

---

## 6. Success Criteria

### 6.1 Functional
- Successfully classify all 3 Iris classes
- Achieve reasonable accuracy (>80% expected)
- Generate all required visualizations
- Complete 5 iterations without errors

### 6.2 Technical
- Code adheres to 150 lines per file limit
- Logging system works as specified
- Relative paths function correctly
- Package structure is proper and importable

### 6.3 Quality
- Clean, readable, maintainable code
- Proper error handling
- Comprehensive logging
- Clear documentation

---

## 7. Risk Mitigation

### 7.1 Technical Risks
- **Risk:** Path issues between Windows and WSL
  - **Mitigation:** Use `pathlib` for cross-platform compatibility
  
- **Risk:** Memory issues with multiprocessing
  - **Mitigation:** Monitor resource usage, limit worker processes

### 7.2 Data Risks
- **Risk:** Imbalanced dataset split
  - **Mitigation:** Use stratified splitting
  
- **Risk:** Poor classification in hierarchical approach
  - **Mitigation:** Document performance, consider alternative groupings

---

## 8. Future Enhancements
- Support for other multi-class datasets
- Configurable number of iterations
- Additional SVM kernels comparison
- Cross-validation implementation
- Export trained models for reuse