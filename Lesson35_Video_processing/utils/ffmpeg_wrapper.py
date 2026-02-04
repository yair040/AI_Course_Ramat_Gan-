"""
FFmpeg and FFprobe wrapper utilities.
Author: Yair Levi
"""

import json
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any

from .logger import get_logger
from ..config import (
    FFMPEG_BINARY,
    FFPROBE_BINARY,
    FFMPEG_QUIET_ARGS,
    FFMPEG_OVERWRITE_ARGS,
    MOTION_VECTOR_FILTER,
    FRAME_FILENAME_PATTERN,
    FRAMES_DIR
)

logger = get_logger()


def check_ffmpeg_installed() -> bool:
    """Check if FFmpeg and FFprobe are installed."""
    ffmpeg_path = shutil.which(FFMPEG_BINARY)
    ffprobe_path = shutil.which(FFPROBE_BINARY)
    
    if not ffmpeg_path:
        logger.error(f"{FFMPEG_BINARY} not found in PATH")
        raise EnvironmentError(f"{FFMPEG_BINARY} not found. Please install FFmpeg.")
    
    if not ffprobe_path:
        logger.error(f"{FFPROBE_BINARY} not found in PATH")
        raise EnvironmentError(f"{FFPROBE_BINARY} not found. Please install FFmpeg (includes FFprobe).")
    
    logger.info(f"FFmpeg found at: {ffmpeg_path}")
    logger.info(f"FFprobe found at: {ffprobe_path}")
    
    return True


def run_ffprobe(video_path: Path, args: List[str]) -> Dict[str, Any]:
    """Execute FFprobe command and return parsed JSON output."""
    cmd = [FFPROBE_BINARY] + args + [str(video_path)]
    
    logger.debug(f"Running FFprobe: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        return json.loads(output)
    
    except subprocess.CalledProcessError as e:
        logger.error(f"FFprobe failed: {e.stderr}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse FFprobe JSON output: {e}")
        raise


def run_ffmpeg(args: List[str]) -> bool:
    """Execute FFmpeg command."""
    cmd = [FFMPEG_BINARY] + args
    
    logger.debug(f"Running FFmpeg: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        if result.stderr:
            logger.debug(f"FFmpeg stderr: {result.stderr}")
        
        return True
    
    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg failed: {e.stderr}")
        raise


def get_video_metadata(video_path: Path) -> Dict[str, Any]:
    """Extract comprehensive video metadata using FFprobe."""
    args = ["-v", "error", "-print_format", "json", "-show_format", "-show_streams"]
    
    logger.info(f"Extracting metadata from: {video_path}")
    metadata = run_ffprobe(video_path, args)
    logger.info("Metadata extraction complete")
    
    return metadata


def get_frame_data(video_path: Path) -> Dict[str, Any]:
    """Extract frame-level data for GOP analysis."""
    args = [
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "frame=pict_type,pts_time",
        "-of", "json"
    ]
    
    logger.info(f"Extracting frame data from: {video_path}")
    frame_data = run_ffprobe(video_path, args)
    logger.info(f"Extracted data for {len(frame_data.get('frames', []))} frames")
    
    return frame_data


def extract_frames_with_motion_vectors(
    video_path: Path,
    output_dir: Optional[Path] = None
) -> int:
    """Extract video frames with motion vector visualization."""
    if output_dir is None:
        output_dir = FRAMES_DIR
    
    output_dir.mkdir(exist_ok=True)
    
    # Clear existing frames
    for frame_file in output_dir.glob("*.png"):
        frame_file.unlink()
    
    output_pattern = str(output_dir / FRAME_FILENAME_PATTERN)
    
    args = [
        "-flags2", "+export_mvs",
        "-i", str(video_path)
    ] + FFMPEG_OVERWRITE_ARGS + [
        "-vf", MOTION_VECTOR_FILTER,
        output_pattern
    ]
    
    logger.info(f"Extracting frames to: {output_dir}")
    run_ffmpeg(args)
    
    # Count extracted frames
    frame_count = len(list(output_dir.glob("*.png")))
    logger.info(f"Extracted {frame_count} frames")
    
    return frame_count
