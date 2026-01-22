"""
Triangle detection using Hough transform.
Author: Yair Levi
"""

import cv2
import numpy as np
from typing import List, Tuple, Optional
from config import logger, HOUGH_THRESHOLD, HOUGH_RHO_RESOLUTION, HOUGH_THETA_RESOLUTION
from config import LINE_RHO_THRESHOLD, LINE_THETA_THRESHOLD


def detect_lines_hough(
    binary_image: np.ndarray,
    rho_resolution: float = HOUGH_RHO_RESOLUTION,
    theta_resolution: float = HOUGH_THETA_RESOLUTION,
    threshold: int = HOUGH_THRESHOLD
) -> List[Tuple[float, float]]:
    """
    Detect lines using Hough transform (standard method).
    
    Args:
        binary_image: Binary edge image (uint8)
        rho_resolution: Distance resolution in pixels
        theta_resolution: Angle resolution in radians
        threshold: Minimum votes for line detection
    
    Returns:
        List of detected lines as [(rho1, theta1), (rho2, theta2), ...]
    """
    logger.info("Detecting lines using Hough transform")
    logger.debug(f"Parameters: rho={rho_resolution}, theta={theta_resolution:.4f}, "
                f"threshold={threshold}")
    
    # Apply standard Hough transform
    lines = cv2.HoughLines(binary_image, rho_resolution, theta_resolution, threshold)
    
    if lines is None:
        logger.warning("No lines detected by Hough transform")
        return []
    
    # Extract (rho, theta) pairs
    lines_list = [(rho, theta) for rho, theta in lines[:, 0, :]]
    
    logger.info(f"Detected {len(lines_list)} lines")
    for i, (rho, theta) in enumerate(lines_list[:10]):  # Log first 10
        logger.debug(f"Line {i+1}: rho={rho:.2f}, theta={np.degrees(theta):.2f}°")
    
    return lines_list


def filter_similar_lines(
    lines: List[Tuple[float, float]],
    rho_threshold: float = LINE_RHO_THRESHOLD,
    theta_threshold: float = LINE_THETA_THRESHOLD
) -> List[Tuple[float, float]]:
    """
    Filter out similar lines to keep only distinct ones.
    
    Args:
        lines: List of (rho, theta) line parameters
        rho_threshold: Maximum rho difference for similar lines
        theta_threshold: Maximum theta difference (radians) for similar lines
    
    Returns:
        Filtered list of distinct lines
    """
    if not lines:
        return []
    
    logger.debug(f"Filtering similar lines from {len(lines)} candidates")
    logger.debug(f"Thresholds: rho={rho_threshold}, theta={theta_threshold:.4f} rad")
    
    # Normalize theta to [0, π] and handle negative rho
    normalized_lines = []
    for rho, theta in lines:
        # Normalize theta to [0, π]
        while theta < 0:
            theta += np.pi
        while theta >= np.pi:
            theta -= np.pi
        
        # If rho is negative, flip both rho and theta
        if rho < 0:
            rho = -rho
            theta = theta + np.pi if theta < np.pi/2 else theta - np.pi
        
        normalized_lines.append((rho, theta))
    
    # Sort by rho for consistent ordering
    lines_sorted = sorted(normalized_lines, key=lambda x: x[0])
    
    distinct_lines = [lines_sorted[0]]
    
    for rho, theta in lines_sorted[1:]:
        is_similar = False
        
        for ref_rho, ref_theta in distinct_lines:
            # Check if current line is similar to any existing distinct line
            rho_diff = abs(rho - ref_rho)
            
            # Handle theta wrapping around π
            theta_diff = abs(theta - ref_theta)
            theta_diff = min(theta_diff, np.pi - theta_diff)
            
            if rho_diff < rho_threshold and theta_diff < theta_threshold:
                is_similar = True
                logger.debug(f"Filtering similar line: rho_diff={rho_diff:.2f}, theta_diff={theta_diff:.4f}")
                break
        
        if not is_similar:
            distinct_lines.append((rho, theta))
    
    logger.info(f"Filtered to {len(distinct_lines)} distinct lines")
    
    return distinct_lines


def select_best_three_lines(lines: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    """
    Select the best 3 lines from detected lines.
    
    Strategy: Take the 3 most distinct lines by angular separation.
    
    Args:
        lines: List of detected lines
    
    Returns:
        List of exactly 3 lines
    
    Raises:
        ValueError: If fewer than 3 lines available
    """
    if len(lines) < 3:
        raise ValueError(f"Need at least 3 lines, got {len(lines)}")
    
    if len(lines) == 3:
        logger.debug("Exactly 3 lines detected, using all")
        return lines
    
    logger.info(f"Selecting best 3 lines from {len(lines)} candidates")
    
    # Strategy: Select lines with maximum angular separation
    # Use a greedy approach to maximize minimum pairwise angle difference
    
    best_combination = None
    max_min_angle = 0
    
    # Try all combinations of 3 lines
    from itertools import combinations
    
    for combo in combinations(range(len(lines)), 3):
        angles = [lines[i][1] for i in combo]
        
        # Calculate minimum pairwise angle difference
        min_angle = float('inf')
        for i in range(3):
            for j in range(i+1, 3):
                angle_diff = abs(angles[i] - angles[j])
                angle_diff = min(angle_diff, np.pi - angle_diff)
                min_angle = min(min_angle, angle_diff)
        
        if min_angle > max_min_angle:
            max_min_angle = min_angle
            best_combination = combo
    
    selected = [lines[i] for i in best_combination]
    
    logger.info(f"Selected 3 lines with minimum angular separation: {np.degrees(max_min_angle):.2f}°")
    for i, (rho, theta) in enumerate(selected):
        logger.debug(f"Selected line {i+1}: rho={rho:.2f}, theta={np.degrees(theta):.2f}°")
    
    return selected