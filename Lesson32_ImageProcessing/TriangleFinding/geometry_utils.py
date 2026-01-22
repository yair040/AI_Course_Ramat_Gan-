"""
Geometry utilities for line intersection and vertex calculation.
Author: Yair Levi
"""

import numpy as np
from typing import List, Optional, Tuple
from config import logger


def line_intersection(
    line1: Tuple[float, float],
    line2: Tuple[float, float]
) -> Optional[Tuple[float, float]]:
    """
    Calculate intersection point of two lines in Hough (rho, theta) format.
    
    Lines are represented as: rho = x*cos(theta) + y*sin(theta)
    
    Args:
        line1: (rho1, theta1) in radians
        line2: (rho2, theta2) in radians
    
    Returns:
        (x, y) intersection point, or None if lines are parallel
    """
    rho1, theta1 = line1
    rho2, theta2 = line2
    
    # Convert to Cartesian line equation: ax + by = c
    # From rho = x*cos(theta) + y*sin(theta)
    a1, b1, c1 = np.cos(theta1), np.sin(theta1), rho1
    a2, b2, c2 = np.cos(theta2), np.sin(theta2), rho2
    
    # Solve system of linear equations
    # a1*x + b1*y = c1
    # a2*x + b2*y = c2
    determinant = a1 * b2 - a2 * b1
    
    # Check if lines are parallel (determinant near zero)
    if abs(determinant) < 1e-6:
        logger.debug(f"Lines are parallel: det={determinant}")
        return None
    
    # Cramer's rule
    x = (c1 * b2 - c2 * b1) / determinant
    y = (a1 * c2 - a2 * c1) / determinant
    
    return (x, y)


def find_triangle_vertices(lines: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    """
    Find triangle vertices from 3 lines by calculating pairwise intersections.
    
    Args:
        lines: List of 3 lines in (rho, theta) format
    
    Returns:
        List of 3 vertex coordinates [(x1, y1), (x2, y2), (x3, y3)]
    
    Raises:
        ValueError: If lines don't form a valid triangle
    """
    if len(lines) != 3:
        raise ValueError(f"Expected 3 lines, got {len(lines)}")
    
    logger.info("Calculating triangle vertices from line intersections")
    
    vertices = []
    
    # Calculate all pairwise intersections
    # Line 0 ∩ Line 1
    vertex1 = line_intersection(lines[0], lines[1])
    if vertex1:
        vertices.append(vertex1)
        logger.debug(f"Vertex 1 (L0∩L1): ({vertex1[0]:.2f}, {vertex1[1]:.2f})")
    
    # Line 1 ∩ Line 2
    vertex2 = line_intersection(lines[1], lines[2])
    if vertex2:
        vertices.append(vertex2)
        logger.debug(f"Vertex 2 (L1∩L2): ({vertex2[0]:.2f}, {vertex2[1]:.2f})")
    
    # Line 2 ∩ Line 0
    vertex3 = line_intersection(lines[2], lines[0])
    if vertex3:
        vertices.append(vertex3)
        logger.debug(f"Vertex 3 (L2∩L0): ({vertex3[0]:.2f}, {vertex3[1]:.2f})")
    
    if len(vertices) != 3:
        raise ValueError(f"Could not find 3 valid vertices, found {len(vertices)}")
    
    logger.info(f"Successfully calculated {len(vertices)} triangle vertices")
    
    return vertices


def calculate_vertex_errors(
    detected_vertices: List[Tuple[float, float]],
    original_vertices: np.ndarray
) -> Tuple[List[float], float]:
    """
    Calculate distance errors between detected and original vertices.
    
    Matches vertices by finding closest pairs.
    
    Args:
        detected_vertices: List of detected (x, y) coordinates
        original_vertices: Array of original vertices, shape (3, 2)
    
    Returns:
        Tuple of (list of individual errors, mean error)
    """
    detected = np.array(detected_vertices)
    original = np.array(original_vertices)
    
    errors = []
    used_original = set()
    
    # Match each detected vertex to closest unused original vertex
    for det_vertex in detected:
        min_dist = float('inf')
        best_match = None
        
        for i, orig_vertex in enumerate(original):
            if i in used_original:
                continue
            
            dist = np.sqrt(np.sum((det_vertex - orig_vertex) ** 2))
            if dist < min_dist:
                min_dist = dist
                best_match = i
        
        if best_match is not None:
            errors.append(min_dist)
            used_original.add(best_match)
    
    mean_error = np.mean(errors) if errors else 0.0
    
    return errors, mean_error


def is_point_in_bounds(point: Tuple[float, float], width: int, height: int) -> bool:
    """
    Check if a point is within image bounds.
    
    Args:
        point: (x, y) coordinates
        width: Image width
        height: Image height
    
    Returns:
        True if point is within bounds
    """
    x, y = point
    return 0 <= x < width and 0 <= y < height