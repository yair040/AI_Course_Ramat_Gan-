"""
Edge detection module using frequency domain filtering.
Author: Yair Levi
"""

import cv2
import numpy as np
from typing import Tuple
from config import logger, FILTER_CUTOFF_RADIUS


def apply_frequency_filter(
    image: np.ndarray,
    cutoff_radius: float = FILTER_CUTOFF_RADIUS,
    filter_type: str = 'highpass'
) -> np.ndarray:
    """
    Apply frequency domain filter to image for edge detection.
    
    Args:
        image: Input image (grayscale, uint8 or float)
        cutoff_radius: Filter cutoff radius in frequency domain
        filter_type: 'highpass' or 'ideal_highpass'
    
    Returns:
        Filtered frequency domain data (complex128)
    """
    logger.info(f"Applying frequency domain filter: {filter_type}, cutoff={cutoff_radius}")
    
    # Convert to float for FFT processing
    image_float = image.astype(np.float64)
    
    # Apply 2D FFT
    logger.debug("Computing 2D FFT...")
    fft_result = np.fft.fft2(image_float)
    
    # Shift zero-frequency to center
    fft_shifted = np.fft.fftshift(fft_result)
    logger.debug(f"FFT shape: {fft_shifted.shape}")
    
    # Create high-pass filter mask
    filter_mask = _create_highpass_filter(
        fft_shifted.shape,
        cutoff_radius,
        filter_type
    )
    
    # Apply filter
    filtered_fft = fft_shifted * filter_mask
    
    logger.info("Frequency domain filtering complete")
    logger.debug(f"Filtered FFT magnitude range: [{np.abs(filtered_fft).min():.2f}, {np.abs(filtered_fft).max():.2f}]")
    
    return filtered_fft


def _create_highpass_filter(
    shape: Tuple[int, int],
    cutoff_radius: float,
    filter_type: str
) -> np.ndarray:
    """
    Create high-pass filter mask in frequency domain.
    
    Args:
        shape: Filter shape (height, width)
        cutoff_radius: Cutoff radius for filter
        filter_type: 'highpass' (Gaussian) or 'ideal_highpass'
    
    Returns:
        Filter mask array (float64)
    """
    rows, cols = shape
    crow, ccol = rows // 2, cols // 2
    
    # Create coordinate grids
    y, x = np.ogrid[:rows, :cols]
    
    # Calculate distance from center
    distance = np.sqrt((x - ccol) ** 2 + (y - crow) ** 2)
    
    # Create filter based on type
    if filter_type == 'ideal_highpass':
        # Ideal high-pass: 1 if distance > cutoff, else 0
        filter_mask = (distance > cutoff_radius).astype(np.float64)
        logger.debug(f"Created ideal high-pass filter with cutoff {cutoff_radius}")
    else:  # 'highpass' (Gaussian)
        # Gaussian high-pass: 1 - exp(-(distance^2)/(2*cutoff^2))
        filter_mask = 1.0 - np.exp(-(distance ** 2) / (2 * (cutoff_radius ** 2)))
        logger.debug(f"Created Gaussian high-pass filter with cutoff {cutoff_radius}")
    
    return filter_mask


def inverse_fft_reconstruction(filtered_fft: np.ndarray) -> np.ndarray:
    """
    Reconstruct spatial domain image from filtered frequency data.
    
    Args:
        filtered_fft: Filtered frequency domain data (complex)
    
    Returns:
        Edge-enhanced grayscale image (uint8)
    """
    logger.info("Reconstructing image via inverse FFT...")
    
    # Inverse shift
    fft_ishifted = np.fft.ifftshift(filtered_fft)
    
    # Inverse FFT
    image_reconstructed = np.fft.ifft2(fft_ishifted)
    
    # Extract magnitude (edges are in magnitude)
    magnitude = np.abs(image_reconstructed)
    logger.debug(f"Magnitude range before normalization: [{magnitude.min():.2f}, {magnitude.max():.2f}]")
    
    # Normalize to [0, 255]
    magnitude_normalized = _normalize_to_uint8(magnitude)
    
    logger.info("Inverse FFT reconstruction complete")
    logger.debug(f"Output shape: {magnitude_normalized.shape}, dtype: {magnitude_normalized.dtype}")
    
    return magnitude_normalized


def _normalize_to_uint8(array: np.ndarray) -> np.ndarray:
    """
    Normalize array to uint8 range [0, 255].
    
    Args:
        array: Input array (any numeric type)
    
    Returns:
        Normalized array (uint8)
    """
    # Avoid division by zero
    array_min = array.min()
    array_max = array.max()
    
    if array_max - array_min < 1e-10:
        logger.warning("Array has zero range, returning zeros")
        return np.zeros_like(array, dtype=np.uint8)
    
    # Normalize to [0, 1]
    normalized = (array - array_min) / (array_max - array_min)
    
    # Scale to [0, 255] and convert to uint8
    uint8_array = (normalized * 255).astype(np.uint8)
    
    return uint8_array


def thin_edges(binary_image: np.ndarray) -> np.ndarray:
    """
    Thin edges to single-pixel width using morphological operations.
    
    Args:
        binary_image: Binary edge image (uint8)
    
    Returns:
        Thinned binary image with single-pixel edges
    """
    logger.info("Thinning edges to single-pixel width")
    
    # Apply morphological thinning (skeletonization)
    # Using Zhang-Suen thinning algorithm
    thinned = cv2.ximgproc.thinning(binary_image, thinningType=cv2.ximgproc.THINNING_ZHANGSUEN)
    
    logger.debug(f"Edge thinning complete")
    
    return thinned