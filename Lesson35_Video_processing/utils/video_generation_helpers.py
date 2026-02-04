"""
Video generation helper functions.

This module contains helper functions for generating test videos in Task 3.

Author: Yair Levi
"""

from pathlib import Path
from typing import Tuple

from PIL import Image, ImageDraw

from ..config import (
    DEFAULT_OBJECT_WIDTH,
    DEFAULT_OBJECT_HEIGHT,
    DEFAULT_OBJECT_COLOR,
    DEFAULT_BACKGROUND_COLOR
)


def calculate_diagonal_position(
    frame_num: int,
    total_frames: int,
    width: int,
    height: int,
    obj_width: int,
    obj_height: int
) -> Tuple[int, int]:
    """
    Calculate object position for linear diagonal movement.
    
    Args:
        frame_num: Current frame number (0-indexed)
        total_frames: Total number of frames
        width: Video width in pixels
        height: Video height in pixels
        obj_width: Object width in pixels
        obj_height: Object height in pixels
    
    Returns:
        tuple: (x, y) position for the object
    """
    # Calculate progress from 0.0 to 1.0
    progress = frame_num / (total_frames - 1) if total_frames > 1 else 0
    
    # Calculate position (top-left to bottom-right)
    x = int(progress * (width - obj_width))
    y = int(progress * (height - obj_height))
    
    return x, y


def create_frame_with_object(
    width: int,
    height: int,
    obj_x: int,
    obj_y: int,
    obj_width: int = DEFAULT_OBJECT_WIDTH,
    obj_height: int = DEFAULT_OBJECT_HEIGHT,
    obj_color: Tuple[int, int, int] = DEFAULT_OBJECT_COLOR,
    bg_color: Tuple[int, int, int] = DEFAULT_BACKGROUND_COLOR
) -> Image.Image:
    """
    Create a single frame with object at specified position.
    
    Args:
        width: Frame width in pixels
        height: Frame height in pixels
        obj_x: Object x position
        obj_y: Object y position
        obj_width: Object width in pixels
        obj_height: Object height in pixels
        obj_color: Object RGB color tuple
        bg_color: Background RGB color tuple
    
    Returns:
        PIL.Image: Generated frame
    """
    # Create background
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw rectangle
    draw.rectangle(
        [obj_x, obj_y, obj_x + obj_width, obj_y + obj_height],
        fill=obj_color
    )
    
    return img


def print_generation_report(
    output_path: Path,
    width: int,
    height: int,
    fps: int,
    duration: int,
    frame_count: int,
    processing_time: float
) -> None:
    """Print formatted test video generation report."""
    print("\n" + "=" * 70)
    print("TEST VIDEO GENERATION REPORT")
    print("=" * 70)
    
    print(f"\nOutput File: {output_path}")
    print(f"File Size: {output_path.stat().st_size / 1024:.2f} KB")
    
    print(f"\nVideo Parameters:")
    print(f"  Resolution: {width}x{height}")
    print(f"  Frame Rate: {fps} fps")
    print(f"  Duration: {duration} seconds")
    print(f"  Total Frames: {frame_count}")
    
    print(f"\nObject Parameters:")
    print(f"  Size: {DEFAULT_OBJECT_WIDTH}x{DEFAULT_OBJECT_HEIGHT} pixels")
    print(f"  Color: Black ({DEFAULT_OBJECT_COLOR})")
    print(f"  Background: White ({DEFAULT_BACKGROUND_COLOR})")
    print(f"  Motion: Diagonal (top-left to bottom-right)")
    
    print(f"\nProcessing Time: {processing_time:.2f} seconds")
    
    print("\nVIDEO CHARACTERISTICS:")
    print("-" * 70)
    print("The generated video demonstrates:")
    print("  - Predictable motion (ideal for P-frame compression)")
    print("  - Consistent GOP structure")
    print("  - Simple motion vectors (single direction)")
    print("  - High compression efficiency (minimal change between frames)")
    
    print("=" * 70 + "\n")
