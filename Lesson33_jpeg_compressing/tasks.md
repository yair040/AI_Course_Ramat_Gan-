# Tasks Checklist
## JPEG Compression Analysis Tool

**Author:** Yair Levi  
**Project Status:** Planning Phase

---

## Setup Tasks

### Environment Setup
- [ ] Navigate to project directory: `C:\Users\yair0\AI_continue\Lesson33_jpeg_compressing\jpeg_compressing\`
- [ ] Create virtual environment at `../../venv`
  ```bash
  cd C:\Users\yair0\AI_continue
  python3 -m venv venv
  ```
- [ ] Activate virtual environment
  ```bash
  source venv/bin/activate  # WSL
  ```
- [ ] Install dependencies from requirements.txt
  ```bash
  pip install -r Lesson33_jpeg_compressing/jpeg_compressing/requirements.txt
  ```

### Directory Structure
- [ ] Create `tasks/` directory
- [ ] Create `utils/` directory
- [ ] Create `data/input/` directory
- [ ] Create `output/compressed/` directory
- [ ] Create `output/decompressed/` directory
- [ ] Create `output/metrics/` directory
- [ ] Create `output/plots/` directory
- [ ] Create `output/logs/` directory

---

## Development Tasks

### Phase 1: Core Infrastructure

#### `utils/config.py` (≤150 lines)
- [ ] Define quality levels constant: `[10, 20, 30, 40, 50, 60, 70, 80, 90, 95]`
- [ ] Define relative path constants
- [ ] Define logging configuration constants
- [ ] Define histogram parameters (bins, figure size, etc.)
- [ ] Add data directory paths
- [ ] Add output directory paths

#### `utils/logger.py` (≤150 lines)
- [ ] Import logging and RotatingFileHandler
- [ ] Create ring buffer logger configuration
  - 20 log files
  - 16MB per file
  - Format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- [ ] Set log level to INFO
- [ ] Create `get_logger()` function
- [ ] Test ring buffer rotation

#### `__init__.py` (root)
- [ ] Package initialization
- [ ] Version information
- [ ] Import main modules

---

### Phase 2: Task Modules

#### `tasks/__init__.py`
- [ ] Import all task functions
- [ ] Define `__all__` list

#### `tasks/compress_task.py` (≤150 lines)
- [ ] Import PIL, multiprocessing, logging
- [ ] Function: `compress_single(image_array, quality, output_path)`
  - Convert array to PIL Image
  - Save as JPEG with specified quality
  - Return compressed file path and size
- [ ] Function: `compress_image(image_path, quality_levels, output_dir)`
  - Load original image
  - Create multiprocessing pool
  - Parallel compression for all quality levels
  - Log progress for each quality
  - Return list of compressed file paths
- [ ] Add error handling for file I/O
- [ ] Add logging for each compression operation

#### `tasks/decompress_task.py` (≤150 lines)
- [ ] Import PIL, numpy, multiprocessing, logging
- [ ] Function: `decompress_single(jpeg_path)`
  - Load JPEG file
  - Convert to numpy array
  - Return array
- [ ] Function: `decompress_images(compressed_paths, output_dir)`
  - Create multiprocessing pool
  - Parallel decompression
  - Save decompressed images (optional)
  - Log progress
  - Return list of numpy arrays
- [ ] Add error handling
- [ ] Add validation for image dimensions

#### `tasks/error_task.py` (≤150 lines)
- [ ] Import numpy, pandas, logging, pathlib
- [ ] Function: `calculate_mse(original, decompressed)`
  - Compute mean squared error
  - Handle different image shapes
  - Return MSE value
- [ ] Function: `calculate_mae(original, decompressed)`
  - Compute mean absolute error
  - Return MAE value
- [ ] Function: `calculate_errors(original, decompressed_list, quality_levels, compressed_paths)`
  - Iterate through all decompressed images
  - Calculate MSE and MAE for each
  - Get file sizes
  - Calculate compression ratios
  - Create pandas DataFrame
  - Save to CSV in output/metrics/
  - Log all metrics
  - Return DataFrame
- [ ] Add error handling for array operations

#### `tasks/visualize_task.py` (≤150 lines)
- [ ] Import matplotlib, numpy, logging
- [ ] Function: `create_byte_histograms(original, compressed_images, quality_levels, output_dir)`
  - Create figure for original image histogram
  - Save original histogram
  - Create subplot grid for compressed images (2×5)
  - Plot histogram for each quality level
  - Add titles with quality level
  - Save combined compressed histograms
  - Log completion
- [ ] Function: `create_error_histogram(error_df, output_dir)`
  - Create bar chart: Quality vs. MSE
  - Add secondary axis for compression ratio
  - Format axes and labels
  - Add grid and legend
  - Save plot
  - Log completion
- [ ] Configure matplotlib style
- [ ] Add proper labels and titles

---

### Phase 3: Main Application

#### `main.py` (≤150 lines)
- [ ] Import all necessary modules
- [ ] Import argparse for CLI
- [ ] Function: `parse_arguments()`
  - Add argument for input image path
  - Add optional arguments for quality levels
  - Return parsed args
- [ ] Function: `main()`
  - Set up logger
  - Parse arguments
  - Validate input image exists
  - Log start of processing
  - Load original image
  - Call compress_task
  - Call decompress_task
  - Call error_task
  - Call visualize_task (byte histograms)
  - Call visualize_task (error histogram)
  - Log completion with summary
  - Handle exceptions at top level
- [ ] Add `if __name__ == "__main__"` guard
- [ ] Add progress reporting

---

## Testing Tasks

### Unit Testing
- [ ] Test `compress_task.py` with sample image
- [ ] Test `decompress_task.py` with compressed images
- [ ] Test `error_task.py` with known error values
- [ ] Test `visualize_task.py` histogram generation
- [ ] Test `logger.py` ring buffer rotation
- [ ] Verify all files ≤ 150 lines

### Integration Testing
- [ ] Test full pipeline with small image (100×100)
- [ ] Test with medium image (1920×1080)
- [ ] Test with grayscale image
- [ ] Test with RGB image
- [ ] Verify multiprocessing works correctly
- [ ] Check all output files are created
- [ ] Verify relative paths work in WSL

### Validation
- [ ] Verify log files rotate correctly (20 files, 16MB each)
- [ ] Check CSV metrics file format
- [ ] Validate histogram PNG files
- [ ] Verify compressed JPEG quality levels
- [ ] Check decompressed images match expected dimensions
- [ ] Validate error calculations manually for one case

---

## Documentation Tasks

### Code Documentation
- [ ] Add docstrings to all functions
- [ ] Add inline comments for complex logic
- [ ] Add type hints where appropriate
- [ ] Document expected input/output formats

### Project Documentation
- [ ] Complete `Claude.md` with:
  - Project overview
  - Installation instructions
  - Usage examples
  - Expected outputs
  - Troubleshooting guide
- [ ] Update `requirements.txt` with exact versions
- [ ] Create README.md (optional)

---

## Deployment Tasks

### Package Preparation
- [ ] Verify all `__init__.py` files are correct
- [ ] Test package imports
- [ ] Create sample input image in `data/input/`
- [ ] Test from fresh virtual environment

### Final Checks
- [ ] Run pylint or flake8 for code quality
- [ ] Check for hardcoded paths (should be none)
- [ ] Verify logging works in WSL
- [ ] Test multiprocessing on WSL
- [ ] Confirm output directory structure
- [ ] Validate all relative paths

---

## Performance Optimization Tasks

### Multiprocessing
- [ ] Benchmark single-threaded vs. multiprocessed
- [ ] Optimize pool size based on CPU count
- [ ] Add progress bars for long operations (optional)

### Memory Management
- [ ] Test with large images (>10MB)
- [ ] Implement image size validation
- [ ] Add optional image resizing for very large inputs

---

## Optional Enhancements (Future)

- [ ] Add command-line progress bar (tqdm)
- [ ] Support batch processing of multiple images
- [ ] Add SSIM (Structural Similarity Index) metric
- [ ] Add PSNR (Peak Signal-to-Noise Ratio) metric
- [ ] Create summary report (HTML or Markdown)
- [ ] Add configuration file support (YAML/JSON)
- [ ] Implement automated testing suite
- [ ] Add support for PNG, BMP, TIFF formats
- [ ] Create interactive plots (plotly)
- [ ] Add GUI interface (tkinter)

---

## Completion Checklist

### Code Quality
- [ ] All files ≤ 150 lines ✓
- [ ] No absolute paths ✓
- [ ] Multiprocessing implemented ✓
- [ ] Logging at INFO level ✓
- [ ] Ring buffer (20 files × 16MB) ✓
- [ ] Relative paths only ✓
- [ ] Package structure complete ✓

### Functionality
- [ ] Image compression at 10 Q levels ✓
- [ ] Image decompression ✓
- [ ] Error calculation (MSE) ✓
- [ ] Byte histograms generated ✓
- [ ] Error histograms generated ✓
- [ ] Metrics saved to CSV ✓

### Testing
- [ ] Works in WSL ✓
- [ ] Virtual environment at ../../venv ✓
- [ ] All dependencies in requirements.txt ✓
- [ ] Sample run completed successfully ✓

### Documentation
- [ ] PRD complete ✓
- [ ] planning.md complete ✓
- [ ] tasks.md complete ✓
- [ ] Claude.md complete ✓

---

**Next Steps:**
1. Set up virtual environment
2. Create directory structure
3. Begin Phase 1 development
4. Test each component independently
5. Integrate and test full pipeline
