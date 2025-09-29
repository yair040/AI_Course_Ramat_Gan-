# Linear Regression Visualization with Random Line Sampling

A Monte Carlo approach to finding the best-fitting line through random sampling of candidate lines, visualized with scatter plots.

## Overview

This project demonstrates an alternative approach to linear regression by randomly generating candidate lines and selecting the one with minimum squared error. Instead of using analytical methods (like least squares), it uses random sampling to find an approximate best-fit line.

## Features

- **Random Point Generation**: Creates 1000 random points in a unit square [0,1] × [0,1]
- **Vectorized Computation**: All error calculations use array operations for optimal performance
- **Random Line Sampling**: Evaluates 100 randomly generated lines
- **Best-Fit Selection**: Identifies and visualizes the line with minimum total squared error
- **Visual Output**: Scatter plot with points and best-fit line

## Algorithm

### 1. Data Generation
- Generate 1000 random points with coordinates (x, y)
  - x ∈ [0, 1]
  - y ∈ [0, 1]

### 2. Line Parameter Generation
For each of 100 random lines (y = ax + b):
- **Intercept (b)**: Uniform random in [0, 1]
- **Slope (a)**: Uniform random in [0, π/2 - 0.0017]
  - Maximum slope ≈ 1.5691 radians
  - Ensures slope doesn't reach vertical (π/2)

### 3. Error Calculation (Vectorized)
For each line, calculate total squared error:
```
error = Σ(y - a*x - b)²
```
- No loops used - all calculations vectorized
- Computes errors for all 1000 points simultaneously

### 4. Best Line Selection
- Find line with minimum total squared error
- Display this line on the scatter plot

## Mathematical Background

### Squared Error Formula
The squared error measures the vertical distance from each point to the line:
```
error_i = (y_i - a*x_i - b)²
```

Total error for a line:
```
Total_Error = Σ(i=1 to 1000) error_i
```

### Slope Constraint
- Slope range: [0, π/2 - 0.0017) radians
- In degrees: [0°, 89.9°)
- This prevents near-vertical lines while maintaining uniform distribution

## Technical Specifications

### Requirements
- Python 3.7+
- NumPy (vectorized operations)
- Matplotlib (visualization)

### Performance
- **Vectorization**: All 1000 × 100 = 100,000 error calculations performed without loops
- **Memory Efficient**: Uses array broadcasting for optimal memory usage
- **Fast Execution**: Typically completes in under 1 second

## Output

### Visualization
- **Title**: "Scatter plot of points"
- **Red Points**: 1000 randomly generated data points
- **Best-Fit Line**: Line with minimum squared error across all 100 candidates
- **Axes**: X-axis and Y-axis ranging from 0 to 1

## Usage Example

```python
import numpy as np
import matplotlib.pyplot as plt

# 1. Generate 1000 random points
n_points = 1000
x = np.random.uniform(0, 1, n_points)
y = np.random.uniform(0, 1, n_points)

# 2. Generate 100 random lines
n_lines = 100
b = np.random.uniform(0, 1, n_lines)
a = np.random.uniform(0, np.pi/2 - 0.0017, n_lines)

# 3. Vectorized error calculation
# Reshape for broadcasting: (n_points, 1) and (n_lines,)
errors = (y[:, np.newaxis] - a * x[:, np.newaxis] - b) ** 2
total_errors = np.sum(errors, axis=0)

# 4. Find best line
min_idx = np.argmin(total_errors)
best_a, best_b = a[min_idx], b[min_idx]

# 5. Plot
plt.scatter(x, y, color='red', s=10)
x_line = np.linspace(0, 1, 100)
y_line = best_a * x_line + best_b
plt.plot(x_line, y_line, 'b-', linewidth=2)
plt.title('Scatter plot of points')
plt.xlabel('x')
plt.ylabel('y')
plt.show()
```

## Key Concepts

### Why Vectorization?
- **Speed**: 100-1000x faster than loops for large datasets
- **Readability**: More concise and mathematical notation
- **Optimization**: Leverages optimized C/Fortran libraries

### Why Random Sampling?
- **Educational**: Demonstrates Monte Carlo methods
- **Comparison**: Shows alternative to analytical solutions
- **Simplicity**: Easier to understand than gradient descent

### Limitations
- **Not Optimal**: Random sampling doesn't guarantee global minimum
- **Computational Cost**: More lines needed for better approximation
- **Convergence**: No guarantee of finding true best-fit line

## Comparison with Least Squares

| Method | Computation | Accuracy | Speed |
|--------|-------------|----------|-------|
| Random Sampling (100 lines) | O(n × k) | Approximate | Fast |
| Least Squares | O(n) | Optimal | Faster |

Where n = number of points, k = number of candidate lines

## Extensions

Potential improvements and variations:
- Increase number of candidate lines (1000, 10000)
- Compare result with analytical least squares regression
- Add confidence intervals or error metrics
- Implement adaptive sampling (focus on promising regions)
- Visualize all candidate lines with transparency

## License

This project is provided as-is for educational purposes.

## Author

Created as a demonstration of Monte Carlo methods and vectorized computing in Python.

---

**Version**: 1.0  
**Last Updated**: September 2025