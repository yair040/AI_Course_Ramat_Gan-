#!/bin/bash
# Run example with test pattern
# Author: Yair Levi
# Demonstrates all filters with a generated test image

set -e

echo "=========================================="
echo "Image Frequency Filter - Example Run"
echo "=========================================="
echo ""

# Check if venv is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    source ../../venv/bin/activate
fi

# Check if Python script exists
if [ ! -f "test_filters.py" ]; then
    echo "Error: test_filters.py not found"
    exit 1
fi

# Run test to create test pattern
echo "Step 1: Creating test pattern..."
python test_filters.py

if [ $? -ne 0 ]; then
    echo "Test pattern creation failed"
    exit 1
fi

# Check if test pattern was created
if [ ! -f "output/test_pattern.png" ]; then
    echo "Error: Test pattern not created"
    exit 1
fi

echo ""
echo "Step 2: Running all filters on test pattern..."
python main.py --input test_pattern.png --filter all

if [ $? -ne 0 ]; then
    echo "Filter application failed"
    exit 1
fi

echo ""
echo "=========================================="
echo "Example Run Complete!"
echo "=========================================="
echo ""
echo "Results in output/ directory:"
ls -lh output/ | grep test_pattern
echo ""
echo "You should see:"
echo "  ✓ test_pattern.png                          (original)"
echo "  ✓ test_pattern_spectrum_original.png        (original spectrum)"
echo "  ✓ test_pattern_spectrum_HighPassFilter.png  (HPF spectrum)"
echo "  ✓ test_pattern_spectrum_LowPassFilter.png   (LPF spectrum)"
echo "  ✓ test_pattern_spectrum_BandPassFilter.png  (BPF spectrum)"
echo "  ✓ test_pattern_HighPassFilter.png           (HPF result)"
echo "  ✓ test_pattern_LowPassFilter.png            (LPF result)"
echo "  ✓ test_pattern_BandPassFilter.png           (BPF result)"
echo "  ✓ test_pattern_comparison.png               (comparison grid)"
echo ""
echo "To view results:"
echo "  eog output/test_pattern_comparison.png"
echo ""
echo "Or copy to Windows:"
echo "  cp output/test_pattern*.png /mnt/c/Users/yair0/Desktop/"
echo ""