"""
Logging configuration module with ring buffer support.
Author: Yair Levi
"""

import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pathlib import Path
from iris_classifier.config import LOG_DIR, LOG_MAX_BYTES, LOG_BACKUP_COUNT, LOG_FORMAT, LOG_LEVEL


def setup_logging():
    """
    Initialize logging system with rotating file handler.
    Creates ring buffer of 20 files, each up to 16MB.
    """
    # Ensure log directory exists
    LOG_DIR.mkdir(exist_ok=True)
    
    # Generate log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = LOG_DIR / f"iris_svm_{timestamp}.log"
    
    # Create rotating file handler
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT
    )
    
    # Create console handler
    console_handler = logging.StreamHandler()
    
    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVEL)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    return root_logger


def get_logger(name):
    """
    Get logger for specific module.
    
    Args:
        name: Module name (typically __name__)
    
    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(name)


def log_config_info(logger, config):
    """
    Log configuration information at startup.
    
    Args:
        logger: Logger instance
        config: Configuration dictionary
    """
    logger.info("="*60)
    logger.info("Iris SVM Classification System Started")
    logger.info("="*60)
    logger.info(f"Configuration: {config}")
    logger.info(f"Log directory: {LOG_DIR}")
    logger.info(f"Log rotation: {LOG_BACKUP_COUNT + 1} files × {LOG_MAX_BYTES / (1024*1024):.0f}MB")
    logger.info("="*60)