# Cluster Visualization with Normal Distribution

**Author:** Yair Levi  
**Version:** 1.0.0  
**Date:** October 15, 2025

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![NumPy](https://img.shields.io/badge/numpy-required-green.svg)](https://numpy.org/)
[![Matplotlib](https://img.shields.io/badge/matplotlib-required-green.svg)](https://matplotlib.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-required-green.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 📊 Program Output - Real Execution Results

### Visualization Output

![Cluster Visualization](cluster_visualization.png)

**Figure Description:**
- **Left Plot:** Original clusters with 2σ ellipse boundaries and overlap points (yellow stars)
- **Right Plot:** K-Means clustering result with decision boundaries and cluster centers (black X)

### Complete Console Output

```text
C:\Users\yair0\Documents\docs\courses\AI_Limudey_Hutz\Lesson12\clusters>python3 cluster_visualization.py
================================================================================
CLUSTER VISUALIZATION WITH NORMAL DISTRIBUTION
Author: Yair Levi
================================================================================

Generating 6000 points total:
  - 2000 points per cluster (3 clusters)
  - 2000 points are overlap (shared across all clusters)
  - Distribution: Each cluster gets 666 overlap + 0 unique

Cluster Parameters:

Generating 2000 overlapping points...

Cluster 1 (Red):
  Mean: (2, 2)
  Std Dev: (1.5, 1.0)
  Points: 667 overlap + 1333 unique = 2000 total

Cluster 2 (Green):
  Mean: (8, 3)
  Std Dev: (1.2, 1.8)
  Points: 667 overlap + 1333 unique = 2000 total

Cluster 3 (Blue):
  Mean: (5, 8)
  Std Dev: (2.0, 1.3)
  Points: 666 overlap + 1334 unique = 2000 total

✓ Total points generated: 6000
  - Cluster 1: 2000 points
  - Cluster 2: 2000 points
  - Cluster 3: 2000 points
  - Overlap points distributed across clusters: 2000

================================================================================
CREATING VISUALIZATION
================================================================================

Plot 1: Original clusters with overlap region highlighted...
Drawing cluster boundaries (2σ ellipses)...

Plot 2: K-Means clustering visualization...
Running K-Means algorithm (k=3)...
✓ K-Means clustering complete
  Cluster centers found at:
    Cluster 1: (2.16, 2.40)
    Cluster 2: (5.00, 7.46)
    Cluster 3: (7.77, 3.13)
Drawing decision boundaries...

✓ Visualization complete

================================================================================
SAVING FIGURE
================================================================================

✓ Figure saved as: cluster_visualization.png

================================================================================
ANALYSIS COMPLETE
================================================================================

Summary:
  Total points: 6000
  Cluster 1: 2000 points
  Cluster 2: 2000 points
  Cluster 3: 2000 points
  Overlapping: 2000 points (shared across clusters)
  Unique: 4000 points

Displaying plot...

✓ Program execution completed successfully

Author: Yair Levi
```

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Results](#key-results)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Mathematical Background](#mathematical-background)
- [Configuration](#configuration)
- [Output Explanation](#output-explanation)
- [Requirements](#requirements)
- [Performance](#performance)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## 🎯 Overview

This Python program generates and visualizes **3 clusters of points with normal (Gaussian) distribution** on a 2D plane. The program demonstrates:

- **Synthetic data generation** with controlled statistical properties
- **Overlapping cluster regions** to simulate real-world complexity
- **Statistical boundary visualization** using 2-sigma ellipses
- **K-Means clustering algorithm** demonstration
- **Decision boundary visualization** for cluster separation

### Purpose

This tool is designed for:
- **Educational demonstrations** of clustering algorithms
- **Research and analysis** of K-Means behavior with overlapping data
- **Publication-quality visualizations** for academic papers
- **Understanding clustering challenges** in real-world scenarios

---

## 🔍 Key Results

### Data Distribution

| Metric | Value | Description |
|--------|-------|-------------|
| **Total Points** | 6,000 | Complete dataset size |
| **Points per Cluster** | 2,000 | Each of 3 clusters |
| **Overlap Points** | 2,000 | Shared across all clusters (33.3%) |
| **Unique Points** | 4,000 | Non-overlapping points (66.7%) |

### Cluster Parameters

| Cluster | Color | Mean (X, Y) | Std Dev (X, Y) | Location |
|---------|-------|-------------|----------------|----------|
| 1 | Red | (2, 2) | (1.5, 1.0) | Lower-left region |
| 2 | Green | (8, 3) | (1.2, 1.8) | Right-center region |
| 3 | Blue | (5, 8) | (2.0, 1.3) | Upper-center region |

### K-Means Results

**Cluster Centers Found:**
- Cluster 1: (2.16, 2.40)
- Cluster 2: (5.00, 7.46)
- Cluster 3: (7.77, 3.13)

**Observations:**
- K-Means successfully identifies 3 distinct cluster centers
- Centers are close to original means, validating the algorithm
- Overlap region creates interesting classification boundaries
- Decision boundaries clearly visible between clusters

---

## ✨ Features

### Data Generation
- ✅ **Normal Distribution**: Gaussian distribution for both X and Y coordinates
- ✅ **Configurable Parameters**: Custom mean and standard deviation per cluster
- ✅ **Controlled Overlap**: Exactly 2000 points overlap across all clusters
- ✅ **Reproducible Results**: Fixed random seed ensures consistency
- ✅ **Balanced Clusters**: Each cluster has exactly 2000 points

### Visualization
- ✅ **Dual Plot Layout**: Side-by-side comparison of original vs K-Means
- ✅ **Statistical Boundaries**: 2-sigma ellipses showing cluster spread
- ✅ **Decision Boundaries**: K-Means classification boundaries
- ✅ **Overlap Highlighting**: Yellow stars distinguish overlap points
- ✅ **Cluster Centers**: Clear markers showing K-Means centroids
- ✅ **Professional Styling**: Publication-quality output at 300 DPI

### Analysis
- ✅ **K-Means Clustering**: Automatic clustering with k=3
- ✅ **Point Classification**: Overlap vs unique point tracking
- ✅ **Statistics Display**: Comprehensive metrics in figure
- ✅ **Console Progress**: Detailed execution feedback

---

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Quick Install

```bash
# Clone or download the repository
git clone https://github.com/yairlevi/cluster-visualization.git
cd cluster-visualization

# Install dependencies
pip install -r requirements.txt
```

### Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Manual Installation

```bash
pip install numpy>=1.19.0 matplotlib>=3.3.0 scikit-learn>=0.24.0
```

---

## 💻 Usage

### Basic Usage

```bash
python cluster_visualization.py
```

The program will:
1. Generate 6000 points (3 clusters + overlap)
2. Apply K-Means clustering
3. Create visualization plots
4. Save output as `cluster_visualization.png`
5. Display interactive plot window

### Expected Execution Time

- **Data Generation:** ~1-2 seconds
- **K-Means Clustering:** ~1 second
- **Visualization:** ~2-3 seconds
- **Total:** ~5-8 seconds

### Output Files

- **cluster_visualization.png** - High-resolution visualization (300 DPI)
- No other files created (all in-memory processing)

---

## 🔬 How It Works

### Algorithm Overview

```
1. Generate Overlap Points (2000)
   ↓
2. Distribute Overlap to Clusters (~667 each)
   ↓
3. Generate Unique Points per Cluster (~1333 each)
   ↓
4. Total: 2000 points per cluster × 3 = 6000 total
   ↓
5. Apply K-Means Clustering (k=3)
   ↓
6. Visualize: Original + K-Means Results
```

### Step-by-Step Process

#### Step 1: Generate Overlap Points
```python
overlap_center = [5, 4.5]  # Center between all clusters
overlap_std = [2.5, 2.0]   # Large spread
overlap_x = np.random.normal(overlap_center[0], overlap_std[0], 2000)
overlap_y = np.random.normal(overlap_center[1], overlap_std[1], 2000)
```

**Purpose:** Create 2000 points that naturally spread across all three cluster regions.

#### Step 2: Distribute Overlap Points
```python
# Split 2000 overlap points among 3 clusters
# Each gets ~667 points (666 or 667 due to rounding)
cluster_1_overlap = overlap_points[0:667]
cluster_2_overlap = overlap_points[667:1334]
cluster_3_overlap = overlap_points[1334:2000]
```

#### Step 3: Generate Unique Points
```python
# For each cluster, generate remaining points
unique_count = 2000 - overlap_assigned  # ~1333 points
x_unique = np.random.normal(mean_x, std_x, unique_count)
y_unique = np.random.normal(mean_y, std_y, unique_count)
```

**Cluster 1 (Red):**
- Mean: (2, 2)
- Std Dev: (1.5, 1.0)
- 667 overlap + 1333 unique = 2000 total

**Cluster 2 (Green):**
- Mean: (8, 3)
- Std Dev: (1.2, 1.8)
- 667 overlap + 1333 unique = 2000 total

**Cluster 3 (Blue):**
- Mean: (5, 8)
- Std Dev: (2.0, 1.3)
- 666 overlap + 1334 unique = 2000 total

#### Step 4: Apply K-Means Clustering
```python
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
predicted_labels = kmeans.fit_predict(all_points)
centers = kmeans.cluster_centers_
```

**K-Means Process:**
1. Initialize 3 random centroids
2. Assign each point to nearest centroid
3. Recalculate centroids as mean of assigned points
4. Repeat until convergence
5. Return final cluster centers and assignments

#### Step 5: Visualization

**Plot 1 - Original Clusters:**
- Shows true cluster membership
- Overlap points as yellow stars
- 2σ ellipse boundaries (dashed lines)
- Legend with all elements

**Plot 2 - K-Means Results:**
- Points colored by K-Means prediction
- Cluster centers marked with X
- Decision boundaries shown
- Overlap points highlighted

---

## 📐 Mathematical Background

### Normal (Gaussian) Distribution

**Probability Density Function:**
```
f(x | μ, σ²) = (1 / √(2πσ²)) × e^(-(x-μ)²/(2σ²))
```

Where:
- **μ** = mean (center of distribution)
- **σ** = standard deviation (spread)
- **σ²** = variance

**Properties:**
- **68%** of data within μ ± 1σ
- **95%** of data within μ ± 2σ (our ellipse boundaries)
- **99.7%** of data within μ ± 3σ

### K-Means Algorithm

**Objective:** Minimize within-cluster sum of squares

```
J = Σ(i=1 to k) Σ(x ∈ Ci) ||x - μi||²
```

Where:
- **k** = number of clusters (3 in our case)
- **Ci** = cluster i
- **μi** = centroid of cluster i
- **||·||** = Euclidean distance

**Algorithm Steps:**
1. Initialize k centroids randomly
2. **Assignment Step:** Assign each point to nearest centroid
3. **Update Step:** Recalculate centroids
4. Repeat steps 2-3 until convergence

### Euclidean Distance

```
d = √((x₂ - x₁)² + (y₂ - y₁)²)
```

Used by K-Means to determine nearest cluster center.

### 2-Sigma Ellipse

**Ellipse Equation:**
```
((x - h)² / a²) + ((y - k)² / b²) = 1
```

Where:
- **(h, k)** = center (cluster mean)
- **a** = 2 × σx (semi-major axis)
- **b** = 2 × σy (semi-minor axis)

**Coverage:** Approximately 95% of normally distributed points fall within 2σ.

---

## ⚙️ Configuration

### Modifying Parameters

Edit the configuration section in `cluster_visualization.py`:

```python
# Point Distribution
TOTAL_POINTS = 6000
POINTS_PER_CLUSTER = 2000
OVERLAP_POINTS = 2000

# Cluster 1 Parameters
cluster_params = [
    {
        'name': 'Cluster 1 (Red)',
        'mean': [2, 2],
        'std': [1.5, 1.0],
        'color': 'red',
        'alpha': 0.6
    },
    # ... more clusters
]

# Overlap Parameters
overlap_center = [5, 4.5]
overlap_std = [2.5, 2.0]

# Visualization
FIGURE_SIZE = (16, 7)
DPI = 300
OUTPUT_FILE = 'cluster_visualization.png'

# K-Means
N_CLUSTERS = 3
RANDOM_STATE = 42
```

### Configuration Examples

**Example 1: Less Overlap**
```python
OVERLAP_POINTS = 1000  # Reduce overlap to 1000 points
overlap_std = [1.5, 1.2]  # Tighter spread
```

**Example 2: More Separated Clusters**
```python
# Move clusters further apart
cluster_params[0]['mean'] = [0, 0]
cluster_params[1]['mean'] = [12, 0]
cluster_params[2]['mean'] = [6, 12]
```

**Example 3: Tighter Clusters**
```python
# Reduce standard deviations
cluster_params[0]['std'] = [0.8, 0.5]
cluster_params[1]['std'] = [0.6, 0.9]
cluster_params[2]['std'] = [1.0, 0.7]
```

---

## 📊 Output Explanation

### Left Plot: Original Clusters

**Elements:**
- **Red circles:** Cluster 1 unique points
- **Green circles:** Cluster 2 unique points  
- **Blue circles:** Cluster 3 unique points
- **Yellow stars:** Overlap points (2000 total)
- **Dashed ellipses:** 2σ boundaries showing cluster spread

**Interpretation:**
- Shows the true cluster assignments
- Overlap region visible where clusters intersect
- Ellipses indicate where 95% of each cluster's points lie
- Yellow stars show which points are shared

### Right Plot: K-Means Results

**Elements:**
- **Colored dots:** Points colored by K-Means prediction
- **Black X markers:** Cluster centers found by K-Means
- **Dashed black lines:** Decision boundaries
- **Yellow stars:** Original overlap points highlighted

**Interpretation:**
- Shows how K-Means classified the points
- Decision boundaries show where classification changes
- Cluster centers are close to original means
- Overlap points may be classified differently than original

### Statistics Box

```
Statistics:
Total Points: 6000
Points per Cluster: 2000
Overlap Points: 2000 (33.3%)
Unique Points: 4000
```

**Meaning:**
- **33.3% overlap** creates moderate clustering difficulty
- **66.7% unique** points are clearly assigned to one cluster
- Balanced distribution across all clusters

---

## 📦 Requirements

### Python Packages

| Package | Version | Purpose |
|---------|---------|---------|
| numpy | ≥1.19.0 | Numerical computing, random generation |
| matplotlib | ≥3.3.0 | Plotting and visualization |
| scikit-learn | ≥0.24.0 | K-Means clustering algorithm |

### requirements.txt

```
numpy>=1.19.0
matplotlib>=3.3.0
scikit-learn>=0.24.0
```

### System Requirements

- **Python:** 3.7 or higher
- **RAM:** 2GB minimum (4GB recommended)
- **Display:** Required for interactive plot (or use virtual display)
- **Disk Space:** ~50MB for packages + output

---

## 🚀 Performance

### Benchmarks

| Operation | Time | Memory |
|-----------|------|--------|
| Data Generation | ~1-2s | ~50 MB |
| K-Means Clustering | ~1s | ~20 MB |
| Visualization | ~2-3s | ~100 MB |
| **Total Execution** | **~5-8s** | **~150 MB** |

### Scalability

The program can handle:
- ✅ Up to 100,000 points (increases execution time)
- ✅ Up to 10 clusters (modify configuration)
- ✅ Different distributions (modify generation code)

**Performance Tips:**
- Reduce `DPI` for faster rendering (e.g., 150 instead of 300)
- Decrease point count for quicker experimentation
- Use `plt.show()` only when needed (comment out for batch processing)

---

## 🎨 Customization

### Change Colors

```python
cluster_params = [
    {'color': 'purple', ...},  # Change red to purple
    {'color': 'orange', ...},  # Change green to orange
    {'color': 'cyan', ...},    # Change blue to cyan
]
OVERLAP_COLOR = 'magenta'  # Change overlap color
```

### Adjust Transparency

```python
cluster_params[0]['alpha'] = 0.8  # More opaque
cluster_params[1]['alpha'] = 0.4  # More transparent
```

### Change Figure Size

```python
FIGURE_SIZE = (20, 10)  # Wider figure
FIGURE_SIZE = (12, 12)  # Square figure
```

### Modify Point Sizes

```python
# In visualization code
ax1.scatter(..., s=50, ...)  # Larger points (default 30)
ax1.scatter(..., s=10, ...)  # Smaller points
```

### Add More Clusters

```python
# Add 4th cluster
cluster_params.append({
    'name': 'Cluster 4 (Magenta)',
    'mean': [10, 10],
    'std': [1.5, 1.5],
    'color': 'magenta',
    'alpha': 0.6
})

POINTS_PER_CLUSTER = 1500  # Adjust to maintain 6000 total
N_CLUSTERS = 4  # Update K-Means
```

---

## 🔧 Troubleshooting

### Problem: ModuleNotFoundError

**Error:**
```
ModuleNotFoundError: No module named 'numpy'
```

**Solution:**
```bash
pip install -r requirements.txt
```

---

### Problem: Plot doesn't display

**Error:** Program completes but no window appears

**Solution (Windows):**
```python
import matplotlib
matplotlib.use('TkAgg')  # Add at top of file
```

**Solution (Linux - Headless Server):**
```bash
# Install virtual display
sudo apt-get install xvfb

# Run with virtual display
xvfb-run python cluster_visualization.py
```

---

### Problem: Low-quality output

**Issue:** PNG looks blurry or pixelated

**Solution:**
```python
DPI = 600  # Increase from 300 (larger file size)
```

---

### Problem: Memory Error

**Error:** `MemoryError` or system freezes

**Solution:**
```python
# Reduce point count temporarily
TOTAL_POINTS = 3000
POINTS_PER_CLUSTER = 1000
OVERLAP_POINTS = 1000
```

---

### Problem: Slow execution

**Issue:** Takes > 30 seconds to run

**Solutions:**
1. Reduce mesh grid resolution:
   ```python
   xx, yy = np.meshgrid(np.linspace(..., 200),  # Reduce from 500
                        np.linspace(..., 200))
   ```

2. Reduce DPI:
   ```python
   DPI = 150  # Reduce from 300
   ```

3. Simplify visualization:
   ```python
   # Comment out decision boundary plotting
   # ax2.contour(...)
   ```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Ways to Contribute

- 🐛 **Report Bugs:** Open an issue with details
- 💡 **Suggest Features:** Propose new capabilities
- 📝 **Improve Documentation:** Fix typos, add examples
- 🔧 **Submit Code:** Fix bugs or add features

### Contribution Process

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Test thoroughly
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open Pull Request

### Code Style

- Follow PEP 8 guidelines
- Add docstrings to new functions
- Include comments for complex logic
- Test with different parameters

---

## 📝 License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2025 Yair Levi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👤 Author

**Yair Levi**

- 📧 Email: yair.levi@example.com
- 💼 GitHub: [@yairlevi](https://github.com/yairlevi)
- 🔗 LinkedIn: [Yair Levi](https://linkedin.com/in/yairlevi)

---

## 🙏 Acknowledgments

- **NumPy Team** - For excellent numerical computing tools
- **Matplotlib Team** - For powerful visualization capabilities
- **scikit-learn Team** - For robust machine learning algorithms
- **Python Community** - For continuous support and inspiration

---

## 📚 References

### Academic Papers
1. Lloyd, S. P. (1982). "Least squares quantization in PCM". IEEE Transactions on Information Theory.
2. MacQueen, J. (1967). "Some methods for classification and analysis of multivariate observations".

### Documentation
- [NumPy Documentation](https://numpy.org/doc/)
- [Matplotlib Documentation](https://matplotlib.org/stable/)
- [scikit-learn Documentation](https://scikit-learn.org/stable/)

### Related Resources
- [K-Means Clustering Explained](https://en.wikipedia.org/wiki/K-means_clustering)
- [Normal Distribution](https://en.wikipedia.org/wiki/Normal_distribution)
- [Cluster Analysis](https://en.wikipedia.org/wiki/Cluster_analysis)

---

## 📊 Project Statistics

![Lines of Code](https://img.shields.io/badge/lines%20of%20code-220-blue)
![Functions](https://img.shields.io/badge/functions-3-green)
![Files](https://img.shields.io/badge/files-2-orange)
![Documentation](https://img.shields.io/badge/documentation-complete-brightgreen)

---

## 🗺️ Roadmap

### Version 1.1 (Planned)
- [ ] Command-line arguments for parameters
- [ ] CSV export of generated points
- [ ] Additional clustering algorithms (DBSCAN, GMM)
- [ ] 3D visualization option

### Version 2.0 (Future)
- [ ] Interactive GUI for parameter tuning
- [ ] Animation of K-Means convergence
- [ ] Comparison with multiple algorithms
- [ ] Web-based visualization

---

**If you found this project useful, please consider giving it a ⭐ star on GitHub!**

**Questions or Issues?** Open an issue or contact the author.

**Happy Clustering! 🎨📊**