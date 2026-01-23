"""
JPEG Compression Analysis Tool
Author: Yair Levi
Version: 1.0
"""

__version__ = "1.0.0"
__author__ = "Yair Levi"
__description__ = "JPEG Compression Analysis Tool"

# Package-level imports
from .utils.logger import get_logger
from .utils.config import QUALITY_LEVELS, create_directories

__all__ = [
    "get_logger",
    "QUALITY_LEVELS",
    "create_directories",
]
