"""
Utility Module

Provides logging setup, credential management, and helper functions.

Author: Yair Levi
"""

import json
import logging
import pickle
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from config import (
    API_KEY_FILE,
    TOKEN_FILE,
    LOG_DIR,
    LOG_FILE_NAME,
    LOG_MAX_BYTES,
    LOG_BACKUP_COUNT,
    LOG_FORMAT,
    LOG_DATE_FORMAT,
    LOG_LEVEL
)


# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging() -> logging.Logger:
    """
    Set up logging with rotating file handler (ring buffer).

    Creates a ring buffer of 20 log files, each up to 16MB.
    When the last file is full, the first file starts to be overwritten.

    Returns:
        Configured logger instance
    """
    # Ensure log directory exists
    LOG_DIR.mkdir(exist_ok=True)

    # Create logger
    logger = logging.getLogger("lost_in_middle")
    logger.setLevel(getattr(logging, LOG_LEVEL))

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # Create rotating file handler
    log_file_path = LOG_DIR / LOG_FILE_NAME
    handler = RotatingFileHandler(
        log_file_path,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding='utf-8'
    )

    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)

    # Also add console handler for user feedback
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.info("Logging initialized successfully")
    logger.info(f"Log directory: {LOG_DIR}")
    logger.info(f"Ring buffer: {LOG_BACKUP_COUNT + 1} files × {LOG_MAX_BYTES / (1024*1024):.0f}MB")

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(f"lost_in_middle.{name}")


# ============================================================================
# CREDENTIAL MANAGEMENT
# ============================================================================

def load_credentials() -> str:
    """
    Load Anthropic API key from api_key.dat file.

    Returns:
        API key string

    Raises:
        FileNotFoundError: If api_key.dat not found
        ValueError: If API key is empty
    """
    logger = get_logger(__name__)

    if not API_KEY_FILE.exists():
        error_msg = f"API key file not found: {API_KEY_FILE}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    try:
        with open(API_KEY_FILE, 'r', encoding='utf-8') as f:
            api_key = f.read().strip()

        if not api_key:
            raise ValueError("API key is empty or invalid")

        # CRITICAL: Never log the actual API key
        logger.info("API key loaded successfully")
        logger.info(f"API key length: {len(api_key)} characters")

        return api_key

    except Exception as e:
        logger.error(f"Error loading API key: {e}")
        raise


def load_token() -> Optional[dict]:
    """
    Load token from token.pickle file if it exists.

    Returns:
        Token dictionary or None if file doesn't exist
    """
    logger = get_logger(__name__)

    if not TOKEN_FILE.exists():
        logger.info("Token file not found (this is optional)")
        return None

    try:
        with open(TOKEN_FILE, 'rb') as f:
            token = pickle.load(f)

        logger.info("Token loaded successfully")
        return token

    except Exception as e:
        logger.warning(f"Error loading token (continuing anyway): {e}")
        return None


# ============================================================================
# FILE OPERATIONS
# ============================================================================

def count_words(text: str) -> int:
    """
    Count words in text.

    Args:
        text: Text to count words in

    Returns:
        Number of words
    """
    return len(text.split())


def read_file(file_path: Path) -> str:
    """
    Read text file and return contents.

    Args:
        file_path: Path to file

    Returns:
        File contents as string

    Raises:
        FileNotFoundError: If file doesn't exist
        IOError: If file cannot be read
    """
    logger = get_logger(__name__)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        logger.info(f"Read file: {file_path.name} ({count_words(content)} words)")
        return content

    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        raise IOError(f"Cannot read file: {file_path}") from e


def write_file(file_path: Path, content: str) -> None:
    """
    Write content to text file.

    Args:
        file_path: Path to file
        content: Content to write

    Raises:
        IOError: If file cannot be written
    """
    logger = get_logger(__name__)

    try:
        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"Wrote file: {file_path.name} ({count_words(content)} words)")

    except Exception as e:
        logger.error(f"Error writing file {file_path}: {e}")
        raise IOError(f"Cannot write file: {file_path}") from e
