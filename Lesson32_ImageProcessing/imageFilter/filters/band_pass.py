"""
Band-Pass Filter implementation.
Author: Yair Levi

Implements ideal, Gaussian, and Butterworth band-pass filters.
"""

import numpy as np
from typing import Tuple, Dict, Any
from filters.base_filter import BaseFilter
from utils.logger import get_logger

logger = get_logger(__name__)


class BandPassFilter(BaseFilter):
    """Band-Pass Filter for frequency domain filtering."""
    
    def __init__(self, low_cutoff: float = 20.0, high_cutoff: float = 80.0, 
                 filter_type: str = 'ideal', order: int = 2):
        """
        Initialize Band-Pass Filter.
        
        Args:
            low_cutoff: Lower cutoff frequency (inner radius)
            high_cutoff: Higher cutoff frequency (outer radius)
            filter_type: 'ideal', 'gaussian', or 'butterworth'
            order: Order for Butterworth filter
        """
        super().__init__(filter_type)
        self.low_cutoff = low_cutoff
        self.high_cutoff = high_cutoff
        self.order = order
        logger.info(f"BPF initialized: low={low_cutoff}, high={high_cutoff}, "
                   f"type={filter_type}, order={order}")
    
    def create_mask(self, shape: Tuple[int, int]) -> np.ndarray:
        """
        Create BPF mask for given image shape.
        
        Args:
            shape: Image shape (height, width)
        
        Returns:
            BPF mask (1 in band, 0 elsewhere)
        """
        distance = self.create_distance_matrix(shape)
        
        if self.filter_type == 'ideal':
            mask = self._create_ideal_mask(distance)
        elif self.filter_type == 'gaussian':
            mask = self._create_gaussian_mask(distance)
        elif self.filter_type == 'butterworth':
            mask = self._create_butterworth_mask(distance)
        else:
            logger.warning(f"Unknown filter type: {self.filter_type}, using ideal")
            mask = self._create_ideal_mask(distance)
        
        logger.debug(f"Created BPF mask: shape={shape}, "
                    f"band=[{self.low_cutoff}, {self.high_cutoff}]")
        return mask
    
    def _create_ideal_mask(self, distance: np.ndarray) -> np.ndarray:
        """Create ideal BPF mask."""
        mask = np.zeros_like(distance, dtype=np.float32)
        mask[(distance > self.low_cutoff) & (distance < self.high_cutoff)] = 1
        return mask
    
    def _create_gaussian_mask(self, distance: np.ndarray) -> np.ndarray:
        """Create Gaussian BPF mask."""
        center = (self.low_cutoff + self.high_cutoff) / 2
        width = (self.high_cutoff - self.low_cutoff) / 2
        mask = np.exp(-((distance - center)**2) / (2 * (width**2)))
        return mask.astype(np.float32)
    
    def _create_butterworth_mask(self, distance: np.ndarray) -> np.ndarray:
        """Create Butterworth BPF mask."""
        center = (self.low_cutoff + self.high_cutoff) / 2
        width = (self.high_cutoff - self.low_cutoff) / 2
        
        with np.errstate(divide='ignore', invalid='ignore'):
            mask = 1 / (1 + ((distance - center) / width)**(2 * self.order))
        mask = np.nan_to_num(mask, nan=0.0, posinf=1.0, neginf=0.0)
        return mask.astype(np.float32)
    
    def apply(self, fft_image: np.ndarray) -> np.ndarray:
        """
        Apply BPF to FFT image.
        
        Args:
            fft_image: FFT-transformed image
        
        Returns:
            Filtered FFT image
        """
        mask = self.create_mask(fft_image.shape)
        filtered = fft_image * mask
        logger.info(f"Applied BPF: passed frequencies "
                   f"[{self.low_cutoff}, {self.high_cutoff}]")
        return filtered
    
    def get_filter_info(self) -> Dict[str, Any]:
        """Get BPF information."""
        info = super().get_filter_info()
        info.update({
            'low_cutoff': self.low_cutoff,
            'high_cutoff': self.high_cutoff,
            'order': self.order
        })
        return info