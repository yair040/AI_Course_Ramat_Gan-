# Task Breakdown
## Image Frequency Filter Application

**Author:** Yair Levi  
**Project:** Image Filtering with FFT  
**Location:** `C:\Users\yair0\AI_continue\Lesson32_imageProcessing\imageFilter\`

---

## Task Overview

| Task # | Description | Estimated Time | Dependencies |
|--------|-------------|----------------|--------------|
| T1 | Project Setup | 1-2 hours | None |
| T2 | Logging System | 1 hour | T1 |
| T3 | Path & Image Utilities | 1-2 hours | T1 |
| T4 | Configuration Module | 1 hour | T1 |
| T5 | FFT Transform Task | 2 hours | T3, T4 |
| T6 | Frequency Display Task | 2 hours | T5 |
| T7 | Base Filter Class | 1 hour | T4 |
| T8 | High-Pass Filter | 2 hours | T7 |
| T9 | Low-Pass Filter | 2 hours | T7 |
| T10 | Band-Pass Filter | 2 hours | T7 |
| T11 | Filter Application Task | 2 hours | T8, T9, T10 |
| T12 | Inverse FFT Task | 1 hour | T5 |
| T13 | Image Display Task | 2 hours | T12 |
| T14 | Main Application | 3 hours | All |
| T15 | Testing & Refinement | 2-3 hours | T14 |

**Total Estimated Time:** 24-28 hours

---

## Detailed Task Breakdown

### T1: Project Setup
**Priority:** Critical  
**Status:** Not Started

#### Subtasks:
1. Create complete directory structure
2. Initialize all `__init__.py` files
3. Create input, output, log directories
4. Set up virtual environment at `../../venv/`
5. Create empty module files

#### Directory Structure to Create:
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
├── input/
└── output/
```

#### Commands:
```bash
cd /mnt/c/Users/yair0/AI_continue/Lesson32_imageProcessing/imageFilter
mkdir -p tasks filters utils config log input output
touch __init__.py main.py
touch tasks/__init__.py filters/__init__.py utils/__init__.py config/__init__.py
python3 -m venv ../../venv
source ../../venv/bin/activate
```

#### Deliverables:
- Complete directory structure
- All `__init__.py` files created
- Virtual environment ready

---

### T2: Logging System
**Priority:** High  
**Status:** Not Started  
**File:** `utils/logger.py` (≤150 lines)

#### Subtasks:
1. Implement ring buffer with RotatingFileHandler
2. Configure 20 files × 16MB rotation
3. Set INFO level as minimum
4. Create custom formatter
5. Add helper functions for logger setup

#### Requirements:
- Automatic log directory creation
- Proper rotation (overwrite oldest)
- Thread-safe logging
- Clean log format

#### Key Functions:
```python
def setup_logger(name: str, level=logging.INFO) -> logging.Logger
def get_logger(name: str) -> logging.Logger
```

#### Testing:
- Verify 20 files are created
- Confirm 16MB size limit
- Test rotation (oldest file overwritten)
- Validate thread safety

#### Deliverables:
- `utils/logger.py` fully implemented
- Working ring buffer logging system

---

### T3: Path & Image Utilities
**Priority:** High  
**Status:** Not Started  
**Files:** `utils/path_handler.py`, `utils/image_loader.py` (each ≤150 lines)

#### T3.1: Path Handler
**File:** `utils/path_handler.py`

##### Subtasks:
1. Implement relative path resolution
2. Create path constants (VENV, INPUT, OUTPUT, LOG)
3. Add path validation functions
4. Handle WSL path compatibility

##### Key Functions:
```python
def get_project_root() -> Path
def get_venv_path() -> Path
def get_input_path(filename: str) -> Path
def get_output_path(filename: str) -> Path
def get_log_path() -> Path
def ensure_directory(path: Path) -> None
```

#### T3.2: Image Loader
**File:** `utils/image_loader.py`

##### Subtasks:
1. Implement image loading with OpenCV
2. Add format validation (PNG, JPG, BMP)
3. Handle grayscale conversion
4. Add image saving functionality
5. Implement error handling

##### Key Functions:
```python
def load_image(path: Path, grayscale: bool = True) -> np.ndarray
def save_image(image: np.ndarray, path: Path) -> None
def validate_image_format(path: Path) -> bool
def get_image_info(image: np.ndarray) -> dict
```

#### Testing:
- Load various image formats
- Test path resolution on WSL
- Validate error handling
- Verify grayscale conversion

#### Deliverables:
- `utils/path_handler.py` complete
- `utils/image_loader.py` complete
- Both files under 150 lines

---

### T4: Configuration Module
**Priority:** High  
**Status:** Not Started  
**File:** `config/settings.py` (≤150 lines)

#### Subtasks:
1. Define filter configuration classes
2. Set default parameters
3. Add validation methods
4. Create configuration loader

#### Configuration Classes:
```python
class FilterConfig:
    filter_type: str  # 'ideal', 'gaussian', 'butterworth'
    cutoff_frequency: float

class HPFConfig(FilterConfig):
    cutoff: float = 30.0

class BPFConfig(FilterConfig):
    low_cutoff: float = 20.0
    high_cutoff: float = 80.0

class AppConfig:
    log_level: int = logging.INFO
    max_image_size: int = 4096
    show_display: bool = True
    save_output: bool = True
```

#### Deliverables:
- Complete configuration system
- Validated default values
- Easy parameter modification

---

### T5: FFT Transform Task
**Priority:** Critical  
**Status:** Not Started  
**File:** `tasks/fft_transform.py` (≤150 lines)

#### Subtasks:
1. Implement 2D FFT using NumPy
2. Apply FFT shift (center zero frequency)
3. Calculate magnitude spectrum
4. Handle complex number operations
5. Add logging for each step

#### Key Functions:
```python
def apply_fft(image: np.ndarray) -> np.ndarray
def get_magnitude_spectrum(fft_image: np.ndarray) -> np.ndarray
def get_phase_spectrum(fft_image: np.ndarray) -> np.ndarray
```

#### Algorithm:
1. Convert image to float
2. Apply `np.fft.fft2()`
3. Apply `np.fft.fftshift()`
4. Calculate magnitude: `np.abs(fft_shifted)`
5. Return complex FFT result

#### Testing:
- Verify FFT dimensions match input
- Check magnitude spectrum range
- Validate zero-frequency at center

#### Deliverables:
- Working FFT transformation
- Proper frequency centering
- Clean magnitude calculation

---

### T6: Frequency Display Task
**Priority:** High  
**Status:** Not Started  
**File:** `tasks/frequency_display.py` (≤150 lines)

#### Subtasks:
1. Implement magnitude spectrum visualization
2. Apply logarithmic scaling
3. Create side-by-side comparison plots
4. Save frequency domain images
5. Handle matplotlib display/save

#### Key Functions:
```python
def visualize_spectrum(magnitude: np.ndarray, title: str) -> None
def save_spectrum(magnitude: np.ndarray, output_path: Path) -> None
def plot_comparison(original: np.ndarray, spectrum: np.ndarray) -> None
```

#### Visualization Requirements:
- Logarithmic scale: `20 * np.log10(magnitude + 1)`
- Grayscale colormap
- Clear labels and titles
- Save to output directory

#### Testing:
- Verify visualization clarity
- Test save functionality
- Check display without X11

#### Deliverables:
- Clear frequency visualizations
- Working save functionality
- Optional display mode

---

### T7: Base Filter Class
**Priority:** High  
**Status:** Not Started  
**File:** `filters/base_filter.py` (≤150 lines)

#### Subtasks:
1. Create abstract base class
2. Define filter interface
3. Implement common utilities
4. Add mask generation helpers

#### Abstract Class Structure:
```python
from abc import ABC, abstractmethod

class BaseFilter(ABC):
    @abstractmethod
    def create_mask(self, shape: tuple) -> np.ndarray:
        """Create filter mask for given image shape"""
        pass
    
    @abstractmethod
    def apply(self, fft_image: np.ndarray) -> np.ndarray:
        """Apply filter to FFT image"""
        pass
    
    def get_filter_info(self) -> dict:
        """Return filter parameters"""
        pass
```

#### Common Utilities:
- Distance matrix calculation
- Circular mask generation
- Normalization functions

#### Deliverables:
- Complete abstract base class
- Reusable utility functions
- Clear interface definition

---

### T8: High-Pass Filter
**Priority:** Critical  
**Status:** Not Started  
**File:** `filters/high_pass.py` (≤150 lines)

#### Subtasks:
1. Implement ideal HPF
2. Create circular mask (remove center)
3. Add configurable cutoff frequency
4. Integrate with base filter class
5. Add filter visualization

#### Key Functions:
```python
class HighPassFilter(BaseFilter):
    def __init__(self, cutoff: float = 30.0):
        self.cutoff = cutoff
    
    def create_mask(self, shape: tuple) -> np.ndarray:
        """Create HPF mask: 0 at center, 1 at edges"""
        pass
    
    def apply(self, fft_image: np.ndarray) -> np.ndarray:
        """Apply HPF to FFT image"""
        pass
```

#### Mask Generation:
1. Create distance matrix from center
2. Set mask = 1 where distance > cutoff
3. Set mask = 0 where distance ≤ cutoff
4. Return binary mask

#### Testing:
- Verify edge enhancement in output
- Test various cutoff values
- Check mask shape matches image

#### Deliverables:
- Working HPF implementation
- Configurable cutoff parameter
- Clean filter application

---

### T9: Low-Pass Filter
**Priority:** Critical  
**Status:** Not Started  
**File:** `filters/low_pass.py` (≤150 lines)

#### Subtasks:
1. Implement ideal LPF
2. Create circular mask (keep center)
3. Add configurable cutoff frequency
4. Integrate with base filter class
5. Add filter visualization

#### Key Functions:
```python
class LowPassFilter(BaseFilter):
    def __init__(self, cutoff: float = 30.0):
        self.cutoff = cutoff
    
    def create_mask(self, shape: tuple) -> np.ndarray:
        """Create LPF mask: 1 at center, 0 at edges"""
        pass
    
    def apply(self, fft_image: np.ndarray) -> np.ndarray:
        """Apply LPF to FFT image"""
        pass
```

#### Mask Generation:
1. Create distance matrix from center
2. Set mask = 1 where distance ≤ cutoff
3. Set mask = 0 where distance > cutoff
4. Return binary mask

#### Testing:
- Verify image smoothing in output
- Test various cutoff values
- Check mask shape matches image

#### Deliverables:
- Working LPF implementation
- Configurable cutoff parameter
- Clean filter application

---

### T10: Band-Pass Filter
**Priority:** Critical  
**Status:** Not Started  
**File:** `filters/band_pass.py` (≤150 lines)

#### Subtasks:
1. Implement ideal BPF
2. Create annular (ring) mask
3. Add low and high cutoff frequencies
4. Integrate with base filter class
5. Add filter visualization

#### Key Functions:
```python
class BandPassFilter(BaseFilter):
    def __init__(self, low_cutoff: float = 20.0, high_cutoff: float = 80.0):
        self.low_cutoff = low_cutoff
        self.high_cutoff = high_cutoff
    
    def create_mask(self, shape: tuple) -> np.ndarray:
        """Create BPF mask: 1 in ring, 0 elsewhere"""
        pass
    
    def apply(self, fft_image: np.ndarray) -> np.ndarray:
        """Apply BPF to FFT image"""
        pass
```

#### Mask Generation:
1. Create distance matrix from center
2. Set mask = 1 where low_cutoff < distance < high_cutoff
3. Set mask = 0 elsewhere
4. Return binary mask

#### Testing:
- Verify band isolation
- Test various cutoff combinations
- Validate frequency range

#### Deliverables:
- Working BPF implementation
- Configurable frequency range
- Proper band isolation

---

### T11: Filter Application Task
**Priority:** High  
**Status:** Not Started  
**File:** `tasks/filter_apply.py` (≤150 lines)

#### Subtasks:
1. Implement filter application orchestration
2. Add multiprocessing support for parallel filters
3. Handle filter mask generation
4. Apply filter to FFT data
5. Add logging and error handling

#### Key Functions:
```python
def apply_filter(fft_image: np.ndarray, filter_obj: BaseFilter) -> np.ndarray
def apply_filters_parallel(fft_image: np.ndarray, filters: list) -> list
def save_filtered_spectrum(filtered_fft: np.ndarray, output_path: Path) -> None
```

#### Multiprocessing Strategy:
```python
from multiprocessing import Pool

def process_single_filter(args):
    fft_image, filter_obj = args
    return apply_filter(fft_image, filter_obj)

def apply_filters_parallel(fft_image, filters):
    with Pool() as pool:
        results = pool.map(process_single_filter, [(fft_image, f) for f in filters])
    return results
```

#### Deliverables:
- Efficient filter application
- Parallel processing support
- Clean error handling

---

### T12: Inverse FFT Task
**Priority:** Critical  
**Status:** Not Started  
**File:** `tasks/inverse_transform.py` (≤150 lines)

#### Subtasks:
1. Implement inverse FFT using NumPy
2. Apply inverse FFT shift
3. Extract real component
4. Normalize to valid image range [0, 255]
5. Add logging

#### Key Functions:
```python
def apply_ifft(fft_image: np.ndarray) -> np.ndarray
def normalize_image(image: np.ndarray) -> np.ndarray
def reconstruct_image(filtered_fft: np.ndarray) -> np.ndarray
```

#### Algorithm:
1. Apply `np.fft.ifftshift()`
2. Apply `np.fft.ifft2()`
3. Take real part: `np.real()`
4. Normalize to [0, 255]
5. Convert to uint8

#### Testing:
- Verify FFT/IFFT roundtrip accuracy
- Check output dimensions
- Validate image range

#### Deliverables:
- Working inverse FFT
- Proper normalization
- Clean image reconstruction

---

### T13: Image Display Task
**Priority:** Medium  
**Status:** Not Started  
**File:** `tasks/image_display.py` (≤150 lines)

#### Subtasks:
1. Implement comparison visualization
2. Create side-by-side plots
3. Add original vs. filtered comparison
4. Save comparison images
5. Handle display vs. save-only modes

#### Key Functions:
```python
def display_images(images: list, titles: list, save_path: Path = None) -> None
def create_comparison(original: np.ndarray, filtered: list, filter_names: list) -> None
def save_comparison_grid(images: dict, output_path: Path) -> None
```

#### Display Modes:
- Interactive display (if available)
- Save-only mode (WSL compatibility)
- Grid layout for multiple filters

#### Testing:
- Test with/without X11 display
- Verify save functionality
- Check grid layout

#### Deliverables:
- Flexible display system
- WSL-compatible operation
- Clean comparison visualizations

---

### T14: Main Application
**Priority:** Critical  
**Status:** Not Started  
**File:** `main.py` (≤150 lines)

#### Subtasks:
1. Implement command-line argument parsing
2. Orchestrate complete pipeline
3. Integrate all tasks
4. Add multiprocessing for filters
5. Implement error handling
6. Add progress indicators

#### Command-Line Interface:
```python
import argparse

parser = argparse.ArgumentParser(description='Image Frequency Filter')
parser.add_argument('--input', required=True, help='Input image path')
parser.add_argument('--filter', choices=['hpf', 'lpf', 'bpf', 'all'], default='all')
parser.add_argument('--hpf-cutoff', type=float, default=30.0, help='HPF cutoff')
parser.add_argument('--lpf-cutoff', type=float, default=30.0, help='LPF cutoff')
parser.add_argument('--low-cutoff', type=float, default=20.0)
parser.add_argument('--high-cutoff', type=float, default=80.0)
parser.add_argument('--show', action='store_true', help='Display results')
parser.add_argument('--no-save', action='store_true', help='Don\'t save outputs')
```

#### Pipeline Flow:
1. Parse arguments
2. Load image
3. Apply FFT
4. Display and save original frequency spectrum
5. Apply filters (parallel if multiple)
6. For each filter:
   - Display and save filtered spectrum
   - Apply inverse FFT
   - Save reconstructed image
7. Display/save comparison of all results

#### Deliverables:
- Complete working application
- Clean CLI interface
- Robust error handling

---

### T15: Testing & Refinement
**Priority:** High  
**Status:** Not Started

#### Subtasks:
1. Create test suite
2. Test with various images
3. Validate all filter types
4. Check edge cases
5. Performance optimization
6. Code review and cleanup

#### Test Cases:
- Small images (256×256)
- Large images (4K)
- Various formats (PNG, JPG, BMP)
- Grayscale and color
- All filter combinations
- Error conditions

#### Performance Tests:
- Measure processing time
- Compare single vs. multiprocessing
- Memory usage profiling

#### Refinement:
- Code cleanup
- Documentation review
- Line count verification (≤150 per file)
- Final path validation

#### Deliverables:
- Fully tested application
- Performance benchmarks
- Clean, documented code

---

## Task Dependencies Graph

```
T1 (Setup)
  ├─→ T2 (Logging)
  ├─→ T3 (Path & Image)
  └─→ T4 (Config)
       ├─→ T5 (FFT) ─→ T6 (Freq Display)
       │                    ↓
       └─→ T7 (Base Filter)
            ├─→ T8 (HPF)
            └─→ T9 (BPF)
                 ↓
            T10 (Filter Apply)
                 ↓
            T12 (Inverse FFT)
                 ↓
            T12 (Display)
                 ↓
            T14 (Main) ─→ T15 (Testing)
```

---

## Progress Tracking

### Checklist:
- [ ] T1: Project Setup
- [ ] T2: Logging System
- [ ] T3.1: Path Handler
- [ ] T3.2: Image Loader
- [ ] T4: Configuration Module
- [ ] T5: FFT Transform
- [ ] T6: Frequency Display
- [ ] T7: Base Filter Class
- [ ] T8: High-Pass Filter
- [ ] T9: Low-Pass Filter
- [ ] T10: Band-Pass Filter
- [ ] T11: Filter Application
- [ ] T12: Inverse FFT
- [ ] T13: Image Display
- [ ] T14: Main Application
- [ ] T15: Testing & Refinement

---

**Document Status:** Complete  
**Ready to Start:** T1 (Project Setup)