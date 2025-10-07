# Linear Regression Coefficient Estimation Using Dot Product

A Python application that generates synthetic linear regression data and estimates coefficients using **dot product operations** to demonstrate the connection between linear algebra and statistical regression.

**Author**: Yair Levi

## 📋 Overview

This project implements a complete linear regression analysis workflow using **explicit dot product operations** for coefficient estimation:

1. **Data Generation**: Creates 1000 random points following normal distribution
2. **Linear Model**: Applies Y = β₀ + β₁*X + ε with Gaussian noise
3. **Coefficient Estimation**: Calculates β₀ and β₁ using **dot product formulas**
4. **Visualization**: Single graph showing data points with true and estimated regression lines

## 🎯 Key Features

- ✅ Generates 1000 X points from Normal(μ=0, σ=1)
- ✅ Calculates Y using Y = 0.2 + 0.9*X + ε
- ✅ **Uses dot product for all summation operations**
- ✅ Numerator: `np.dot(X_dev, Y_dev)`
- ✅ Denominator: `np.dot(X_dev, X_dev)`
- ✅ Fully vectorized - no loops!
- ✅ Single comprehensive visualization
- ✅ Educational demonstration of linear algebra in statistics

## 🔑 What Makes This Implementation Special?

### Dot Product Implementation

This implementation **explicitly uses dot product operations** instead of traditional summation methods, making the connection between linear algebra and regression clear:

```python
# Traditional approach (NOT used here):
numerator = np.sum(X_dev * Y_dev)
denominator = np.sum(X_dev ** 2)

# Dot product approach (USED in this implementation):
numerator = np.dot(X_dev, Y_dev)      # Dot product of two vectors
denominator = np.dot(X_dev, X_dev)    # Dot product of vector with itself
```

**Why dot product?**
- Makes the linear algebra foundation explicit
- Demonstrates vector operations in statistics
- Educational value for understanding regression
- More mathematically elegant

## 🚀 Quick Start

### Prerequisites

- Python 3.6 or higher
- NumPy
- Matplotlib

### Installation

```bash
# Clone or download the repository
git clone https://github.com/yourusername/linear-regression-dot-product.git
cd linear-regression-dot-product

# Install required packages
pip install numpy matplotlib
```

### Usage

```bash
python linear_regression_estimation.py
```

The program will:
1. Generate 1000 random (X, Y) data points
2. Calculate regression coefficients using **dot product operations**
3. Display statistical comparison between true and estimated parameters
4. Show visualization with data points and both regression lines

## 📊 Mathematical Foundation

### Data Generation Model

```
X ~ Normal(μ=0, σ=1)
ε ~ Normal(0, σ_ε)
Y = β₀ + β₁*X + ε
```

**True Parameters:**
- β₀ = 0.2 (intercept)
- β₁ = 0.9 (slope)
- σ_ε = 0.3 (noise standard deviation)

### Coefficient Estimation Using Dot Product

#### Formula 1: Slope (β₁)

**Mathematical Formula:**
```
β₁ = Σⁿᵢ₌₁((Xi - X̄) * (Yi - Ȳ)) / Σⁿᵢ₌₁((Xi - X̄)²)
```

**Dot Product Formulation:**
```
β₁ = (X_dev · Y_dev) / (X_dev · X_dev)
```

**Python Implementation:**
```python
X_avg = np.mean(X)
Y_avg = np.mean(Y)

# Calculate deviation vectors
X_dev = X - X_avg          # [X₁-X̄, X₂-X̄, ..., Xₙ-X̄]
Y_dev = Y - Y_avg          # [Y₁-Ȳ, Y₂-Ȳ, ..., Yₙ-Ȳ]

# Dot product for numerator (sum of cross-products)
numerator = np.dot(X_dev, Y_dev)

# Dot product with itself for denominator (sum of squares)
denominator = np.dot(X_dev, X_dev)

beta_1_est = numerator / denominator
```

#### Formula 2: Intercept (β₀)

**Mathematical Formula:**
```
β₀ = Ȳ - β₁ * X̄
```

**Python Implementation:**
```python
beta_0_est = Y_avg - beta_1_est * X_avg
```

## 🧮 Understanding Dot Product in Regression

### What is Dot Product?

For two vectors **a** = [a₁, a₂, ..., aₙ] and **b** = [b₁, b₂, ..., bₙ]:

```
a · b = a₁b₁ + a₂b₂ + ... + aₙbₙ = Σⁿᵢ₌₁(aᵢ * bᵢ)
```

### Application to Regression

#### Numerator (Covariance-like term):
```
X_dev · Y_dev = Σⁿᵢ₌₁((Xi - X̄) * (Yi - Ȳ))
```
This measures how X and Y vary **together**. When X is above its mean and Y is above its mean (or both below), the product is positive.

#### Denominator (Variance of X):
```
X_dev · X_dev = Σⁿᵢ₌₁((Xi - X̄)²)
```
This is the sum of squared deviations from the mean, measuring the spread of X values.

#### Slope Interpretation:
```
β₁ = (how X and Y vary together) / (how X varies with itself)
```

This tells us: for every unit increase in X, how much does Y change?

## 📈 Visualization

The program generates a single comprehensive graph showing:

| Element | Description | Style |
|---------|-------------|-------|
| **Blue scatter points** | The 1000 generated (X, Y) data points | Alpha=0.4, size=20 |
| **Red solid line** | True regression line (Y = 0.2 + 0.9*X) | Width=3, solid |
| **Green dashed line** | Estimated regression line from dot product | Width=2.5, dashed |

The visualization demonstrates how well the dot product method recovers the true relationship despite random noise.

## 🔧 Configuration

Adjust parameters by modifying constants at the top of the file:

```python
NUM_POINTS = 1000        # Number of data points
MU_X = 0                 # Mean of X distribution
SIGMA_X = 1              # Standard deviation of X
BETA_0 = 0.2             # True intercept
BETA_1 = 0.9             # True slope
EPSILON_SIGMA = 0.3      # Noise level
SEED = None              # Random seed (int for reproducibility)
```

### Example: Reproducible Results
```python
SEED = 42  # Same results every time
```

### Example: Different Noise Levels
```python
EPSILON_SIGMA = 0.1   # Low noise - estimates very accurate
EPSILON_SIGMA = 1.0   # High noise - more scatter in estimates
```

## 📝 Example Output

### Console Output
```
======================================================================
LINEAR REGRESSION WITH COEFFICIENT ESTIMATION
======================================================================
Author: Yair Levi

Configuration:
  Number of Points:    1000
  X ~ Normal(μ=0, σ=1)
  Y = 0.2 + 0.9*X + ε
  ε ~ Normal(0, 0.3)

[Step 1] Generating 1000 random points...
  X range: [-3.045, 3.156]
  Y range: [-2.387, 3.024]
  X mean: 0.008, X std: 1.002
  Y mean: 0.207, Y std: 0.948

[Step 2] Estimating coefficients using dot product...
  Formula for β₁: dot(Xi - X_avg, Yi - Y_avg) / dot(Xi - X_avg, Xi - X_avg)
  Formula for β₀: Y_avg - β₁ * X_avg

======================================================================
COEFFICIENT ESTIMATION RESULTS
======================================================================

True Parameters:
  β₀ (Intercept):           0.2
  β₁ (Slope):               0.9

Estimated Parameters (using vector calculations):
  β₀_est (Intercept):       0.199847
  β₁_est (Slope):           0.901234

Estimation Errors:
  Error in β₀:              0.000153
  Error in β₁:              0.001234
  Relative Error β₀:        0.08%
  Relative Error β₁:        0.14%

======================================================================

[Step 3] Displaying plot with data points and lines...

Analysis complete!
```

## 💡 Code Structure

### Main Components

```
linear_regression_estimation.py
├── Configuration constants (NUM_POINTS, BETA_0, etc.)
├── generate_data()              # Generate X and Y data
├── estimate_coefficients()      # Calculate β₀ and β₁ using DOT PRODUCT
├── plot_data_and_lines()       # Create single visualization
├── print_results()             # Display comparison
└── main()                      # Orchestrate workflow
```

### Core Function: estimate_coefficients()

```python
def estimate_coefficients(X, Y):
    """
    Estimate β₀ and β₁ using least squares formulas with dot product.
    
    This implementation explicitly uses dot product operations to
    demonstrate the linear algebra foundation of regression.
    """
    # Calculate means
    X_avg = np.mean(X)
    Y_avg = np.mean(Y)
    
    # Calculate deviation vectors (vectorized)
    X_dev = X - X_avg  # Broadcasting
    Y_dev = Y - Y_avg  # Broadcasting
    
    # Calculate β₁ using DOT PRODUCT
    # Numerator: sum of cross-products
    numerator = np.dot(X_dev, Y_dev)
    
    # Denominator: sum of squared deviations
    denominator = np.dot(X_dev, X_dev)
    
    beta_1_est = numerator / denominator
    
    # Calculate β₀
    beta_0_est = Y_avg - beta_1_est * X_avg
    
    return beta_0_est, beta_1_est
```

## 🧪 Verification and Testing

### Test 1: Verify Dot Product Equivalence

```python
import numpy as np

# Create simple test data
X_dev = np.array([1, 2, 3])
Y_dev = np.array([4, 5, 6])

# Method 1: Dot product
result_dot = np.dot(X_dev, Y_dev)
print(f"Dot product: {result_dot}")  # Output: 32

# Method 2: Traditional sum (for comparison)
result_sum = np.sum(X_dev * Y_dev)
print(f"Sum method: {result_sum}")    # Output: 32

# They should be identical
assert result_dot == result_sum  # ✓ Passes
```

### Test 2: Perfect Linear Relationship

```python
# Create perfect linear data (no noise)
X = np.array([1, 2, 3, 4, 5])
Y = 0.2 + 0.9 * X  # Exact relationship

beta_0, beta_1 = estimate_coefficients(X, Y)

print(f"β₀: {beta_0:.10f}")  # Should be exactly 0.2
print(f"β₁: {beta_1:.10f}")  # Should be exactly 0.9
```

### Test 3: Self Dot Product (Sum of Squares)

```python
X_dev = np.array([1, -2, 3])

# Dot product with itself
dot_result = np.dot(X_dev, X_dev)
print(f"Dot product: {dot_result}")  # Output: 14 (1² + 4 + 9)

# Traditional sum of squares
sum_result = np.sum(X_dev ** 2)
print(f"Sum of squares: {sum_result}")  # Output: 14

assert dot_result == sum_result  # ✓ Identical
```

## 📚 Educational Value

### What You Learn from This Implementation

1. **Linear Algebra in Statistics**: How dot products naturally arise in regression formulas
2. **Vector Operations**: Understanding deviation vectors and their properties
3. **Computational Efficiency**: Vectorized operations are faster than loops
4. **Mathematical Elegance**: Dot product notation is cleaner than explicit summation
5. **NumPy Mastery**: Professional-level use of NumPy for scientific computing

### Dot Product Advantages

| Aspect | Dot Product | Traditional Sum |
|--------|-------------|-----------------|
| Mathematical elegance | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Code readability | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Educational value | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Performance | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Linear algebra connection | ⭐⭐⭐⭐⭐ | ⭐⭐ |

## 🎓 Understanding the Results

### Expected Accuracy

With 1000 points and moderate noise (σ_ε = 0.3):

- **β₁ estimate**: Typically within 0.5-3% of true value (0.9)
- **β₀ estimate**: Typically within 1-10% of true value (0.2)
- **Visual alignment**: Green dashed line very close to red solid line
- **Point scatter**: Data points distributed around both lines

### Why Estimates Aren't Exact

The random noise (ε) causes sampling variability:
- Each run produces slightly different estimates
- With more data, estimates get closer to true values
- The dot product method is mathematically optimal (OLS is BLUE)

### Factors Affecting Accuracy

| Factor | Effect on Accuracy |
|--------|-------------------|
| **Sample size (n)** | Larger n → better estimates |
| **Noise level (σ_ε)** | Lower noise → better estimates |
| **X spread** | Wider X range → better β₁ estimation |
| **Random seed** | Different samples → slight variations |

## 🔍 Comparison: Dot Product vs Traditional

### Mathematically Equivalent

```python
# These two approaches give IDENTICAL results:

# Approach 1: Dot Product (this implementation)
numerator = np.dot(X_dev, Y_dev)
denominator = np.dot(X_dev, X_dev)

# Approach 2: Traditional sum
numerator = np.sum(X_dev * Y_dev)
denominator = np.sum(X_dev ** 2)

# Result is the same (within floating-point precision)
```

### Why Choose Dot Product?

1. **Conceptual clarity**: Connects to linear algebra theory
2. **Educational value**: Shows regression as vector operations
3. **Mathematical elegance**: Cleaner notation in formulas
4. **Professional practice**: Common in advanced implementations
5. **Foundation for extensions**: Matrix formulations use dot products

## 🛠️ Troubleshooting

### Common Issues

#### Q: Why are my estimates different from true values?
```
A: This is expected! Random noise causes variation.
   - With 1000 points, estimates should be within 1-5%
   - Run multiple times to see variation
   - Set SEED for reproducible results
```

#### Q: Can I verify the dot product is working correctly?
```python
# Add this to your code for verification:
X_dev = X - np.mean(X)
Y_dev = Y - np.mean(Y)

dot_result = np.dot(X_dev, Y_dev)
sum_result = np.sum(X_dev * Y_dev)

print(f"Dot product: {dot_result}")
print(f"Sum method:  {sum_result}")
print(f"Difference:  {abs(dot_result - sum_result)}")  # Should be ~0
```

#### Q: How do I improve estimation accuracy?
```python
# Increase sample size
NUM_POINTS = 10000

# Reduce noise
EPSILON_SIGMA = 0.1

# Both changes improve accuracy
```

#### Q: What if the lines don't appear close?
```
Check:
- EPSILON_SIGMA value (high noise = more separation)
- Verify formulas are correct
- Look at relative errors in output (should be < 5%)
```

## 📖 Advanced Topics

### Matrix Formulation

The dot product approach extends naturally to matrix form:

```python
# Single variable (this implementation):
β₁ = dot(X_dev, Y_dev) / dot(X_dev, X_dev)

# Matrix form (multiple variables):
# β = (X^T X)^(-1) X^T Y
# This is also built on dot products!
```

### Connection to Covariance

The dot product in the numerator is related to covariance:

```python
# Numerator divided by n:
cov_XY = np.dot(X_dev, Y_dev) / n

# This is the sample covariance between X and Y
# β₁ = cov(X,Y) / var(X)
```

### Geometric Interpretation

The dot product has a geometric meaning:
```
a · b = ||a|| ||b|| cos(θ)
```
Where θ is the angle between vectors a and b.

In regression:
- Large positive dot product → strong positive relationship
- Near-zero dot product → weak relationship
- Large negative dot product → strong negative relationship

## 🤝 Contributing

### Enhancement Ideas

- [ ] Add matrix formulation for multiple regression
- [ ] Implement confidence intervals using dot products
- [ ] Create visualization of dot product computation
- [ ] Add weighted least squares using dot products
- [ ] Compare performance: dot product vs loop vs sum
- [ ] Interactive demo with adjustable parameters

### Development

```bash
git clone https://github.com/yourusername/linear-regression-dot-product.git
cd linear-regression-dot-product

# Make changes to linear_regression_estimation.py
python linear_regression_estimation.py

# Verify dot product usage
grep "np.dot" linear_regression_estimation.py
```

## 📚 References

### Statistical Theory
- **Ordinary Least Squares**: Classical regression method
- **Gauss-Markov Theorem**: OLS estimators are BLUE
- **Linear Algebra in Statistics**: Connection between vectors and regression

### Mathematical Resources
- Dot product properties and applications
- Vector spaces and linear regression
- Least squares as projection in vector space

### Further Reading
- Introduction to Statistical Learning (James et al.)
- Linear Algebra and Its Applications (Strang)
- NumPy Documentation: https://numpy.org/doc/

## 📄 License

This project is licensed under the MIT License.

## 🙋 FAQ

**Q: What's the difference between dot product and element-wise multiplication?**  
A: 
- Element-wise: `[1,2,3] * [4,5,6] = [4,10,18]` (array result)
- Dot product: `[1,2,3] · [4,5,6] = 32` (scalar result = sum of element-wise)

**Q: Why use dot product instead of np.sum()?**  
A: For educational clarity and to show the linear algebra foundation. Both give identical results, but dot product is more mathematically elegant.

**Q: Is dot product faster than sum?**  
A: Performance is essentially identical - both are highly optimized in NumPy. The choice is about clarity and mathematical elegance.

**Q: Can I use @ operator instead of np.dot()?**  
A: Yes! `a @ b` is equivalent to `np.dot(a, b)` in Python 3.5+. Both work perfectly.

**Q: How does this extend to multiple regression?**  
A: Multiple regression uses matrix dot products: β = (X^T X)^(-1) X^T Y, where each operation is a dot product.

**Q: Why do the green and red lines look so close?**  
A: That's exactly what we want! With 1000 points, the dot product method accurately recovers the true parameters.

## 📞 Support

- **Author**: Yair Levi
- **Issues**: Create an issue in the repository
- **Questions**: See FAQ above or open a discussion
- **Documentation**: Refer to PRD for detailed specifications

---

**Version**: 2.0 (Dot Product Edition)  
**Author**: Yair Levi  
**Last Updated**: October 3, 2025  
**Key Feature**: Explicit dot product operations for coefficient estimation  
**Python**: 3.6+  
**Status**: Production Ready