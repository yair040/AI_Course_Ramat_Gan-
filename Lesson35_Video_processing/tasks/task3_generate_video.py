"""
Task 3: Overlay Moving Object on Video Frames.

Extracts frames from the input video, draws a moving black rectangle
on each frame (diagonal, top-left to bottom-right), then re-encodes
into a new video.

Author: Yair Levi
"""

from pathlib import Path
from typing import Optional, Dict
import shutil
import time

from PIL import Image, ImageDraw

from ..utils.logger import get_logger
from ..utils.ffmpeg_wrapper import run_ffmpeg, run_ffprobe
from ..config import (
    PROJECT_ROOT,
    DEFAULT_OBJECT_WIDTH,
    DEFAULT_OBJECT_HEIGHT,
    DEFAULT_OBJECT_COLOR,
)

logger = get_logger()

# Temporary directory for extracted / modified frames
TEMP_DIR = PROJECT_ROOT / "temp_frames_task3"


def get_video_info(video_path: Path) -> Dict:
    """Return dict with width, height, fps, frame_count from ffprobe."""
    meta = run_ffprobe(video_path, [
        "-v", "error", "-print_format", "json",
        "-show_format", "-show_streams"
    ])
    vs = next((s for s in meta.get("streams", []) if s.get("codec_type") == "video"), {})
    width, height = int(vs.get("width", 1280)), int(vs.get("height", 720))
    num, den = vs.get("r_frame_rate", "30/1").split("/")
    fps = float(num) / float(den) if int(den) else 30.0
    duration = float(meta.get("format", {}).get("duration", 0))
    return {"width": width, "height": height, "fps": fps,
            "frame_count": int(duration * fps) if duration else 300}


def extract_raw_frames(video_path: Path, out_dir: Path) -> int:
    """Extract all frames from the video as PNG files."""
    out_dir.mkdir(exist_ok=True)
    pattern = str(out_dir / "frame_%04d.png")
    run_ffmpeg(["-i", str(video_path), "-y", pattern])
    count = len(list(out_dir.glob("frame_*.png")))
    logger.info(f"Extracted {count} raw frames")
    return count


def overlay_moving_object(out_dir: Path, frame_count: int, width: int, height: int):
    """Draw moving rectangle on each extracted frame (overwrites in place)."""
    obj_w, obj_h = DEFAULT_OBJECT_WIDTH, DEFAULT_OBJECT_HEIGHT
    for i in range(frame_count):
        frame_path = out_dir / f"frame_{i + 1:04d}.png"
        if not frame_path.exists():
            continue
        progress = i / (frame_count - 1) if frame_count > 1 else 0
        x = int(progress * (width - obj_w))
        y = int(progress * (height - obj_h))
        img = Image.open(frame_path)
        ImageDraw.Draw(img).rectangle([x, y, x + obj_w, y + obj_h], fill=DEFAULT_OBJECT_COLOR)
        img.save(frame_path)
        if (i + 1) % 100 == 0:
            logger.info(f"Overlaid object on {i + 1}/{frame_count} frames")
    logger.info("Moving object overlay complete")


def encode_frames_to_video(frames_dir: Path, output_path: Path, fps: float):
    """Encode modified frames back to video with H.264."""
    pattern = str(frames_dir / "frame_%04d.png")
    run_ffmpeg([
        "-framerate", str(fps),
        "-i", pattern,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "23",
        "-y",
        str(output_path)
    ])
    logger.info(f"Encoded output video: {output_path}")


def generate_test_video(
    input_path: Path,
    output_path: Optional[Path] = None
) -> Dict:
    """
    Main entry: extract frames from input_path, overlay moving object,
    encode to output_path.

    Args:
        input_path: Source video file
        output_path: Destination video (default: <stem>_with_object.mp4)

    Returns:
        dict: Result summary
    """
    logger.info(f"Task 3 starting - source video: {input_path}")
    start = time.time()

    if output_path is None:
        output_path = input_path.parent / (input_path.stem + "_with_object.mp4")

    info = get_video_info(input_path)
    logger.info(f"Source: {info['width']}x{info['height']} @ {info['fps']} fps")

    # Prepare temp dir (clean previous run)
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)
    TEMP_DIR.mkdir()

    try:
        actual_count = extract_raw_frames(input_path, TEMP_DIR)
        overlay_moving_object(TEMP_DIR, actual_count, info["width"], info["height"])
        encode_frames_to_video(TEMP_DIR, output_path, info["fps"])

        elapsed = time.time() - start
        size_kb = output_path.stat().st_size / 1024

        sep = "=" * 60
        print(f"\n{sep}\n  TASK 3 — MOVING OBJECT OVERLAY REPORT\n{sep}")
        print(f"  Input   : {input_path}")
        print(f"  Output  : {output_path}  ({size_kb:.1f} KB)")
        print(f"  Frames  : {actual_count}  @ {info['width']}x{info['height']}")
        print(f"  Object  : {DEFAULT_OBJECT_WIDTH}x{DEFAULT_OBJECT_HEIGHT} px black, diagonal TL->BR")
        print(f"  Time    : {elapsed:.2f} s\n{sep}\n")

        logger.info(f"Task 3 complete in {elapsed:.2f}s -> {output_path}")
        return {"output": str(output_path), "frames": actual_count, "time": elapsed}

    finally:
        if TEMP_DIR.exists():
            shutil.rmtree(TEMP_DIR)
            logger.info("Cleaned up temp frames")
