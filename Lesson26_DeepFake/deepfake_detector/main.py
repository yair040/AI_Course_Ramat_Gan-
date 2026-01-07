"""
Command-line interface for DeepFake detector.
Author: Yair Levi
"""

import sys
import argparse
from pathlib import Path
from .config import DetectorConfig
from .detector import DeepFakeDetector
from .utils import setup_logger, ReportGenerator


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='DeepFake Video Detection Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m deepfake_detector.main video.mp4
  python -m deepfake_detector.main video.mp4 --output report.json
  python -m deepfake_detector.main video.mp4 --frame-skip 2 --workers 8
        """
    )
    
    parser.add_argument(
        'video',
        type=str,
        help='Path to video file to analyze'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default=None,
        help='Output report path (default: video_name_report.json)'
    )
    
    parser.add_argument(
        '--frame-skip',
        type=int,
        default=1,
        help='Analyze every Nth frame (default: 1)'
    )
    
    parser.add_argument(
        '--batch-size',
        type=int,
        default=16,
        help='Frames per batch (default: 16)'
    )
    
    parser.add_argument(
        '--workers',
        type=int,
        default=4,
        help='Number of worker processes (default: 4)'
    )
    
    parser.add_argument(
        '--disable-ml',
        action='store_true',
        help='Disable ML models'
    )
    
    parser.add_argument(
        '--gpu',
        action='store_true',
        help='Enable GPU acceleration'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose logging'
    )
    
    parser.add_argument(
        '--log-level',
        type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Logging level (default: INFO)'
    )
    
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()
    
    # Validate video file
    video_path = Path(args.video)
    if not video_path.exists():
        print(f"Error: Video file not found: {video_path}")
        sys.exit(1)
    
    # Create configuration
    config = DetectorConfig(
        frame_skip=args.frame_skip,
        batch_size=args.batch_size,
        num_workers=args.workers,
        use_gpu=args.gpu,
        log_level='DEBUG' if args.verbose else args.log_level,
    )
    
    # Disable ML if requested
    if args.disable_ml:
        config.analyzers['ml'].enabled = False
    
    # Setup logging
    logger = setup_logger(
        log_dir=config.log_dir,
        log_level=config.log_level,
        console=True,
        file=True
    )
    
    logger.info("=" * 60)
    logger.info("DeepFake Detection Tool - Starting Analysis")
    logger.info(f"Video: {video_path.name}")
    logger.info(f"Configuration: {args.frame_skip} frame skip, "
               f"{args.batch_size} batch size, {args.workers} workers")
    logger.info("=" * 60)
    
    try:
        # Initialize detector
        detector = DeepFakeDetector(config)
        
        # Run analysis
        results = detector.analyze(video_path)
        
        # Generate output path
        if args.output:
            output_path = Path(args.output)
        else:
            output_path = video_path.parent / f"{video_path.stem}_report.json"
        
        # Save report
        report_gen = ReportGenerator()
        report_gen.generate_json_report(results, output_path)
        
        # Print summary
        print("\n" + "=" * 60)
        print("ANALYSIS COMPLETE")
        print("=" * 60)
        print(f"Verdict: {results['verdict']}")
        print(f"Confidence: {results['confidence']:.2%}")
        print(f"Processing Time: {results['processing_time']:.2f}s")
        print(f"\nReport saved to: {output_path}")
        print("=" * 60)
        
        # Print scores
        print("\nScores by Analyzer:")
        for name, score in results['scores'].items():
            print(f"  {name:20s}: {score:.2%}")
        
        # Print anomalies if any
        if results['anomalies']:
            print(f"\nAnomalies Detected: {len(results['anomalies'])}")
            for anom in results['anomalies'][:5]:
                print(f"  - {anom['type']}: {anom['description']}")
        
        # Return exit code based on verdict
        if results['verdict'] == 'FAKE':
            sys.exit(2)
        elif results['verdict'] == 'REAL':
            sys.exit(0)
        else:
            sys.exit(1)
    
    except KeyboardInterrupt:
        logger.warning("Analysis interrupted by user")
        sys.exit(130)
    
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
