# Claude AI Assistant Guide
# Video Compression Analysis Tool

**Project:** Video Compression Analysis Tool  
**Author:** Yair Levi  
**Date:** February 1, 2026

---

## Purpose of This Document

This document serves as a guide for Claude AI (or other AI assistants) when working on this project. It contains context, conventions, and specific instructions to maintain consistency and quality throughout development.

---

## Project Context

### Educational Purpose
This project is designed for **Lesson 35: Video Compression** and aims to teach:
- Video container formats and codecs
- GOP (Group of Pictures) structure in video compression
- Motion vectors and macro blocks
- How video compression algorithms work
- Practical use of FFmpeg for video analysis

### Technical Context
- **Environment:** WSL (Windows Subsystem for Linux)
- **Python Version:** 3.8+
- **Key Dependency:** FFmpeg/FFprobe
- **Design Philosophy:** Educational clarity over optimization

---

## Code Conventions

### File Organization
1. **Maximum 150 lines per file** - Strictly enforced
   - If a module exceeds this, split into multiple files
   - Use helper functions in separate utility modules
   
2. **Package structure:**
   ```
   video_compression/
   ├── __init__.py          # Package initialization
   ├── main.py              # Entry point (CLI)
   ├── config.py            # Configuration constants
   ├── utils/               # Utility modules
   └── tasks/               # Task implementations
   ```

3. **Import order:**
   - Standard library imports
   - Third-party imports
   - Local application imports
   - Blank line between each group

### Path Handling
**CRITICAL:** Always use relative paths, never absolute paths.

```python
# ✅ CORRECT
from pathlib import Path
project_root = Path(__file__).parent
log_dir = project_root / "log"
venv_path = project_root / ".." / ".." / "venv"

# ❌ INCORRECT
log_dir = "C:\\Users\\yair0\\AI_continue\\..."
```

### Virtual Environment Location
The virtual environment is at `../../venv/` relative to the project root.

**Activation command:**
```bash
source ../../venv/bin/activate
```

### Logging Requirements
Implement a **ring buffer logger** with these exact specifications:
- **Number of files:** 20
- **File size:** 16MB each
- **Behavior:** When file 20 is full, overwrite file 1
- **Location:** `./log/` subdirectory
- **Level:** INFO and above
- **Format:** `[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s`

**Important:** Use `RotatingFileHandler` with proper configuration.

### Multiprocessing Guidelines
Use multiprocessing for:
- Frame extraction (Task 2) - process frames in parallel
- Motion vector analysis - analyze multiple frames simultaneously
- Any CPU-intensive operations on independent data

**Template:**
```python
from multiprocessing import Pool, cpu_count

def process_frame(frame_data):
    # Process individual frame
    pass

with Pool(processes=cpu_count()) as pool:
    results = pool.map(process_frame, frame_list)
```

---

## FFmpeg Integration

### Command Construction
Always build FFmpeg commands programmatically:

```python
def build_ffprobe_command(video_path):
    """Build FFprobe command for metadata extraction."""
    return [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration,bit_rate:stream=codec_name,width,height",
        "-of", "json",
        str(video_path)
    ]
```

### Error Handling
Always check if FFmpeg/FFprobe is installed:

```python
import shutil

def check_ffmpeg():
    """Verify FFmpeg is available."""
    if not shutil.which("ffmpeg"):
        raise EnvironmentError("FFmpeg not found in PATH")
    if not shutil.which("ffprobe"):
        raise EnvironmentError("FFprobe not found in PATH")
```

### Motion Vector Extraction (Task 2)
Use this FFmpeg filter for motion vectors:

```bash
ffmpeg -flags2 +export_mvs -i input.mp4 \
  -vf "codecview=mv=pf+bf+bb" \
  decoded_frames/frame_%04d.png
```

Explanation:
- `flags2 +export_mvs`: Export motion vectors
- `codecview=mv=pf+bf+bb`: Draw motion vectors (P-forward, B-forward, B-backward)

---

## Task-Specific Guidance

### Task 1: Metadata Extraction
**Key Challenges:**
1. Parsing FFprobe JSON output
2. Calculating GOP statistics
3. Identifying frame types (I/P/B)

**FFprobe Commands Needed:**
```bash
# General metadata
ffprobe -v error -show_format -show_streams -of json input.mp4

# Frame-level data
ffprobe -v error -show_frames -of json input.mp4
```

**GOP Analysis:**
- GOP starts at each I-frame
- Count frames between I-frames
- Calculate I/P/B frame distribution

### Task 2: Motion Vector Visualization
**Key Challenges:**
1. Large number of frames (memory management)
2. FFmpeg filter syntax
3. Interpreting motion vector overlays

**Approach:**
1. Create `decoded_frames/` directory
2. Use `codecview` filter for motion vectors
3. Process in batches if video is large (>1000 frames)
4. Analyze vector patterns (optional: detect dominant motion direction)

**Motion Flow Analysis:**
- Long vectors = fast motion
- Vector direction = motion direction
- Clustered vectors = coherent motion
- Scattered vectors = complex motion

### Task 3: Generate Test Video
**Key Challenges:**
1. Drawing moving object frame-by-frame
2. Encoding frames into video
3. Calculating diagonal movement

**Approach:**
```python
# Calculate position for diagonal movement
def calculate_position(frame_num, total_frames, width, height):
    progress = frame_num / total_frames
    x = int(progress * (width - 20))
    y = int(progress * (height - 10))
    return x, y
```

**Video Generation:**
- Use PIL/OpenCV to draw frames
- Save frames as PNG
- Use FFmpeg to encode: `ffmpeg -framerate 30 -i frame_%04d.png output.mp4`

---

## Common Pitfalls and Solutions

### 1. Path Issues on WSL
**Problem:** Windows paths (C:\...) don't work in WSL  
**Solution:** Use WSL paths (/mnt/c/...) or let Python handle it with `pathlib`

### 2. FFmpeg Output Parsing
**Problem:** FFmpeg writes to stderr, not stdout  
**Solution:** Capture stderr or use `-v error` flag

### 3. Large Video Memory
**Problem:** Loading entire video into memory  
**Solution:** Process frame-by-frame or in batches

### 4. Motion Vectors Not Visible
**Problem:** Codec doesn't preserve motion vectors  
**Solution:** Use H.264 video, avoid re-encoding when possible

---

## Testing Strategy

### Manual Testing
1. **Small test video** (10 seconds, 720p)
2. **Large video** (5 minutes, 1080p)
3. **Different codecs** (H.264, H.265, VP9)
4. **Edge cases:**
   - Video without audio
   - Very short video (<1 second)
   - Corrupt file

### Expected Outputs
- **Task 1:** JSON or formatted text with all metadata
- **Task 2:** Folder with numbered frames showing motion vectors
- **Task 3:** Playable MP4 video with moving rectangle

---

## Code Quality Standards

### Documentation
- Every function has a docstring
- Complex logic has inline comments
- README explains how to run each task

### Type Hints
Use type hints for function signatures:
```python
def extract_metadata(video_path: Path) -> dict:
    """Extract video metadata using FFprobe."""
    pass
```

### Error Messages
Make errors informative:
```python
# ✅ GOOD
raise FileNotFoundError(f"Video file not found: {video_path}")

# ❌ BAD
raise Exception("Error")
```

---

## Development Workflow

### Step 1: Setup
1. Create virtual environment at `../../venv/`
2. Install dependencies from `requirements.txt`
3. Verify FFmpeg is installed

### Step 2: Implementation Order
1. `config.py` - Configuration constants
2. `utils/logger.py` - Logging setup
3. `utils/ffmpeg_wrapper.py` - FFmpeg interface
4. `tasks/task1_metadata.py` - Metadata extraction
5. `tasks/task2_motion_vectors.py` - Frame extraction
6. `tasks/task3_generate_video.py` - Video generation
7. `main.py` - CLI interface

### Step 3: Testing
Test each task independently before integration.

---

## Performance Considerations

### Multiprocessing Benefits
- **Task 2:** Parallel frame processing (4x speedup on 4-core CPU)
- **Task 1:** Parallel GOP analysis for very long videos

### Memory Management
- Process frames in batches of 100-500
- Use generators for large datasets
- Clear frame buffers after processing

---

## Debugging Tips

### FFmpeg Debugging
Add `-v debug` to see detailed FFmpeg output:
```bash
ffmpeg -v debug -i input.mp4 ...
```

### Logging for Debugging
Temporarily increase log level:
```python
logging.getLogger().setLevel(logging.DEBUG)
```

### Common Issues
1. **"FFmpeg not found"** → Check PATH in WSL
2. **"Permission denied"** → Check file permissions
3. **"No motion vectors"** → Video codec may not support it

---

## Future Enhancements Ideas

When extending this project, consider:
- Web interface using Flask
- Real-time video stream analysis
- Comparison tool for compression efficiency
- Machine learning for motion prediction
- GPU acceleration for frame processing

---

## Questions to Ask During Development

1. Is this path relative or absolute?
2. Will this work on WSL?
3. Is this file under 150 lines?
4. Are errors handled gracefully?
5. Is logging at appropriate level?
6. Can this benefit from multiprocessing?
7. Is the code educational and clear?

---

## Contact and Support

**Project Author:** Yair Levi  
**Purpose:** Lesson 35 - Video Compression  
**Repository:** Local WSL directory at `C:\Users\yair0\AI_continue\Lesson35_video_processing\Video_processing\`

For questions about video compression concepts, refer to:
- FFmpeg documentation: https://ffmpeg.org/documentation.html
- H.264 specification for GOP structure
- Video compression textbooks

---

**Last Updated:** February 1, 2026  
**Version:** 1.0
