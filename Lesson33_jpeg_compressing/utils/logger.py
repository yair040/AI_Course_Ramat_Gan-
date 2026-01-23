"""
Logging module with ring buffer implementation.
Author: Yair Levi
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Direct configuration (avoid circular import)
PROJECT_ROOT = Path(__file__).parent.parent
LOGS_DIR = PROJECT_ROOT / "output" / "logs"
LOG_FILE_NAME = "app.log"
LOG_MAX_BYTES = 16 * 1024 * 1024  # 16MB per file
LOG_BACKUP_COUNT = 19  # Total 20 files (1 current + 19 backups)
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger(name=None):
    """
    Set up logger with ring buffer (rotating file handler).
    
    Args:
        name: Logger name. If None, returns root logger.
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    # Ensure logs directory exists
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Get or create logger
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.INFO)
    
    # Create rotating file handler (ring buffer)
    log_file_path = LOGS_DIR / LOG_FILE_NAME
    file_handler = RotatingFileHandler(
        filename=str(log_file_path),
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        mode='a',
    )
    file_handler.setLevel(logging.INFO)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        fmt=LOG_FORMAT,
        datefmt=LOG_DATE_FORMAT,
    )
    
    # Set formatter for handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def get_logger(name=None):
    """
    Get or create a logger instance.
    
    Args:
        name: Logger name. If None, returns root logger.
    
    Returns:
        logging.Logger: Logger instance.
    """
    return setup_logger(name)
