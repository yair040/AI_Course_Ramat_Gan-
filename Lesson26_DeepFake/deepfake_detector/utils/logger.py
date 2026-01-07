"""
Ring buffer logging system.
Author: Yair Levi
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


class RingBufferLogger:
    """Logger with ring buffer (20 files × 16MB)."""
    
    MAX_BYTES = 16 * 1024 * 1024  # 16MB
    BACKUP_COUNT = 19  # 20 total files (1 current + 19 backups)
    
    def __init__(self, log_dir: Path, log_level: str = 'INFO',
                 console: bool = True, file: bool = True):
        """Initialize ring buffer logger."""
        self.log_dir = log_dir
        self.log_dir.mkdir(exist_ok=True)
        self.log_file = self.log_dir / 'deepfake.log'
        
        # Create logger
        self.logger = logging.getLogger('deepfake_detector')
        self.logger.setLevel(getattr(logging, log_level.upper()))
        self.logger.handlers.clear()
        
        # Create formatter
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler with rotation
        if file:
            file_handler = RotatingFileHandler(
                filename=str(self.log_file),
                maxBytes=self.MAX_BYTES,
                backupCount=self.BACKUP_COUNT,
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        
        # Console handler
        if console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
    
    def get_logger(self, name: Optional[str] = None) -> logging.Logger:
        """Get logger instance."""
        if name:
            return logging.getLogger(f'deepfake_detector.{name}')
        return self.logger
    
    def debug(self, msg: str, **kwargs):
        """Log debug message."""
        self.logger.debug(msg, **kwargs)
    
    def info(self, msg: str, **kwargs):
        """Log info message."""
        self.logger.info(msg, **kwargs)
    
    def warning(self, msg: str, **kwargs):
        """Log warning message."""
        self.logger.warning(msg, **kwargs)
    
    def error(self, msg: str, **kwargs):
        """Log error message."""
        self.logger.error(msg, **kwargs)
    
    def critical(self, msg: str, **kwargs):
        """Log critical message."""
        self.logger.critical(msg, **kwargs)


# Global logger instance
_logger_instance: Optional[RingBufferLogger] = None


def setup_logger(log_dir: Path, log_level: str = 'INFO',
                 console: bool = True, file: bool = True) -> RingBufferLogger:
    """Setup and return global logger instance."""
    global _logger_instance
    _logger_instance = RingBufferLogger(log_dir, log_level, console, file)
    return _logger_instance


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get logger instance."""
    if _logger_instance is None:
        raise RuntimeError("Logger not initialized. Call setup_logger first.")
    return _logger_instance.get_logger(name)
