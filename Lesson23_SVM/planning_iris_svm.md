# Planning Document
## Iris SVM Classification System

**Author:** Yair Levi  
**Project:** Lesson23_SVM

---

## 1. Architecture Overview

```
Lesson23_SVM/
├── iris_classifier/          # Main package
│   ├── __init__.py
│   ├── config.py            # Configuration and constants
│   ├── logger_setup.py      # Logging configuration
│   ├── data_loader.py       # Data loading and splitting
│   ├── preprocessor.py      # Data preprocessing
│   ├── svm_trainer.py       # SVM training logic
│   ├── evaluator.py         # Model evaluation
│   ├── visualizer.py        # Visualization generation
│   └── statistics.py        # Statistical analysis
├── tasks/                    # Task modules
│   ├── __init__.py
│   ├── task_stage1.py       # Stage 1 classification
│   ├── task_stage2.py       # Stage 2 classification
│   └── task_analysis.py     # Results analysis
├── main.py                   # Entry point
├── log/                      # Log files (auto-created)
├── results/                  # Output files (auto-created)
├── iris.csv                  # Input dataset
├── requirements.txt
├── README.md
├── Claude.md
├── planning.md
└── tasks.md
```

---

## 2. Module Responsibilities

### 2.1 Core Package (`iris_classifier/`)

#### `config.py`
- Define constants (paths, parameters)
- Configuration class for runtime settings
- Lines: ~50

#### `logger_setup.py`
- Initialize rotating file handler (20 files × 16MB)
- Configure logging format
- Provide logger factory function
- Lines: ~60

#### `data_loader.py`
- Load iris.csv using relative paths
- Validate data integrity
- Split data (75% train, 25% test, stratified)
- Lines: ~80

#### `preprocessor.py`
- Feature scaling/normalization
- Handle missing values (if any)
- Encode target labels
- Lines: ~70

#### `svm_trainer.py`
- Train SVM models with specified kernel
- Hyperparameter management
- Model persistence (optional)
- Lines: ~90

#### `evaluator.py`
- Calculate accuracy, precision, recall, F1
- Generate confusion matrices
- Store metrics per iteration
- Lines: ~100

#### `visualizer.py`
- Plot accuracy distributions
- Confusion matrix heatmaps
- Statistical summaries
- Decision boundary plots (optional)
- Lines: ~130

#### `statistics.py`
- Aggregate results from multiple iterations
- Calculate mean, std, min, max
- Generate statistical reports
- Lines: ~80

### 2.2 Task Modules (`tasks/`)

#### `task_stage1.py`
- Implement Stage 1: Group A (1 class) vs Group B (2 classes)
- Load data, preprocess, train, evaluate
- Return results dictionary
- Lines: ~120

#### `task_stage2.py`
- Implement Stage 2: Separate 2 classes in Group B
- Filter data for Group B only
- Train, evaluate on Group B
- Return results dictionary
- Lines: ~100

#### `task_analysis.py`
- Aggregate all iteration results
- Generate final statistics
- Coordinate visualization creation
- Save summary reports
- Lines: ~110

### 2.3 Entry Point

#### `main.py`
- Parse command-line arguments (optional)
- Initialize logging system
- Orchestrate 5 iterations
- Call task modules
- Handle multiprocessing coordination
- Generate final output
- Lines: ~140

---

## 3. Data Flow

```
1. main.py starts execution
   ↓
2. logger_setup initializes logging
   ↓
3. Loop: 5 iterations
   ↓
   3a. task_stage1.py
       - Load iris.csv (data_loader)
       - Preprocess (preprocessor)
       - Group classes: {0} vs {1,2}
       - Train SVM (svm_trainer)
       - Evaluate (evaluator)
       - Return stage1_results
   ↓
   3b. task_stage2.py
       - Filter Group B samples (classes 1,2)
       - Preprocess
       - Train SVM
       - Evaluate
       - Return stage2_results
   ↓
   3c. Collect results for this iteration
   ↓
4. task_analysis.py
   - Aggregate all iterations
   - Calculate statistics
   - Generate visualizations (visualizer)
   - Save reports
   ↓
5. Program completion
```

---

## 4. Hierarchical Classification Strategy

### 4.1 Stage 1: First Binary Split
**Classes:** Iris-setosa (0), Iris-versicolor (1), Iris-virginica (2)

**Grouping Strategy:**
- **Group A:** Class 0 (Iris-setosa) - label as 0
- **Group B:** Classes 1 & 2 (Iris-versicolor, Iris-virginica) - label as 1

**Rationale:** Iris-setosa is linearly separable from the other two species

### 4.2 Stage 2: Second Binary Split
**Filter:** Only samples from Group B (original classes 1 & 2)

**New Binary Problem:**
- **Class 1:** Iris-versicolor - label as 0
- **Class 2:** Iris-virginica - label as 1

### 4.3 Final Classification
Combine Stage 1 and Stage 2 predictions:
- If Stage 1 predicts Group A → Final class: 0
- If Stage 1 predicts Group B → Use Stage 2 prediction:
  - Stage 2 predicts 0 → Final class: 1
  - Stage 2 predicts 1 → Final class: 2

---

## 5. Logging Strategy

### 5.1 Ring Buffer Configuration
```python
RotatingFileHandler:
  - maxBytes: 16 * 1024 * 1024  (16MB)
  - backupCount: 19  (20 total files including current)
  - File pattern: iris_svm_YYYYMMDD_HHMMSS.log
```

### 5.2 Log Levels
- **INFO:** Normal operations (loading data, training start/end, iteration progress)
- **WARNING:** Non-critical issues (data anomalies, performance degradation)
- **ERROR:** Recoverable errors (single iteration failure)
- **CRITICAL:** Unrecoverable errors (corrupted data, system failure)

### 5.3 Log Content
- Timestamp (ISO 8601)
- Log level
- Module name
- Function name
- Message
- Exception traceback (if applicable)

---

## 6. Multiprocessing Strategy

### 6.1 Parallelizable Tasks
- **5 iterations:** Can run in parallel (data independent)
- **Visualization:** Can generate plots in parallel

### 6.2 Implementation
```python
from multiprocessing import Pool, cpu_count

# Use 80% of available CPUs, max 5 (for 5 iterations)
num_workers = min(5, max(1, int(cpu_count() * 0.8)))

with Pool(processes=num_workers) as pool:
    results = pool.map(run_iteration, range(5))
```

### 6.3 Considerations
- Each process needs independent data copy
- Logging must be process-safe
- Results aggregation after all processes complete

---

## 7. Testing Strategy

### 7.1 Unit Tests
- Test data loader with sample data
- Test preprocessing functions
- Test SVM training with known data
- Test evaluator calculations

### 7.2 Integration Tests
- Test Stage 1 complete pipeline
- Test Stage 2 complete pipeline
- Test full iteration

### 7.3 System Tests
- Run complete 5-iteration cycle
- Verify log files created correctly
- Verify visualizations generated
- Check results accuracy

---

## 8. Error Handling

### 8.1 Data Errors
- Missing iris.csv → Log critical error, exit gracefully
- Corrupted data → Log error, attempt recovery or exit
- Insufficient samples → Log warning, continue if possible

### 8.2 Training Errors
- SVM convergence failure → Log warning, try alternative parameters
- Memory errors → Log error, reduce batch size or features

### 8.3 System Errors
- Log directory creation failure → Log error, fallback to stderr
- Multiprocessing errors → Log error, fallback to sequential

---

## 9. Configuration Parameters

### 9.1 Paths
```python
PROJECT_ROOT = Path(__file__).parent
DATA_PATH = PROJECT_ROOT / "iris.csv"
LOG_DIR = PROJECT_ROOT / "log"
RESULTS_DIR = PROJECT_ROOT / "results"
VENV_PATH = PROJECT_ROOT / ".." / ".." / "venv"
```

### 9.2 ML Parameters
```python
TRAIN_SPLIT = 0.75
TEST_SPLIT = 0.25
RANDOM_STATE = 42
SVM_KERNEL = 'rbf'
SVM_C = 1.0
SVM_GAMMA = 'scale'
NUM_ITERATIONS = 5
```

### 9.3 Logging Parameters
```python
LOG_MAX_BYTES = 16 * 1024 * 1024  # 16MB
LOG_BACKUP_COUNT = 19  # 20 total files
LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s'
```

---

## 10. Development Phases

### Phase 1: Setup (Estimated: 1 hour)
- Create directory structure
- Set up virtual environment
- Install dependencies
- Create placeholder files

### Phase 2: Core Implementation (Estimated: 4 hours)
- Implement config.py
- Implement logger_setup.py
- Implement data_loader.py
- Implement preprocessor.py
- Test basic functionality

### Phase 3: ML Pipeline (Estimated: 3 hours)
- Implement svm_trainer.py
- Implement evaluator.py
- Test training and evaluation

### Phase 4: Task Modules (Estimated: 3 hours)
- Implement task_stage1.py
- Implement task_stage2.py
- Implement task_analysis.py

### Phase 5: Main Program (Estimated: 2 hours)
- Implement main.py
- Add multiprocessing support
- Test complete pipeline

### Phase 6: Visualization (Estimated: 2 hours)
- Implement visualizer.py
- Implement statistics.py
- Generate all required plots

### Phase 7: Testing & Documentation (Estimated: 2 hours)
- Complete testing
- Finalize documentation
- Create README

**Total Estimated Time:** ~17 hours

---

## 11. Success Metrics

### 11.1 Code Quality
- ✓ All files under 150 lines
- ✓ No absolute paths used
- ✓ Proper package structure
- ✓ PEP 8 compliance

### 11.2 Functionality
- ✓ 5 iterations complete successfully
- ✓ Logs generated in ring buffer format
- ✓ All visualizations created
- ✓ Statistical summary accurate

### 11.3 Performance
- ✓ Each iteration completes in < 30 seconds
- ✓ Total runtime < 5 minutes
- ✓ Multiprocessing provides speedup

### 11.4 Results
- ✓ Stage 1 accuracy > 90% (setosa is very separable)
- ✓ Stage 2 accuracy > 80% (versicolor/virginica harder)
- ✓ Overall accuracy > 85%