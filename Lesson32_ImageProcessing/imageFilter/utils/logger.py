"""
Logging utility with ring buffer configuration.
Author: Yair Levi

Implements a rotating file handler with 20 files × 16MB capacity.
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional

# Global logger registry
_loggers = {}


def setup_logger(
    name: str,
    level: int = logging.INFO,
    log_dir: Optional[Path] = None
) -> logging.Logger:
    """
    Set up a logger with ring buffer file handler.
    
    Args:
        name: Logger name (typically module name)
        level: Logging level (default: INFO)
        log_dir: Directory for log files (default: ./log/)
    
    Returns:
        Configured logger instance
    """
    if name in _loggers:
        return _loggers[name]
    
    # Determine log directory
    if log_dir is None:
        project_root = Path(__file__).parent.parent
        log_dir = project_root / 'log'
    
    # Create log directory if it doesn't exist
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Ring buffer file handler: 20 files × 16MB
    log_file = log_dir / f'{name.replace(".", "_")}.log'
    file_handler = RotatingFileHandler(
        filename=str(log_file),
        maxBytes=16 * 1024 * 1024,  # 16 MB
        backupCount=19  # 20 total files (1 current + 19 backups)
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler for errors and above
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Register logger
    _loggers[name] = logger
    
    logger.info(f"Logger '{name}' initialized at {level} level")
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get an existing logger or create a new one.
    
    Args:
        name: Logger name
    
    Returns:
        Logger instance
    """
    if name not in _loggers:
        return setup_logger(name)
    return _loggers[name]


def close_all_loggers() -> None:
    """Close all logger handlers and clear registry."""
    for logger in _loggers.values():
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)
    _loggers.clear()
    logging.info("All loggers closed")