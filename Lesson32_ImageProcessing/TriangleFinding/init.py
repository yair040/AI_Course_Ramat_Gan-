"""
Triangle Edge Detection System
Author: Yair Levi

A Python application for detecting triangle edges using frequency domain filtering.
"""

__version__ = '1.0.0'
__author__ = 'Yair Levi'
__all__ = [
    'generate_triangle_image',
    'apply_frequency_filter',
    'inverse_fft_reconstruction',
    'interactive_threshold_display',
    'run_all_tasks'
]

from .image_generator import generate_triangle_image
from .edge_detector import apply_frequency_filter, inverse_fft_reconstruction
from .visualizer import interactive_threshold_display, apply_threshold
from .tasks import run_all_tasks