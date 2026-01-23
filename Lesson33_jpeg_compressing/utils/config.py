"""
Configuration module for JPEG Compression Analysis Tool.
Author: Yair Levi
"""

from pathlib import Path

# Project root directory (current folder)
PROJECT_ROOT = Path(__file__).parent.parent

# Quality levels for JPEG compression
QUALITY_LEVELS = [10, 20, 30, 40, 50, 60, 70, 80, 90, 95]

# Directory paths (relative to project root)
INPUT_DIR = PROJECT_ROOT / "input"
OUTPUT_DIR = PROJECT_ROOT / "output"
COMPRESSED_DIR = OUTPUT_DIR / "compressed"
DECOMPRESSED_DIR = OUTPUT_DIR / "decompressed"
METRICS_DIR = OUTPUT_DIR / "metrics"
PLOTS_DIR = OUTPUT_DIR / "plots"
LOGS_DIR = OUTPUT_DIR / "logs"

# Logging configuration
LOG_FILE_NAME = "app.log"
LOG_MAX_BYTES = 16 * 1024 * 1024  # 16MB per file
LOG_BACKUP_COUNT = 19  # Total 20 files (1 current + 19 backups)
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Histogram configuration
HISTOGRAM_BINS = 256  # For 8-bit images (0-255)
HISTOGRAM_DPI = 100
HISTOGRAM_FIGSIZE_SINGLE = (10, 6)
HISTOGRAM_FIGSIZE_GRID = (20, 8)
HISTOGRAM_GRID_ROWS = 2
HISTOGRAM_GRID_COLS = 5

# Image processing
SUPPORTED_FORMATS = [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif"]
JPEG_FORMAT = "JPEG"
PNG_FORMAT = "PNG"

# Metrics
METRIC_COLUMNS = ["Quality", "MSE", "MAE", "FileSize_KB", "CompressionRatio"]


def create_directories():
    """Create all necessary output directories if they don't exist."""
    directories = [
        INPUT_DIR,
        COMPRESSED_DIR,
        DECOMPRESSED_DIR,
        METRICS_DIR,
        PLOTS_DIR,
        LOGS_DIR,
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def get_compressed_filename(quality):
    """Generate filename for compressed image at given quality."""
    return f"compressed_q{quality}.jpg"


def get_decompressed_filename(quality):
    """Generate filename for decompressed image at given quality."""
    return f"decompressed_q{quality}.png"


def get_metrics_filename():
    """Generate filename for metrics CSV."""
    return "metrics.csv"


def get_plot_filename(plot_type):
    """Generate filename for plot."""
    plot_names = {
        "original": "byte_histogram_original.png",
        "compressed": "byte_histogram_compressed.png",
        "error": "error_vs_quality.png",
    }
    return plot_names.get(plot_type, f"{plot_type}.png")
