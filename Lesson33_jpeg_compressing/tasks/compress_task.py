"""
Image compression task using JPEG at multiple quality levels.
Author: Yair Levi
"""

from pathlib import Path
from PIL import Image
from multiprocessing import Pool, cpu_count

from ..utils.logger import get_logger
from ..utils.config import (
    COMPRESSED_DIR,
    get_compressed_filename,
    JPEG_FORMAT,
)

logger = get_logger(__name__)


def compress_single(args):
    """
    Compress a single image at specified quality.
    
    Args:
        args: Tuple of (image_path, quality, output_dir)
    
    Returns:
        Tuple of (quality, output_path, file_size)
    """
    image_path, quality, output_dir = args
    
    try:
        # Load image
        img = Image.open(image_path)
        
        # Generate output filename
        output_filename = get_compressed_filename(quality)
        output_path = output_dir / output_filename
        
        # Save as JPEG with specified quality
        img.save(output_path, format=JPEG_FORMAT, quality=quality)
        
        # Get file size
        file_size = output_path.stat().st_size
        
        logger.info(
            f"Compressed at Q={quality}: {output_path.name} "
            f"({file_size / 1024:.2f} KB)"
        )
        
        return quality, str(output_path), file_size
    
    except Exception as e:
        logger.error(f"Error compressing at Q={quality}: {e}")
        return quality, None, 0


def compress_image(image_path, quality_levels, output_dir=None):
    """
    Compress image at multiple quality levels using multiprocessing.
    
    Args:
        image_path: Path to input image
        quality_levels: List of JPEG quality levels (1-100)
        output_dir: Output directory (defaults to COMPRESSED_DIR)
    
    Returns:
        List of tuples: [(quality, path, size), ...]
    """
    if output_dir is None:
        output_dir = COMPRESSED_DIR
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    image_path = Path(image_path)
    
    # Validate input
    if not image_path.exists():
        logger.error(f"Input image not found: {image_path}")
        raise FileNotFoundError(f"Input image not found: {image_path}")
    
    logger.info(f"Starting compression of {image_path.name} "
                f"at {len(quality_levels)} quality levels")
    
    # Prepare arguments for multiprocessing
    compress_args = [
        (image_path, quality, output_dir)
        for quality in quality_levels
    ]
    
    # Use multiprocessing pool
    num_processes = min(len(quality_levels), cpu_count())
    logger.info(f"Using {num_processes} parallel processes")
    
    with Pool(processes=num_processes) as pool:
        results = pool.map(compress_single, compress_args)
    
    # Filter successful results
    successful_results = [r for r in results if r[1] is not None]
    
    logger.info(
        f"Compression complete: {len(successful_results)}/{len(quality_levels)} "
        f"succeeded"
    )
    
    return successful_results
