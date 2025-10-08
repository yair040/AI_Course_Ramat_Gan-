# Sinusoidal Peak Detection using Convolution

A Python-based signal processing tool that demonstrates peak detection in periodic signals using convolution-based template matching.

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Output](#output)
- [Configuration](#configuration)
- [Examples](#examples)
- [Technical Details](#technical-details)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

## 🎯 Overview

This project implements a convolution-based peak detection algorithm for sinusoidal signals. It generates a synthetic sine wave, extracts a template around a peak, and uses cross-correlation (via convolution) to identify all peak locations in the signal.

**Use Cases:**
- Educational demonstrations of convolution and template matching
- Prototype for periodic signal analysis
- Baseline for developing custom peak detection algorithms
- Signal processing research and experimentation

## ✨ Features

- **Synthetic Signal Generation**: Creates clean 10-cycle sinusoidal signals with 200 samples per cycle
- **Template Extraction**: Automatically extracts a 30-sample peak template
- **Convolution-Based Detection**: Uses template matching to identify all peaks
- **Comprehensive Visualization**: Generates three detailed plots showing signal, template, and detection results
- **Performance Metrics**: Reports detection accuracy, peak locations, and spacing
- **Zero Configuration**: Works out-of-the-box with sensible defaults

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Quick Install

```bash
# Clone the repository
git clone https://github.com/yourusername/peak-detection-convolution.git
cd peak-detection-convolution

# Install dependencies
pip install -r requirements.txt
```

### Manual Installation

```bash
pip install numpy matplotlib
```

### Dependencies

```
numpy>=1.19.0
matplotlib>=3.3.0
```

## 💻 Usage

### Basic Usage

Simply run the script:

```bash
python peak_detection.py
```

The program will:
1. Generate a 10-cycle sinusoidal signal
2. Extract a peak template
3. Perform convolution-based detection
4. Display three visualization plots
5. Print detection statistics to console

### Expected Output

```
Number of detected peaks: 10
Peak locations (sample indices): [50, 250, 450, 650, 850, 1050, 1250, 1450, 1650, 1850]

Summary:
Total samples: 2000
Samples per cycle: 200
Template length: 30 samples
Expected peak spacing: ~200 samples
Actual peak spacings: [200, 200, 200, 200, 200, 200, 200, 200, 200]
```

## 🔬 How It Works

### Step 1: Signal Generation

Creates a sinusoidal signal with:
- **Cycles**: 10 complete periods
- **Amplitude**: -1 to +1
- **Sampling**: 200 samples per cycle (2000 total)
- **Time span**: 0 to 20π radians

```python
t = np.linspace(0, cycles * 2 * np.pi, total_samples)
x = np.sin(t)
```

### Step 2: Template Extraction

Extracts a 30-sample window centered on the first peak:
- 15 samples before the peak
- The peak sample itself
- 14 samples after the peak

This template captures the characteristic shape of a peak.

### Step 3: Convolution

Performs 1D convolution between the signal and the flipped template:

```python
output = np.convolve(x, h_flipped, mode='same')
```

The convolution output shows high values where the signal matches the template pattern.

### Step 4: Peak Detection

Identifies peaks in the convolution output using:
- Local maximum detection (higher than neighbors)
- Threshold filtering (90% of maximum response)
- Duplicate removal (minimum spacing of 100 samples)

### Step 5: Visualization

Generates three plots:
1. **Original Signal**: The input sinusoidal wave
2. **Template**: The extracted peak pattern
3. **Detection Results**: Convolution output with marked peaks

## 📊 Output

### Visualization Plots

The program generates a figure with three subplots:

**Plot 1: Original Sinusoidal Signal**
- Shows all 10 cycles of the sine wave
- Amplitude range: -1 to +1
- Time axis in radians

**Plot 2: Template Signal**
- Displays the 30-sample peak template
- Shows the characteristic peak shape
- Used for pattern matching

**Plot 3: Peak Detection Output**
- Convolution response across the entire signal
- Red circles mark detected peaks (10 total)
- Orange dashed line shows detection threshold
- Green line shows convolution magnitude

### Console Output

Statistics printed to console:
- Number of peaks detected
- Peak locations (sample indices)
- Peak spacing intervals
- Template and signal parameters

## ⚙️ Configuration

### Modifying Parameters

Edit the following variables at the top of the script:

```python
# Number of sine wave cycles
cycles = 10

# Samples per cycle (resolution)
samples_per_cycle = 200

# Template window size (samples around peak)
half_window = 15  # Total template: 2*15 + 1 = 31 samples

# Detection threshold (% of maximum)
threshold = np.max(output) * 0.9  # 90% threshold
```

### Custom Signals

To test with different signal types, modify the signal generation:

```python
# Example: Add noise
x = np.sin(t) + 0.1 * np.random.randn(len(t))

# Example: Different frequency
x = np.sin(2 * t)  # Double frequency

# Example: Multiple harmonics
x = np.sin(t) + 0.5 * np.sin(2 * t)
```

## 📈 Examples

### Example 1: Default Configuration

```python
python peak_detection.py
```
Detects all 10 peaks with 100% accuracy in a clean sinusoidal signal.

### Example 2: High Resolution

```python
samples_per_cycle = 500  # Increase resolution
```
Results in smoother visualization and more precise peak localization.

### Example 3: Wider Template

```python
half_window = 25  # 51-sample template
```
Captures more context around peaks, may improve detection in noisy signals.

## 🔧 Technical Details

### Algorithm Complexity

- **Time Complexity**: O(n·m) where n is signal length, m is template length
- **Space Complexity**: O(n) for storing signal and convolution output
- **Typical Runtime**: < 2 seconds for 2000 samples

### Mathematical Foundation

**Convolution Formula:**
```
y[n] = Σ x[k] · h[n-k]
```

**Peak Detection Criteria:**
```
Peak at index i if:
  1. y[i] > y[i-1] AND y[i] > y[i+1]  (local maximum)
  2. y[i] > threshold                  (significant response)
  3. |i - prev_peak| > min_spacing     (isolated peaks)
```

### Signal Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| Total Samples | 2000 | Full signal length |
| Sampling Rate | 200 samples/cycle | Resolution per period |
| Signal Frequency | 1/(2π) Hz | Cycles per unit time |
| Template Length | 30 samples | Detection window size |
| Detection Threshold | 90% of max | Sensitivity level |

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Areas for Improvement

- Add support for noisy signals
- Implement adaptive threshold detection
- Add unit tests and continuous integration
- Support for multi-frequency signals
- Real-time signal processing capabilities
- Export results to file formats (CSV, JSON)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Yair Levi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

## 👤 Author

**Yair Levi**

- GitHub: [@yairlevi](https://github.com/yairlevi)
- Email: your.email@example.com

## 📚 References

- [Convolution in Signal Processing](https://en.wikipedia.org/wiki/Convolution)
- [Template Matching Techniques](https://en.wikipedia.org/wiki/Template_matching)
- [NumPy Convolution Documentation](https://numpy.org/doc/stable/reference/generated/numpy.convolve.html)

## 🙏 Acknowledgments

- NumPy team for excellent numerical computing tools
- Matplotlib team for powerful visualization capabilities
- Signal processing community for algorithm foundations

---

**Project Status**: Active Development  
**Last Updated**: October 8, 2025  
**Version**: 1.0.0

If you found this project helpful, please consider giving it a ⭐️!