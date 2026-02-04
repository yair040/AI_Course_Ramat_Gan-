# Development Planning Document
# Video Compression Analysis Tool

**Author:** Yair Levi  
**Date:** February 1, 2026  
**Project:** Lesson 35 - Video Compression

---

## Project Overview

### Goal
Create a Python package for video compression analysis running on WSL with three main tasks:
1. Extract and display video metadata
2. Visualize motion vectors on extracted frames
3. Generate test video with moving object

### Timeline
- **Estimated Duration:** 2-3 days
- **Complexity:** Medium
- **Dependencies:** FFmpeg, FFprobe

---

## Phase 1: Project Setup (Day 1, Morning)

### 1.1 Environment Setup
- [ ] Create virtual environment at `../../venv/`
- [ ] Create project directory structure
- [ ] Initialize `__init__.py` files for packages
- [ ] Create placeholder files for all modules

**Commands:**
```bash
# Navigate to venv location
cd ../../
python3 -m venv venv
source venv/bin/activate

# Install pip tools
pip install --upgrade pip setuptools wheel

# Return to project directory
cd AI_continue/Lesson35_video_processing/Video_processing/
```

### 1.2 Directory Structure Creation
```bash
mkdir -p utils tasks log decoded_frames
touch __init__.py main.py config.py
touch utils/__init__.py utils/logger.py utils/ffmpeg_wrapper.py
touch tasks/__init__.py tasks/task1_metadata.py tasks/task2_motion_vectors.py tasks/task3_generate_video.py
```

### 1.3 Dependencies Installation
Create `requirements.txt` and install packages.

**Priority:** HIGH  
**Estimated Time:** 30 minutes

---

## Phase 2: Core Infrastructure (Day 1, Afternoon)

### 2.1 Configuration Module (`config.py`)
**Purpose:** Central configuration for paths, constants, logging settings

**Components:**
- Project root path (relative)
- Log directory path
- FFmpeg/FFprobe paths
- Logging configuration (ring buffer settings)
- Default video parameters

**Key Decisions:**
- Use `pathlib.Path` for all paths
- Store constants as module-level variables
- Include validation functions

**Estimated Time:** 1 hour

### 2.2 Logging Infrastructure (`utils/logger.py`)
**Purpose:** Ring buffer logging with rotation

**Components:**
- `RotatingFileHandler` setup
- Custom formatter
- Logger initialization function
- Log file naming scheme

**Technical Requirements:**
- 20 files maximum
- 16MB per file (16 * 1024 * 1024 bytes)
- When file 20 is full, overwrite file 1
- Format: `[timestamp] [level] [module] message`

**Implementation Notes:**
```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    filename='log/app.log',
    maxBytes=16 * 1024 * 1024,  # 16MB
    backupCount=19  # 20 total files (1 current + 19 backups)
)
```

**Estimated Time:** 1.5 hours

### 2.3 FFmpeg Wrapper (`utils/ffmpeg_wrapper.py`)
**Purpose:** Interface for FFmpeg/FFprobe operations

**Functions:**
- `check_ffmpeg_installed()` - Verify FFmpeg availability
- `run_ffprobe(video_path, args)` - Execute FFprobe commands
- `run_ffmpeg(input_path, output_path, args)` - Execute FFmpeg commands
- `parse_ffprobe_json(output)` - Parse JSON output
- `extract_frames(video_path, output_dir, filters)` - Extract frames with filters

**Error Handling:**
- Check return codes
- Capture stderr
- Provide meaningful error messages
- Log all commands executed

**Estimated Time:** 2 hours

**Priority:** HIGH (required for all tasks)

---

## Phase 3: Task 1 Implementation (Day 2, Morning)

### 3.1 Task 1: Metadata Extraction (`tasks/task1_metadata.py`)

**Components:**
1. **Metadata Extraction Function**
   - Use FFprobe to get format and stream info
   - Parse JSON output
   - Extract relevant fields

2. **GOP Analysis Function**
   - Use FFprobe to get frame-level data
   - Identify I/P/B frames
   - Count frames between I-frames
   - Calculate statistics

3. **Output Formatting Function**
   - Create human-readable report
   - Include all required parameters
   - Format durations, bitrates, resolutions

**FFprobe Commands:**
```bash
# Basic metadata
ffprobe -v error -print_format json -show_format -show_streams input.mp4

# Frame data (for GOP analysis)
ffprobe -v error -select_streams v:0 -show_entries frame=pict_type,pts_time -of json input.mp4
```

**Data Flow:**
```
video_file → FFprobe (metadata) → JSON → Parser → Formatted Output
         ↘ FFprobe (frames)   → JSON → GOP Analysis → Statistics
```

**Output Format Example:**
```
========================================
Video Metadata Analysis
========================================
File: sample_video.mp4
Container Format: MP4 (mov,mp4,m4a,3gp,3g2,mj2)
Duration: 00:01:23.456 (83.456 seconds)

Video Stream #0:
  Codec: H.264 (High Profile)
  Resolution: 1920x1080 (1080p)
  Pixel Format: yuv420p
  Frame Rate: 30.00 fps
  Bitrate: 5000 kbps

Audio Stream #1:
  Codec: AAC (LC)
  Sample Rate: 48000 Hz
  Channels: 2 (Stereo)
  Bitrate: 128 kbps

GOP Analysis:
  Total Frames: 2504
  I-Frames: 84 (3.4%)
  P-Frames: 1680 (67.1%)
  B-Frames: 740 (29.5%)
  Total GOPs: 84
  Average GOP Size: 29.8 frames
  GOP Duration: ~1.0 seconds

Frame Type Distribution:
  [Frame #] [Timestamp] [Type]
  0         0.000       I
  1         0.033       P
  2         0.067       B
  ...
```

**Estimated Time:** 3 hours

**Testing:**
- Small video (10 seconds)
- Large video (5 minutes)
- Different codecs (H.264, H.265)
- Video without audio

**Priority:** HIGH

---

## Phase 4: Task 2 Implementation (Day 2, Afternoon)

### 4.1 Task 2: Motion Vector Visualization (`tasks/task2_motion_vectors.py`)

**Components:**

1. **Frame Extraction with Motion Vectors**
   - Create output directory
   - Use FFmpeg with `codecview` filter
   - Extract all frames with motion vector overlay

2. **Multiprocessing Framework**
   - Divide frames into batches
   - Process batches in parallel
   - Merge results

3. **Motion Analysis** (Optional Enhancement)
   - Analyze vector patterns
   - Detect dominant motion direction
   - Calculate average motion speed

**FFmpeg Command:**
```bash
ffmpeg -flags2 +export_mvs -i input.mp4 \
  -vf "codecview=mv=pf+bf+bb" \
  decoded_frames/frame_%04d.png
```

**Filter Explanation:**
- `flags2 +export_mvs`: Enable motion vector export
- `codecview`: Video filter for visualization
- `mv=pf+bf+bb`: Show P-forward, B-forward, B-backward motion vectors

**Multiprocessing Strategy:**
Since FFmpeg extracts all frames in one command, multiprocessing can be used for:
- Post-processing analysis of extracted frames
- Parallel processing of frame batches for analysis
- Concurrent I/O operations

**Alternative Approach (for large videos):**
Extract frames in segments:
```python
# Segment 1: frames 0-1000
ffmpeg -i input.mp4 -vf "select=between(n\,0\,1000),codecview=mv=pf+bf+bb" out_%04d.png

# Process segments in parallel
```

**Motion Flow Detection:**
```python
def analyze_motion_flow(frame_path):
    """Analyze motion vectors in a single frame."""
    # Load frame
    # Detect vector patterns
    # Return motion statistics
    pass
```

**Output Structure:**
```
decoded_frames/
├── frame_0001.png  (with motion vectors)
├── frame_0002.png
├── frame_0003.png
└── ...
```

**Estimated Time:** 4 hours

**Challenges:**
- Large number of frames (memory management)
- Motion vector visibility (depends on video codec)
- Processing time for long videos

**Testing:**
- Short video with camera pan (horizontal motion)
- Video with fast action (large motion vectors)
- Static scene (minimal motion)

**Priority:** MEDIUM-HIGH

---

## Phase 5: Task 3 Implementation (Day 3, Morning)

### 5.1 Task 3: Test Video Generation (`tasks/task3_generate_video.py`)

**Components:**

1. **Frame Generation**
   - Create blank frames (black background)
   - Draw moving rectangle (20x10 pixels, black)
   - Calculate diagonal path (top-left to bottom-right)
   - Save frames as images

2. **Video Encoding**
   - Use FFmpeg to encode frames
   - Specify codec (H.264)
   - Set frame rate (30 fps default)

3. **Configuration**
   - Configurable duration, resolution, FPS
   - Configurable object size and color
   - Configurable path (diagonal, horizontal, etc.)

**Mathematics for Diagonal Movement:**
```python
def calculate_position(frame_num, total_frames, width, height, obj_width=20, obj_height=10):
    """Calculate object position for linear diagonal movement."""
    progress = frame_num / (total_frames - 1)  # 0.0 to 1.0
    x = int(progress * (width - obj_width))
    y = int(progress * (height - obj_height))
    return x, y
```

**Frame Drawing (using PIL):**
```python
from PIL import Image, ImageDraw

def create_frame(width, height, obj_x, obj_y, obj_width=20, obj_height=10):
    """Create a single frame with object at specified position."""
    # Create white background
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw black rectangle
    draw.rectangle(
        [obj_x, obj_y, obj_x + obj_width, obj_y + obj_height],
        fill='black'
    )
    
    return img
```

**Video Encoding:**
```bash
ffmpeg -framerate 30 -i frame_%04d.png -c:v libx264 -pix_fmt yuv420p output.mp4
```

**Default Parameters:**
- Resolution: 1280x720 (720p)
- Duration: 10 seconds
- Frame Rate: 30 fps
- Object Size: 20x10 pixels
- Background: White
- Object Color: Black

**Estimated Time:** 2.5 hours

**Testing:**
- Play generated video in media player
- Verify smooth motion
- Check object visibility
- Confirm diagonal path

**Priority:** MEDIUM

---

## Phase 6: Main Program Integration (Day 3, Afternoon)

### 6.1 Main Module (`main.py`)

**Components:**

1. **Command-Line Interface**
   - Argument parsing (task selection, input/output files)
   - Help text and usage examples
   - Validation of inputs

2. **Task Orchestration**
   - Route to appropriate task handler
   - Handle task dependencies
   - Provide progress feedback

3. **Error Handling**
   - Catch and log exceptions
   - Provide user-friendly error messages
   - Graceful degradation

**CLI Design:**
```bash
# Run specific task
python -m video_compression.main --task 1 --input video.mp4
python -m video_compression.main --task 2 --input video.mp4
python -m video_compression.main --task 3 --output test.mp4 --duration 10

# Run all tasks
python -m video_compression.main --all --input video.mp4

# Help
python -m video_compression.main --help
```

**Argument Parser:**
```python
import argparse

parser = argparse.ArgumentParser(description="Video Compression Analysis Tool")
parser.add_argument('--task', type=int, choices=[1, 2, 3], help='Task number')
parser.add_argument('--input', type=str, help='Input video file')
parser.add_argument('--output', type=str, help='Output file (Task 3)')
parser.add_argument('--all', action='store_true', help='Run all tasks')
```

**Estimated Time:** 2 hours

---

## Phase 7: Testing and Documentation (Day 3, Evening)

### 7.1 Integration Testing
- [ ] Test all tasks with sample videos
- [ ] Test error conditions
- [ ] Test on different video formats
- [ ] Verify logging works correctly
- [ ] Check file size limits (150 lines per file)

### 7.2 Documentation Updates
- [ ] Update README with usage instructions
- [ ] Add code comments
- [ ] Document any deviations from plan
- [ ] Create example outputs

### 7.3 Code Review Checklist
- [ ] All imports are relative
- [ ] No absolute paths used
- [ ] All files under 150 lines
- [ ] Logging at INFO level
- [ ] Error handling in place
- [ ] Type hints added
- [ ] Docstrings complete

**Estimated Time:** 2 hours

---

## Risk Management

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| FFmpeg not installed on WSL | Medium | High | Add clear setup instructions, check in code |
| Motion vectors not visible | Medium | Medium | Test with H.264 videos, document limitations |
| Large video memory issues | High | Medium | Implement batch processing, add memory checks |
| WSL path compatibility | Low | High | Use `pathlib`, test thoroughly |
| Ring buffer logging bugs | Medium | Low | Test with small file sizes first |

### Schedule Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Task 2 takes longer than expected | Medium | Medium | Start with simpler implementation, enhance later |
| GOP analysis complexity | Medium | Low | Focus on basic statistics first |
| Integration issues | Low | Medium | Test each task independently first |

---

## Success Metrics

### Functionality
- [ ] All three tasks execute without errors
- [ ] Metadata extraction is accurate
- [ ] Motion vectors are visible on frames
- [ ] Generated video plays correctly

### Code Quality
- [ ] All files under 150 lines
- [ ] Comprehensive logging
- [ ] No absolute paths
- [ ] Proper error handling

### Performance
- [ ] Task 1 completes in < 5 seconds for typical video
- [ ] Task 2 processes frames efficiently
- [ ] Task 3 generates video in < 10 seconds

### Documentation
- [ ] README clear and complete
- [ ] Code well-commented
- [ ] Usage examples provided

---

## Dependencies Tracking

### Python Packages (requirements.txt)
- Pillow (image processing for Task 3)
- opencv-python (alternative for image processing)
- numpy (if needed for calculations)

### External Tools
- FFmpeg (>= 4.0)
- FFprobe (included with FFmpeg)

### System Requirements
- Python 3.8+
- WSL (Ubuntu 20.04+ recommended)
- 500MB free disk space

---

## Notes and Decisions

### Design Decisions

1. **Path Handling:** Use `pathlib.Path` throughout for cross-platform compatibility
2. **Logging:** Standard Python `logging` with `RotatingFileHandler`
3. **FFmpeg Interface:** Subprocess calls with proper error handling
4. **Multiprocessing:** Use `multiprocessing.Pool` for parallel frame processing
5. **Configuration:** Centralized in `config.py` rather than command-line args

### Technical Choices

1. **Image Library:** Pillow (PIL) for simplicity in Task 3
2. **JSON Parsing:** Standard library `json` module
3. **CLI Framework:** Standard `argparse` (no external dependencies)
4. **Video Encoding:** H.264 via FFmpeg (widely compatible)

### Future Enhancements (Out of Scope)

- GUI interface
- Real-time video stream processing
- Batch processing of multiple videos
- Advanced compression metrics
- Comparison between different codecs

---

## Development Environment

### Required Setup
```bash
# Install FFmpeg on WSL (Ubuntu)
sudo apt update
sudo apt install ffmpeg

# Verify installation
ffmpeg -version
ffprobe -version

# Create and activate virtual environment
cd ../../
python3 -m venv venv
source venv/bin/activate

# Install dependencies
cd AI_continue/Lesson35_video_processing/Video_processing/
pip install -r requirements.txt
```

### Recommended Tools
- VSCode with Python extension
- WSL terminal
- Media player for testing (VLC, mpv)

---

## Appendix: File Size Monitoring

To ensure no file exceeds 150 lines:

```bash
# Count lines in all Python files
find . -name "*.py" -exec wc -l {} \; | sort -rn

# Check specific file
wc -l tasks/task1_metadata.py
```

**Action if file exceeds limit:**
- Split into multiple modules
- Move utility functions to `utils/`
- Create helper submodules

---

**Status:** Planning Complete  
**Ready for Development:** Yes  
**Next Step:** Phase 1 - Project Setup
