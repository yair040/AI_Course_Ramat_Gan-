#!/usr/bin/env python3
"""
Quick test script to verify all filters work correctly.
Author: Yair Levi

Creates a simple test pattern and applies all filters.
"""

import numpy as np
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from utils import setup_logger, get_logger, ensure_directory, get_output_path, save_image
from filters import HighPassFilter, LowPassFilter, BandPassFilter
from tasks import apply_fft, get_magnitude_spectrum, reconstruct_image

# Setup logger
logger = setup_logger('test')


def create_test_image(size=256):
    """Create a simple test pattern."""
    x = np.linspace(-2, 2, size)
    y = np.linspace(-2, 2, size)
    X, Y = np.meshgrid(x, y)
    
    # Create pattern with low and high frequencies
    pattern = (np.sin(2*np.pi*X) + np.sin(6*np.pi*Y)) * 50 + 128
    pattern = np.clip(pattern, 0, 255).astype(np.uint8)
    
    logger.info(f"Created test pattern: {size}x{size}")
    return pattern


def test_filter(filter_obj, fft_image, filter_name):
    """Test a single filter."""
    try:
        logger.info(f"Testing {filter_name}...")
        
        # Apply filter
        filtered_fft = filter_obj.apply(fft_image)
        
        # Check output
        assert filtered_fft is not None, f"{filter_name} returned None"
        assert filtered_fft.shape == fft_image.shape, f"{filter_name} changed shape"
        
        # Reconstruct
        reconstructed = reconstruct_image(filtered_fft)
        assert reconstructed is not None, f"{filter_name} reconstruction failed"
        
        logger.info(f"✓ {filter_name} passed")
        return True
        
    except Exception as e:
        logger.error(f"✗ {filter_name} failed: {e}")
        return False


def main():
    """Run filter tests."""
    logger.info("=" * 60)
    logger.info("Filter Test Suite")
    logger.info("=" * 60)
    
    try:
        # Ensure output directory
        ensure_directory(get_output_path())
        
        # Create test image
        logger.info("Step 1: Creating test image...")
        test_image = create_test_image(256)
        
        # Save test image
        test_path = get_output_path("test_pattern.png")
        save_image(test_image, test_path)
        logger.info(f"Test image saved: {test_path}")
        
        # Apply FFT
        logger.info("Step 2: Applying FFT...")
        fft_image = apply_fft(test_image)
        logger.info(f"FFT shape: {fft_image.shape}")
        
        # Get magnitude
        magnitude = get_magnitude_spectrum(fft_image)
        logger.info(f"Magnitude range: [{magnitude.min():.2f}, {magnitude.max():.2f}]")
        
        # Test filters
        logger.info("Step 3: Testing filters...")
        results = {}
        
        # Test HPF
        hpf = HighPassFilter(cutoff=30.0)
        results['HPF'] = test_filter(hpf, fft_image, "High-Pass Filter")
        
        # Test LPF
        lpf = LowPassFilter(cutoff=30.0)
        results['LPF'] = test_filter(lpf, fft_image, "Low-Pass Filter")
        
        # Test BPF
        bpf = BandPassFilter(low_cutoff=20.0, high_cutoff=80.0)
        results['BPF'] = test_filter(bpf, fft_image, "Band-Pass Filter")
        
        # Summary
        logger.info("=" * 60)
        logger.info("Test Results")
        logger.info("=" * 60)
        
        passed = sum(results.values())
        total = len(results)
        
        for filter_name, result in results.items():
            status = "✓ PASS" if result else "✗ FAIL"
            logger.info(f"{filter_name}: {status}")
        
        logger.info(f"\nTotal: {passed}/{total} tests passed")
        
        if passed == total:
            logger.info("✓ All tests passed!")
            return 0
        else:
            logger.error(f"✗ {total - passed} test(s) failed")
            return 1
            
    except Exception as e:
        logger.error(f"Test suite failed: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())