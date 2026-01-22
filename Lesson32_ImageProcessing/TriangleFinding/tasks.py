"""
Task orchestration module for Triangle Edge Detection System.
Author: Yair Levi
"""

import numpy as np
from typing import Dict, Any, Optional, List, Tuple
from config import logger, IMAGE_WIDTH, IMAGE_HEIGHT, FILTER_CUTOFF_RADIUS, EDGE_THRESHOLD
from config import LINE_RHO_THRESHOLD, LINE_THETA_THRESHOLD
from image_generator import generate_triangle_image
from edge_detector import apply_frequency_filter, inverse_fft_reconstruction, thin_edges
from visualizer import apply_threshold, display_image, save_image
from visualizer import draw_triangle_overlay, draw_hough_lines
from triangle_detector import detect_lines_hough, filter_similar_lines, select_best_three_lines
from geometry_utils import find_triangle_vertices, calculate_vertex_errors


def task1_generate_image(
    width: int = IMAGE_WIDTH,
    height: int = IMAGE_HEIGHT,
    vertices: Optional[np.ndarray] = None
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Task 1: Generate triangle image.
    
    Returns:
        Tuple of (binary triangle image, original vertices)
    """
    logger.info("=== TASK 1: Generate Triangle Image ===")
    
    try:
        from image_generator import _create_default_triangle
        
        # Get original vertices before generating image
        if vertices is None:
            vertices = _create_default_triangle(width, height)
        
        image = generate_triangle_image(width, height, vertices)
        logger.info(f"Task 1 completed: Generated {width}x{height} triangle image")
        
        save_image(image, "01_original_triangle.png")
        
        return image, vertices
    
    except Exception as e:
        logger.error(f"Task 1 failed: {e}", exc_info=True)
        raise


def task2_apply_filter(
    image: np.ndarray,
    cutoff_radius: float = FILTER_CUTOFF_RADIUS
) -> np.ndarray:
    """Task 2: Apply frequency domain filter for edge detection."""
    logger.info("=== TASK 2: Apply Frequency Domain Filter ===")
    
    try:
        filtered_fft = apply_frequency_filter(image, cutoff_radius, 'highpass')
        logger.info("Task 2 completed: Applied frequency domain filter")
        return filtered_fft
    
    except Exception as e:
        logger.error(f"Task 2 failed: {e}", exc_info=True)
        raise


def task3_reconstruct_image(filtered_fft: np.ndarray) -> np.ndarray:
    """Task 3: Reconstruct image via inverse FFT."""
    logger.info("=== TASK 3: Reconstruct Image via Inverse FFT ===")
    
    try:
        edge_image = inverse_fft_reconstruction(filtered_fft)
        logger.info("Task 3 completed: Reconstructed edge-enhanced image")
        
        save_image(edge_image, "02_edge_detected.png")
        
        return edge_image
    
    except Exception as e:
        logger.error(f"Task 3 failed: {e}", exc_info=True)
        raise


def task4_threshold_image(edge_image: np.ndarray, threshold: int = EDGE_THRESHOLD) -> np.ndarray:
    """Task 4: Apply threshold with edge thinning."""
    logger.info(f"=== TASK 4: Apply Threshold (value={threshold}) ===")
    
    try:
        binary_image = apply_threshold(edge_image, threshold)
        logger.info("Task 4 completed: Applied threshold")
        
        save_image(binary_image, "03_thresholded.png")
        
        # Apply edge thinning for better line detection
        logger.info("Applying edge thinning for improved accuracy")
        try:
            thinned_image = thin_edges(binary_image)
            save_image(thinned_image, "03b_thinned_edges.png")
            logger.info("Edge thinning successful")
            return thinned_image
        except Exception as thin_error:
            logger.warning(f"Edge thinning failed: {thin_error}, using original binary image")
            return binary_image
    
    except Exception as e:
        logger.error(f"Task 4 failed: {e}", exc_info=True)
        raise


def task5_display_result(binary_image: np.ndarray) -> None:
    """Task 5: Display thresholded result (non-interactive)."""
    logger.info("=== TASK 5: Display Result ===")
    
    try:
        display_image(binary_image, "Thresholded Edge Image", wait_time=2000)
        logger.info("Task 5 completed: Displayed result")
    
    except Exception as e:
        logger.error(f"Task 5 failed: {e}", exc_info=True)
        raise


def task6_draw_triangle(
    original_image: np.ndarray,
    vertices: List[Tuple[float, float]]
) -> np.ndarray:
    """Task 6: Draw detected triangle on original image."""
    logger.info("=== TASK 6: Draw Triangle Overlay ===")
    logger.info("Coordinate system: Y-axis points downward (image coordinates)")
    
    try:
        overlay_image = draw_triangle_overlay(original_image, vertices)
        logger.info("Task 6 completed: Drew triangle overlay")
        
        save_image(overlay_image, "04_triangle_overlay.png")
        display_image(overlay_image, "Triangle Overlay", wait_time=2000)
        
        return overlay_image
    
    except Exception as e:
        logger.error(f"Task 6 failed: {e}", exc_info=True)
        raise


def task7_detect_triangle(
    binary_image: np.ndarray,
    original_vertices: np.ndarray
) -> List[Tuple[float, float]]:
    """Task 7: Mathematically detect triangle using Hough transform."""
    logger.info("=== TASK 7: Detect Triangle Mathematically ===")
    
    try:
        # 7a: Detect lines using Hough transform
        logger.info("Step 7a: Detecting lines with Hough transform")
        all_lines = detect_lines_hough(binary_image)
        
        if not all_lines:
            raise ValueError("No lines detected by Hough transform")
        
        # Filter similar lines
        distinct_lines = filter_similar_lines(
            all_lines, 
            rho_threshold=LINE_RHO_THRESHOLD, 
            theta_threshold=LINE_THETA_THRESHOLD
        )
        
        # Select best 3 lines
        if len(distinct_lines) < 3:
            raise ValueError(f"Found only {len(distinct_lines)} distinct lines, need 3")
        
        best_lines = select_best_three_lines(distinct_lines)
        logger.info(f"Selected 3 best lines from {len(distinct_lines)} candidates")
        
        # Visualize Hough lines
        hough_viz = draw_hough_lines(binary_image, best_lines)
        save_image(hough_viz, "05_hough_lines.png")
        
        # 7b: Find vertices (intersections)
        logger.info("Step 7b: Finding triangle vertices from line intersections")
        detected_vertices = find_triangle_vertices(best_lines)
        
        # 7c: Print results
        logger.info("Step 7c: Printing detected vertices")
        print_vertex_results(detected_vertices, original_vertices)
        
        return detected_vertices
    
    except Exception as e:
        logger.error(f"Task 7 failed: {e}", exc_info=True)
        raise


def print_vertex_results(
    detected: List[Tuple[float, float]],
    original: np.ndarray
) -> None:
    """Print detected vertices and comparison with original."""
    print("\n" + "=" * 50)
    print("DETECTED TRIANGLE VERTICES")
    print("=" * 50)
    
    for i, (x, y) in enumerate(detected, 1):
        print(f"Vertex {i}: ({x:.2f}, {y:.2f})")
    
    print("\n" + "-" * 50)
    print("ORIGINAL TRIANGLE VERTICES")
    print("-" * 50)
    
    for i, vertex in enumerate(original, 1):
        print(f"Vertex {i}: ({vertex[0]:.2f}, {vertex[1]:.2f})")
    
    # Calculate errors
    errors, mean_error = calculate_vertex_errors(detected, original)
    
    print("\n" + "-" * 50)
    print("DETECTION ERRORS (pixels)")
    print("-" * 50)
    
    for i, error in enumerate(errors, 1):
        print(f"Vertex {i}: {error:.2f} pixels")
    
    print(f"\nMean Error: {mean_error:.2f} pixels")
    print("=" * 50 + "\n")
    
    # Log results
    logger.info(f"Detection mean error: {mean_error:.2f} pixels")
    for i, error in enumerate(errors, 1):
        logger.info(f"Vertex {i} error: {error:.2f} pixels")


def run_all_tasks(config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Execute all tasks in sequence."""
    logger.info("=" * 60)
    logger.info("STARTING TRIANGLE EDGE DETECTION AND RECONSTRUCTION")
    logger.info("=" * 60)
    
    if config is None:
        config = {}
    
    results = {}
    
    try:
        # Tasks 1-3: Generate and process
        triangle_image, original_vertices = task1_generate_image(
            config.get('width', IMAGE_WIDTH),
            config.get('height', IMAGE_HEIGHT)
        )
        results['triangle_image'] = triangle_image
        results['original_vertices'] = original_vertices
        
        filtered_fft = task2_apply_filter(triangle_image, config.get('cutoff_radius', FILTER_CUTOFF_RADIUS))
        edge_image = task3_reconstruct_image(filtered_fft)
        
        # Task 4-5: Threshold (with thinning) and display
        binary_image = task4_threshold_image(edge_image, threshold=EDGE_THRESHOLD)
        task5_display_result(binary_image)
        
        # Task 7: Detect triangle
        detected_vertices = task7_detect_triangle(binary_image, original_vertices)
        results['detected_vertices'] = detected_vertices
        
        # Task 6: Draw overlay
        task6_draw_triangle(triangle_image, detected_vertices)
        
        logger.info("=" * 60)
        logger.info("PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("=" * 60)
        
        return results
    
    except Exception as e:
        logger.error("PIPELINE FAILED", exc_info=True)
        raise