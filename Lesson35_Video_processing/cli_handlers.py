"""
CLI task handlers for the video processing analysis tool.

This module contains functions that run each task from the command line.

Author: Yair Levi
"""

from pathlib import Path

from .utils.logger import get_logger
from .tasks import (
    analyze_video_metadata,
    extract_and_analyze_motion_vectors,
    generate_test_video
)

logger = get_logger()


def run_task_1(input_path: Path) -> bool:
    """
    Run Task 1: Metadata Analysis.
    
    Args:
        input_path: Path to input video
    
    Returns:
        bool: True if successful
    """
    logger.info("=" * 70)
    logger.info("TASK 1: VIDEO METADATA ANALYSIS")
    logger.info("=" * 70)
    
    try:
        analyze_video_metadata(input_path)
        return True
    except Exception as e:
        logger.error(f"Task 1 failed: {e}", exc_info=True)
        return False


def run_task_2(input_path: Path) -> bool:
    """
    Run Task 2: Motion Vector Visualization.
    
    Args:
        input_path: Path to input video
    
    Returns:
        bool: True if successful
    """
    logger.info("=" * 70)
    logger.info("TASK 2: MOTION VECTOR VISUALIZATION")
    logger.info("=" * 70)
    
    try:
        extract_and_analyze_motion_vectors(input_path)
        return True
    except Exception as e:
        logger.error(f"Task 2 failed: {e}", exc_info=True)
        return False


def run_task_3(input_path: Path, output_path: Path, width: int, height: int, fps: int, duration: int) -> bool:
    """
    Run Task 3: Overlay moving object on input video frames.
    
    Args:
        input_path: Path to source video (frames extracted from this)
        output_path: Path for output video (None = auto-generated name)
        width: Not used (taken from source video)
        height: Not used (taken from source video)
        fps: Not used (taken from source video)
        duration: Not used (taken from source video)
    
    Returns:
        bool: True if successful
    """
    logger.info("=" * 70)
    logger.info("TASK 3: OVERLAY MOVING OBJECT ON VIDEO")
    logger.info("=" * 70)
    
    try:
        generate_test_video(input_path, output_path)
        return True
    except Exception as e:
        logger.error(f"Task 3 failed: {e}", exc_info=True)
        return False
