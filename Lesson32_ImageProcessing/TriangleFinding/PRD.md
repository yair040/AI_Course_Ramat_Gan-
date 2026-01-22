# Product Requirements Document (PRD)
## Triangle Edge Detection and Reconstruction System

**Author:** Yair Levi  
**Date:** January 22, 2026  
**Version:** 2.0

---

## 1. Overview

A Python-based image processing application that generates synthetic triangle images, applies edge detection using frequency domain filtering techniques, and mathematically reconstructs the triangle using the Hough transform and line intersection algorithms.

---

## 2. Technical Requirements

### 2.1 Environment
- **Platform:** Windows Subsystem for Linux (WSL)
- **Python Version:** 3.8+
- **Virtual Environment:** Located at `../../venv/` relative to project root
- **Package Structure:** Installable Python package with proper `__init__.py`

### 2.2 Code Organization
- Maximum 150 lines per Python file
- Relative path usage throughout
- Multiprocessing where applicable
- Modular task-based architecture

### 2.3 Logging
- **Level:** INFO and above
- **Format:** Rotating ring buffer
- **Configuration:**
  - 20 log files maximum
  - 16MB per file
  - Circular overwrite when full
- **Location:** `./log/` subfolder

---

## 3. Functional Requirements

### 3.1 Image Generation (Task 1)
- Generate synthetic triangle image
- **Specifications:**
  - Triangle interior: White (255)
  - Triangle exterior: Black (0)
  - Configurable dimensions
  - Clean binary output

### 3.2 Frequency Domain Filtering (Task 2)
- Apply 2D Fourier Transform to input image
- Implement high-pass filter for edge detection
- **Filter Characteristics:**
  - Frequency domain manipulation
  - Edge enhancement capability
  - Configurable cutoff parameters

### 3.3 Inverse Transform (Task 3)
- Apply inverse FFT to filtered frequency data
- Reconstruct spatial domain image
- Normalize output appropriately

### 3.4 Binary Thresholding (Task 4)
- Convert edge-enhanced image to binary
- **Fixed threshold: 48** (no interactive adjustment)
- Automated processing

### 3.5 Non-Interactive Visualization (Task 5)
- Display processed image with threshold=48
- Save result to file
- No user interaction required

### 3.6 Triangle Overlay Visualization (Task 6) - NEW
- Draw detected triangle on original image
- **Coordinate System:** 
  - Origin: Top-left (0, 0)
  - Positive X: Right
  - Positive Y: **Downward** (image coordinates)
- Visual verification of detection accuracy
- Save annotated image

### 3.7 Mathematical Triangle Detection (Task 7) - NEW

#### 7a. Hough Line Detection
- Apply Hough transform to binary edge image
- Detect exactly 3 lines (triangle edges)
- **Parameters:**
  - Line threshold and resolution configurable
  - Minimum line length validation
  - Line separation criteria

#### 7b. Vertex Calculation
- Find intersections of line pairs
- Identify 3 vertices where exactly 2 edges meet
- Validate triangle geometry (non-collinear points)
- Handle edge cases (parallel lines, no intersection)

#### 7c. Results Output
- Print vertex coordinates to console and log
- **Format:** (x, y) in image coordinate system
- Coordinate precision: 2 decimal places
- Comparison with original triangle vertices

---

## 4. Non-Functional Requirements

### 4.1 Performance
- Utilize multiprocessing for computationally intensive operations
- Efficient memory management for image data
- Hough transform optimization for speed

### 4.2 Accuracy
- Vertex detection tolerance: ±5 pixels acceptable
- Line detection: All 3 edges must be found
- Intersection calculation: Sub-pixel precision

### 4.3 Robustness
- Handle cases where Hough doesn't find exactly 3 lines
- Graceful degradation with warnings
- Comprehensive error logging

---

## 5. System Architecture

### 5.1 Updated Project Structure
```
TriangleFinding/
├── __init__.py
├── main.py
├── tasks.py
├── image_generator.py
├── edge_detector.py
├── visualizer.py
├── triangle_detector.py (NEW)
├── geometry_utils.py (NEW)
├── config.py
├── log/
├── output/ (NEW - saved images)
├── requirements.txt
├── PRD.md
├── Claude.md
├── planning.md
└── tasks.md
```

### 5.2 New Module Responsibilities
- **triangle_detector.py:** Hough transform and line detection
- **geometry_utils.py:** Line intersection and vertex calculation

---

## 6. Updated Dependencies

### 6.1 Core Libraries
- **numpy:** Numerical operations and array handling
- **scipy:** FFT operations and signal processing
- **opencv-python:** Image processing, display, and Hough transform
- **Pillow:** Image I/O operations

---

## 7. Updated Workflow

1. User launches main program
2. System generates triangle image (Task 1)
3. Applies frequency domain high-pass filter (Task 2)
4. Reconstructs edge image via iFFT (Task 3)
5. Applies fixed threshold of 48 (Task 4)
6. Displays and saves thresholded image (Task 5)
7. **NEW:** Draws original triangle on image (Task 6)
8. **NEW:** Applies Hough transform to find 3 lines (Task 7a)
9. **NEW:** Calculates vertex intersections (Task 7b)
10. **NEW:** Prints detected vertices and compares with original (Task 7c)

---

## 8. Output Specifications

### 8.1 Console Output
```
=== DETECTED TRIANGLE VERTICES ===
Vertex 1: (256.00, 76.32)
Vertex 2: (104.15, 407.68)
Vertex 3: (407.85, 407.68)

Original Triangle Vertices:
Vertex 1: (256.00, 76.80)
Vertex 2: (104.67, 408.00)
Vertex 3: (407.33, 408.00)

Detection Error (pixels):
Vertex 1: 0.48
Vertex 2: 0.69
Vertex 3: 0.56
Mean Error: 0.58 pixels
```

### 8.2 Saved Images
- `output/01_original_triangle.png` - Original binary triangle
- `output/02_edge_detected.png` - Edge-enhanced grayscale
- `output/03_thresholded.png` - Binary edges (threshold=48)
- `output/04_triangle_overlay.png` - Detected triangle drawn on original
- `output/05_hough_lines.png` - Detected Hough lines visualization

---

## 9. Success Criteria

- ✓ All tasks execute without errors
- ✓ Edge detection clearly highlights triangle boundaries
- ✓ Fixed threshold of 48 produces clean binary edges
- ✓ Hough transform detects exactly 3 lines
- ✓ Vertex calculation produces 3 distinct points
- ✓ Detected vertices within 5 pixels of original vertices
- ✓ Triangle overlay correctly visualizes detection
- ✓ Logging captures all major operations
- ✓ Code adheres to 150-line file limit

---

## 10. Future Enhancements

- Support for multiple geometric shapes
- Adaptive threshold selection
- RANSAC for robust line fitting
- Sub-pixel edge refinement
- Noise robustness testing