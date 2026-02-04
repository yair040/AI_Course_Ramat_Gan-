"""Task 2: Motion Vector Visualization. Author: Yair Levi"""

from pathlib import Path
from typing import Dict, List, Optional
from multiprocessing import Pool, cpu_count
import time

from ..utils.logger import get_logger
from ..utils.ffmpeg_wrapper import check_ffmpeg_installed, extract_frames_with_motion_vectors
from ..config import FRAMES_DIR, USE_MULTIPROCESSING, MAX_WORKERS, FRAME_BATCH_SIZE

logger = get_logger()


def analyze_motion_in_frame(frame_path: Path) -> Dict:
    """Analyze motion vectors in a single frame."""
    return {
        'frame': frame_path.name,
        'exists': frame_path.exists(),
        'size': frame_path.stat().st_size if frame_path.exists() else 0
    }


def process_frames_parallel(frame_paths: List[Path]) -> List[Dict]:
    """Process multiple frames in parallel using multiprocessing."""
    if not USE_MULTIPROCESSING or len(frame_paths) < FRAME_BATCH_SIZE:
        logger.info("Processing frames sequentially")
        return [analyze_motion_in_frame(fp) for fp in frame_paths]
    
    logger.info(f"Processing {len(frame_paths)} frames using {MAX_WORKERS} workers")
    with Pool(processes=MAX_WORKERS) as pool:
        results = pool.map(analyze_motion_in_frame, frame_paths)
    return results


def analyze_motion_patterns(frame_results: List[Dict]) -> Dict:
    """Analyze overall motion patterns from frame analysis results."""
    total_frames = len(frame_results)
    valid_frames = sum(1 for r in frame_results if r.get('exists', False))
    total_size = sum(r.get('size', 0) for r in frame_results)
    avg_size = total_size / valid_frames if valid_frames > 0 else 0
    
    return {
        'total_frames': total_frames,
        'valid_frames': valid_frames,
        'total_size_bytes': total_size,
        'average_frame_size_bytes': avg_size,
        'average_frame_size_kb': avg_size / 1024
    }


def print_motion_vector_report(video_path: Path, frame_count: int, output_dir: Path,
                                motion_stats: Dict, processing_time: float) -> None:
    """Print formatted motion vector analysis report."""
    print("\n" + "=" * 70)
    print("MOTION VECTOR VISUALIZATION REPORT")
    print("=" * 70)
    print(f"\nInput Video: {video_path.name}")
    print(f"Output Directory: {output_dir}")
    print(f"\nFrames Extracted: {frame_count}")
    print(f"Valid Frames: {motion_stats['valid_frames']}")
    
    if motion_stats['average_frame_size_kb'] > 0:
        print(f"Average Frame Size: {motion_stats['average_frame_size_kb']:.2f} KB")
        print(f"Total Size: {motion_stats['total_size_bytes'] / (1024*1024):.2f} MB")
    
    print(f"\nProcessing Time: {processing_time:.2f} seconds")
    print("\nMOTION VECTOR VISUALIZATION:")
    print("-" * 70)
    print("The extracted frames show motion vectors overlaid on the video.")
    print("Vector interpretation:")
    print("  - Arrow direction: Direction of motion")
    print("  - Arrow length: Speed/magnitude of motion")
    print("  - Colors: Different motion vector types (P-forward, B-forward, B-backward)")
    print("\nFRAME ANALYSIS:")
    print("-" * 70)
    print("Motion vectors indicate how each macroblock moved between frames.")
    print("Longer vectors = faster motion")
    print("Clustered vectors = coherent motion (e.g., camera pan)")
    print("Scattered vectors = complex motion (e.g., multiple moving objects)")
    print("=" * 70 + "\n")


def extract_and_analyze_motion_vectors(video_path: Path, output_dir: Optional[Path] = None) -> Dict:
    """Main function to extract frames with motion vectors and analyze them."""
    logger.info(f"Starting motion vector extraction for: {video_path}")
    start_time = time.time()
    
    check_ffmpeg_installed()
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")
    
    if output_dir is None:
        output_dir = FRAMES_DIR
    
    frame_count = extract_frames_with_motion_vectors(video_path, output_dir)
    logger.info(f"Extracted {frame_count} frames")
    frame_paths = sorted(output_dir.glob("frame_*.png"))
    
    if len(frame_paths) <= 1000:
        logger.info("Analyzing frame motion patterns")
        frame_results = process_frames_parallel(frame_paths)
        motion_stats = analyze_motion_patterns(frame_results)
    else:
        logger.info("Skipping detailed frame analysis (too many frames)")
        motion_stats = {
            'total_frames': len(frame_paths),
            'valid_frames': len(frame_paths),
            'total_size_bytes': sum(fp.stat().st_size for fp in frame_paths),
            'average_frame_size_bytes': 0,
            'average_frame_size_kb': 0
        }
        if motion_stats['valid_frames'] > 0:
            motion_stats['average_frame_size_bytes'] = motion_stats['total_size_bytes'] / motion_stats['valid_frames']
            motion_stats['average_frame_size_kb'] = motion_stats['average_frame_size_bytes'] / 1024
    
    processing_time = time.time() - start_time
    print_motion_vector_report(video_path, frame_count, output_dir, motion_stats, processing_time)
    logger.info(f"Motion vector extraction complete in {processing_time:.2f}s")
    
    return {
        'frame_count': frame_count,
        'output_dir': str(output_dir),
        'motion_stats': motion_stats,
        'processing_time': processing_time
    }
