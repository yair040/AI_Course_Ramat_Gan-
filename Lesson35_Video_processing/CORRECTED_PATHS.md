# Corrected Paths Reference

## ✅ Correct Project Location

**Full Windows Path:**
```
C:\Users\yair0\AI_continue\Lesson35_video_processing\Video_processing\
```

**WSL Path:**
```
/mnt/c/Users/yair0/AI_continue/Lesson35_video_processing/Video_processing/
```

## 📁 Directory Structure

```
Lesson35_video_processing/
├── venv/                          # Virtual environment (at ../../venv from project)
└── Video_processing/              # Project root
    ├── video_compression/         # Python package
    │   ├── __init__.py
    │   ├── main.py
    │   ├── config.py
    │   ├── cli_handlers.py
    │   ├── utils/
    │   │   ├── __init__.py
    │   │   ├── logger.py
    │   │   ├── ffmpeg_wrapper.py
    │   │   ├── metadata_helpers.py
    │   │   └── video_generation_helpers.py
    │   └── tasks/
    │       ├── __init__.py
    │       ├── task1_metadata.py
    │       ├── task2_motion_vectors.py
    │       └── task3_generate_video.py
    ├── log/                       # Log files (created automatically)
    ├── decoded_frames/            # Extracted frames (created automatically)
    ├── test_videos/               # Put your test videos here (create manually)
    ├── requirements.txt
    ├── README.md
    ├── PRD.md
    ├── Claude.md
    ├── planning.md
    └── tasks.md
```

## 🚀 Setup Commands (Corrected)

### 1. Install FFmpeg
```bash
sudo apt update
sudo apt install ffmpeg
ffmpeg -version
ffprobe -version
```

### 2. Create Virtual Environment
```bash
# From Video_processing directory
cd ../../
python3 -m venv venv
source venv/bin/activate

# Return to project
cd AI_continue/Lesson35_video_processing/Video_processing/
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Verify Installation
```bash
python -m video_compression.main --version
```

## 🎬 Usage Examples

### Run All Tasks
```bash
# Make sure you're in Video_processing directory
cd /mnt/c/Users/yair0/AI_continue/Lesson35_video_processing/Video_processing/

# Activate virtual environment
source ../../venv/bin/activate

# Run all tasks
python -m video_compression.main --all --input test_videos/sample.mp4
```

### Individual Tasks
```bash
# Task 1: Analyze metadata
python -m video_compression.main --task 1 --input test_videos/sample.mp4

# Task 2: Extract motion vectors
python -m video_compression.main --task 2 --input test_videos/sample.mp4

# Task 3: Generate test video
python -m video_compression.main --task 3 --output my_test.mp4 --duration 15
```

## 📍 Where to Put Input Videos

**Recommended location:**
```
Video_processing/
├── test_videos/           # ← Create this folder
│   ├── sample1.mp4
│   ├── sample2.mp4
│   └── demo.mp4
└── video_compression/
```

**Command:**
```bash
python -m video_compression.main --all --input test_videos/sample1.mp4
```

## 📤 Output Locations

All outputs are created in the `Video_processing/` directory:

- **Log files:** `./log/video_compression.log` (+ 19 backup files)
- **Extracted frames:** `./decoded_frames/frame_*.png`
- **Generated test video:** `./test_video.mp4` (or custom path with --output)

## 🔧 Virtual Environment Path

The virtual environment is located at:
```
Lesson35_video_processing/venv/
```

Which is `../../venv/` relative to the project root at:
```
Lesson35_video_processing/Video_processing/
```

## ✅ All Documentation Updated

The following files have been corrected with the new path:
- ✅ PRD.md
- ✅ Claude.md
- ✅ planning.md
- ✅ README.md
- ✅ PACKAGE_SUMMARY.md
- ✅ CORRECTED_PATHS.md (this file)

## 📝 Quick Reference Card

```
Project Name: Video Compression Analysis Tool
Lesson: 35 - Video Processing
Author: Yair Levi
Location: C:\Users\yair0\AI_continue\Lesson35_video_processing\Video_processing\
Virtual Env: ../../venv/ (relative to project root)
Python Files: 13 files, all ≤ 150 lines
Package Name: video_compression
```

---

**Note:** All relative paths in the Python code are already correct and don't need modification. Only the documentation paths have been updated.
