# Iris Naive Bayes Classification Project

**Author:** Yair Levi
**Project:** Iris Flower Classification using Naive Bayes Algorithm

---

## Overview

This project implements a comprehensive Naive Bayes classifier for the classic Iris flower dataset. The implementation includes both a manual (from-scratch) implementation using NumPy and a library-based implementation using scikit-learn, allowing for educational comparison and validation.

## Key Features

- **Dual Implementation:** Manual NumPy-based and scikit-learn library implementations
- **Educational Focus:** Detailed histogram visualization and probability calculations
- **Professional Logging:** Ring buffer logging system with 20 files × 16MB each
- **Modular Design:** Task-based architecture with files under 200 lines
- **WSL Compatible:** Designed for Windows Subsystem for Linux environment
- **Reproducible:** Fixed random seed for consistent train/test splits

---

## Project Structure

```
Bayes_Classification/
├── iris_classifier/          # Main package
│   ├── __init__.py
│   ├── data_loader.py       # Data loading and preprocessing
│   ├── naive_bayes_manual.py # Manual NumPy implementation
│   ├── naive_bayes_library.py # Scikit-learn implementation
│   ├── visualization.py     # Histogram and confusion matrix plots
│   └── logger_config.py     # Ring buffer logging setup
├── log/                      # Log files (auto-created)
├── iris.csv                  # Dataset
├── main.py                   # Entry point
├── requirements.txt          # Python dependencies
├── PRD.md                    # Product Requirements Document
├── Claude.md                 # This file
├── planning.md               # Technical architecture
└── tasks.md                  # Implementation tasks
```

---

## Installation

### 1. Prerequisites
- WSL (Windows Subsystem for Linux)
- Python 3.8 or higher
- Virtual environment capability

### 2. Setup Virtual Environment

```bash
# Navigate to project directory
cd /mnt/c/Users/yair0/OneDrive/Documents/AI/AI_course_Ramat_Gan/Lesson21/Bayes_Classification

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

### Basic Execution

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Run the main program
python main.py
```

### What the Program Does

1. **Data Loading:** Loads iris.csv and splits into 75% train, 25% test
2. **Training Phase:**
   - Manual method: Calculates prior probabilities and builds histograms
   - Library method: Trains scikit-learn Naive Bayes classifier
3. **Visualization:** Displays 4 graphs showing feature histograms across classes
4. **Testing Phase:**
   - Manual method: Uses logarithmic Naive Bayes formula
   - Library method: Uses trained scikit-learn model
5. **Evaluation:** Displays confusion matrices for both methods

---

## Understanding the Output

### Console Output

- **Prior Probabilities:** P(Ci) for each class (setosa, versicolor, virginica)
- **Training Progress:** Status of histogram generation
- **Test Accuracy:** Confusion matrices for both methods
- **Comparison:** Performance comparison between manual and library methods

### Visualizations

1. **Sepal Length Histogram** - Shows distribution across 3 classes
2. **Sepal Width Histogram** - Shows distribution across 3 classes
3. **Petal Length Histogram** - Shows distribution across 3 classes
4. **Petal Width Histogram** - Shows distribution across 3 classes
5. **Confusion Matrices** - One for manual method, one for library method

### Log Files

- Located in `log/` directory
- 20 rotating files, each up to 16MB
- Format: `iris_classifier_01.log` through `iris_classifier_20.log`
- INFO level and above messages

---

## Algorithm Details

### Manual Implementation

**Training:**
1. Calculate P(Ci) = count(class i) / total_samples
2. For each class and each feature:
   - Build histogram with automatic binning
   - Apply Laplace smoothing (add 1 to empty bins)

**Testing:**
1. For each test sample:
   - Find histogram bin for each feature value
   - Calculate P(Xi|Ci) = bin_area / total_histogram_area
   - Apply formula: P(Ci|X) = log(P(Ci)) + Σ log(P(Xi|Ci))
   - Assign class with highest probability

### Library Implementation

Uses scikit-learn's GaussianNB (Gaussian Naive Bayes):
- Assumes features follow Gaussian distribution
- Automatically calculates mean and variance per class per feature
- Applies Bayes theorem for classification

---

## Performance Considerations

- **Multiprocessing:** Used for parallel histogram generation (12 histograms)
- **NumPy Vectorization:** Efficient array operations for probability calculations
- **Memory Management:** Ring buffer prevents unlimited log file growth

---

## Troubleshooting

### Issue: Virtual environment activation fails
**Solution:** Ensure Python 3 and venv module are installed:
```bash
sudo apt update
sudo apt install python3 python3-venv
```

### Issue: iris.csv not found
**Solution:** Ensure iris.csv is in the project root directory with proper headers

### Issue: Log directory permission denied
**Solution:** The program auto-creates the log/ directory. Ensure write permissions:
```bash
chmod +w .
```

### Issue: Plots not displaying
**Solution:** Ensure matplotlib backend is configured. For WSL:
```bash
export DISPLAY=:0
```
Or use non-interactive backend in the code (already configured).

---

## Educational Value

This project demonstrates:

1. **Probability Theory:** Prior probabilities, conditional probabilities, Bayes theorem
2. **Statistical Methods:** Histogram binning, Laplace smoothing
3. **Numerical Stability:** Logarithmic form to prevent underflow
4. **Software Engineering:** Modular design, logging, package structure
5. **Validation:** Comparing manual implementation with established library

---

## Dataset Information

**Iris Dataset:**
- **Samples:** 150 total (50 per class)
- **Features:** 4 continuous measurements in centimeters
- **Classes:** 3 species (setosa, versicolor, virginica)
- **Source:** Classic dataset from R.A. Fisher (1936)

**Feature Descriptions:**
1. Sepal Length: Length of the sepal (cm)
2. Sepal Width: Width of the sepal (cm)
3. Petal Length: Length of the petal (cm)
4. Petal Width: Width of the petal (cm)

---

## Extension Ideas

- Add k-fold cross-validation
- Experiment with different bin sizes
- Implement other probability distributions
- Add feature importance analysis
- Create interactive visualization dashboard
- Export results to CSV or JSON

---

## References

- Fisher, R.A. (1936). "The use of multiple measurements in taxonomic problems"
- Naive Bayes Classification: [Scikit-learn Documentation](https://scikit-learn.org/stable/modules/naive_bayes.html)
- Laplace Smoothing in Naive Bayes

---

## License

Educational project for AI course at Ramat Gan.

## Contact

**Author:** Yair Levi
**Purpose:** AI Course - Lesson 21
**Date:** 2025-12-03
