"""
Low-Pass Filter implementation.
Author: Yair Levi

Implements ideal, Gaussian, and Butterworth low-pass filters.
"""

import numpy as np
from typing import Tuple, Dict, Any
from filters.base_filter import BaseFilter
from utils.logger import get_logger

logger = get_logger(__name__)


class LowPassFilter(BaseFilter):
    """Low-Pass Filter for frequency domain filtering."""
    
    def __init__(self, cutoff: float = 30.0, filter_type: str = 'ideal', order: int = 2):
        """
        Initialize Low-Pass Filter.
        
        Args:
            cutoff: Cutoff frequency (radius in pixels or percentage)
            filter_type: 'ideal', 'gaussian', or 'butterworth'
            order: Order for Butterworth filter
        """
        super().__init__(filter_type)
        self.cutoff = cutoff
        self.order = order
        logger.info(f"LPF initialized: cutoff={cutoff}, type={filter_type}, order={order}")
    
    def create_mask(self, shape: Tuple[int, int]) -> np.ndarray:
        """
        Create LPF mask for given image shape.
        
        Args:
            shape: Image shape (height, width)
        
        Returns:
            LPF mask (1 at center, 0 at edges)
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
        
        logger.debug(f"Created LPF mask: shape={shape}, cutoff={self.cutoff}")
        return mask
    
    def _create_ideal_mask(self, distance: np.ndarray) -> np.ndarray:
        """Create ideal LPF mask."""
        mask = np.zeros_like(distance, dtype=np.float32)
        mask[distance <= self.cutoff] = 1
        return mask
    
    def _create_gaussian_mask(self, distance: np.ndarray) -> np.ndarray:
        """Create Gaussian LPF mask."""
        mask = np.exp(-(distance**2) / (2 * (self.cutoff**2)))
        return mask.astype(np.float32)
    
    def _create_butterworth_mask(self, distance: np.ndarray) -> np.ndarray:
        """Create Butterworth LPF mask."""
        with np.errstate(divide='ignore', invalid='ignore'):
            mask = 1 / (1 + (distance / (self.cutoff + 1e-10))**(2 * self.order))
        mask = np.nan_to_num(mask, nan=1.0, posinf=1.0, neginf=0.0)
        return mask.astype(np.float32)
    
    def apply(self, fft_image: np.ndarray) -> np.ndarray:
        """
        Apply LPF to FFT image.
        
        Args:
            fft_image: FFT-transformed image
        
        Returns:
            Filtered FFT image
        """
        mask = self.create_mask(fft_image.shape)
        filtered = fft_image * mask
        logger.info(f"Applied LPF: kept low frequencies <= {self.cutoff}")
        return filtered
    
    def get_filter_info(self) -> Dict[str, Any]:
        """Get LPF information."""
        info = super().get_filter_info()
        info.update({
            'cutoff': self.cutoff,
            'order': self.order
        })
        return info