# Product Requirements Document (PRD)
# Perceptron Gates Neural Network

**Author:** Yair Levi
**Date:** 2025-12-30
**Version:** 1.0

## 1. Overview

Implementation of AND and XOR logic gates using Keras neural networks with perceptrons. The project demonstrates fundamental neural network concepts including training, dataset generation with noise, and visualization.

## 2. Objectives

- Implement minimum perceptron networks for AND and XOR gates
- Generate synthetic datasets with controlled noise
- Train neural networks to learn logic gate behavior
- Visualize network architecture and data distributions
- Provide comprehensive logging and error tracking

## 3. Technical Requirements

### 3.1 Environment
- **Platform:** WSL (Windows Subsystem for Linux)
- **Python Version:** 3.8+
- **Virtual Environment:** Located at `../../venv` relative to project root

### 3.2 Architecture
- Package-based structure with proper `__init__.py`
- Modular design: each file ≤ 150 lines
- Relative paths throughout
- Multiprocessing where applicable

### 3.3 Neural Network Specifications

#### AND Gate
- **Architecture:** Minimum perceptrons required
- **Input:** 2 binary inputs (0 or 1)
- **Output:** 1 binary output
- **Truth Table:** Standard AND logic

#### XOR Gate
- **Architecture:** Minimum perceptrons required (requires hidden layer)
- **Input:** 2 binary inputs (0 or 1)
- **Output:** 1 binary output
- **Truth Table:** Standard XOR logic

### 3.4 Dataset Requirements
- **Size:** 600 samples per gate (AND, XOR)
- **Base Data:** Truth table values
- **Noise:** 15% random positive noise around true points
- **Format:** NumPy arrays compatible with Keras

### 3.5 Training Parameters
- **Loss Function:** Mean Squared Error (MSE): `(expected - result)²`
- **Learning Rate:** Keras default
- **Optimizer:** Adam (default)
- **Metrics:** Accuracy, Loss

### 3.6 Logging System
- **Level:** INFO and above
- **Format:** Ring buffer system
- **Files:** 20 rotating log files
- **Size:** 16 MB per file
- **Location:** `./log/` subfolder
- **Behavior:** Overwrite oldest when full

### 3.7 Visualization
- Network architecture diagram showing:
  - Input nodes
  - Hidden layers with perceptrons
  - Output nodes
  - Weights and connections
- Data point clouds for both gates
- Training history plots

## 4. Functional Requirements

### 4.1 Core Modules

1. **Dataset Generator** (`dataset_generator.py`)
   - Generate truth tables
   - Add controlled noise
   - Create training/validation splits

2. **Network Models** (`models.py`)
   - Define AND gate network architecture
   - Define XOR gate network architecture
   - Model compilation and configuration

3. **Training Engine** (`trainer.py`)
   - Train models with datasets
   - Track training metrics
   - Save trained models

4. **Visualization** (`visualizer.py`)
   - Plot network architecture
   - Plot data point clouds
   - Plot training history

5. **Logging Configuration** (`logger_config.py`)
   - Configure rotating file handler
   - Set up ring buffer logging
   - Format log messages

6. **Main Program** (`main.py`)
   - Orchestrate all tasks
   - Handle multiprocessing
   - Coordinate module execution

## 5. Performance Requirements

- Training time: < 5 minutes per gate
- Memory usage: < 500 MB
- Log file management: Automatic rotation
- Multiprocessing for parallel tasks where beneficial

## 6. Deliverables

- [ ] Complete Python package structure
- [ ] All modules (≤ 150 lines each)
- [ ] requirements.txt
- [ ] Documentation (PRD, planning, tasks, Claude)
- [ ] Trained models
- [ ] Visualization outputs
- [ ] Log system

## 7. Success Criteria

- AND gate: > 95% accuracy
- XOR gate: > 95% accuracy
- All visualizations generated
- Logging system functional
- Package installable and runnable

## 8. Constraints

- File size: ≤ 150 lines per Python file
- Relative paths only
- Virtual environment location fixed
- WSL compatibility required

## 9. Future Enhancements

- Additional logic gates (OR, NAND, NOR)
- More complex noise patterns
- Hyperparameter tuning interface
- Web-based visualization dashboard
