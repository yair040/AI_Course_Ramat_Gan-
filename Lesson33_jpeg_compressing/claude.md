# JPEG Compression Analysis Tool
## User Guide

**Author:** Yair Levi  
**Version:** 1.0  
**Platform:** WSL (Windows Subsystem for Linux)

---

## Overview

This tool analyzes JPEG compression by compressing images at multiple quality levels, decompressing them, and measuring the reconstruction error. It provides visual insights through histograms showing byte distributions and error metrics.

### Key Features
- ✅ Compress images at 10 different JPEG quality levels
- ✅ Calculate Mean Squared Error (MSE) and Mean Absolute Error (MAE)
- ✅ Generate byte distribution histograms
- ✅ Generate error vs. quality histograms
- ✅ Multiprocessing for fast parallel execution
- ✅ Comprehensive logging with ring buffer (20 files × 16MB)
- ✅ CSV export of all metrics

---

## Installation

### Prerequisites
- WSL (Windows Subsystem for Linux)
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Navigate to project directory:**
   ```bash
   cd /mnt/c/Users/yair0/AI_continue/Lesson33_jpeg_compressing/jpeg_compressing
   ```

2. **Create virtual environment** (at `../../venv`):
   ```bash
   cd /mnt/c/Users/yair0/AI_continue
   python3 -m venv venv
   ```

3. **Activate virtual environment:**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   cd Lesson33_jpeg_compressing/jpeg_compressing
   pip install -r requirements.txt
   ```

5. **Verify installation:**
   ```bash
   python -c "import PIL, numpy, matplotlib; print('All dependencies installed!')"
   ```

---

## Usage

### Basic Usage

```bash
python main.py --input data/input/sample_image.jpg
```

### Command-Line Arguments

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `--input` | Yes | Path to input image | `data/input/photo.jpg` |
| `--output` | No | Output directory (default: `output/`) | `custom_output/` |
| `--quality-levels` | No | Custom quality levels (default: 10,20,...,95) | `10,50,90` |

### Examples

**Example 1: Basic analysis**
```bash
python main.py --input data/input/landscape.jpg
```

**Example 2: Custom quality levels**
```bash
python main.py --input data/input/portrait.jpg --quality-levels 10,30,50,70,90
```

**Example 3: Custom output directory**
```bash
python main.py --input data/input/photo.jpg --output results/experiment_1/
```

---

## Directory Structure

```
jpeg_compressing/
├── main.py                    # Main entry point
├── requirements.txt           # Python dependencies
├── Claude.md                  # This file
├── planning.md               # Planning document
├── tasks.md                  # Task checklist
│
├── tasks/                    # Task modules
│   ├── __init__.py
│   ├── compress_task.py      # Image compression
│   ├── decompress_task.py    # Image decompression
│   ├── error_task.py         # Error calculation
│   └── visualize_task.py     # Histogram generation
│
├── utils/                    # Utility modules
│   ├── __init__.py
│   ├── logger.py             # Ring buffer logging
│   └── config.py             # Configuration constants
│
├── data/
│   └── input/                # Place input images here
│
└── output/
    ├── compressed/           # JPEG compressed images
    ├── decompressed/         # Decompressed images
    ├── metrics/              # CSV files with metrics
    ├── plots/                # Histogram visualizations
    └── logs/                 # Application logs (ring buffer)
```

---

## Output Files

### 1. Compressed Images
**Location:** `output/compressed/`

**Files:**
- `compressed_q10.jpg`
- `compressed_q20.jpg`
- ...
- `compressed_q95.jpg`

### 2. Decompressed Images
**Location:** `output/decompressed/`

**Files:**
- `decompressed_q10.png`
- `decompressed_q20.png`
- ...
- `decompressed_q95.png`

### 3. Metrics CSV
**Location:** `output/metrics/metrics.csv`

**Columns:**
- `Quality`: JPEG quality level (10-95)
- `MSE`: Mean Squared Error
- `MAE`: Mean Absolute Error
- `FileSize_KB`: Compressed file size in kilobytes
- `CompressionRatio`: Original size / Compressed size

**Example:**
```csv
Quality,MSE,MAE,FileSize_KB,CompressionRatio
10,245.67,12.34,45.2,22.1
20,156.23,9.87,78.5,12.7
...
```

### 4. Visualizations
**Location:** `output/plots/`

**Files:**
- `byte_histogram_original.png` - Original image byte distribution
- `byte_histogram_compressed.png` - 10 subplots showing compressed images
- `error_vs_quality.png` - MSE and compression ratio vs. quality

---

## Understanding the Results

### Byte Distribution Histograms

**Original Image Histogram:**
- Shows the distribution of pixel intensity values (0-255)
- Useful for understanding image characteristics
- Peaks indicate common pixel values

**Compressed Image Histograms:**
- Grid of 10 histograms (one per quality level)
- Observe how distribution changes with compression
- Lower quality → Loss of detail in distribution

### Error vs. Quality Plot

**MSE (Mean Squared Error):**
- Lower is better
- Higher quality → Lower MSE
- Exponential relationship typically

**Compression Ratio:**
- Higher is better (more compression)
- Lower quality → Higher compression ratio
- Trade-off between quality and size

**Interpretation:**
- Find the "sweet spot" where error is acceptable and compression is high
- Typical: Q=80-85 offers good balance for photos

---

## Performance

### Execution Time
- **Small images (< 1MP):** ~5-10 seconds
- **Medium images (2-5MP):** ~15-30 seconds
- **Large images (> 10MP):** ~1-2 minutes

### Multiprocessing
The tool uses multiprocessing to parallelize compression and decompression across quality levels:
- Up to 10 parallel processes (one per quality level)
- Speedup: ~5-7× compared to sequential processing
- Automatically scales to available CPU cores

---

## Logging

### Ring Buffer Configuration
- **Total Files:** 20
- **File Size:** 16MB each
- **Total Capacity:** 320MB
- **Rotation:** When file 20 is full, file 1 is overwritten

### Log Levels
- **INFO:** Normal operation (compression started, completed, etc.)
- **WARNING:** Non-critical issues (large file size, etc.)
- **ERROR:** Failures (file not found, compression error, etc.)

### Log Format
```
2026-01-22 10:15:23,456 - tasks.compress - INFO - Starting compression at quality 50
2026-01-22 10:15:24,789 - tasks.compress - INFO - Compressed image saved: compressed_q50.jpg
```

### Viewing Logs
```bash
# View latest log
tail -f output/logs/app.log

# View specific log file
cat output/logs/app.log.1

# Search logs
grep "ERROR" output/logs/*.log
```

---

## Troubleshooting

### Issue: "No module named 'PIL'"
**Solution:**
```bash
source ../../venv/bin/activate
pip install -r requirements.txt
```

### Issue: "FileNotFoundError: Input image not found"
**Solution:**
- Verify the input path is correct
- Use relative paths from the project root
- Example: `data/input/image.jpg`

### Issue: "Permission denied" when creating output files
**Solution:**
```bash
# Ensure output directories exist
mkdir -p output/{compressed,decompressed,metrics,plots,logs}

# Check permissions
chmod -R 755 output/
```

### Issue: Multiprocessing not working in WSL
**Solution:**
- Ensure you're using WSL2 (not WSL1)
- Update WSL: `wsl --update`
- Check: `python -c "import multiprocessing; print(multiprocessing.cpu_count())"`

### Issue: Plots not displaying
**Solution:**
- Plots are saved as PNG files in `output/plots/`
- Open with: `explorer.exe output/plots/` (from WSL)
- Or copy to Windows: `cp output/plots/*.png /mnt/c/Users/yair0/Desktop/`

### Issue: Very large log files
**Solution:**
- Ring buffer automatically manages size
- Manually clear if needed: `rm output/logs/*.log`
- Adjust rotation in `utils/logger.py` if necessary

---

## Best Practices

### Image Selection
- **Format:** JPG, PNG, BMP supported
- **Size:** 500KB - 5MB recommended
- **Resolution:** 1024×768 to 3840×2160
- **Type:** Photographic images show best results

### Quality Level Selection
- **Default:** 10, 20, 30, 40, 50, 60, 70, 80, 90, 95
- **For photos:** Focus on 70-95 range
- **For compression research:** Use full range
- **Custom:** Modify in `utils/config.py`

### Performance Tips
1. Use SSD for faster I/O
2. Close unnecessary applications
3. Process one image at a time
4. Use smaller images for testing

---

## Advanced Configuration

### Modifying Quality Levels
Edit `utils/config.py`:
```python
QUALITY_LEVELS = [10, 30, 50, 70, 90]  # Custom levels
```

### Changing Log Settings
Edit `utils/logger.py`:
```python
# Increase to 30 files
handler = RotatingFileHandler(
    filename='output/logs/app.log',
    maxBytes=16 * 1024 * 1024,
    backupCount=29,  # 30 total files
)
```

### Customizing Histograms
Edit `tasks/visualize_task.py`:
```python
# Change figure size
fig, axes = plt.subplots(2, 5, figsize=(20, 8))  # Larger

# Change bins
plt.hist(data, bins=128)  # Fewer bins
```

---

## Example Workflow

1. **Prepare input image:**
   ```bash
   cp ~/Pictures/photo.jpg data/input/
   ```

2. **Run analysis:**
   ```bash
   python main.py --input data/input/photo.jpg
   ```

3. **Check logs:**
   ```bash
   tail -n 50 output/logs/app.log
   ```

4. **View metrics:**
   ```bash
   cat output/metrics/metrics.csv
   ```

5. **Open visualizations:**
   ```bash
   explorer.exe output/plots/
   ```

6. **Analyze results:**
   - Review error vs. quality plot
   - Identify optimal quality level
   - Compare file sizes

---

## API Reference (for developers)

### compress_task.py
```python
compress_image(image_path: str, quality_levels: list, output_dir: str) -> list
```
Compresses image at multiple quality levels using multiprocessing.

### decompress_task.py
```python
decompress_images(compressed_paths: list, output_dir: str) -> list
```
Decompresses JPEG images to numpy arrays.

### error_task.py
```python
calculate_errors(original: np.ndarray, decompressed_list: list, 
                quality_levels: list, compressed_paths: list) -> pd.DataFrame
```
Calculates MSE, MAE, and compression metrics.

### visualize_task.py
```python
create_byte_histograms(original: np.ndarray, compressed_images: list,
                      quality_levels: list, output_dir: str) -> None
create_error_histogram(error_df: pd.DataFrame, output_dir: str) -> None
```
Generates histogram visualizations.

---

## FAQ

**Q: Can I process multiple images at once?**  
A: Currently, the tool processes one image at a time. Batch processing is planned for future versions.

**Q: What image formats are supported?**  
A: Input: JPG, PNG, BMP, TIFF. Output: JPEG for compressed, PNG for decompressed.

**Q: How is MSE calculated?**  
A: MSE = mean((original_pixels - decompressed_pixels)²) across all pixels and channels.

**Q: Why use MSE instead of MAE?**  
A: MSE penalizes larger errors more heavily, which is important for image quality assessment. Both are provided for comparison.

**Q: Can I change the number of quality levels?**  
A: Yes, modify `QUALITY_LEVELS` in `utils/config.py` or use `--quality-levels` argument.

**Q: How much disk space is needed?**  
A: Approximately 10× the input image size for all outputs (compressed images, plots, logs).

---

## Support

For issues or questions:
1. Check logs in `output/logs/`
2. Review troubleshooting section above
3. Verify all dependencies are installed
4. Check WSL2 is properly configured

---

## License

This tool is for educational and research purposes.

**Author:** Yair Levi  
**Date:** January 22, 2026
