"""
Main entry point for Triangle Edge Detection System.
Author: Yair Levi
"""

import sys
import argparse
from typing import Optional
from config import logger, IMAGE_WIDTH, IMAGE_HEIGHT, FILTER_CUTOFF_RADIUS
from tasks import run_all_tasks


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description='Triangle Edge Detection System',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        '--width',
        type=int,
        default=IMAGE_WIDTH,
        help='Image width in pixels'
    )
    
    parser.add_argument(
        '--height',
        type=int,
        default=IMAGE_HEIGHT,
        help='Image height in pixels'
    )
    
    parser.add_argument(
        '--cutoff',
        type=float,
        default=FILTER_CUTOFF_RADIUS,
        help='High-pass filter cutoff radius'
    )
    
    return parser.parse_args()


def main() -> int:
    """
    Main function to execute the pipeline.
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    try:
        # Parse arguments
        args = parse_arguments()
        
        logger.info("Triangle Edge Detection and Reconstruction System")
        logger.info(f"Configuration: width={args.width}, height={args.height}, "
                   f"cutoff={args.cutoff}")
        logger.info("Fixed threshold: 48 (non-interactive mode)")
        
        # Prepare configuration
        config = {
            'width': args.width,
            'height': args.height,
            'cutoff_radius': args.cutoff
        }
        
        # Run all tasks
        results = run_all_tasks(config)
        
        logger.info("Program completed successfully")
        return 0
    
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
        return 130  # Standard exit code for Ctrl+C
    
    except Exception as e:
        logger.error(f"Program failed with error: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())