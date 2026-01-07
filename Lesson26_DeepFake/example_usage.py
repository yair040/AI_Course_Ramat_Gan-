"""
Example usage of DeepFake detector.
Author: Yair Levi
"""

from pathlib import Path
from deepfake_detector import DeepFakeDetector, DetectorConfig
from deepfake_detector.utils import setup_logger, ReportGenerator


def main():
    """Example of using the detector programmatically."""
    
    # Setup configuration
    config = DetectorConfig(
        frame_skip=2,          # Analyze every 2nd frame for speed
        batch_size=16,         # Process 16 frames at a time
        num_workers=4,         # Use 4 parallel workers
        use_gpu=False,         # Set to True if GPU available
    )
    
    # Setup logging
    logger = setup_logger(
        log_dir=config.log_dir,
        log_level='INFO',
        console=True,
        file=True
    )
    
    logger.info("Starting DeepFake detection example")
    
    # Initialize detector
    detector = DeepFakeDetector(config)
    
    # Path to video (update with your video path)
    video_path = Path('sample_video.mp4')
    
    if not video_path.exists():
        logger.error(f"Video not found: {video_path}")
        logger.info("Please provide a valid video file path")
        return
    
    # Run analysis
    logger.info(f"Analyzing video: {video_path.name}")
    results = detector.analyze(video_path)
    
    # Display results
    print("\n" + "=" * 60)
    print("DETECTION RESULTS")
    print("=" * 60)
    print(f"Video: {video_path.name}")
    print(f"Verdict: {results['verdict']}")
    print(f"Confidence: {results['confidence']:.2%}")
    print(f"Processing Time: {results['processing_time']:.2f} seconds")
    
    print("\nScores by Analyzer:")
    for analyzer_name, score in results['scores'].items():
        print(f"  {analyzer_name:20s}: {score:.2%}")
    
    if results['anomalies']:
        print(f"\nAnomalies Detected: {len(results['anomalies'])}")
        for i, anomaly in enumerate(results['anomalies'][:5], 1):
            print(f"  {i}. [{anomaly['timestamp']:.2f}s] {anomaly['type']}")
            print(f"     {anomaly['description']}")
    
    # Save report
    report_gen = ReportGenerator()
    output_path = video_path.parent / f"{video_path.stem}_report.json"
    report_gen.generate_json_report(results, output_path)
    
    # Also save text summary
    text_path = video_path.parent / f"{video_path.stem}_summary.txt"
    report_gen.save_text_report(results, text_path)
    
    print(f"\nReports saved:")
    print(f"  - JSON: {output_path}")
    print(f"  - Text: {text_path}")
    print("=" * 60)


if __name__ == '__main__':
    main()
