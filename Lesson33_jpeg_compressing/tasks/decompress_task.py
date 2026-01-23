"""
Image decompression task.
Author: Yair Levi
"""

from pathlib import Path
import numpy as np
from PIL import Image
from multiprocessing import Pool, cpu_count

from ..utils.logger import get_logger
from ..utils.config import DECOMPRESSED_DIR, get_decompressed_filename, PNG_FORMAT

logger = get_logger(__name__)


def decompress_single(args):
    """
    Decompress a single JPEG image.
    
    Args:
        args: Tuple of (compressed_path, quality, output_dir, save_to_disk)
    
    Returns:
        Tuple of (quality, numpy_array, output_path)
    """
    compressed_path, quality, output_dir, save_to_disk = args
    
    try:
        # Load compressed image
        img = Image.open(compressed_path)
        
        # Convert to numpy array
        img_array = np.array(img)
        
        # Optionally save decompressed image
        output_path = None
        if save_to_disk:
            output_filename = get_decompressed_filename(quality)
            output_path = output_dir / output_filename
            img.save(output_path, format=PNG_FORMAT)
            logger.info(f"Decompressed Q={quality}: {output_path.name}")
        else:
            logger.info(f"Decompressed Q={quality} (in-memory only)")
        
        return quality, img_array, str(output_path) if output_path else None
    
    except Exception as e:
        logger.error(f"Error decompressing Q={quality}: {e}")
        return quality, None, None


def decompress_images(compressed_results, output_dir=None, save_to_disk=False):
    """
    Decompress multiple JPEG images using multiprocessing.
    
    Args:
        compressed_results: List of tuples from compress_task
        output_dir: Output directory (defaults to DECOMPRESSED_DIR)
        save_to_disk: Whether to save decompressed images to disk
    
    Returns:
        List of tuples: [(quality, numpy_array, path), ...]
    """
    if output_dir is None:
        output_dir = DECOMPRESSED_DIR
    
    output_dir = Path(output_dir)
    if save_to_disk:
        output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Starting decompression of {len(compressed_results)} images")
    
    # Prepare arguments for multiprocessing
    decompress_args = [
        (result[1], result[0], output_dir, save_to_disk)
        for result in compressed_results
    ]
    
    # Use multiprocessing pool
    num_processes = min(len(compressed_results), cpu_count())
    logger.info(f"Using {num_processes} parallel processes")
    
    with Pool(processes=num_processes) as pool:
        results = pool.map(decompress_single, decompress_args)
    
    # Filter successful results
    successful_results = [r for r in results if r[1] is not None]
    
    logger.info(
        f"Decompression complete: {len(successful_results)}/"
        f"{len(compressed_results)} succeeded"
    )
    
    return successful_results
