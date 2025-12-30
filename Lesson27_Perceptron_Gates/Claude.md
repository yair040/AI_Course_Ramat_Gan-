# Claude.md - AI Assistant Guide
# Perceptron Gates Neural Network Project

**Author:** Yair Levi
**Project:** Perceptron Gates Implementation
**Date:** 2025-12-30

## Project Overview

This project implements AND and XOR logic gates using Keras neural networks with perceptrons. It demonstrates fundamental concepts in neural network design, training, and visualization.

## Quick Start for AI Assistants

### Project Context
- **Language:** Python 3.8+
- **Platform:** WSL (Windows Subsystem for Linux)
- **Virtual Environment:** Located at `../../venv` from project root
- **Current Directory:** `/mnt/c/Users/yair0/AI_continue/Lesson27/perceptron_gates`

### Key Constraints
1. Each Python file must be ≤ 150 lines
2. Use relative paths only (no absolute paths)
3. Virtual environment at `../../venv`
4. All artifacts in current folder
5. Multiprocessing where beneficial

### Project Structure
```
perceptron_gates/
├── __init__.py              # Package initialization
├── logger_config.py         # Ring buffer logging setup
├── dataset_generator.py     # Generate noisy datasets
├── models.py                # Keras model definitions
├── trainer.py               # Training orchestration
├── visualizer.py            # Network and data visualization
├── main.py                  # Main entry point
├── requirements.txt         # Python dependencies
├── PRD.md                   # Product requirements
├── planning.md              # Architecture planning
├── tasks.md                 # Implementation tasks
├── Claude.md                # This file
└── log/                     # Log files (runtime)
```

## Technical Specifications

### Neural Network Architectures

**AND Gate (Linearly Separable):**
- Input: 2 neurons
- Hidden: None
- Output: 1 neuron (sigmoid)
- Total: 3 parameters

**XOR Gate (Non-Linearly Separable):**
- Input: 2 neurons
- Hidden: 2 neurons (sigmoid)
- Output: 1 neuron (sigmoid)
- Total: 9 parameters

### Dataset Specifications
- **Size:** 600 samples per gate
- **Base:** Truth table (4 combinations × 150 replications)
- **Noise:** +15% uniform random noise
- **Format:** NumPy arrays

### Logging System
- **Type:** Ring buffer with 20 rotating files
- **Size:** 16 MB per file
- **Location:** `./log/` subfolder
- **Format:** `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- **Level:** INFO and above

### Training Parameters
- **Loss:** Mean Squared Error (MSE)
- **Optimizer:** Adam (default learning rate: 0.001)
- **Epochs:** 500
- **Batch Size:** 32
- **Validation Split:** 20%

## Code Guidelines

### Import Standards
```python
# Standard library
import os
import logging
from pathlib import Path

# Third-party
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from keras import layers

# Local
from . import logger_config
from . import dataset_generator
```

### Path Handling
```python
# Get project root
PROJECT_ROOT = Path(__file__).parent

# Log directory
LOG_DIR = PROJECT_ROOT / "log"

# Model directory
MODEL_DIR = PROJECT_ROOT / "models"

# Always use relative paths
```

### Logging Usage
```python
import logging

logger = logging.getLogger(__name__)

logger.info("Training started")
logger.warning("Convergence slow")
logger.error("Model save failed")
```

### Multiprocessing Pattern
```python
from multiprocessing import Pool, cpu_count

def process_gate(gate_type):
    # Process single gate
    return result

if __name__ == "__main__":
    with Pool(processes=2) as pool:
        results = pool.map(process_gate, ["and", "xor"])
```

## Common Tasks

### Running the Project
```bash
# Activate virtual environment
source ../../venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run main program
python -m perceptron_gates.main
```

### Adding New Gate
1. Update `models.py` with new architecture
2. Add truth table to `dataset_generator.py`
3. Update `trainer.py` to include new gate
4. Update `visualizer.py` for new diagrams

### Debugging
- Check logs in `./log/` directory
- Use `logging.DEBUG` level for detailed output
- Verify dataset shapes before training
- Check model summaries with `model.summary()`

## Module Descriptions

### logger_config.py
- Sets up rotating file handler
- Configures ring buffer (20 files × 16 MB)
- Provides `setup_logger()` function

### dataset_generator.py
- `generate_truth_table(gate_type)`: Creates base truth table
- `add_noise(data, noise_level)`: Adds random noise
- `create_dataset(gate_type, samples)`: Full dataset with noise

### models.py
- `create_and_model()`: Single layer network
- `create_xor_model()`: Two-layer network
- Both compiled with MSE loss and Adam optimizer

### trainer.py
- `train_model(model, X, y, epochs, batch_size)`: Training loop
- `evaluate_model(model, X, y)`: Performance metrics
- Saves training history and models

### visualizer.py
- `plot_network_architecture(model, gate_type)`: Network diagram
- `plot_data_points(X, y, gate_type)`: Scatter plot with colors
- `plot_training_history(history, gate_type)`: Loss/accuracy curves

### main.py
- Orchestrates all modules
- Uses multiprocessing for parallel tasks
- Coordinates dataset generation, training, visualization

## Expected Outputs

### Files Generated
- `models/and_model.keras` - Trained AND gate model
- `models/xor_model.keras` - Trained XOR gate model
- `visualizations/and_network.png` - AND architecture
- `visualizations/xor_network.png` - XOR architecture
- `visualizations/and_data.png` - AND data points
- `visualizations/xor_data.png` - XOR data points
- `visualizations/and_training.png` - AND training curves
- `visualizations/xor_training.png` - XOR training curves
- `log/*.log` - Rotating log files

### Performance Expectations
- AND gate accuracy: > 95%
- XOR gate accuracy: > 95%
- Training time: < 5 minutes total
- Memory usage: < 500 MB

## Troubleshooting

### Issue: Import errors
**Solution:** Ensure running as package: `python -m perceptron_gates.main`

### Issue: Log directory not found
**Solution:** Code creates it automatically, check permissions

### Issue: Virtual environment not found
**Solution:** Verify venv at `../../venv` or create new one

### Issue: XOR not converging
**Solution:** Increase epochs or adjust network architecture

### Issue: Keras/TensorFlow warnings
**Solution:** Normal for CPU-only execution on WSL

## Development Workflow

1. **Setup:** Create venv, install requirements
2. **Test Logger:** Run logger_config standalone
3. **Test Data:** Run dataset_generator standalone
4. **Test Models:** Create and inspect model summaries
5. **Test Training:** Train on small epochs count
6. **Test Visualization:** Generate one plot at a time
7. **Integration:** Run full main.py
8. **Validation:** Check accuracy, logs, plots

## Notes for AI Assistants

- Always check file line counts (≤ 150)
- Use relative paths in all code
- Test each module independently before integration
- Respect the ring buffer logging pattern
- Keep visualizations simple and clear
- Use multiprocessing for independent tasks only
- Handle keyboard interrupts gracefully
- Save models with `.keras` extension (Keras 3)
- Close matplotlib figures to prevent memory leaks

## References

- **Keras Documentation:** https://keras.io/
- **TensorFlow:** https://www.tensorflow.org/
- **NumPy:** https://numpy.org/
- **Matplotlib:** https://matplotlib.org/
- **Python Logging:** https://docs.python.org/3/library/logging.html
- **Multiprocessing:** https://docs.python.org/3/library/multiprocessing.html
