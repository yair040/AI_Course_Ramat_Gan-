"""
Task modules for Video Processing Analysis Tool.

This package contains implementations for the three main tasks:
1. Metadata extraction and analysis
2. Motion vector visualization
3. Test video generation

Author: Yair Levi
"""

from .task1_metadata import analyze_video_metadata
from .task2_motion_vectors import extract_and_analyze_motion_vectors
from .task3_generate_video import generate_test_video

__all__ = [
    'analyze_video_metadata',
    'extract_and_analyze_motion_vectors',
    'generate_test_video'
]
