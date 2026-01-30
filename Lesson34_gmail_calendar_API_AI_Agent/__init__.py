"""
Gmail Event Scanner & Calendar Integration Package

This package provides automated scanning of Gmail for meeting invitations
and integration with Google Calendar using AI-powered email parsing.

Author: Yair Levi
Version: 1.0.0
Date: January 29, 2026
"""

__version__ = "1.0.0"
__author__ = "Yair Levi"
__email__ = "yair0@example.com"

from .main import main
from .tasks import run_one_time_mode, run_polling_mode

__all__ = [
    'main',
    'run_one_time_mode',
    'run_polling_mode',
]
