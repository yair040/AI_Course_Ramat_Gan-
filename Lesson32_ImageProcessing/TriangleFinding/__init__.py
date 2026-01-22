"""
Triangle Edge Detection System
Author: Yair Levi

A Python application for detecting triangle edges using frequency domain filtering.
"""

__version__ = '2.0.0'
__author__ = 'Yair Levi'
__all__ = [
    'generate_triangle_image',
    'apply_frequency_filter',
    'inverse_fft_reconstruction',
    'apply_threshold',
    'draw_triangle_overlay',
    'detect_lines_hough',
    'find_triangle_vertices',
    'run_all_tasks'
]

from .image_generator import generate_triangle_image
from .edge_detector import apply_frequency_filter, inverse_fft_reconstruction
from .visualizer import apply_threshold, draw_triangle_overlay, draw_hough_lines
from .triangle_detector import detect_lines_hough, filter_similar_lines
from .geometry_utils import find_triangle_vertices, calculate_vertex_errors
from .tasks import run_all_tasks