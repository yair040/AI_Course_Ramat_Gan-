"""
Error calculation task for comparing original and compressed images.
Author: Yair Levi
"""

from pathlib import Path
import numpy as np
import pandas as pd

from ..utils.logger import get_logger
from ..utils.config import METRICS_DIR, get_metrics_filename, METRIC_COLUMNS

logger = get_logger(__name__)


def calculate_mse(original, decompressed):
    """
    Calculate Mean Squared Error between two images.
    
    Args:
        original: Original image as numpy array
        decompressed: Decompressed image as numpy array
    
    Returns:
        float: MSE value
    """
    if original.shape != decompressed.shape:
        logger.warning(
            f"Shape mismatch: original {original.shape} vs "
            f"decompressed {decompressed.shape}"
        )
        return float('inf')
    
    # Convert to float to avoid overflow
    original_float = original.astype(np.float64)
    decompressed_float = decompressed.astype(np.float64)
    
    # Calculate MSE
    mse = np.mean((original_float - decompressed_float) ** 2)
    
    return float(mse)


def calculate_mae(original, decompressed):
    """
    Calculate Mean Absolute Error between two images.
    
    Args:
        original: Original image as numpy array
        decompressed: Decompressed image as numpy array
    
    Returns:
        float: MAE value
    """
    if original.shape != decompressed.shape:
        return float('inf')
    
    # Convert to float
    original_float = original.astype(np.float64)
    decompressed_float = decompressed.astype(np.float64)
    
    # Calculate MAE
    mae = np.mean(np.abs(original_float - decompressed_float))
    
    return float(mae)


def calculate_errors(original, decompressed_results, compressed_results, output_dir=None):
    """
    Calculate error metrics for all quality levels.
    
    Args:
        original: Original image as numpy array
        decompressed_results: List of (quality, array, path) tuples
        compressed_results: List of (quality, path, size) tuples
        output_dir: Output directory for CSV (defaults to METRICS_DIR)
    
    Returns:
        pandas.DataFrame: Metrics for all quality levels
    """
    if output_dir is None:
        output_dir = METRICS_DIR
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info("Calculating error metrics for all quality levels")
    
    # Create mapping from quality to file size
    size_map = {q: size for q, _, size in compressed_results}
    
    # Calculate original image size (in bytes)
    original_size = original.nbytes
    
    # Collect metrics
    metrics_data = []
    
    for quality, decompressed_array, _ in decompressed_results:
        # Calculate errors
        mse = calculate_mse(original, decompressed_array)
        mae = calculate_mae(original, decompressed_array)
        
        # Get compressed file size
        compressed_size = size_map.get(quality, 0)
        
        # Calculate compression ratio
        compression_ratio = original_size / compressed_size if compressed_size > 0 else 0
        
        # Convert size to KB
        size_kb = compressed_size / 1024
        
        metrics_data.append({
            "Quality": quality,
            "MSE": mse,
            "MAE": mae,
            "FileSize_KB": size_kb,
            "CompressionRatio": compression_ratio,
        })
        
        logger.info(
            f"Q={quality}: MSE={mse:.4f}, MAE={mae:.4f}, "
            f"Size={size_kb:.2f}KB, Ratio={compression_ratio:.2f}x"
        )
    
    # Create DataFrame
    df = pd.DataFrame(metrics_data, columns=METRIC_COLUMNS)
    df = df.sort_values("Quality")
    
    # Save to CSV
    csv_path = output_dir / get_metrics_filename()
    df.to_csv(csv_path, index=False)
    logger.info(f"Metrics saved to {csv_path}")
    
    return df
