# Product Requirements Document (PRD)
## Image Frequency Filter Application

**Author:** Yair Levi  
**Version:** 1.0  
**Date:** January 19, 2026  
**Project Location:** `C:\Users\yair0\AI_continue\Lesson32_imageProcessing\imageFilter\`

---

## 1. Executive Summary

A Python-based image processing application that applies frequency domain filtering to images using Fast Fourier Transform (FFT). The application will process images through various filters (High-Pass, Low-Pass, Band-Pass) and visualize both frequency domain and spatial domain results.

---

## 2. Objectives

- Apply FFT-based filtering to images for educational and analytical purposes
- Demonstrate frequency domain image processing techniques
- Provide visual feedback of filtering operations
- Support multiple filter types (HPF, BPF)
- Ensure efficient processing using multiprocessing where applicable

---

## 3. Technical Requirements

### 3.1 Environment
- **Platform:** WSL (Windows Subsystem for Linux)
- **Python Version:** 3.8+
- **Virtual Environment:** Located at `../../venv/` relative to project root
- **Package Structure:** Proper Python package with `__init__.py`

### 3.2 Code Organization
- **File Limit:** Maximum 150 lines per Python file
- **Path Handling:** All paths must be relative, no absolute paths
- **Modularity:** Task-based architecture with main program calling individual tasks

### 3.3 Dependencies
- NumPy - Array operations and FFT
- OpenCV (cv2) - Image I/O
- Matplotlib - Visualization
- Pillow - Image manipulation
- scipy - Additional signal processing (optional)

### 3.4 Logging Requirements
- **Level:** INFO and above
- **Format:** Ring buffer (rotating file handler)
- **File Count:** 20 files maximum
- **File Size:** 16 MB per file
- **Location:** `./log/` subdirectory
- **Behavior:** When file 20 is full, overwrite file 1 (circular rotation)

### 3.5 Performance
- **Multiprocessing:** Utilize multiprocessing for parallel filter operations when applicable
- **Memory:** Efficient handling of large images

---

## 4. Functional Requirements

### 4.1 Core Processing Pipeline

#### Step 1: FFT Conversion
- Load input image
- Convert to grayscale if needed
- Apply 2D Fast Fourier Transform
- Shift zero-frequency component to center

#### Step 2: Frequency Visualization
- Display magnitude spectrum
- Apply logarithmic scaling for visualization
- Save frequency domain image

#### Step 3: High-Pass Filter (HPF) Application
- Create circular HPF mask
- Apply mask to frequency domain
- Remove low-frequency components

#### Step 4: Inverse FFT
- Apply inverse FFT to filtered frequency data
- Reconstruct spatial domain image
- Handle complex to real conversion

#### Step 5: Result Display
- Show filtered image
- Save output image
- Display side-by-side comparison

#### Step 6: Low-Pass Filter (LPF) Application
- Repeat steps 2-5 with LPF
- Keep only low-frequency components
- Process and display results

#### Step 7: Band-Pass Filter (BPF) Application
- Repeat steps 2-5 with BPF
- Allow low and high frequency cutoffs
- Process and display results

**Note:** After each filter application, the frequency spectrum of the filtered result is displayed.

### 4.2 Filter Specifications

#### High-Pass Filter (HPF)
- **Type:** Ideal/Gaussian/Butterworth (configurable)
- **Cutoff:** Percentage of frequency range (e.g., remove lowest 10%)
- **Shape:** Circular mask
- **Effect:** Removes low frequencies, enhances edges

#### Low-Pass Filter (LPF)
- **Type:** Ideal/Gaussian/Butterworth (configurable)
- **Cutoff:** Percentage of frequency range (e.g., keep lowest 30%)
- **Shape:** Circular mask
- **Effect:** Removes high frequencies, smooths image

#### Band-Pass Filter (BPF)
- **Type:** Ideal/Gaussian/Butterworth (configurable)
- **Lower Cutoff:** Minimum frequency to pass
- **Upper Cutoff:** Maximum frequency to pass
- **Shape:** Circular annular mask
- **Effect:** Isolates specific frequency range

---

## 5. Non-Functional Requirements

### 5.1 Usability
- Clear console output indicating processing steps
- Informative error messages
- Progress indicators for long operations

### 5.2 Maintainability
- Modular code structure
- Clear function documentation
- Type hints where applicable
- Consistent naming conventions

### 5.3 Reliability
- Graceful error handling
- Input validation
- Logging of all operations

### 5.4 Portability
- WSL compatible
- Relative path usage for cross-platform compatibility
- Virtual environment isolation

---

## 6. System Architecture

### 6.1 Package Structure
```
imageFilter/
├── __init__.py
├── main.py
├── tasks/
│   ├── __init__.py
│   ├── fft_transform.py
│   ├── frequency_display.py
│   ├── filter_apply.py
│   ├── inverse_transform.py
│   └── image_display.py
├── filters/
│   ├── __init__.py
│   ├── high_pass.py
│   ├── low_pass.py
│   ├── band_pass.py
│   └── base_filter.py
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   ├── image_loader.py
│   └── path_handler.py
├── config/
│   ├── __init__.py
│   └── settings.py
├── log/
│   └── (rotating log files)
├── input/
│   └── (input images)
└── output/
    └── (processed images)
```

### 6.2 Data Flow
```
Input Image → FFT → Frequency Visualization → Filter Application → 
Inverse FFT → Output Image → Display
```

---

## 7. Configuration

### 7.1 Filter Parameters
- Cutoff frequencies (configurable)
- Filter types (Ideal/Gaussian/Butterworth)
- Image scaling factors

### 7.2 Paths
- Input image directory: `./input/`
- Output image directory: `./output/`
- Log directory: `./log/`
- Virtual environment: `../../venv/`

### 7.3 Logging
- Format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- Rotation: 20 files × 16 MB

---

## 8. User Interface

### 8.1 Command Line Interface
```bash
python main.py --input <image_path> --filter <hpf|bpf> [options]
```

### 8.2 Options
- `--input`: Path to input image (required)
- `--filter`: Filter type (hpf, lpf, bpf, or all)
- `--hpf-cutoff`: Cutoff frequency for HPF (default: 30)
- `--lpf-cutoff`: Cutoff frequency for LPF (default: 30)
- `--low-cutoff`: Lower cutoff for BPF (default: 20)
- `--high-cutoff`: Upper cutoff for BPF (default: 80)
- `--show`: Display results interactively
- `--save`: Save output images

---

## 9. Testing Requirements

### 9.1 Unit Tests
- Test each filter independently
- Validate FFT/IFFT roundtrip
- Check image dimensions preservation

### 9.2 Integration Tests
- End-to-end pipeline testing
- Multiple image format support
- Edge cases (very small/large images)

---

## 10. Deliverables

1. **Code Package**
   - All Python modules as specified
   - `__init__.py` files for package structure
   
2. **Configuration**
   - `requirements.txt` for dependencies
   - Settings configuration file

3. **Documentation**
   - This PRD
   - `planning.md` - Development planning
   - `tasks.md` - Task breakdown
   - `Claude.md` - Claude AI interaction guide
   - Code comments and docstrings

4. **Directory Structure**
   - Pre-created input/output/log directories

---

## 11. Success Criteria

- ✓ Successfully apply FFT to images
- ✓ Visualize frequency domain clearly
- ✓ Apply HPF, LPF, and BPF filters correctly
- ✓ Show frequency spectrum after each filter application
- ✓ Reconstruct images via IFFT with minimal artifacts
- ✓ Maintain code files under 150 lines each
- ✓ Implement rotating log system as specified
- ✓ Use only relative paths throughout
- ✓ Utilize multiprocessing where beneficial

---

## 12. Timeline

- **Phase 1:** Core FFT implementation (Tasks 1-2)
- **Phase 2:** Filter implementation (Tasks 3-4)
- **Phase 3:** Visualization and display (Task 5)
- **Phase 4:** Testing and refinement (Task 6)

---

## 13. Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Large image memory usage | High | Implement image resizing option |
| FFT artifacts | Medium | Use proper windowing techniques |
| Display compatibility | Low | Fallback to file save only |
| Path resolution issues | Medium | Robust path handling utilities |

---

## 14. Future Enhancements

- Support for color image filtering (per-channel)
- Additional filter types (Notch, etc.)
- GUI interface
- Batch processing capability
- Real-time video filtering

---

## 15. References

- NumPy FFT Documentation
- OpenCV Image Processing Guide
- Digital Image Processing (Gonzalez & Woods)
- Python Logging Cookbook

---

**Document Status:** Draft  
**Next Review:** Upon implementation completion