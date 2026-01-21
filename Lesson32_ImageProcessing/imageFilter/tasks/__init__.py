"""
Task modules for image processing pipeline.
Author: Yair Levi
"""

from tasks.fft_transform import apply_fft, get_magnitude_spectrum, get_phase_spectrum
from tasks.frequency_display import visualize_spectrum, save_spectrum, plot_comparison
from tasks.filter_apply import apply_filter, apply_filters_parallel, apply_filters_sequential
from tasks.inverse_transform import apply_ifft, normalize_image, reconstruct_image
from tasks.image_display import display_images, create_comparison, save_comparison_grid

__all__ = [
    'apply_fft',
    'get_magnitude_spectrum',
    'get_phase_spectrum',
    'visualize_spectrum',
    'save_spectrum',
    'plot_comparison',
    'apply_filter',
    'apply_filters_parallel',
    'apply_filters_sequential',
    'apply_ifft',
    'normalize_image',
    'reconstruct_image',
    'display_images',
    'create_comparison',
    'save_comparison_grid'
]