"""
Image display and comparison task.
Author: Yair Levi

Visualizes original and filtered images with comparison grids.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for WSL
import matplotlib.pyplot as plt
from pathlib import Path
from typing import List, Optional, Dict
from utils.logger import get_logger

logger = get_logger(__name__)


def display_images(images: List[np.ndarray], titles: List[str],
                  save_path: Optional[Path] = None, 
                  show: bool = False) -> plt.Figure:
    """
    Display multiple images in a grid.
    
    Args:
        images: List of images to display
        titles: List of titles for each image
        save_path: Optional path to save figure
        show: Whether to display interactively
    
    Returns:
        Matplotlib figure object
    """
    if len(images) != len(titles):
        logger.error("Number of images and titles must match")
        raise ValueError("Images and titles length mismatch")
    
    logger.info(f"Displaying {len(images)} images")
    
    try:
        n_images = len(images)
        cols = min(3, n_images)
        rows = (n_images + cols - 1) // cols
        
        fig, axes = plt.subplots(rows, cols, figsize=(5*cols, 5*rows))
        
        # Handle single image case
        if n_images == 1:
            axes = np.array([axes])
        axes = axes.flatten()
        
        for idx, (image, title) in enumerate(zip(images, titles)):
            axes[idx].imshow(image, cmap='gray')
            axes[idx].set_title(title, fontsize=12, fontweight='bold')
            axes[idx].axis('off')
        
        # Hide extra subplots
        for idx in range(n_images, len(axes)):
            axes[idx].axis('off')
        
        plt.tight_layout()
        
        if save_path:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(str(save_path), dpi=150, bbox_inches='tight')
            logger.info(f"Images saved to {save_path.name}")
        
        if show:
            plt.show()
        else:
            plt.close(fig)
        
        return fig
    
    except Exception as e:
        logger.error(f"Image display failed: {e}")
        raise


def create_comparison(original: np.ndarray, filtered_dict: Dict[str, np.ndarray],
                     output_path: Optional[Path] = None,
                     show: bool = False) -> plt.Figure:
    """
    Create comparison grid: original vs. filtered results.
    
    Args:
        original: Original image
        filtered_dict: Dictionary of {filter_name: filtered_image}
        output_path: Optional path to save comparison
        show: Whether to display interactively
    
    Returns:
        Matplotlib figure object
    """
    logger.info(f"Creating comparison with {len(filtered_dict)} filtered versions")
    
    try:
        images = [original]
        titles = ['Original Image']
        
        for filter_name, filtered_img in filtered_dict.items():
            images.append(filtered_img)
            titles.append(f'Filtered: {filter_name}')
        
        fig = display_images(images, titles, save_path=output_path, show=show)
        
        logger.info("Comparison created successfully")
        return fig
    
    except Exception as e:
        logger.error(f"Comparison creation failed: {e}")
        raise


def save_comparison_grid(images_dict: Dict[str, np.ndarray], 
                        output_path: Path) -> None:
    """
    Save comparison grid from dictionary of images.
    
    Args:
        images_dict: Dictionary of {label: image}
        output_path: Path to save comparison
    """
    logger.info(f"Saving comparison grid with {len(images_dict)} images")
    
    try:
        images = list(images_dict.values())
        titles = list(images_dict.keys())
        
        display_images(images, titles, save_path=output_path, show=False)
        
        logger.info(f"Comparison grid saved: {output_path.name}")
    
    except Exception as e:
        logger.error(f"Failed to save comparison grid: {e}")
        raise


def create_side_by_side(image1: np.ndarray, image2: np.ndarray,
                       title1: str = "Image 1", title2: str = "Image 2",
                       output_path: Optional[Path] = None,
                       show: bool = False) -> plt.Figure:
    """
    Create simple side-by-side comparison of two images.
    
    Args:
        image1: First image
        image2: Second image
        title1: Title for first image
        title2: Title for second image
        output_path: Optional path to save comparison
        show: Whether to display interactively
    
    Returns:
        Matplotlib figure object
    """
    logger.info(f"Creating side-by-side: {title1} vs {title2}")
    
    return display_images([image1, image2], [title1, title2], 
                         save_path=output_path, show=show)