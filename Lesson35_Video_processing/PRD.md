# Product Requirements Document (PRD)
# Video Compression Analysis Tool

**Author:** Yair Levi  
**Date:** February 1, 2026  
**Version:** 1.0

---

## 1. Overview

### 1.1 Purpose
The Video Compression Analysis Tool is a Python-based command-line application designed to analyze video files, extract compression metadata, visualize motion vectors, and generate test videos with moving objects. This tool is intended for educational purposes in understanding video compression techniques, GOP structures, and motion estimation.

### 1.2 Target Environment
- **Platform:** WSL (Windows Subsystem for Linux)
- **Python Version:** 3.8+
- **Virtual Environment:** Located at `../../venv/` relative to project root
- **Working Directory:** `C:\Users\yair0\AI_continue\Lesson35_video_processing\Video_processing\`

### 1.3 Key Technologies
- **FFmpeg:** Video processing and frame extraction
- **FFprobe:** Metadata extraction
- **Python Multiprocessing:** Parallel processing where applicable
- **Logging:** Ring buffer with 20 files, 16MB each

---

## 2. Functional Requirements

### 2.1 Task 1: Video Metadata Analysis
**Description:** Extract and display comprehensive video file metadata in a human-readable format.

**Input:** Path to video file

**Output Parameters:**
- Container format (e.g., MP4, AVI, MKV)
- Duration (hours:minutes:seconds.milliseconds)
- Video and audio stream information
- Video dimensions (width × height)
- Resolution classification (e.g., 720p, 1080p, 4K)
- Pixel format (e.g., yuv420p, rgb24)
- Bitrate (video and overall)
- Audio codec, sample rate, channels, bitrate
- GOP (Group of Pictures) composition:
  - I-Frame count and percentage
  - P-Frame count and percentage
  - B-Frame count and percentage
- Total number of GOPs
- Frame timestamps with frame types (I/P/B)

**Acceptance Criteria:**
- All metadata displayed in clear, formatted output
- Error handling for corrupt or unsupported files
- Output includes both raw values and user-friendly descriptions

### 2.2 Task 2: Motion Vector Visualization
**Description:** Extract individual frames from video and visualize motion vectors with macro blocks.

**Input:** Path to video file

**Output:**
- Decoded frames saved to `./decoded_frames/` directory
- Each frame annotated with:
  - Macro blocks (rectangular divisions)
  - Motion vectors (directional arrows)
  - Vector length indicating movement speed
- Analysis summary indicating detected motion flow patterns

**Acceptance Criteria:**
- All frames extracted successfully
- Motion vectors clearly visible on frames
- Automatic detection and reporting of motion patterns
- Frame numbering sequential and consistent

### 2.3 Task 3: Test Video Generation
**Description:** Create a test video with a moving black rectangle to demonstrate motion compression.

**Input:** Video parameters (optional: duration, FPS, resolution)

**Output:** 
- Generated video file with moving object
- Black rectangle: 20×10 pixels
- Movement: Top-left corner to bottom-right corner
- Linear diagonal motion path

**Acceptance Criteria:**
- Video playable in standard players
- Smooth motion without artifacts
- Object clearly visible throughout video
- Configurable parameters (duration, FPS)

---

## 3. Non-Functional Requirements

### 3.1 Code Structure
- **Package Structure:** Organized as Python package with `__init__.py`
- **File Length:** Maximum 150 lines per Python file
- **Path Handling:** All paths relative, no absolute paths
- **Modularity:** Each task in separate module

### 3.2 Performance
- **Multiprocessing:** Utilize multiprocessing for frame extraction and processing
- **Memory Management:** Efficient handling of large video files
- **Progress Indicators:** Real-time feedback during long operations

### 3.3 Logging
- **Log Level:** INFO and above
- **Format:** Ring buffer implementation
- **Configuration:**
  - 20 log files maximum
  - 16MB per file
  - Oldest file overwritten when buffer full
- **Location:** `./log/` subdirectory
- **Content:** Timestamps, log levels, module names, messages

### 3.4 Error Handling
- Graceful handling of missing FFmpeg/FFprobe
- Clear error messages for invalid input files
- Recovery from partial failures
- Validation of user inputs

### 3.5 Dependencies
- FFmpeg (external binary, must be in PATH)
- FFprobe (external binary, must be in PATH)
- Python packages (see requirements.txt)

---

## 4. System Architecture

### 4.1 Directory Structure
```
Video_processing/
├── __init__.py
├── main.py
├── config.py
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   └── ffmpeg_wrapper.py
├── tasks/
│   ├── __init__.py
│   ├── task1_metadata.py
│   ├── task2_motion_vectors.py
│   └── task3_generate_video.py
├── log/
│   └── (ring buffer log files)
├── decoded_frames/
│   └── (extracted frames)
├── requirements.txt
├── Claude.md
├── planning.md
└── tasks.md
```

### 4.2 Module Responsibilities

**main.py**
- Entry point for application
- Command-line argument parsing
- Task orchestration
- High-level error handling

**config.py**
- Configuration constants
- Path definitions
- Logging configuration
- FFmpeg/FFprobe settings

**utils/logger.py**
- Ring buffer logging implementation
- Log rotation logic
- Formatter configuration

**utils/ffmpeg_wrapper.py**
- FFmpeg/FFprobe command execution
- Output parsing utilities
- Error handling for external processes

**tasks/task1_metadata.py**
- Metadata extraction logic
- GOP analysis
- Frame type detection
- Formatted output generation

**tasks/task2_motion_vectors.py**
- Frame extraction
- Motion vector overlay
- Motion pattern analysis
- Multiprocessing for frame processing

**tasks/task3_generate_video.py**
- Test video generation
- Moving object rendering
- Video encoding

---

## 5. User Interface

### 5.1 Command-Line Interface
```bash
# Activate virtual environment
source ../../venv/bin/activate

# Run specific task
python -m video_compression.main --task 1 --input video.mp4
python -m video_compression.main --task 2 --input video.mp4
python -m video_compression.main --task 3 --output test_video.mp4

# Run all tasks
python -m video_compression.main --all --input video.mp4
```

### 5.2 Output Examples

**Task 1 Output:**
```
Video Metadata Analysis
========================
Container Format: MP4 (H.264/AAC)
Duration: 00:01:23.456
Video Stream: H.264, 1920x1080 (1080p), 30 fps
Audio Stream: AAC, 48000 Hz, Stereo, 128 kbps
Bitrate: 5000 kbps
Pixel Format: yuv420p

GOP Structure:
- I-Frames: 25 (8.3%)
- P-Frames: 200 (66.7%)
- B-Frames: 75 (25.0%)
- Total GOPs: 25
- Average GOP Size: 12 frames
```

---

## 6. Testing Requirements

### 6.1 Test Cases
1. Valid video file processing
2. Multiple video formats (MP4, AVI, MKV)
3. Corrupt file handling
4. Missing FFmpeg/FFprobe detection
5. Large file processing (> 1GB)
6. High-resolution video (4K)
7. Videos without audio
8. Short videos (< 1 second)

### 6.2 Performance Benchmarks
- Task 1: Complete within 5 seconds for typical video
- Task 2: Process 1000 frames within 2 minutes
- Task 3: Generate 30-second video within 10 seconds

---

## 7. Future Enhancements
- GUI interface for non-technical users
- Batch processing of multiple videos
- Advanced GOP pattern analysis
- Compression efficiency metrics
- Side-by-side comparison of videos
- Export results to CSV/JSON
- Real-time video stream analysis

---

## 8. Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| FFmpeg not installed | High | Check and provide installation instructions |
| Large video memory issues | Medium | Process frames in batches |
| WSL path compatibility | Medium | Test thoroughly, use posixpath |
| Log file disk space | Low | Monitor and document requirements |

---

## 9. Success Criteria
- All three tasks execute successfully
- Clear, accurate output for all metadata
- Motion vectors visible and interpretable
- Generated video plays correctly
- No crashes or unhandled exceptions
- Comprehensive logging
- Clean, maintainable code structure

---

## 10. Dependencies and Prerequisites

### 10.1 System Requirements
- WSL installed and configured
- Python 3.8 or higher
- FFmpeg 4.0 or higher
- FFprobe (included with FFmpeg)
- At least 500MB free disk space

### 10.2 Python Packages
See `requirements.txt` for complete list.

---

**Document Control:**
- Review Date: February 1, 2026
- Next Review: March 1, 2026
- Status: Approved for Development
