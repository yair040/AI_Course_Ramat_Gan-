"""
Path handling utilities for relative path management.
Author: Yair Levi

Provides functions for resolving project-relative paths on WSL.
"""

from pathlib import Path
from typing import Union


def get_project_root() -> Path:
    """
    Get the project root directory.
    
    Returns:
        Path to project root
    """
    # This file is in utils/, so parent.parent is project root
    return Path(__file__).parent.parent


def get_venv_path() -> Path:
    """
    Get the virtual environment path (../../venv/).
    
    Returns:
        Path to virtual environment
    """
    return get_project_root().parent.parent / 'venv'


def get_input_path(filename: str = '') -> Path:
    """
    Get path to input directory or specific input file.
    
    Args:
        filename: Optional filename within input directory
    
    Returns:
        Path to input directory or file
    """
    input_dir = get_project_root() / 'input'
    return input_dir / filename if filename else input_dir


def get_output_path(filename: str = '') -> Path:
    """
    Get path to output directory or specific output file.
    
    Args:
        filename: Optional filename within output directory
    
    Returns:
        Path to output directory or file
    """
    output_dir = get_project_root() / 'output'
    return output_dir / filename if filename else output_dir


def get_log_path() -> Path:
    """
    Get path to log directory.
    
    Returns:
        Path to log directory
    """
    return get_project_root() / 'log'


def ensure_directory(path: Union[str, Path]) -> Path:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        path: Directory path to ensure exists
    
    Returns:
        Path object for the directory
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def resolve_relative_path(path: Union[str, Path], base: Path = None) -> Path:
    """
    Resolve a path relative to a base directory.
    
    Args:
        path: Path to resolve
        base: Base directory (default: project root)
    
    Returns:
        Resolved absolute path
    """
    if base is None:
        base = get_project_root()
    
    path = Path(path)
    if path.is_absolute():
        return path
    return (base / path).resolve()


def validate_path_exists(path: Union[str, Path], path_type: str = 'file') -> bool:
    """
    Check if a path exists and is of the expected type.
    
    Args:
        path: Path to validate
        path_type: 'file' or 'directory'
    
    Returns:
        True if path exists and matches type
    """
    path = Path(path)
    if not path.exists():
        return False
    
    if path_type == 'file':
        return path.is_file()
    elif path_type == 'directory':
        return path.is_dir()
    return False