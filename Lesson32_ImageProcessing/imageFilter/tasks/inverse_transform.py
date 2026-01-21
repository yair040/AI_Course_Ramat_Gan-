"""
Inverse FFT transformation task.
Author: Yair Levi

Converts filtered frequency domain back to spatial domain.
"""

import numpy as np
from utils.logger import get_logger

logger = get_logger(__name__)


def apply_ifft(fft_image: np.ndarray) -> np.ndarray:
    """
    Apply inverse FFT to convert back to spatial domain.
    
    Args:
        fft_image: Complex FFT array (shifted)
    
    Returns:
        Real-valued image in spatial domain
    
    Raises:
        ValueError: If FFT image is invalid
    """
    if fft_image is None or fft_image.size == 0:
        logger.error("Cannot apply IFFT to empty array")
        raise ValueError("FFT image is empty or None")
    
    logger.info(f"Applying inverse FFT to shape {fft_image.shape}")
    
    try:
        # Inverse shift to move zero frequency back to corners
        fft_ishifted = np.fft.ifftshift(fft_image)
        
        # Apply inverse FFT
        image_reconstructed = np.fft.ifft2(fft_ishifted)
        
        # Take real part (imaginary part should be negligible)
        image_real = np.real(image_reconstructed)
        
        logger.info(f"Inverse FFT completed: output shape {image_real.shape}")
        return image_real
    
    except Exception as e:
        logger.error(f"Inverse FFT failed: {e}")
        raise


def normalize_image(image: np.ndarray, target_range: tuple = (0, 255)) -> np.ndarray:
    """
    Normalize image to target range.
    
    Args:
        image: Input image array
        target_range: Target (min, max) values
    
    Returns:
        Normalized image
    """
    if image is None or image.size == 0:
        logger.error("Cannot normalize empty image")
        raise ValueError("Image is empty or None")
    
    try:
        # Get current range
        img_min, img_max = image.min(), image.max()
        
        if img_max - img_min < 1e-10:
            logger.warning("Image has no dynamic range, returning zeros")
            return np.zeros_like(image)
        
        # Normalize to [0, 1]
        normalized = (image - img_min) / (img_max - img_min)
        
        # Scale to target range
        target_min, target_max = target_range
        scaled = normalized * (target_max - target_min) + target_min
        
        logger.info(f"Normalized image: [{img_min:.2f}, {img_max:.2f}] -> "
                   f"[{target_min}, {target_max}]")
        return scaled
    
    except Exception as e:
        logger.error(f"Normalization failed: {e}")
        raise


def reconstruct_image(filtered_fft: np.ndarray) -> np.ndarray:
    """
    Complete reconstruction: IFFT + normalization to uint8.
    
    Args:
        filtered_fft: Filtered complex FFT array
    
    Returns:
        Reconstructed image as uint8 array
    """
    logger.info("Reconstructing image from filtered FFT")
    
    try:
        # Apply inverse FFT
        image_real = apply_ifft(filtered_fft)
        
        # Normalize to [0, 255]
        image_normalized = normalize_image(image_real, (0, 255))
        
        # Convert to uint8
        image_uint8 = image_normalized.astype(np.uint8)
        
        logger.info(f"Image reconstruction complete: shape {image_uint8.shape}, "
                   f"dtype {image_uint8.dtype}")
        return image_uint8
    
    except Exception as e:
        logger.error(f"Image reconstruction failed: {e}")
        raise


def get_reconstruction_quality(original: np.ndarray, 
                              reconstructed: np.ndarray) -> dict:
    """
    Calculate quality metrics for reconstruction.
    
    Args:
        original: Original image
        reconstructed: Reconstructed image
    
    Returns:
        Dictionary with quality metrics
    """
    try:
        # Mean Squared Error
        mse = np.mean((original.astype(float) - reconstructed.astype(float)) ** 2)
        
        # Peak Signal-to-Noise Ratio
        if mse > 0:
            psnr = 10 * np.log10((255.0 ** 2) / mse)
        else:
            psnr = float('inf')
        
        metrics = {
            'mse': float(mse),
            'psnr': float(psnr)
        }
        
        logger.debug(f"Reconstruction quality: MSE={mse:.2f}, PSNR={psnr:.2f}dB")
        return metrics
    
    except Exception as e:
        logger.error(f"Quality calculation failed: {e}")
        return {'mse': None, 'psnr': None}