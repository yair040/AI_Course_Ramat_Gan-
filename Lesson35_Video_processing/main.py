"""
Video Processing Analysis Tool - Main Entry Point

This is the main entry point for the video processing analysis tool.
It provides a command-line interface to run the three main tasks.

Author: Yair Levi
Date: February 1, 2026
"""

import argparse
import sys
from pathlib import Path

from .utils.logger import setup_logger
from .utils.ffmpeg_wrapper import check_ffmpeg_installed
from .cli_handlers import run_task_1, run_task_2, run_task_3
from . import __version__, __author__
from .config import PROJECT_ROOT

logger = setup_logger()


def create_argument_parser():
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Video Processing Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  python -m video_processing.main --task 1 --input sample.mp4
  python -m video_processing.main --task 2 --input sample.mp4
  python -m video_processing.main --task 3 --input sample.mp4
  python -m video_processing.main --all   --input sample.mp4

v{__version__}  Author: {__author__}
        """
    )
    
    parser.add_argument('--version', action='version',
                       version=f'Video Processing Analysis Tool v{__version__}')
    parser.add_argument('--task', type=int, choices=[1, 2, 3],
                       help='Task number (1: Metadata, 2: Motion Vectors, 3: Generate Video)')
    parser.add_argument('--all', action='store_true', help='Run all tasks sequentially')
    parser.add_argument('--input', type=str, help='Input video file path (required for tasks 1 and 2)')
    parser.add_argument('--output', type=str, help='Output file path (for task 3)')
    parser.add_argument('--width', type=int, default=1280, help='Video width in pixels (default: 1280)')
    parser.add_argument('--height', type=int, default=720, help='Video height in pixels (default: 720)')
    parser.add_argument('--fps', type=int, default=30, help='Frames per second (default: 30)')
    parser.add_argument('--duration', type=int, default=10, help='Video duration in seconds (default: 10)')
    
    return parser


def main():
    """Main entry point for the application."""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    logger.info(f"Video Processing Analysis Tool v{__version__}")
    logger.info(f"Author: {__author__}")
    
    # Check FFmpeg
    try:
        check_ffmpeg_installed()
    except EnvironmentError as e:
        logger.error(str(e))
        print(f"Error: {e}\nInstall FFmpeg:")
        print("  Ubuntu/WSL: sudo apt update && sudo apt install ffmpeg")
        sys.exit(1)
    
    # Validate arguments
    if not args.all and args.task is None:
        print("Error: Must specify --task or --all.  Use --help for usage.")
        sys.exit(1)
    
    if args.all:
        if not args.input:
            print("Error: --input required when using --all")
            sys.exit(1)
        tasks_to_run = [1, 2, 3]
    else:
        tasks_to_run = [args.task]
    
    # Run tasks
    success_count = 0
    # Resolve input path relative to PROJECT_ROOT (works from any CWD)
    input_path = None
    if args.input:
        input_path = Path(args.input)
        if not input_path.is_absolute():
            input_path = PROJECT_ROOT / input_path
        input_path = input_path.resolve()
        logger.info(f"Resolved input path: {input_path}")
    
    # Resolve output path the same way
    output_path = None
    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = PROJECT_ROOT / output_path
        output_path = output_path.resolve()
    
    for task_num in tasks_to_run:
        if task_num in [1, 2]:
            if not input_path:
                logger.error(f"Task {task_num} requires --input argument")
                print(f"Error: Task {task_num} requires --input argument")
                continue
            
            if not input_path.exists():
                logger.error(f"Input file not found: {input_path}")
                print(f"Error: Input file not found: {input_path}")
                continue
            
            if task_num == 1:
                if run_task_1(input_path):
                    success_count += 1
            elif task_num == 2:
                if run_task_2(input_path):
                    success_count += 1
        
        elif task_num == 3:
            # Task 3 needs the input video (extracts its frames, overlays object)
            if not input_path:
                logger.error("Task 3 requires --input argument")
                print("Error: Task 3 requires --input (source video to overlay)")
                continue
            if not input_path.exists():
                logger.error(f"Input file not found: {input_path}")
                print(f"Error: Input file not found: {input_path}")
                continue
            
            if run_task_3(input_path, output_path, args.width, args.height, args.fps, args.duration):
                success_count += 1
    
    # Summary
    total_tasks = len(tasks_to_run)
    logger.info(f"Completed {success_count}/{total_tasks} tasks successfully")
    
    if success_count == total_tasks:
        logger.info("All tasks completed successfully!")
        sys.exit(0)
    else:
        logger.warning(f"{total_tasks - success_count} task(s) failed")
        sys.exit(1)


if __name__ == '__main__':
    main()
