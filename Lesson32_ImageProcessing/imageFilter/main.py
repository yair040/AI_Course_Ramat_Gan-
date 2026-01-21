#!/usr/bin/env python3
"""
Image Frequency Filter Application - Main Entry Point
Author: Yair Levi

Applies frequency domain filters (HPF, LPF, BPF) to images using FFT.
"""

import sys
import argparse
from pathlib import Path
from typing import List

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from utils import (setup_logger, get_logger, get_input_path, get_output_path,
                   ensure_directory, load_image, save_image)
from config import HPFConfig, LPFConfig, BPFConfig, AppConfig
from filters import HighPassFilter, LowPassFilter, BandPassFilter, BaseFilter
from tasks import (apply_fft, get_magnitude_spectrum, save_spectrum,
                   apply_filters_parallel, reconstruct_image, create_comparison)

# Setup main logger
logger = setup_logger('main')


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Image Frequency Filter Application',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --input sample.jpg --filter all
  python main.py --input photo.png --filter hpf --hpf-cutoff 40
  python main.py --input photo.png --filter lpf --lpf-cutoff 25
  python main.py --input test.bmp --filter bpf --low-cutoff 30 --high-cutoff 70
        """
    )
    
    parser.add_argument('--input', required=True, help='Input image filename (in input/ directory)')
    parser.add_argument('--filter', choices=['hpf', 'lpf', 'bpf', 'all'], default='all',
                       help='Filter type to apply (default: all)')
    parser.add_argument('--hpf-cutoff', type=float, default=30.0,
                       help='HPF cutoff frequency (default: 30.0)')
    parser.add_argument('--lpf-cutoff', type=float, default=30.0,
                       help='LPF cutoff frequency (default: 30.0)')
    parser.add_argument('--low-cutoff', type=float, default=20.0,
                       help='BPF lower cutoff frequency (default: 20.0)')
    parser.add_argument('--high-cutoff', type=float, default=80.0,
                       help='BPF upper cutoff frequency (default: 80.0)')
    parser.add_argument('--show', action='store_true',
                       help='Display results interactively (may not work in WSL)')
    parser.add_argument('--no-save', action='store_true',
                       help='Do not save output images')
    parser.add_argument('--no-multiprocessing', action='store_true',
                       help='Disable multiprocessing for filter application')
    
    return parser.parse_args()


def create_filters(args: argparse.Namespace) -> List[BaseFilter]:
    """
    Create filter objects based on arguments.
    
    Args:
        args: Parsed command-line arguments
    
    Returns:
        List of filter objects
    """
    filters = []
    
    if args.filter in ['hpf', 'all']:
        hpf = HighPassFilter(cutoff=args.hpf_cutoff)
        filters.append(hpf)
        logger.info(f"Created HPF with cutoff={args.hpf_cutoff}")
    
    if args.filter in ['lpf', 'all']:
        lpf = LowPassFilter(cutoff=args.lpf_cutoff)
        filters.append(lpf)
        logger.info(f"Created LPF with cutoff={args.lpf_cutoff}")
    
    if args.filter in ['bpf', 'all']:
        bpf = BandPassFilter(low_cutoff=args.low_cutoff, high_cutoff=args.high_cutoff)
        filters.append(bpf)
        logger.info(f"Created BPF with band=[{args.low_cutoff}, {args.high_cutoff}]")
    
    return filters


def main():
    """Main application entry point."""
    logger.info("=" * 60)
    logger.info("Image Frequency Filter Application Started")
    logger.info("=" * 60)
    
    try:
        # Parse arguments
        args = parse_arguments()
        logger.info(f"Processing image: {args.input}")
        logger.info(f"Filter mode: {args.filter}")
        
        # Ensure output directory exists
        ensure_directory(get_output_path())
        
        # Step 1: Load image
        logger.info("Step 1: Loading image...")
        input_path = get_input_path(args.input)
        image = load_image(input_path, grayscale=True)
        
        # Step 2: Apply FFT
        logger.info("Step 2: Applying FFT transformation...")
        fft_image = apply_fft(image)
        
        # Step 3: Visualize and save original frequency spectrum
        logger.info("Step 3: Visualizing original frequency spectrum...")
        magnitude = get_magnitude_spectrum(fft_image)
        
        if not args.no_save:
            spectrum_path = get_output_path(f"{Path(args.input).stem}_spectrum_original.png")
            save_spectrum(magnitude, spectrum_path, "Original Frequency Spectrum")
        
        # Step 4: Create and apply filters
        logger.info("Step 4: Creating and applying filters...")
        filters = create_filters(args)
        
        if not filters:
            logger.error("No filters specified")
            return 1
        
        # Apply filters (with or without multiprocessing)
        if args.no_multiprocessing:
            logger.info("Applying filters sequentially...")
            from tasks import apply_filters_sequential
            filtered_results = apply_filters_sequential(fft_image, filters)
        else:
            logger.info("Applying filters in parallel...")
            filtered_results = apply_filters_parallel(fft_image, filters)
        
        # Step 5: Process each filter result
        logger.info("Step 5: Processing filtered results...")
        reconstructed_images = {}
        
        for filter_name, filtered_fft in filtered_results.items():
            logger.info(f"Processing: {filter_name}")
            
            # Show spectrum after filter
            filtered_magnitude = get_magnitude_spectrum(filtered_fft)
            if not args.no_save:
                filtered_spectrum_path = get_output_path(
                    f"{Path(args.input).stem}_spectrum_{filter_name}.png"
                )
                save_spectrum(filtered_magnitude, filtered_spectrum_path, 
                            f"Frequency Spectrum after {filter_name}")
                logger.info(f"Saved filtered spectrum: {filter_name}")
            
            # Reconstruct image
            logger.info(f"Reconstructing image: {filter_name}")
            reconstructed = reconstruct_image(filtered_fft)
            reconstructed_images[filter_name] = reconstructed
            
            # Save individual filtered images
            if not args.no_save:
                output_filename = f"{Path(args.input).stem}_{filter_name}.png"
                output_path = get_output_path(output_filename)
                save_image(reconstructed, output_path)
        
        # Step 6: Create and save comparison
        logger.info("Step 6: Creating comparison visualization...")
        if not args.no_save:
            comparison_path = get_output_path(f"{Path(args.input).stem}_comparison.png")
            create_comparison(image, reconstructed_images, 
                            output_path=comparison_path, show=args.show)
        elif args.show:
            create_comparison(image, reconstructed_images, show=True)
        
        logger.info("=" * 60)
        logger.info("Processing completed successfully!")
        logger.info(f"Total filters applied: {len(filters)}")
        logger.info(f"Results saved to: {get_output_path()}")
        logger.info("=" * 60)
        
        return 0
    
    except Exception as e:
        logger.error(f"Application failed: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())