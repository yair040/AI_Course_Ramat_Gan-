"""
Base filter class for frequency domain filtering.
Author: Yair Levi

Provides abstract base class and common utilities for filters.
"""

from abc import ABC, abstractmethod
import numpy as np
from typing import Dict, Any, Tuple
from utils.logger import get_logger

logger = get_logger(__name__)


class BaseFilter(ABC):
    """Abstract base class for frequency domain filters."""
    
    def __init__(self, filter_type: str = 'ideal'):
        """
        Initialize base filter.
        
        Args:
            filter_type: Type of filter ('ideal', 'gaussian', 'butterworth')
        """
        self.filter_type = filter_type
        logger.info(f"Initialized {self.__class__.__name__} with type: {filter_type}")
    
    @abstractmethod
    def create_mask(self, shape: Tuple[int, int]) -> np.ndarray:
        """
        Create filter mask for given image shape.
        
        Args:
            shape: Image shape (height, width)
        
        Returns:
            Filter mask as numpy array
        """
        pass
    
    @abstractmethod
    def apply(self, fft_image: np.ndarray) -> np.ndarray:
        """
        Apply filter to FFT image.
        
        Args:
            fft_image: FFT-transformed image
        
        Returns:
            Filtered FFT image
        """
        pass
    
    def get_filter_info(self) -> Dict[str, Any]:
        """
        Get filter parameters and information.
        
        Returns:
            Dictionary with filter information
        """
        return {
            'name': self.__class__.__name__,
            'type': self.filter_type
        }
    
    @staticmethod
    def create_distance_matrix(shape: Tuple[int, int]) -> np.ndarray:
        """
        Create distance matrix from center of image.
        
        Args:
            shape: Image shape (height, width)
        
        Returns:
            Distance matrix
        """
        rows, cols = shape
        crow, ccol = rows // 2, cols // 2
        
        # Create coordinate grids
        y, x = np.ogrid[:rows, :cols]
        
        # Calculate distance from center
        distance = np.sqrt((x - ccol)**2 + (y - crow)**2)
        
        return distance
    
    @staticmethod
    def normalize_mask(mask: np.ndarray) -> np.ndarray:
        """
        Normalize mask to [0, 1] range.
        
        Args:
            mask: Filter mask
        
        Returns:
            Normalized mask
        """
        if mask.max() > 0:
            return mask / mask.max()
        return mask