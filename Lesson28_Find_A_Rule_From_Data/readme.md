# Finds a Rule from Data

## Overview

This project demonstrates how a **machine can discover a mathematical rule from data** using a **neuron-based model** trained with **backpropagation**, without activation functions.

The project is implemented as a **Google Colab / Jupyter notebook** and follows the specifications defined in `PRD.md`.

The discovered rule corresponds to the well-known **Celsius → Fahrenheit** conversion.

---

## Project Goals

- Show that a simple neuron can discover a mathematical rule from examples
- Compare a **single-neuron** solution with a **multi-neuron** solution
- Use **Keras** and **backpropagation** in a transparent, educational way
- Visualize learning error and neuron structures
- Keep the code clear, readable, and demo-oriented

---

## Dataset

The dataset is fixed, known in advance, and contains **no noise**.

```python
celsius_q = np.array([-40, -10, 0, 8, 15, 22, 38], dtype=float)
fahrenheit_a = np.array([-40, 14, 32, 46.4, 59, 71.6, 100], dtype=float)
```

Each training step evaluates **a single scalar input → scalar output**.

---

## Tasks Implemented

### Task A — Single Neuron Rule Discovery

- One linear neuron (`Dense(1)`)
- No activation function
- Adam optimizer (learning rate = 0.1)
- 500 training epochs
- Learned rule printed as an explicit equation
- Neuron diagram drawn (input, weight, bias, output)
- Test on **100°C** with absolute error calculation

### Task B — Multi-Neuron Rule Discovery

- Linear hidden layer + linear output layer
- No activation functions
- Adam optimizer (learning rate = 0.1)
- 500 training epochs
- Neuron network diagram drawn
- Test on **100°C** with absolute error calculation

---

## Metrics & Visualization

- **Mean Squared Error (MSE)** used for training and evaluation
- MSE vs Epoch plots generated using Keras history
- Neuron network diagrams rendered with Matplotlib

---

## Technologies Used

- Python 3
- Google Colab / Jupyter Notebook
- TensorFlow / Keras
- NumPy
- Matplotlib
- Python logging (rotating ring buffer)

---

## Logging

- INFO-level logging
- Rotating ring buffer:
  - 20 log files
  - 16 MB per file
  - Circular overwrite
- Logs stored in the `log/` directory

---

## How to Run

### Option 1: Google Colab
1. Open Google Colab
2. Upload `Finds_a_Rule_From_Data.ipynb`
3. Run all cells

### Option 2: Local Jupyter
1. Install dependencies:
   ```bash
   pip install tensorflow numpy matplotlib
   ```
2. Open the notebook:
   ```bash
   jupyter notebook Finds_a_Rule_From_Data.ipynb
   ```
3. Run all cells

---

## Project Structure

```
.
├── PRD.md
├── README.md
├── Finds_a_Rule_From_Data.ipynb
└── log/
```

---

## Conceptual Takeaways

- A **single linear neuron** is sufficient to learn the Celsius → Fahrenheit rule
- Multi-neuron networks converge to the same solution
- Backpropagation works even without activation functions for linear problems
- Rule discovery is possible without classification or deep architectures

---

## License

This project is intended for **educational and demonstration purposes**.

