"""
Main program for Iris SVM Classification System
Hierarchical classification using two-stage SVM approach
Author: Yair Levi
"""

import sys
import time
from iris_classifier.logger_setup import setup_logging, get_logger, log_config_info
from iris_classifier.config import Config
from iris_classifier.iteration_runner import run_with_multiprocessing
from iris_classifier.output_formatter import print_summary
from tasks.task_analysis import analyze_results


def main():
    """Main entry point."""
    # Initialize logging
    setup_logging()
    logger = get_logger(__name__)
    
    # Load and validate configuration
    try:
        config = Config()
        log_config_info(logger, config.get_config_summary())
    except Exception as e:
        logger.critical(f"Configuration error: {e}")
        sys.exit(1)
    
    # Record start time
    start_time = time.time()
    
    try:
        # Run iterations with multiprocessing
        logger.info("Starting Iris SVM Classification System")
        all_results = run_with_multiprocessing()
        
        # Analyze results
        aggregated_stats = analyze_results(all_results)
        
        # Calculate total runtime
        total_time = time.time() - start_time
        logger.info(f"Total runtime: {total_time:.2f} seconds")
        
        # Print summary to console
        print_summary(aggregated_stats)
        
        logger.info("Program completed successfully")
        sys.exit(0)
    
    except Exception as e:
        logger.critical(f"Program failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()