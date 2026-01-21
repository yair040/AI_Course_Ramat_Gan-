"""
FFT transformation task.
Author: Yair Levi

Performs 2D Fast Fourier Transform on images.
"""

import numpy as np
from typing import Tuple
from utils.logger import get_logger

logger = get_logger(__name__)


def apply_fft(image: np.ndarray) -> np.ndarray:
    """
    Apply 2D FFT to an image.
    
    Args:
        image: Input image as numpy array
    
    Returns:
        FFT-shifted complex array
    
    Raises:
        ValueError: If image is invalid
    """
    if image is None or image.size == 0:
        logger.error("Cannot apply FFT to empty image")
        raise ValueError("Image is empty or None")
    
    logger.info(f"Applying FFT to image of shape {image.shape}")
    
    try:
        # Convert to float for FFT
        image_float = image.astype(np.float32)
        
        # Apply 2D FFT
        fft_result = np.fft.fft2(image_float)
        
        # Shift zero frequency to center
        fft_shifted = np.fft.fftshift(fft_result)
        
        logger.info(f"FFT completed: output shape {fft_shifted.shape}")
        return fft_shifted
    
    except Exception as e:
        logger.error(f"FFT transformation failed: {e}")
        raise


def get_magnitude_spectrum(fft_image: np.ndarray) -> np.ndarray:
    """
    Calculate magnitude spectrum from FFT image.
    
    Args:
        fft_image: Complex FFT array
    
    Returns:
        Magnitude spectrum
    """
    if fft_image is None or fft_image.size == 0:
        logger.error("Cannot calculate magnitude of empty FFT")
        raise ValueError("FFT image is empty or None")
    
    try:
        magnitude = np.abs(fft_image)
        logger.info(f"Magnitude spectrum calculated: range [{magnitude.min():.2f}, "
                   f"{magnitude.max():.2f}]")
        return magnitude
    
    except Exception as e:
        logger.error(f"Magnitude calculation failed: {e}")
        raise


def get_phase_spectrum(fft_image: np.ndarray) -> np.ndarray:
    """
    Calculate phase spectrum from FFT image.
    
    Args:
        fft_image: Complex FFT array
    
    Returns:
        Phase spectrum in radians
    """
    if fft_image is None or fft_image.size == 0:
        logger.error("Cannot calculate phase of empty FFT")
        raise ValueError("FFT image is empty or None")
    
    try:
        phase = np.angle(fft_image)
        logger.info(f"Phase spectrum calculated: range [{phase.min():.2f}, "
                   f"{phase.max():.2f}]")
        return phase
    
    except Exception as e:
        logger.error(f"Phase calculation failed: {e}")
        raise


def get_fft_stats(fft_image: np.ndarray) -> dict:
    """
    Get statistics about FFT image.
    
    Args:
        fft_image: Complex FFT array
    
    Returns:
        Dictionary with FFT statistics
    """
    magnitude = get_magnitude_spectrum(fft_image)
    
    stats = {
        'shape': fft_image.shape,
        'dtype': str(fft_image.dtype),
        'magnitude_min': float(magnitude.min()),
        'magnitude_max': float(magnitude.max()),
        'magnitude_mean': float(magnitude.mean())
    }
    
    logger.debug(f"FFT stats: {stats}")
    return stats