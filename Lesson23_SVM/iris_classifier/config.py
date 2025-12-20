"""
Configuration module for Iris SVM Classification System.
Author: Yair Levi
"""

from pathlib import Path
import logging

# Project paths - all relative
PROJECT_ROOT = Path(__file__).parent.parent
DATA_PATH = PROJECT_ROOT / "iris.csv"
LOG_DIR = PROJECT_ROOT / "log"
RESULTS_DIR = PROJECT_ROOT / "results"
VENV_PATH = PROJECT_ROOT.parent.parent / "venv"

# ML Parameters
TRAIN_SPLIT = 0.75
TEST_SPLIT = 0.25
RANDOM_STATE = 42
NUM_ITERATIONS = 5

# SVM Hyperparameters
SVM_KERNEL = 'rbf'
SVM_C = 1.0
SVM_GAMMA = 'scale'

# Logging Parameters
LOG_MAX_BYTES = 16 * 1024 * 1024  # 16MB
LOG_BACKUP_COUNT = 19  # 20 total files (current + 19 backups)
LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s'

# Class grouping for hierarchical classification
# Stage 1: Group A (class 0) vs Group B (classes 1,2)
STAGE1_GROUP_A = [0]  # Iris-setosa
STAGE1_GROUP_B = [1, 2]  # Iris-versicolor, Iris-virginica

# Visualization parameters
FIGURE_DPI = 100
FIGURE_SIZE = (10, 6)


class Config:
    """Configuration class for runtime settings."""
    
    def __init__(self):
        self.project_root = PROJECT_ROOT
        self.data_path = DATA_PATH
        self.log_dir = LOG_DIR
        self.results_dir = RESULTS_DIR
        self.validate_paths()
    
    def validate_paths(self):
        """Validate critical paths exist."""
        if not self.data_path.exists():
            raise FileNotFoundError(f"Data file not found: {self.data_path}")
        
        # Create directories if they don't exist
        self.log_dir.mkdir(exist_ok=True)
        self.results_dir.mkdir(exist_ok=True)
    
    def get_config_summary(self):
        """Return configuration summary as dictionary."""
        return {
            'train_split': TRAIN_SPLIT,
            'test_split': TEST_SPLIT,
            'random_state': RANDOM_STATE,
            'num_iterations': NUM_ITERATIONS,
            'svm_kernel': SVM_KERNEL,
            'svm_c': SVM_C,
            'svm_gamma': SVM_GAMMA,
        }