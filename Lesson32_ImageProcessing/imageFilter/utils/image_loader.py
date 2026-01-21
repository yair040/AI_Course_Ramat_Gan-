"""
Image loading and saving utilities.
Author: Yair Levi

Handles image I/O operations with format validation and conversion.
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Optional, Dict, Any
from utils.logger import get_logger

logger = get_logger(__name__)

# Supported image formats
SUPPORTED_FORMATS = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif'}


def validate_image_format(path: Path) -> bool:
    """
    Check if image format is supported.
    
    Args:
        path: Path to image file
    
    Returns:
        True if format is supported
    """
    suffix = path.suffix.lower()
    is_valid = suffix in SUPPORTED_FORMATS
    
    if not is_valid:
        logger.warning(f"Unsupported format: {suffix}. Supported: {SUPPORTED_FORMATS}")
    
    return is_valid


def load_image(path: Path, grayscale: bool = True) -> Optional[np.ndarray]:
    """
    Load an image from file.
    
    Args:
        path: Path to image file
        grayscale: If True, convert to grayscale
    
    Returns:
        Image as numpy array, or None if loading fails
    
    Raises:
        FileNotFoundError: If image file doesn't exist
        ValueError: If image format is not supported
    """
    path = Path(path)
    
    if not path.exists():
        logger.error(f"Image file not found: {path}")
        raise FileNotFoundError(f"Image not found: {path}")
    
    if not validate_image_format(path):
        logger.error(f"Unsupported image format: {path.suffix}")
        raise ValueError(f"Unsupported format: {path.suffix}")
    
    try:
        # Load image
        if grayscale:
            image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
            logger.info(f"Loaded grayscale image: {path.name}, shape: {image.shape}")
        else:
            image = cv2.imread(str(path), cv2.IMREAD_COLOR)
            logger.info(f"Loaded color image: {path.name}, shape: {image.shape}")
        
        if image is None:
            logger.error(f"Failed to load image: {path}")
            raise ValueError(f"OpenCV failed to load image: {path}")
        
        return image
    
    except Exception as e:
        logger.error(f"Error loading image {path}: {e}")
        raise


def save_image(image: np.ndarray, path: Path) -> None:
    """
    Save an image to file.
    
    Args:
        image: Image as numpy array
        path: Destination path
    
    Raises:
        ValueError: If image data is invalid
    """
    path = Path(path)
    
    if image is None or image.size == 0:
        logger.error("Cannot save empty or None image")
        raise ValueError("Image is empty or None")
    
    # Ensure output directory exists
    path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        success = cv2.imwrite(str(path), image)
        if not success:
            logger.error(f"Failed to save image: {path}")
            raise ValueError(f"OpenCV failed to save image: {path}")
        
        logger.info(f"Saved image: {path.name}, shape: {image.shape}")
    
    except Exception as e:
        logger.error(f"Error saving image {path}: {e}")
        raise


def get_image_info(image: np.ndarray) -> Dict[str, Any]:
    """
    Get information about an image.
    
    Args:
        image: Image as numpy array
    
    Returns:
        Dictionary with image properties
    """
    if len(image.shape) == 2:
        height, width = image.shape
        channels = 1
    else:
        height, width, channels = image.shape
    
    info = {
        'shape': image.shape,
        'height': height,
        'width': width,
        'channels': channels,
        'dtype': str(image.dtype),
        'min': float(np.min(image)),
        'max': float(np.max(image)),
        'mean': float(np.mean(image))
    }
    
    logger.debug(f"Image info: {info}")
    return info