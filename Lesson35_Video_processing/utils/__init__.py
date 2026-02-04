"""
Utility modules for Video Processing Analysis Tool.

This package contains helper modules for logging and FFmpeg operations.

Author: Yair Levi
"""

from .logger import setup_logger, get_logger
from .ffmpeg_wrapper import (
    check_ffmpeg_installed,
    run_ffprobe,
    run_ffmpeg,
    extract_frames_with_motion_vectors,
    get_video_metadata,
    get_frame_data
)

__all__ = [
    'setup_logger',
    'get_logger',
    'check_ffmpeg_installed',
    'run_ffprobe',
    'run_ffmpeg',
    'extract_frames_with_motion_vectors',
    'get_video_metadata',
    'get_frame_data'
]
