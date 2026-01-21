# Project Planning Document
## Image Frequency Filter Application

**Author:** Yair Levi  
**Project:** Image Filtering with FFT  
**Location:** `C:\Users\yair0\AI_continue\Lesson32_imageProcessing\imageFilter\`

---

## Development Phases

### Phase 1: Project Setup
**Duration:** 1-2 hours

#### Activities:
1. Create directory structure
2. Set up virtual environment at `../../venv/`
3. Install dependencies from `requirements.txt`
4. Initialize package structure with `__init__.py` files
5. Set up logging system with ring buffer
6. Create input/output/log directories

#### Deliverables:
- Complete directory structure
- Working virtual environment
- Logging system operational
- Empty module files ready for implementation

---

### Phase 2: Core Infrastructure
**Duration:** 2-3 hours

#### Activities:
1. Implement logging utility with ring buffer (20 files × 16MB)
2. Create path handler for relative path management
3. Implement image loader utility
4. Create configuration settings module
5. Set up base filter abstract class
6. Implement error handling framework

#### Files to Create:
- `utils/logger.py` - Ring buffer logging
- `utils/path_handler.py` - Relative path utilities
- `utils/image_loader.py` - Image I/O operations
- `config/settings.py` - Application configuration
- `filters/base_filter.py` - Abstract base class

#### Testing:
- Verify logging rotation works correctly
- Test path resolution on WSL
- Validate image loading various formats

---

### Phase 3: FFT Implementation
**Duration:** 3-4 hours

#### Activities:
1. Implement FFT transformation task
2. Create frequency domain visualization
3. Implement inverse FFT transformation
4. Add frequency spectrum calculations
5. Handle edge cases (image sizes, formats)

#### Files to Create:
- `tasks/fft_transform.py` - Forward FFT
- `tasks/frequency_display.py` - Visualization
- `tasks/inverse_transform.py` - Inverse FFT

#### Testing:
- FFT/IFFT roundtrip accuracy
- Frequency spectrum visualization
- Different image sizes
- Grayscale and color images

---

### Phase 4: Filter Implementation
**Duration:** 4-5 hours

#### Activities:
1. Implement High-Pass Filter (HPF)
   - Ideal HPF
   - Gaussian HPF (optional)
   - Butterworth HPF (optional)
2. Implement Low-Pass Filter (LPF)
   - Ideal LPF
   - Gaussian LPF (optional)
   - Butterworth LPF (optional)
3. Implement Band-Pass Filter (BPF)
   - Frequency range selection
   - Mask generation
4. Create filter application task
5. Add filter visualization
6. Show spectrum after each filter application

#### Files to Create:
- `filters/high_pass.py` - HPF implementation
- `filters/low_pass.py` - LPF implementation
- `filters/band_pass.py` - BPF implementation
- `tasks/filter_apply.py` - Filter application logic

#### Testing:
- Filter mask generation
- Frequency cutoff accuracy
- Edge detection quality (HPF validation)
- Smoothing quality (LPF validation)
- Band isolation (BPF validation)
- Spectrum visualization after filtering

---

### Phase 5: Display and Integration
**Duration:** 2-3 hours

#### Activities:
1. Implement image display task
2. Create comparison visualization
3. Integrate all tasks in main.py
4. Add command-line argument parsing
5. Implement multiprocessing for parallel filters

#### Files to Create:
- `tasks/image_display.py` - Display utilities
- `main.py` - Main application entry point

#### Testing:
- End-to-end pipeline
- All filter combinations
- Display functionality
- Multiprocessing correctness

---

### Phase 6: Documentation and Refinement
**Duration:** 2-3 hours

#### Activities:
1. Add comprehensive docstrings
2. Refine error messages
3. Optimize performance bottlenecks
4. Add usage examples
5. Create user documentation

#### Deliverables:
- Fully documented code
- README with usage instructions
- Example images and outputs

---

## Technical Architecture

### Module Dependencies

```
main.py
├── config.settings
├── utils.logger
├── utils.path_handler
├── tasks.fft_transform
├── tasks.frequency_display
├── tasks.filter_apply
│   ├── filters.high_pass
│   └── filters.band_pass
├── tasks.inverse_transform
└── tasks.image_display
```

### Data Flow Architecture

```
[Input Image] 
    ↓
[Image Loader] → Load & Validate
    ↓
[FFT Transform] → Convert to Frequency Domain
    ↓
[Frequency Display] → Visualize Spectrum
    ↓
    ├─→ [HPF Filter] → Apply High-Pass
    ├─→ [BPF Filter] → Apply Band-Pass
    └─→ [HPF Filter 2] → Apply Alternative HPF
        ↓
[Inverse FFT] → Convert Back to Spatial Domain
    ↓
[Image Display] → Show/Save Results
    ↓
[Output Image]
```

### Multiprocessing Strategy

**Parallel Operations:**
1. Apply multiple filters simultaneously (HPF, BPF)
2. Process multiple images in batch mode
3. Parallel visualization generation

**Sequential Operations:**
1. Image loading (I/O bound)
2. FFT transformation (per image)
3. Display (single-threaded matplotlib)

**Implementation:**
- Use `multiprocessing.Pool` for filter applications
- Share frequency domain data via manager
- Collect results and merge for display

---

## File Size Management

### Strategy to Keep Files Under 150 Lines:

1. **Separation of Concerns:**
   - One filter per file
   - One task per file
   - Utilities split by function

2. **Code Reuse:**
   - Base classes for common functionality
   - Utility functions in dedicated modules
   - Configuration in separate file

3. **Minimal Imports:**
   - Only import what's needed per file
   - Use lazy imports where appropriate

4. **Concise Documentation:**
   - Header docstring (10-15 lines)
   - Function docstrings (3-5 lines each)
   - Critical inline comments only

---

## Logging Strategy

### Ring Buffer Implementation

**Using `RotatingFileHandler`:**
```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    filename='log/app.log',
    maxBytes=16*1024*1024,  # 16 MB
    backupCount=19  # 20 total files (1 current + 19 backups)
)
```

**Log Levels:**
- INFO: Normal operations, pipeline stages
- WARNING: Recoverable issues, edge cases
- ERROR: Processing failures, invalid input
- CRITICAL: System failures

**Log Format:**
```
2026-01-19 10:30:45,123 - imageFilter.tasks.fft - INFO - Starting FFT transformation
```

---

## Path Management

### Relative Path Strategy

**Base Paths:**
- Project root: `./` (current directory)
- Virtual env: `../../venv/`
- Input: `./input/`
- Output: `./output/`
- Logs: `./log/`

**Path Resolution:**
```python
import os
from pathlib import Path

# Get project root
PROJECT_ROOT = Path(__file__).parent
VENV_PATH = PROJECT_ROOT / '..' / '..' / 'venv'
INPUT_PATH = PROJECT_ROOT / 'input'
OUTPUT_PATH = PROJECT_ROOT / 'output'
LOG_PATH = PROJECT_ROOT / 'log'
```

**Benefits:**
- WSL compatibility
- No hardcoded paths
- Portable across systems
- Easy relocation

---

## Testing Strategy

### Unit Testing
- Test each filter independently
- Verify FFT/IFFT accuracy (within floating-point tolerance)
- Validate path resolution

### Integration Testing
- Full pipeline with sample images
- All filter types
- Error conditions

### Performance Testing
- Large images (4K resolution)
- Multiprocessing efficiency
- Memory usage monitoring

### Test Images
- Standard test images (Lena, Cameraman)
- Various sizes (256×256 to 4096×4096)
- Different formats (PNG, JPG, BMP)

---

## Risk Mitigation

### Memory Management
**Risk:** Large images consume excessive memory

**Mitigation:**
- Implement max image size check
- Add downscaling option
- Clear intermediate results

### Path Issues on WSL
**Risk:** Windows/Linux path incompatibility

**Mitigation:**
- Use `pathlib.Path` exclusively
- Test on actual WSL environment
- Normalize all path separators

### Display Issues
**Risk:** X11/Display not available in WSL

**Mitigation:**
- Make display optional (`--no-display`)
- Always save images to file
- Use `Agg` backend for matplotlib

### Filter Artifacts
**Risk:** Ringing artifacts from ideal filters

**Mitigation:**
- Implement Gaussian/Butterworth alternatives
- Add windowing option
- Document expected behavior

---

## Performance Optimization

### Opportunities:
1. **NumPy Vectorization:** Use array operations instead of loops
2. **FFT Optimization:** Use `scipy.fftpack` for potentially faster FFT
3. **Parallel Processing:** Apply filters in parallel
4. **Lazy Loading:** Load images only when needed
5. **Result Caching:** Cache frequency domain for multiple filters

### Benchmarking:
- Measure processing time per step
- Compare single vs. multiprocessing
- Profile memory usage

---

## Success Metrics

### Functional:
- ✓ All filters produce expected results
- ✓ Visualization clearly shows frequency content
- ✓ IFFT reconstructs images accurately

### Technical:
- ✓ All files under 150 lines
- ✓ Logging system works as specified
- ✓ Only relative paths used
- ✓ Multiprocessing provides speedup

### Quality:
- ✓ Code is well-documented
- ✓ Error handling is robust
- ✓ Performance is acceptable (<5s per image)

---

## Development Environment

### Setup Commands:
```bash
# Navigate to project
cd /mnt/c/Users/yair0/AI_continue/Lesson32_imageProcessing/imageFilter

# Create and activate virtual environment
python3 -m venv ../../venv
source ../../venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py --input input/sample.jpg --filter all --show
```

---

## Next Steps

1. Review and approve this planning document
2. Create tasks.md with detailed task breakdown
3. Begin Phase 1: Project Setup
4. Implement core infrastructure (Phase 2)
5. Proceed through remaining phases sequentially

---

**Planning Status:** Complete  
**Ready for Implementation:** Yes