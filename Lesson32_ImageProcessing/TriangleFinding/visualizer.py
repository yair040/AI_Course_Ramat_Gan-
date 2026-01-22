"""
Visualization module for triangle detection.
Author: Yair Levi
"""

import cv2
import numpy as np
from typing import List, Tuple, Optional
from pathlib import Path
from config import logger, get_project_root


def apply_threshold(image: np.ndarray, threshold: int) -> np.ndarray:
    """
    Apply binary threshold to grayscale image.
    
    Args:
        image: Grayscale image (uint8)
        threshold: Threshold value [0-255]
    
    Returns:
        Binary image (uint8): pixels > threshold → 255, else 0
    """
    binary_image = (image > threshold).astype(np.uint8) * 255
    return binary_image


def display_image(
    image: np.ndarray,
    window_name: str = "Image Display",
    wait_time: int = 3000
) -> None:
    """
    Display image in a window (non-interactive).
    
    Args:
        image: Image to display
        window_name: Window title
        wait_time: Time to display in milliseconds (0 = wait for key)
    """
    logger.debug(f"Displaying image: {window_name}")
    
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 800, 800)
    cv2.imshow(window_name, image)
    cv2.waitKey(wait_time)
    cv2.destroyAllWindows()


def save_image(image: np.ndarray, filename: str) -> None:
    """
    Save image to output directory.
    
    Args:
        image: Image to save
        filename: Filename (will be saved in output/ directory)
    """
    output_dir = get_project_root() / "output"
    output_dir.mkdir(exist_ok=True)
    
    filepath = output_dir / filename
    success = cv2.imwrite(str(filepath), image)
    
    if success:
        logger.info(f"Image saved: {filepath}")
    else:
        logger.error(f"Failed to save image: {filepath}")


def draw_triangle_overlay(
    image: np.ndarray,
    vertices: List[Tuple[float, float]],
    color: Tuple[int, int, int] = (0, 255, 0),
    thickness: int = 2
) -> np.ndarray:
    """
    Draw detected triangle on image.
    
    Coordinate system: Y-axis points downward (standard image coordinates)
    
    Args:
        image: Input image (grayscale or color)
        vertices: List of 3 vertices [(x1, y1), (x2, y2), (x3, y3)]
        color: Line color (B, G, R) for color images
        thickness: Line thickness
    
    Returns:
        Image with triangle drawn
    """
    # Convert grayscale to color if needed
    if len(image.shape) == 2:
        output = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    else:
        output = image.copy()
    
    # Convert vertices to integer coordinates
    pts = np.array(vertices, dtype=np.int32)
    
    # Draw triangle edges
    cv2.polylines(output, [pts], isClosed=True, color=color, thickness=thickness)
    
    # Draw vertices as circles
    for i, (x, y) in enumerate(vertices):
        cv2.circle(output, (int(x), int(y)), radius=5, color=(0, 0, 255), thickness=-1)
        # Add vertex labels
        label = f"V{i+1}"
        cv2.putText(output, label, (int(x) + 10, int(y) - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
    
    logger.debug(f"Drew triangle with {len(vertices)} vertices")
    
    return output


def draw_hough_lines(
    image: np.ndarray,
    lines: List[Tuple[float, float]],
    color: Tuple[int, int, int] = (255, 0, 0)
) -> np.ndarray:
    """
    Draw Hough lines on image.
    
    Args:
        image: Input image
        lines: List of lines in (rho, theta) format
        color: Line color (B, G, R)
    
    Returns:
        Image with lines drawn
    """
    # Convert grayscale to color if needed
    if len(image.shape) == 2:
        output = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    else:
        output = image.copy()
    
    for rho, theta in lines:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        
        # Calculate points far from the center
        x1 = int(x0 + 2000 * (-b))
        y1 = int(y0 + 2000 * (a))
        x2 = int(x0 - 2000 * (-b))
        y2 = int(y0 - 2000 * (a))
        
        cv2.line(output, (x1, y1), (x2, y2), color, 2)
    
    logger.debug(f"Drew {len(lines)} Hough lines")
    
    return output