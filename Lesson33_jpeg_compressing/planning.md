# Planning Document
## JPEG Compression Analysis Tool

**Author:** Yair Levi  
**Project:** jpeg_compressing  
**Environment:** WSL + Python Virtual Environment

---

## Project Structure

```
AI_continue/
└── Lesson33_jpeg_compressing/
    └── jpeg_compressing/          # Current folder
        ├── __init__.py
        ├── main.py
        ├── Claude.md
        ├── planning.md            # This file
        ├── tasks.md
        ├── requirements.txt
        ├── tasks/
        │   ├── __init__.py
        │   ├── compress_task.py   (~120 lines)
        │   ├── decompress_task.py (~100 lines)
        │   ├── error_task.py      (~130 lines)
        │   └── visualize_task.py  (~140 lines)
        ├── utils/
        │   ├── __init__.py
        │   ├── logger.py          (~100 lines)
        │   └── config.py          (~80 lines)
        ├── data/
        │   └── input/             # Input images
        └── output/
            ├── compressed/        # JPEG compressed images
            ├── decompressed/      # Decompressed images
            ├── metrics/           # CSV metrics files
            ├── plots/             # Histogram visualizations
            └── logs/              # Ring buffer logs (20 files)

../../venv/                        # Virtual environment location
```

---

## Architecture Design

### Component Breakdown

#### 1. Main Entry Point (`main.py`)
- Argument parsing for input image path
- Task orchestration
- Error handling at top level
- Progress reporting

#### 2. Task Modules

##### `tasks/compress_task.py`
- **Function:** `compress_image(image_path, quality_levels, output_dir)`
- **Returns:** List of compressed file paths
- **Multiprocessing:** Pool for parallel compression
- **Quality Levels:** [10, 20, 30, 40, 50, 60, 70, 80, 90, 95]

##### `tasks/decompress_task.py`
- **Function:** `decompress_images(compressed_paths, output_dir)`
- **Returns:** List of decompressed image arrays
- **Multiprocessing:** Pool for parallel decompression

##### `tasks/error_task.py`
- **Function:** `calculate_errors(original, decompressed_list, quality_levels)`
- **Returns:** DataFrame with metrics (Quality, MSE, MAE, FileSize, CompressionRatio)
- **Metrics:** 
  - Mean Squared Error (MSE) - Primary
  - Mean Absolute Error (MAE) - Secondary
  - File size comparison
  - Compression ratio

##### `tasks/visualize_task.py`
- **Function:** `create_byte_histograms(original, compressed_images, quality_levels, output_dir)`
- **Function:** `create_error_histogram(error_df, output_dir)`
- **Output:** PNG files for all visualizations
- **Layout:** Subplots for multi-quality comparison

#### 3. Utility Modules

##### `utils/logger.py`
- Ring buffer implementation using `RotatingFileHandler`
- 20 files × 16MB = 320MB total log capacity
- File naming: `app_01.log` through `app_20.log`
- Centralized logger configuration

##### `utils/config.py`
- Quality levels configuration
- Path configurations (relative)
- Constant definitions
- Default parameters

---

## Technical Implementation Details

### 1. Multiprocessing Strategy

```python
# Parallel compression across quality levels
with multiprocessing.Pool(processes=min(10, cpu_count())) as pool:
    results = pool.starmap(compress_single, quality_params)
```

**Benefits:**
- 10 quality levels → Up to 10 parallel processes
- Significant speedup for large images
- Independent compression operations

### 2. Logging Configuration

```python
# Ring buffer: 20 files, 16MB each
handler = RotatingFileHandler(
    filename='output/logs/app.log',
    maxBytes=16 * 1024 * 1024,  # 16MB
    backupCount=19,              # Total 20 files
    mode='a'
)
```

### 3. Error Calculation Methodology

**Mean Squared Error (MSE):**
- Formula: `MSE = mean((original - decompressed)²)`
- Sensitive to large errors
- Commonly used in image processing
- **Selected as primary metric**

**Mean Absolute Error (MAE):**
- Formula: `MAE = mean(|original - decompressed|)`
- Less sensitive to outliers
- Useful for comparison

**Rationale for MSE:**
- Square emphasizes larger deviations
- Standard metric in JPEG quality assessment
- Relates to PSNR (Peak Signal-to-Noise Ratio)

### 4. Histogram Design

#### Byte Distribution Histograms
- **X-axis:** Pixel intensity values (0-255)
- **Y-axis:** Frequency count
- **Bins:** 256 bins (one per intensity level)
- **Layout:** 
  - Original image: Single plot
  - Compressed images: Grid of 10 subplots (2×5 or 3×4)

#### Error Distribution Histogram
- **X-axis:** Quality level (10-95)
- **Y-axis:** MSE value
- **Type:** Bar chart or line plot
- **Additional:** Compression ratio overlay

---

## Data Flow Diagram

```
                    ┌─────────────────┐
                    │  Input Image    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Load & Validate │
                    └────────┬────────┘
                             │
                ┌────────────┴────────────┐
                ▼                         ▼
       ┌────────────────┐        ┌──────────────┐
       │ Original Bytes │        │ Multiprocess │
       │  Histogram     │        │ Compression  │
       └────────────────┘        └──────┬───────┘
                                        │
                                        ▼
                              ┌──────────────────┐
                              │ 10 JPEG Files    │
                              │ (Q: 10-95)       │
                              └─────────┬────────┘
                                        │
                                        ▼
                              ┌──────────────────┐
                              │  Decompress All  │
                              └─────────┬────────┘
                                        │
                        ┌───────────────┴───────────────┐
                        ▼                               ▼
              ┌──────────────────┐          ┌──────────────────┐
              │ Calculate Errors │          │ Compressed Bytes │
              │  (MSE, MAE)      │          │   Histograms     │
              └─────────┬────────┘          └──────────────────┘
                        │
                        ▼
              ┌──────────────────┐
              │  Save Metrics    │
              │   (CSV)          │
              └─────────┬────────┘
                        │
                        ▼
              ┌──────────────────┐
              │  Error vs Q      │
              │   Histogram      │
              └──────────────────┘
```

---

## Development Phases

### Phase 1: Setup & Infrastructure
- [ ] Create directory structure
- [ ] Set up virtual environment at `../../venv`
- [ ] Configure logging with ring buffer
- [ ] Create configuration module

### Phase 2: Core Tasks
- [ ] Implement compression task with multiprocessing
- [ ] Implement decompression task
- [ ] Implement error calculation (MSE/MAE)
- [ ] Test each task independently

### Phase 3: Visualization
- [ ] Create byte distribution histograms
- [ ] Create error vs. quality histograms
- [ ] Format and style plots

### Phase 4: Integration
- [ ] Implement main.py orchestration
- [ ] Add command-line argument parsing
- [ ] Integrate all tasks into pipeline
- [ ] End-to-end testing

### Phase 5: Documentation & Testing
- [ ] Complete Claude.md with usage instructions
- [ ] Complete tasks.md with task list
- [ ] Test with various image sizes
- [ ] Verify WSL compatibility

---

## Quality Levels Strategy

```python
QUALITY_LEVELS = [10, 20, 30, 40, 50, 60, 70, 80, 90, 95]
```

**Rationale:**
- 10: Very low quality, high compression
- 20-40: Low quality range
- 50-70: Medium quality range
- 80-90: High quality range
- 95: Near-lossless

**Coverage:** Good distribution across compression spectrum

---

## Performance Considerations

### Expected Bottlenecks
1. **Image I/O:** Reading/writing large images
2. **Histogram calculation:** Processing pixel arrays
3. **Decompression:** Can be slower than compression

### Optimizations
1. **Multiprocessing:** Parallel quality level processing
2. **NumPy vectorization:** Fast array operations
3. **Lazy loading:** Load images only when needed
4. **Efficient plotting:** Batch histogram generation

---

## Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Large images cause memory issues | High | Add image size validation; resize if needed |
| Ring buffer logs get corrupted | Medium | Use Python's built-in RotatingFileHandler |
| Multiprocessing overhead | Low | Limit pool size to CPU count |
| Path issues in WSL | Medium | Use pathlib for cross-platform paths |
| JPEG quality not reflecting expected compression | Medium | Validate with known test images |

---

## Testing Strategy

### Unit Tests
- Each task module independently
- Logger ring buffer behavior
- Error calculation accuracy

### Integration Tests
- Full pipeline with sample images
- Different image formats (RGB, grayscale)
- Edge cases (very small/large images)

### Test Images
- Small (100×100 px): Quick testing
- Medium (1920×1080 px): Standard photo
- Large (4K): Performance testing

---

## Success Metrics

1. ✅ All Python files ≤ 150 lines
2. ✅ Multiprocessing reduces runtime by 50%+
3. ✅ Ring buffer maintains 20 files correctly
4. ✅ Histograms are clear and informative
5. ✅ Error metrics match expected JPEG behavior
6. ✅ No absolute paths in code
7. ✅ Runs successfully in WSL + venv
