"""
Logging Setup Module
Configures ring buffer logging system with 20 files, 16MB each.

Author: Yair Levi
"""

import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger(name='gmail_scanner', log_level='INFO'):
    """
    Configure logger with ring buffer file rotation.
    
    Args:
        name: Logger name
        log_level: Minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    if logger.handlers:
        return logger
    
    log_dir = os.path.join(os.path.dirname(__file__), 'log')
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, 'app.log')
    
    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=16 * 1024 * 1024,
        backupCount=19,
        encoding='utf-8'
    )
    
    console_handler = logging.StreamHandler()
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(processName)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def get_logger(name='gmail_scanner'):
    """Get existing logger or create new one."""
    return logging.getLogger(name)
