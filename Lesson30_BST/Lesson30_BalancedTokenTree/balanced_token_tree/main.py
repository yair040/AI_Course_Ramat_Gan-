"""
Main Entry Point

Command-line interface for the Balanced Token Tree program.

Author: Yair Levi
"""

import sys
import argparse
import logging
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from balanced_token_tree.logger_config import setup_logging
from balanced_token_tree.tasks import run_pipeline


def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description='Balanced Token Tree - Binary tree balancing visualization',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Run with random tokens
  python main.py --seed 42          # Run with fixed seed for reproducibility
  python main.py --seed 123         # Run with different seed

Author: Yair Levi
        """
    )

    parser.add_argument(
        '--seed',
        type=int,
        default=None,
        help='Random seed for reproducible results (default: None - random)'
    )

    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Logging level (default: INFO)'
    )

    return parser.parse_args()


def main():
    """
    Main entry point for the application.
    """
    # Parse arguments
    args = parse_arguments()

    # Convert log level string to constant
    log_level = getattr(logging, args.log_level)

    # Setup logging
    setup_logging(level=log_level)

    logger = logging.getLogger(__name__)
    logger.info("Balanced Token Tree Program")
    logger.info(f"Author: Yair Levi")

    if args.seed is not None:
        logger.info(f"Random seed: {args.seed}")

    try:
        # Run the pipeline
        run_pipeline(seed=args.seed)

        logger.info("\nProgram completed successfully!")
        return 0

    except KeyboardInterrupt:
        logger.warning("\nProgram interrupted by user")
        return 130

    except Exception as e:
        logger.error(f"\nProgram failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
