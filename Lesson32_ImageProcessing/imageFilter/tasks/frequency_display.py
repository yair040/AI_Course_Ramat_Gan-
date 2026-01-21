"""
Frequency spectrum visualization task.
Author: Yair Levi

Displays and saves frequency domain visualizations with proper frequency axes.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for WSL compatibility
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Optional
from utils.logger import get_logger

logger = get_logger(__name__)


def get_frequency_axes(shape):
    """
    Calculate frequency axis values for centered spectrum.
    
    Args:
        shape: Image shape (height, width)
    
    Returns:
        Tuple of (freq_y, freq_x) arrays centered at zero
    """
    rows, cols = shape
    
    # Frequency values from -0.5 to 0.5 (normalized)
    freq_y = np.fft.fftshift(np.fft.fftfreq(rows))
    freq_x = np.fft.fftshift(np.fft.fftfreq(cols))
    
    return freq_y, freq_x


def visualize_spectrum(magnitude: np.ndarray, title: str = "Frequency Spectrum",
                       show: bool = False) -> plt.Figure:
    """
    Visualize magnitude spectrum with proper frequency axes.
    
    Args:
        magnitude: Magnitude spectrum array (already shifted)
        title: Plot title
        show: Whether to display interactively
    
    Returns:
        Matplotlib figure object
    """
    logger.info(f"Visualizing spectrum: {title}")
    
    try:
        # Apply logarithmic scaling for better visualization
        spectrum_log = 20 * np.log10(magnitude + 1)
        
        # Get frequency axes
        freq_y, freq_x = get_frequency_axes(magnitude.shape)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Display spectrum with proper extent
        extent = [freq_x[0], freq_x[-1], freq_y[-1], freq_y[0]]
        im = ax.imshow(spectrum_log, cmap='gray', interpolation='nearest',
                      extent=extent, aspect='auto')
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('Frequency X (cycles/pixel)', fontsize=12)
        ax.set_ylabel('Frequency Y (cycles/pixel)', fontsize=12)
        
        # Add grid at zero frequencies
        ax.axhline(y=0, color='r', linestyle='--', linewidth=0.5, alpha=0.5)
        ax.axvline(x=0, color='r', linestyle='--', linewidth=0.5, alpha=0.5)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Magnitude (dB)', fontsize=12)
        
        plt.tight_layout()
        
        if show:
            plt.show()
        
        logger.info(f"Spectrum visualization created: {title}")
        return fig
    
    except Exception as e:
        logger.error(f"Spectrum visualization failed: {e}")
        raise


def save_spectrum(magnitude: np.ndarray, output_path: Path, 
                  title: str = "Frequency Spectrum") -> None:
    """
    Save magnitude spectrum to file.
    
    Args:
        magnitude: Magnitude spectrum array
        output_path: Path to save image
        title: Plot title
    """
    logger.info(f"Saving spectrum to {output_path}")
    
    try:
        fig = visualize_spectrum(magnitude, title, show=False)
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save figure
        fig.savefig(str(output_path), dpi=150, bbox_inches='tight')
        plt.close(fig)
        
        logger.info(f"Spectrum saved successfully: {output_path.name}")
    
    except Exception as e:
        logger.error(f"Failed to save spectrum: {e}")
        raise


def plot_comparison(original: np.ndarray, spectrum: np.ndarray,
                   output_path: Optional[Path] = None, 
                   show: bool = False) -> plt.Figure:
    """
    Create side-by-side comparison of original and spectrum.
    
    Args:
        original: Original image
        spectrum: Magnitude spectrum
        output_path: Optional path to save comparison
        show: Whether to display interactively
    
    Returns:
        Matplotlib figure object
    """
    logger.info("Creating original vs. spectrum comparison")
    
    try:
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # Original image
        axes[0].imshow(original, cmap='gray')
        axes[0].set_title('Original Image', fontsize=14, fontweight='bold')
        axes[0].axis('off')
        
        # Spectrum with frequency axes
        spectrum_log = 20 * np.log10(spectrum + 1)
        freq_y, freq_x = get_frequency_axes(spectrum.shape)
        extent = [freq_x[0], freq_x[-1], freq_y[-1], freq_y[0]]
        
        im = axes[1].imshow(spectrum_log, cmap='gray', extent=extent, aspect='auto')
        axes[1].set_title('Frequency Spectrum', fontsize=14, fontweight='bold')
        axes[1].set_xlabel('Frequency X (cycles/pixel)', fontsize=10)
        axes[1].set_ylabel('Frequency Y (cycles/pixel)', fontsize=10)
        axes[1].axhline(y=0, color='r', linestyle='--', linewidth=0.5, alpha=0.5)
        axes[1].axvline(x=0, color='r', linestyle='--', linewidth=0.5, alpha=0.5)
        
        # Add colorbar to spectrum
        plt.colorbar(im, ax=axes[1], fraction=0.046, pad=0.04)
        
        plt.tight_layout()
        
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(str(output_path), dpi=150, bbox_inches='tight')
            logger.info(f"Comparison saved: {output_path.name}")
        
        if show:
            plt.show()
        else:
            plt.close(fig)
        
        return fig
    
    except Exception as e:
        logger.error(f"Comparison plot failed: {e}")
        raise