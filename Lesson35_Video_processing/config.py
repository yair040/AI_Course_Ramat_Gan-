"""
Configuration module for Video Processing Analysis Tool.

This module contains all configuration constants, paths, and settings
used throughout the application.

Author: Yair Levi
"""

from pathlib import Path
import os

# ============================================================================
# PATH CONFIGURATION
# ============================================================================

# Project root: Video_processing/ (parent of this package folder)
# __file__        = Video_processing/config.py
# .parent         = Video_processing/                     (PROJECT_ROOT)

PROJECT_ROOT = Path(__file__).parent.resolve()

VENV_DIR = PROJECT_ROOT.parent / "venv"   # ../../venv relative to project root
LOG_DIR = PROJECT_ROOT / "log"
FRAMES_DIR = PROJECT_ROOT / "decoded_frames"

LOG_DIR.mkdir(exist_ok=True)
FRAMES_DIR.mkdir(exist_ok=True)

# Logging — ring buffer: 20 files × 16 MB
LOG_MAX_BYTES = 16 * 1024 * 1024
LOG_BACKUP_COUNT = 19  # 1 current + 19 backups = 20 total
LOG_FILENAME = LOG_DIR / "video_processing.log"
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_LEVEL = "INFO"

# Default video parameters (Task 3)
DEFAULT_VIDEO_WIDTH = 1280
DEFAULT_VIDEO_HEIGHT = 720
DEFAULT_VIDEO_FPS = 30
DEFAULT_VIDEO_DURATION = 10  # seconds

# Moving object parameters
DEFAULT_OBJECT_WIDTH = 20
DEFAULT_OBJECT_HEIGHT = 10
DEFAULT_OBJECT_COLOR = (0, 0, 0)        # Black
DEFAULT_BACKGROUND_COLOR = (255, 255, 255)  # White

# FFmpeg
FFMPEG_BINARY = "ffmpeg"
FFPROBE_BINARY = "ffprobe"
FFMPEG_QUIET_ARGS = ["-v", "error"]
FFMPEG_OVERWRITE_ARGS = ["-y"]
MOTION_VECTOR_FILTER = "codecview=mv=pf+bf+bb"
FRAME_FILENAME_PATTERN = "frame_%04d.png"

# Multiprocessing
USE_MULTIPROCESSING = True
MAX_WORKERS = os.cpu_count() or 4
FRAME_BATCH_SIZE = 100

# Resolution name lookup
RESOLUTION_NAMES = {
    (7680, 4320): "8K UHD",
    (3840, 2160): "4K UHD",
    (2560, 1440): "1440p (2K)",
    (1920, 1080): "1080p (Full HD)",
    (1280, 720): "720p (HD)",
    (854, 480): "480p (SD)",
    (640, 360): "360p",
}


def validate_paths() -> bool:
    """Return True if PROJECT_ROOT, LOG_DIR, FRAMES_DIR all exist."""
    return all(d.exists() and d.is_dir() for d in [PROJECT_ROOT, LOG_DIR, FRAMES_DIR])


def get_resolution_name(width: int, height: int) -> str:
    """Return human-readable resolution string for given dimensions."""
    if (width, height) in RESOLUTION_NAMES:
        return RESOLUTION_NAMES[(width, height)]
    if height >= 2160:
        return "4K+"
    elif height >= 1440:
        return "2K+"
    elif height >= 1080:
        return "1080p"
    elif height >= 720:
        return "720p"
    elif height >= 480:
        return "480p"
    return f"{height}p"
