# Product Requirements Document
## JPEG Compression Analysis Tool

**Author:** Yair Levi  
**Version:** 1.0  
**Date:** January 22, 2026

---

## 1. Overview

### 1.1 Purpose
Develop a Python-based tool to analyze JPEG compression quality by measuring the trade-off between compression ratio and image quality degradation across multiple quality levels.

### 1.2 Scope
The program will compress images using JPEG at various quality levels, decompress them, calculate reconstruction errors, and visualize the results through histograms.

---

## 2. Technical Requirements

### 2.1 Environment
- **Platform:** WSL (Windows Subsystem for Linux)
- **Python Version:** 3.8+
- **Virtual Environment:** Located at `../../venv` relative to project root
- **Package Structure:** Full Python package with `__init__.py`

### 2.2 Code Organization
- Maximum 150 lines per Python file
- Task-based architecture with main program calling individual tasks
- Relative paths only (no absolute paths)
- Multiprocessing where applicable for performance

### 2.3 Logging
- **Level:** INFO and above
- **Format:** Ring buffer with 20 rotating files
- **File Size:** Maximum 16MB per file
- **Behavior:** When file 20 is full, overwrite file 1

---

## 3. Functional Requirements

### 3.1 Core Features

#### F1: Image Compression
- Compress input image using JPEG format
- Support 10 different quality levels (Q)
- Quality range: 10, 20, 30, 40, 50, 60, 70, 80, 90, 95

#### F2: Image Decompression
- Decompress JPEG images back to original format
- Maintain pixel dimensions and color channels

#### F3: Error Calculation
- Calculate reconstruction error between original and decompressed images
- Use Mean Squared Error (MSE) as primary metric
- Alternative: Mean Absolute Error (MAE) for comparison
- Per-channel and aggregate error metrics

#### F4: Quality Level Analysis
- Repeat compression-decompression-error cycle for all 10 Q levels
- Parallel processing of different quality levels using multiprocessing

#### F5: Byte Distribution Visualization
- Generate histograms showing byte value distribution
- Before compression (original image)
- After compression at each Q level
- Separate plots for each quality level

#### F6: Error Distribution Visualization
- Generate histograms of error values
- Error distribution vs. Quality level
- Combined visualization showing error progression

---

## 4. Non-Functional Requirements

### 4.1 Performance
- Utilize multiprocessing for parallel Q-level processing
- Efficient memory usage for large images
- Progress indication for long-running operations

### 4.2 Reliability
- Comprehensive error handling
- Validation of input images
- Graceful degradation on failures

### 4.3 Maintainability
- Modular task-based design
- Clear separation of concerns
- Comprehensive logging for debugging

---

## 5. Data Flow

```
Input Image
    ↓
[Task 1: Compress at Q levels] → Compressed JPEGs
    ↓
[Task 2: Decompress] → Reconstructed Images
    ↓
[Task 3: Calculate Errors] → Error Metrics
    ↓
[Task 4: Generate Histograms] → Visualizations
```

---

## 6. Output Deliverables

### 6.1 Compressed Images
- 10 JPEG files at different quality levels
- Naming: `compressed_q{quality}.jpg`

### 6.2 Metrics
- CSV file with quality vs. error data
- Columns: Quality, MSE, MAE, File Size, Compression Ratio

### 6.3 Visualizations
- Byte distribution histograms (11 plots: original + 10 Q levels)
- Error distribution vs. Quality (combined plot)
- Saved as PNG files in output directory

### 6.4 Logs
- Ring buffer of 20 log files
- Detailed operation tracking

---

## 7. Dependencies

### 7.1 Required Libraries
- **Pillow (PIL):** Image I/O and JPEG compression
- **NumPy:** Numerical operations and error calculations
- **Matplotlib:** Histogram generation and plotting
- **multiprocessing:** Parallel processing (standard library)
- **logging:** Structured logging (standard library)

---

## 8. File Structure

```
jpeg_compressing/
├── __init__.py
├── main.py
├── tasks/
│   ├── __init__.py
│   ├── compress_task.py
│   ├── decompress_task.py
│   ├── error_task.py
│   └── visualize_task.py
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   └── config.py
├── data/
│   └── input/
└── output/
    ├── compressed/
    ├── decompressed/
    ├── metrics/
    └── plots/
```

---

## 9. Success Criteria

1. Successfully compress images at 10 quality levels
2. Accurately calculate MSE/MAE for all quality levels
3. Generate clear, informative histograms
4. Complete processing within reasonable time using multiprocessing
5. Maintain comprehensive logs in ring buffer format
6. All code files under 150 lines
7. Package runs successfully in WSL virtual environment

---

## 10. Future Enhancements

- Support for additional image formats (PNG, BMP, TIFF)
- Interactive quality selection
- Batch processing of multiple images
- Web-based dashboard for results
- Additional error metrics (SSIM, PSNR)
