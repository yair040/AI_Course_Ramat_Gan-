"""
Main entry point for JPEG Compression Analysis Tool.
Author: Yair Levi
"""

import argparse
import sys
from pathlib import Path
import numpy as np
from PIL import Image

from .utils.logger import get_logger
from .utils.config import (
    QUALITY_LEVELS,
    INPUT_DIR,
    create_directories,
    SUPPORTED_FORMATS,
)
from .tasks.compress_task import compress_image
from .tasks.decompress_task import decompress_images
from .tasks.error_task import calculate_errors
from .tasks.visualize_task import create_file_size_histogram, create_error_histogram

logger = get_logger(__name__)


def parse_arguments():
    """
    Parse command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="JPEG Compression Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m jpeg_compressing --input input/photo.bmp
  python -m jpeg_compressing --input input/goldhill.bmp --quality-levels 10,50,90
  python main.py --input input/photo.bmp
        """
    )
    
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to input image file (relative to project root or absolute)"
    )
    
    parser.add_argument(
        "--quality-levels",
        type=str,
        default=None,
        help="Comma-separated quality levels (default: 10,20,30,40,50,60,70,80,90,95)"
    )
    
    parser.add_argument(
        "--save-decompressed",
        action="store_true",
        help="Save decompressed images to disk (default: False)"
    )
    
    return parser.parse_args()


def validate_input_image(image_path):
    """
    Validate input image file.
    
    Args:
        image_path: Path to image file
    
    Returns:
        Path: Validated path object
    
    Raises:
        FileNotFoundError: If image doesn't exist
        ValueError: If format not supported
    """
    path = Path(image_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Input image not found: {path}")
    
    if path.suffix.lower() not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported format: {path.suffix}. "
            f"Supported: {', '.join(SUPPORTED_FORMATS)}"
        )
    
    return path


def main():
    """Main execution function."""
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Create output directories
        create_directories()
        
        # Log startup
        logger.info("=" * 60)
        logger.info("JPEG Compression Analysis Tool - Started")
        logger.info("=" * 60)
        
        # Validate input image
        input_path = validate_input_image(args.input)
        logger.info(f"Input image: {input_path}")
        
        # Parse quality levels
        if args.quality_levels:
            quality_levels = [int(q.strip()) for q in args.quality_levels.split(",")]
        else:
            quality_levels = QUALITY_LEVELS
        
        logger.info(f"Quality levels: {quality_levels}")
        
        # Load original image
        logger.info("Loading original image...")
        original_img = Image.open(input_path)
        original_array = np.array(original_img)
        logger.info(
            f"Image loaded: {original_array.shape}, "
            f"Size: {original_array.nbytes / 1024:.2f} KB"
        )
        
        # Task 1: Compress image at multiple quality levels
        logger.info("\n" + "=" * 60)
        logger.info("Task 1: Compressing image...")
        logger.info("=" * 60)
        compressed_results = compress_image(input_path, quality_levels)
        
        # Task 2: Decompress images
        logger.info("\n" + "=" * 60)
        logger.info("Task 2: Decompressing images...")
        logger.info("=" * 60)
        decompressed_results = decompress_images(
            compressed_results,
            save_to_disk=args.save_decompressed
        )
        
        # Task 3: Calculate errors
        logger.info("\n" + "=" * 60)
        logger.info("Task 3: Calculating errors...")
        logger.info("=" * 60)
        metrics_df = calculate_errors(
            original_array,
            decompressed_results,
            compressed_results
        )
        
        # Task 4: Create file size histogram
        logger.info("\n" + "=" * 60)
        logger.info("Task 4: Creating file size histogram...")
        logger.info("=" * 60)
        from .tasks.visualize_task import create_file_size_histogram
        create_file_size_histogram(original_array.nbytes, compressed_results)
        
        # Task 5: Create error histogram
        logger.info("\n" + "=" * 60)
        logger.info("Task 5: Creating error histogram...")
        logger.info("=" * 60)
        create_error_histogram(metrics_df)
        
        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("ANALYSIS COMPLETE")
        logger.info("=" * 60)
        logger.info(f"Processed {len(quality_levels)} quality levels")
        logger.info(f"MSE range: {metrics_df['MSE'].min():.4f} - {metrics_df['MSE'].max():.4f}")
        logger.info(
            f"Compression ratio range: {metrics_df['CompressionRatio'].min():.2f}x - "
            f"{metrics_df['CompressionRatio'].max():.2f}x"
        )
        logger.info("Check 'output/' directory for results")
        logger.info("=" * 60)
        
        return 0
    
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
