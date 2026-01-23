"""
Task modules for JPEG Compression Analysis Tool.
Author: Yair Levi
"""

from .compress_task import compress_image, compress_single
from .decompress_task import decompress_images, decompress_single
from .error_task import calculate_errors, calculate_mse, calculate_mae
from .visualize_task import create_file_size_histogram, create_error_histogram

__all__ = [
    "compress_image",
    "compress_single",
    "decompress_images",
    "decompress_single",
    "calculate_errors",
    "calculate_mse",
    "calculate_mae",
    "create_file_size_histogram",
    "create_error_histogram",
]
