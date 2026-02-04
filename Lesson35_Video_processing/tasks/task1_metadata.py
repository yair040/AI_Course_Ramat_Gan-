"""
Task 1: Video Metadata Extraction and Analysis.

This module extracts and displays comprehensive video metadata including
container format, streams, GOP structure, and frame information.

Author: Yair Levi
"""

from pathlib import Path
from typing import Dict, List

from ..utils.logger import get_logger
from ..utils.ffmpeg_wrapper import (
    check_ffmpeg_installed,
    get_video_metadata,
    get_frame_data
)
from ..utils.metadata_helpers import print_metadata_report

logger = get_logger()


def analyze_gop_structure(frames: List[Dict]) -> Dict:
    """
    Analyze GOP (Group of Pictures) structure from frame data.
    
    Args:
        frames: List of frame dictionaries with 'pict_type' field
    
    Returns:
        dict: GOP statistics including frame counts and percentages
    """
    i_frames = [f for f in frames if f.get('pict_type') == 'I']
    p_frames = [f for f in frames if f.get('pict_type') == 'P']
    b_frames = [f for f in frames if f.get('pict_type') == 'B']
    
    total_frames = len(frames)
    gop_count = len(i_frames)
    
    if gop_count == 0:
        avg_gop_size = 0
    else:
        avg_gop_size = total_frames / gop_count
    
    return {
        'total_frames': total_frames,
        'i_frames': len(i_frames),
        'p_frames': len(p_frames),
        'b_frames': len(b_frames),
        'i_percentage': (len(i_frames) / total_frames * 100) if total_frames > 0 else 0,
        'p_percentage': (len(p_frames) / total_frames * 100) if total_frames > 0 else 0,
        'b_percentage': (len(b_frames) / total_frames * 100) if total_frames > 0 else 0,
        'gop_count': gop_count,
        'avg_gop_size': avg_gop_size
    }


def analyze_video_metadata(video_path: Path) -> Dict:
    """
    Main function to analyze video metadata.
    
    Args:
        video_path: Path to the video file
    
    Returns:
        dict: Complete analysis results
    """
    logger.info(f"Starting metadata analysis for: {video_path}")
    
    # Check FFmpeg installation
    check_ffmpeg_installed()
    
    # Validate video file
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")
    
    # Get metadata
    metadata = get_video_metadata(video_path)
    
    # Get frame data for GOP analysis
    frame_data = get_frame_data(video_path)
    frames = frame_data.get('frames', [])
    
    # Analyze GOP structure
    gop_stats = analyze_gop_structure(frames)
    
    # Print report
    print_metadata_report(video_path, metadata, gop_stats, frames)
    
    logger.info("Metadata analysis complete")
    
    return {
        'metadata': metadata,
        'gop_stats': gop_stats,
        'frame_count': len(frames)
    }
