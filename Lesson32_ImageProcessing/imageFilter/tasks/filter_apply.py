"""
Filter application task with multiprocessing support.
Author: Yair Levi

Applies frequency filters to FFT images, with parallel processing capability.
"""

import numpy as np
from pathlib import Path
from typing import List, Tuple, Optional
from multiprocessing import Pool, cpu_count
from filters.base_filter import BaseFilter
from utils.logger import get_logger

logger = get_logger(__name__)


def apply_filter(fft_image: np.ndarray, filter_obj: BaseFilter) -> np.ndarray:
    """
    Apply a single filter to FFT image.
    
    Args:
        fft_image: Complex FFT array
        filter_obj: Filter object to apply
    
    Returns:
        Filtered FFT array
    
    Raises:
        ValueError: If inputs are invalid
    """
    if fft_image is None or fft_image.size == 0:
        logger.error("Cannot apply filter to empty FFT image")
        raise ValueError("FFT image is empty or None")
    
    logger.info(f"Applying filter: {filter_obj.get_filter_info()['name']}")
    
    try:
        filtered_fft = filter_obj.apply(fft_image)
        logger.info(f"Filter applied successfully")
        return filtered_fft
    
    except Exception as e:
        logger.error(f"Filter application failed: {e}")
        raise


def _process_single_filter(args: Tuple[np.ndarray, BaseFilter]) -> Tuple[str, np.ndarray]:
    """
    Helper function for multiprocessing filter application.
    
    Args:
        args: Tuple of (fft_image, filter_object)
    
    Returns:
        Tuple of (filter_name, filtered_fft)
    """
    fft_image, filter_obj = args
    filter_name = filter_obj.get_filter_info()['name']
    
    try:
        filtered = apply_filter(fft_image, filter_obj)
        return (filter_name, filtered)
    except Exception as e:
        logger.error(f"Error processing filter {filter_name}: {e}")
        return (filter_name, None)


def apply_filters_parallel(fft_image: np.ndarray, 
                          filters: List[BaseFilter],
                          num_processes: Optional[int] = None) -> dict:
    """
    Apply multiple filters in parallel.
    
    Args:
        fft_image: Complex FFT array
        filters: List of filter objects
        num_processes: Number of processes (default: CPU count)
    
    Returns:
        Dictionary mapping filter names to filtered FFT arrays
    """
    if not filters:
        logger.warning("No filters provided for parallel processing")
        return {}
    
    if num_processes is None:
        num_processes = min(len(filters), cpu_count())
    
    logger.info(f"Applying {len(filters)} filters in parallel with {num_processes} processes")
    
    try:
        # Prepare arguments for multiprocessing
        args_list = [(fft_image, filter_obj) for filter_obj in filters]
        
        # Process filters in parallel
        with Pool(processes=num_processes) as pool:
            results = pool.map(_process_single_filter, args_list)
        
        # Convert results to dictionary
        results_dict = {name: filtered for name, filtered in results if filtered is not None}
        
        logger.info(f"Parallel filtering completed: {len(results_dict)} filters successful")
        return results_dict
    
    except Exception as e:
        logger.error(f"Parallel filter processing failed: {e}")
        # Fallback to sequential processing
        logger.info("Falling back to sequential processing")
        return apply_filters_sequential(fft_image, filters)


def apply_filters_sequential(fft_image: np.ndarray, 
                            filters: List[BaseFilter]) -> dict:
    """
    Apply multiple filters sequentially.
    
    Args:
        fft_image: Complex FFT array
        filters: List of filter objects
    
    Returns:
        Dictionary mapping filter names to filtered FFT arrays
    """
    results = {}
    
    for filter_obj in filters:
        filter_name = filter_obj.get_filter_info()['name']
        try:
            filtered = apply_filter(fft_image, filter_obj)
            results[filter_name] = filtered
        except Exception as e:
            logger.error(f"Failed to apply filter {filter_name}: {e}")
    
    return results