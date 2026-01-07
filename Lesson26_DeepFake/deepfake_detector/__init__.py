"""
DeepFake Detection Tool
Author: Yair Levi
Version: 1.0.0

A comprehensive tool for detecting deepfake manipulations in video files.
"""

__version__ = "1.0.0"
__author__ = "Yair Levi"

from .detector import DeepFakeDetector
from .config import DetectorConfig, AnalyzerConfig

__all__ = [
    "DeepFakeDetector",
    "DetectorConfig",
    "AnalyzerConfig",
]
