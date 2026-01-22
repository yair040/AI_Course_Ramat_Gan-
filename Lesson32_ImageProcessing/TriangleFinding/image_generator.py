"""
Image generation module for Triangle Edge Detection System.
Author: Yair Levi
"""

import numpy as np
import cv2
from typing import Optional, Tuple
from config import logger, IMAGE_WIDTH, IMAGE_HEIGHT


def generate_triangle_image(
    width: int = IMAGE_WIDTH,
    height: int = IMAGE_HEIGHT,
    vertices: Optional[np.ndarray] = None
) -> np.ndarray:
    """
    Generate a binary image with a white triangle on black background.
    
    Args:
        width: Image width in pixels
        height: Image height in pixels
        vertices: Triangle vertices as array of shape (3, 2).
                 If None, creates centered equilateral triangle.
    
    Returns:
        Binary image as numpy array (uint8), shape (height, width)
        Triangle interior: 255 (white)
        Triangle exterior: 0 (black)
    """
    logger.info(f"Generating triangle image: {width}x{height}")
    
    # Create black canvas
    image = np.zeros((height, width), dtype=np.uint8)
    
    # Define default triangle vertices if not provided
    if vertices is None:
        vertices = _create_default_triangle(width, height)
        logger.debug(f"Using default triangle vertices: {vertices.tolist()}")
    else:
        logger.debug(f"Using custom triangle vertices: {vertices.tolist()}")
    
    # Validate vertices
    if vertices.shape != (3, 2):
        raise ValueError(f"Vertices must have shape (3, 2), got {vertices.shape}")
    
    # Convert vertices to integer coordinates
    vertices = vertices.astype(np.int32)
    
    # Fill triangle using OpenCV
    cv2.fillPoly(image, [vertices], color=255)
    
    logger.info(f"Triangle image generated successfully")
    logger.debug(f"Image shape: {image.shape}, dtype: {image.dtype}")
    logger.debug(f"Unique pixel values: {np.unique(image)}")
    
    return image


def _create_default_triangle(width: int, height: int) -> np.ndarray:
    """
    Create default centered equilateral triangle vertices.
    
    Args:
        width: Image width
        height: Image height
    
    Returns:
        Triangle vertices array of shape (3, 2)
    """
    # Center coordinates
    cx = width / 2
    cy = height / 2
    
    # Equilateral triangle with radius = min(width, height) * 0.35
    radius = min(width, height) * 0.35
    
    # Calculate vertices (pointing upward)
    vertices = np.array([
        [cx, cy - radius],  # Top vertex
        [cx - radius * np.sin(np.pi / 3), cy + radius * np.cos(np.pi / 3)],  # Bottom-left
        [cx + radius * np.sin(np.pi / 3), cy + radius * np.cos(np.pi / 3)]   # Bottom-right
    ], dtype=np.float32)
    
    return vertices


def save_image(image: np.ndarray, filename: str) -> None:
    """
    Save image to file (utility function).
    
    Args:
        image: Image array to save
        filename: Output filename (relative or absolute path)
    """
    success = cv2.imwrite(filename, image)
    if success:
        logger.info(f"Image saved to: {filename}")
    else:
        logger.error(f"Failed to save image to: {filename}")