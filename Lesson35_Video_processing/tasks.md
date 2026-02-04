# Tasks Breakdown
# Video Compression Analysis Tool

**Author:** Yair Levi  
**Date:** February 1, 2026  
**Project:** Lesson 35 - Video Compression

---

## Task Status Legend
- ⬜ Not Started
- 🔄 In Progress
- ✅ Completed
- ⚠️ Blocked
- ❌ Cancelled

---

## SETUP TASKS

### S1: Environment Setup
**Status:** ⬜  
**Priority:** HIGH  
**Estimated Time:** 30 minutes

**Subtasks:**
- [ ] Create virtual environment at `../../venv/`
- [ ] Activate virtual environment
- [ ] Upgrade pip, setuptools, wheel
- [ ] Verify Python version (3.8+)
- [ ] Check FFmpeg installation: `ffmpeg -version`
- [ ] Check FFprobe installation: `ffprobe -version`

**Commands:**
```bash
cd ../../
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
python --version
ffmpeg -version
ffprobe -version
```

**Deliverables:**
- Working virtual environment
- Confirmed FFmpeg/FFprobe availability

---

### S2: Directory Structure
**Status:** ⬜  
**Priority:** HIGH  
**Estimated Time:** 15 minutes

**Subtasks:**
- [ ] Create main package directory structure
- [ ] Create `utils/` subdirectory
- [ ] Create `tasks/` subdirectory
- [ ] Create `log/` subdirectory
- [ ] Create `decoded_frames/` subdirectory
- [ ] Initialize all `__init__.py` files

**Commands:**
```bash
cd AI_continue/Lesson35_Video_compression/Video_compression/
mkdir -p utils tasks log decoded_frames
touch __init__.py utils/__init__.py tasks/__init__.py
```

**Deliverables:**
```
Video_compression/
├── __init__.py
├── utils/
│   └── __init__.py
├── tasks/
│   └── __init__.py
├── log/
└── decoded_frames/
```

---

### S3: Requirements File
**Status:** ⬜  
**Priority:** HIGH  
**Estimated Time:** 10 minutes

**Subtasks:**
- [ ] Create `requirements.txt`
- [ ] List all required packages
- [ ] Install all requirements
- [ ] Verify installation: `pip list`

**Deliverables:**
- `requirements.txt` file
- All packages installed in venv

---

## CORE INFRASTRUCTURE TASKS

### C1: Configuration Module
**Status:** ⬜  
**Priority:** HIGH  
**Estimated Time:** 1 hour  
**File:** `config.py`

**Subtasks:**
- [ ] Define project root path using `pathlib`
- [ ] Define all directory paths (log, frames, etc.)
- [ ] Define virtual environment path
- [ ] Set logging configuration constants
- [ ] Set default video parameters
- [ ] Add path validation functions
- [ ] Ensure file is under 150 lines

**Key Constants:**
```python
# Paths
PROJECT_ROOT: Path
LOG_DIR: Path
FRAMES_DIR: Path
VENV_DIR: Path

# Logging
LOG_MAX_BYTES: int = 16 * 1024 * 1024
LOG_BACKUP_COUNT: int = 19
LOG_FORMAT: str

# Video defaults
DEFAULT_FPS: int = 30
DEFAULT_WIDTH: int = 1280
DEFAULT_HEIGHT: int = 720
```

**Validation:**
- [ ] All paths are relative
- [ ] No hardcoded absolute paths
- [ ] Line count < 150

**Deliverables:**
- Complete `config.py` module
- All constants defined
- Imports work correctly

---

### C2: Logging Infrastructure
**Status:** ⬜  
**Priority:** HIGH  
**Estimated Time:** 1.5 hours  
**File:** `utils/logger.py`

**Subtasks:**
- [ ] Import `logging` and `RotatingFileHandler`
- [ ] Create logger setup function
- [ ] Configure RotatingFileHandler (16MB, 20 files)
- [ ] Set log format with timestamp, level, module, message
- [ ] Set log level to INFO
- [ ] Create convenience logging functions
- [ ] Test logger with sample messages
- [ ] Verify ring buffer behavior
- [ ] Ensure file is under 150 lines

**Implementation Details:**
```python
def setup_logger(name: str) -> logging.Logger:
    """
    Setup ring buffer logger.
    
    Args:
        name: Logger name (usually __name__)
    
    Returns:
        Configured logger instance
    """
    # Create logger
    # Add RotatingFileHandler
    # Set formatter
    # Return logger
```

**Testing:**
- [ ] Create 20+ MB of logs to verify rotation
- [ ] Check that oldest file is overwritten
- [ ] Verify log format is correct

**Deliverables:**
- Working ring buffer logger
- 20 log files in `log/` directory

---

### C3: FFmpeg Wrapper
**Status:** ⬜  
**Priority:** HIGH  
**Estimated Time:** 2 hours  
**File:** `utils/ffmpeg_wrapper.py`

**Subtasks:**
- [ ] Create FFmpeg availability check function
- [ ] Create FFprobe command execution function
- [ ] Create FFmpeg command execution function
- [ ] Implement JSON output parsing
- [ ] Implement error handling for subprocess calls
- [ ] Add logging for all FFmpeg operations
- [ ] Create frame extraction function
- [ ] Test with sample video
- [ ] Ensure file is under 150 lines

**Functions:**
```python
def check_ffmpeg_installed() -> bool
def run_ffprobe(video_path: Path, args: list) -> dict
def run_ffmpeg(input_path: Path, output_path: Path, args: list) -> bool
def parse_json_output(json_str: str) -> dict
def extract_frames(video_path: Path, output_dir: Path, filters: str) -> bool
```

**Error Handling:**
- [ ] FileNotFoundError for missing FFmpeg
- [ ] subprocess.CalledProcessError for FFmpeg errors
- [ ] JSON parsing errors
- [ ] Invalid video file errors

**Testing:**
- [ ] Test with valid video file
- [ ] Test with invalid file
- [ ] Test with missing FFmpeg
- [ ] Verify JSON parsing

**Deliverables:**
- Complete FFmpeg wrapper module
- All functions tested
- Error handling verified

---

## TASK 1: METADATA EXTRACTION

### T1.1: Basic Metadata Extraction
**Status:** ⬜  
**Priority:** HIGH  
**Estimated Time:** 1.5 hours  
**File:** `tasks/task1_metadata.py`

**Subtasks:**
- [ ] Create main metadata extraction function
- [ ] Execute FFprobe for format information
- [ ] Execute FFprobe for stream information
- [ ] Parse container format
- [ ] Parse duration (convert to readable format)
- [ ] Extract video stream details (codec, dimensions, fps)
- [ ] Extract audio stream details (codec, sample rate, channels)
- [ ] Calculate bitrates
- [ ] Identify resolution category (720p, 1080p, 4K, etc.)
- [ ] Handle videos without audio

**FFprobe Commands:**
```bash
# Format and streams
ffprobe -v error -print_format json -show_format -show_streams video.mp4
```

**Data to Extract:**
- Container format
- Duration (HH:MM:SS.mmm)
- Video codec name
- Width x Height
- Pixel format
- Frame rate
- Video bitrate
- Audio codec name
- Sample rate
- Number of channels
- Audio bitrate

**Deliverables:**
- Function returns structured dictionary
- All metadata fields populated

---

### T1.2: GOP Analysis
**Status:** ⬜  
**Priority:** HIGH  
**Estimated Time:** 1.5 hours  
**File:** `tasks/task1_metadata.py` (continued)

**Subtasks:**
- [ ] Execute FFprobe for frame-level data
- [ ] Parse frame types (I, P, B)
- [ ] Count each frame type
- [ ] Identify GOP boundaries (I-frames)
- [ ] Calculate GOP sizes
- [ ] Calculate average GOP size
- [ ] Compute frame type percentages
- [ ] Create frame timestamp list

**FFprobe Command:**
```bash
# Frame information
ffprobe -v error -select_streams v:0 -show_entries frame=pict_type,pts_time -of json video.mp4
```

**Calculations:**
- Total frame count
- I-frame count and percentage
- P-frame count and percentage
- B-frame count and percentage
- Number of GOPs (number of I-frames)
- Average frames per GOP
- Average GOP duration

**Challenge:**
Large videos may have thousands of frames. Consider:
- [ ] Processing in batches
- [ ] Progress indicator
- [ ] Memory-efficient parsing

**Deliverables:**
- GOP statistics dictionary
- Frame type distribution

---

### T1.3: Output Formatting
**Status:** ⬜  
**Priority:** MEDIUM  
**Estimated Time:** 1 hour  
**File:** `tasks/task1_metadata.py` (continued)

**Subtasks:**
- [ ] Create formatted output function
- [ ] Design readable text layout
- [ ] Format durations (seconds to HH:MM:SS)
- [ ] Format bitrates (bps to kbps/Mbps)
- [ ] Format file sizes (bytes to MB/GB)
- [ ] Create section headers
- [ ] Include frame listing (first 20 and last 20)
- [ ] Test with multiple video files

**Output Sections:**
1. File Information
2. Container Format
3. Video Stream Details
4. Audio Stream Details
5. GOP Analysis
6. Frame Type Distribution
7. Sample Frame Timestamps

**Deliverables:**
- Human-readable formatted output
- Console-friendly display

---

## TASK 2: MOTION VECTOR VISUALIZATION

### T2.1: Frame Extraction Setup
**Status:** ⬜  
**Priority:** HIGH  
**Estimated Time:** 1 hour  
**File:** `tasks/task2_motion_vectors.py`

**Subtasks:**
- [ ] Create output directory (`decoded_frames/`)
- [ ] Clear existing frames (if any)
- [ ] Build FFmpeg command with codecview filter
- [ ] Execute frame extraction
- [ ] Verify frames are created
- [ ] Count extracted frames
- [ ] Log extraction progress

**FFmpeg Command:**
```bash
ffmpeg -flags2 +export_mvs -i input.mp4 \
  -vf "codecview=mv=pf+bf+bb" \
  decoded_frames/frame_%04d.png
```

**Filter Parameters:**
- `pf`: P-frame forward motion vectors
- `bf`: B-frame forward motion vectors
- `bb`: B-frame backward motion vectors

**Error Handling:**
- [ ] Check if video codec supports motion vectors
- [ ] Handle FFmpeg errors
- [ ] Verify output directory is writable

**Deliverables:**
- All frames extracted with motion vector overlays
- Frames numbered sequentially

---

### T2.2: Multiprocessing Implementation
**Status:** ⬜  
**Priority:** MEDIUM  
**Estimated Time:** 2 hours  
**File:** `tasks/task2_motion_vectors.py` (continued)

**Subtasks:**
- [ ] Design multiprocessing strategy
- [ ] Create worker function for frame analysis
- [ ] Divide frames into batches
- [ ] Use `multiprocessing.Pool`
- [ ] Process batches in parallel
- [ ] Collect results
- [ ] Handle errors in worker processes
- [ ] Test with large video (1000+ frames)

**Multiprocessing Design:**
```python
from multiprocessing import Pool, cpu_count

def analyze_frame(frame_path: Path) -> dict:
    """Analyze single frame for motion patterns."""
    # Load frame
    # Analyze motion vectors
    # Return statistics

def process_frames_parallel(frame_paths: list) -> list:
    """Process frames in parallel."""
    with Pool(processes=cpu_count()) as pool:
        results = pool.map(analyze_frame, frame_paths)
    return results
```

**Considerations:**
- [ ] Batch size optimization
- [ ] Memory usage monitoring
- [ ] Progress reporting from workers

**Deliverables:**
- Parallel frame processing working
- Speedup compared to sequential processing

---

### T2.3: Motion Flow Analysis
**Status:** ⬜  
**Priority:** LOW  
**Estimated Time:** 1.5 hours  
**File:** `tasks/task2_motion_vectors.py` (continued)

**Subtasks:**
- [ ] Load extracted frames
- [ ] Detect motion vector patterns (optional)
- [ ] Classify motion types (pan, zoom, static)
- [ ] Calculate average vector magnitudes
- [ ] Identify dominant motion direction
- [ ] Generate analysis report
- [ ] Save report to file

**Analysis Metrics:**
- Average motion vector length
- Dominant motion direction (degrees)
- Motion complexity score
- Frame-by-frame motion intensity

**Note:** This is an optional enhancement. Focus on basic frame extraction first.

**Deliverables:**
- Motion analysis report (optional)
- Visual summary of motion patterns

---

## TASK 3: TEST VIDEO GENERATION

### T3.1: Frame Generation
**Status:** ⬜  
**Priority:** MEDIUM  
**Estimated Time:** 1.5 hours  
**File:** `tasks/task3_generate_video.py`

**Subtasks:**
- [ ] Import Pillow (PIL) for image creation
- [ ] Create blank frame generation function
- [ ] Implement diagonal movement calculation
- [ ] Draw black rectangle on each frame
- [ ] Save frames as PNG images
- [ ] Create temporary directory for frames
- [ ] Test with different resolutions

**Frame Generation Logic:**
```python
from PIL import Image, ImageDraw

def create_frame(width, height, obj_x, obj_y):
    """Create single frame with moving object."""
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    draw.rectangle([obj_x, obj_y, obj_x+20, obj_y+10], fill='black')
    return img

def calculate_diagonal_position(frame_num, total_frames, width, height):
    """Calculate position for diagonal movement."""
    progress = frame_num / (total_frames - 1)
    x = int(progress * (width - 20))
    y = int(progress * (height - 10))
    return x, y
```

**Parameters:**
- Frame size: 1280x720 (default)
- Object size: 20x10 pixels
- Background: White (255, 255, 255)
- Object: Black (0, 0, 0)
- Movement: Linear diagonal

**Deliverables:**
- Set of numbered frame images
- Smooth diagonal motion path

---

### T3.2: Video Encoding
**Status:** ⬜  
**Priority:** MEDIUM  
**Estimated Time:** 1 hour  
**File:** `tasks/task3_generate_video.py` (continued)

**Subtasks:**
- [ ] Create FFmpeg encoding command
- [ ] Specify H.264 codec
- [ ] Set frame rate (30 fps)
- [ ] Set pixel format (yuv420p)
- [ ] Execute encoding
- [ ] Verify output video
- [ ] Clean up temporary frames
- [ ] Test playback in media player

**FFmpeg Command:**
```bash
ffmpeg -framerate 30 -i temp_frames/frame_%04d.png \
  -c:v libx264 -pix_fmt yuv420p -crf 23 output.mp4
```

**Parameters:**
- Codec: libx264 (H.264)
- Frame rate: 30 fps
- Pixel format: yuv420p (widely compatible)
- CRF: 23 (constant quality)

**Deliverables:**
- Playable MP4 video file
- Smooth motion from corner to corner

---

### T3.3: Configuration Options
**Status:** ⬜  
**Priority:** LOW  
**Estimated Time:** 30 minutes  
**File:** `tasks/task3_generate_video.py` (continued)

**Subtasks:**
- [ ] Add command-line arguments for customization
- [ ] Support custom resolution
- [ ] Support custom duration
- [ ] Support custom frame rate
- [ ] Support custom object size
- [ ] Support custom object color
- [ ] Add defaults for all parameters

**Configuration Parameters:**
```python
class VideoConfig:
    width: int = 1280
    height: int = 720
    fps: int = 30
    duration: int = 10  # seconds
    obj_width: int = 20
    obj_height: int = 10
    obj_color: tuple = (0, 0, 0)  # Black
    bg_color: tuple = (255, 255, 255)  # White
```

**Deliverables:**
- Configurable video generation
- Reasonable defaults

---

## INTEGRATION TASKS

### I1: Main Program CLI
**Status:** ⬜  
**Priority:** HIGH  
**Estimated Time:** 2 hours  
**File:** `main.py`

**Subtasks:**
- [ ] Import all task modules
- [ ] Create argument parser
- [ ] Define command-line arguments
- [ ] Implement task routing logic
- [ ] Add --help documentation
- [ ] Add version information
- [ ] Implement --all flag (run all tasks)
- [ ] Add error handling
- [ ] Test all CLI combinations

**Arguments:**
- `--task {1,2,3}`: Run specific task
- `--input PATH`: Input video file
- `--output PATH`: Output file (Task 3)
- `--all`: Run all tasks sequentially
- `--duration N`: Duration for Task 3 (seconds)
- `--fps N`: Frame rate for Task 3
- `--help`: Show help message
- `--version`: Show version

**Usage Examples:**
```bash
# Task 1: Analyze video
python -m video_compression.main --task 1 --input sample.mp4

# Task 2: Extract frames with motion vectors
python -m video_compression.main --task 2 --input sample.mp4

# Task 3: Generate test video
python -m video_compression.main --task 3 --output test.mp4 --duration 10 --fps 30

# Run all tasks
python -m video_compression.main --all --input sample.mp4
```

**Deliverables:**
- Functional command-line interface
- Clear help messages
- All tasks accessible

---

### I2: Package Initialization
**Status:** ⬜  
**Priority:** MEDIUM  
**Estimated Time:** 30 minutes  
**File:** `__init__.py`

**Subtasks:**
- [ ] Define `__version__`
- [ ] Define `__author__`
- [ ] Import main modules
- [ ] Set up package-level exports
- [ ] Add package docstring

**Package Info:**
```python
"""
Video Compression Analysis Tool

A Python package for analyzing video compression,
visualizing motion vectors, and generating test videos.

Author: Yair Levi
Version: 1.0.0
"""

__version__ = '1.0.0'
__author__ = 'Yair Levi'
```

**Deliverables:**
- Package importable: `import video_compression`
- Version accessible: `video_compression.__version__`

---

## TESTING TASKS

### TEST1: Unit Testing
**Status:** ⬜  
**Priority:** MEDIUM  
**Estimated Time:** 2 hours

**Subtasks:**
- [ ] Test config module paths
- [ ] Test logger creation and rotation
- [ ] Test FFmpeg wrapper functions
- [ ] Test metadata extraction
- [ ] Test frame generation
- [ ] Test error handling
- [ ] Create test video files

**Test Files Needed:**
- Small test video (10 seconds, 480p)
- Large test video (2 minutes, 1080p)
- Video without audio
- Corrupt video file (for error testing)

**Deliverables:**
- All modules tested
- Test coverage report

---

### TEST2: Integration Testing
**Status:** ⬜  
**Priority:** HIGH  
**Estimated Time:** 1 hour

**Subtasks:**
- [ ] Test Task 1 end-to-end
- [ ] Test Task 2 end-to-end
- [ ] Test Task 3 end-to-end
- [ ] Test --all flag
- [ ] Test error cases
- [ ] Verify log files created
- [ ] Verify output files created

**Test Scenarios:**
1. Run Task 1 on sample video
2. Run Task 2 and check decoded_frames/
3. Run Task 3 and play generated video
4. Run all tasks together
5. Test with missing input file
6. Test with invalid video format

**Deliverables:**
- All integration tests pass
- No unhandled exceptions

---

## DOCUMENTATION TASKS

### DOC1: README Creation
**Status:** ⬜  
**Priority:** HIGH  
**Estimated Time:** 1 hour

**Sections:**
- [ ] Project overview
- [ ] Requirements and installation
- [ ] Usage instructions
- [ ] Examples for each task
- [ ] Troubleshooting
- [ ] License information

**Deliverables:**
- Complete README.md file
- Clear setup instructions

---

### DOC2: Code Documentation
**Status:** ⬜  
**Priority:** MEDIUM  
**Estimated Time:** 1 hour

**Subtasks:**
- [ ] Add docstrings to all functions
- [ ] Add docstrings to all classes
- [ ] Add module-level docstrings
- [ ] Add inline comments for complex logic
- [ ] Add type hints to function signatures

**Deliverables:**
- Well-documented codebase
- Clear function descriptions

---

## FINAL TASKS

### FINAL1: Code Review
**Status:** ⬜  
**Priority:** HIGH  
**Estimated Time:** 1 hour

**Checklist:**
- [ ] All files under 150 lines
- [ ] No absolute paths used
- [ ] All imports are relative
- [ ] Logging works correctly (INFO level)
- [ ] Ring buffer with 20 files, 16MB each
- [ ] Multiprocessing implemented where beneficial
- [ ] Error handling comprehensive
- [ ] Virtual environment at ../../venv/
- [ ] All paths relative to project root

**Deliverables:**
- Code meets all requirements
- No violations of constraints

---

### FINAL2: Project Cleanup
**Status:** ⬜  
**Priority:** MEDIUM  
**Estimated Time:** 30 minutes

**Subtasks:**
- [ ] Remove temporary files
- [ ] Clean up test outputs
- [ ] Organize sample videos
- [ ] Update .gitignore (if using git)
- [ ] Archive planning documents

**Deliverables:**
- Clean project directory
- Only necessary files remain

---

## Summary Statistics

**Total Tasks:** 32
**Estimated Total Time:** 25-30 hours
**Critical Path:** Setup → Core Infrastructure → Tasks 1-3 → Integration
**High Priority Tasks:** 15
**Medium Priority Tasks:** 12
**Low Priority Tasks:** 5

**Dependencies:**
- Tasks 1, 2, 3 depend on Core Infrastructure (C1, C2, C3)
- Integration (I1, I2) depends on all Tasks
- Testing depends on Integration
- Documentation can be done in parallel

---

**Next Steps:**
1. Start with S1-S3 (Setup)
2. Proceed to C1-C3 (Core Infrastructure)
3. Implement T1, T2, T3 in parallel (if resources allow)
4. Integration testing
5. Final review and documentation

---

**Tracking:**
Update this document as tasks are completed. Mark status with appropriate emoji.

**Last Updated:** February 1, 2026
