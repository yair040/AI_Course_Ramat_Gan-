"""
Configuration module for Triangle Edge Detection System.
Author: Yair Levi
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path


# Application Constants
IMAGE_WIDTH = 512
IMAGE_HEIGHT = 512
FILTER_CUTOFF_RADIUS = 30  # High-pass filter radius in frequency domain
EDGE_THRESHOLD = 80  # Increased from 48 for thinner edges
LOG_DIR = "log"
LOG_FILENAME = "triangle_edge_detection.log"
MAX_LOG_FILES = 20
MAX_LOG_FILE_SIZE = 16 * 1024 * 1024  # 16MB in bytes

# Hough Transform Parameters
HOUGH_THRESHOLD = 100  # Minimum votes for line detection
HOUGH_RHO_RESOLUTION = 1.0  # Distance resolution in pixels
HOUGH_THETA_RESOLUTION = 0.01745329  # Angle resolution (1 degree in radians)

# Line Filtering Parameters
LINE_RHO_THRESHOLD = 25.0  # Maximum rho difference for similar lines
LINE_THETA_THRESHOLD = 0.087  # Maximum theta difference (5 degrees)


def get_project_root() -> Path:
    """Get the project root directory (where this file is located)."""
    return Path(__file__).parent


def ensure_log_directory() -> Path:
    """Ensure log directory exists and return its path."""
    log_path = get_project_root() / LOG_DIR
    log_path.mkdir(exist_ok=True)
    return log_path


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """
    Setup logging with rotating file handler (ring buffer).
    
    Args:
        level: Logging level (default: INFO)
    
    Returns:
        Configured logger instance
    """
    log_dir = ensure_log_directory()
    log_file = log_dir / LOG_FILENAME
    
    # Create logger
    logger = logging.getLogger("TriangleEdgeDetection")
    logger.setLevel(level)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Create rotating file handler (ring buffer)
    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=MAX_LOG_FILE_SIZE,
        backupCount=MAX_LOG_FILES - 1,  # backupCount doesn't include the main file
        encoding='utf-8'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Set formatters
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info("Logging system initialized")
    logger.info(f"Log directory: {log_dir.absolute()}")
    logger.info(f"Log file: {LOG_FILENAME}")
    logger.info(f"Ring buffer: {MAX_LOG_FILES} files x {MAX_LOG_FILE_SIZE / (1024*1024):.1f}MB")
    
    return logger


# Default logger instance
logger = setup_logging()