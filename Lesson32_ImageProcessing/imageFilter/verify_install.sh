#!/bin/bash
# Installation Verification Script
# Author: Yair Levi
# Verifies that all files and dependencies are correctly installed

set -e

echo "=========================================="
echo "Image Frequency Filter - Verification"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
PASS=0
FAIL=0

# Function to check file exists
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
        ((PASS++))
        return 0
    else
        echo -e "${RED}✗${NC} $1 (MISSING)"
        ((FAIL++))
        return 1
    fi
}

# Function to check directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1/"
        ((PASS++))
        return 0
    else
        echo -e "${YELLOW}⚠${NC} $1/ (Will be created)"
        mkdir -p "$1"
        ((PASS++))
        return 0
    fi
}

# Check Python version
echo "Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓${NC} Python found: $PYTHON_VERSION"
    ((PASS++))
else
    echo -e "${RED}✗${NC} Python 3 not found"
    ((FAIL++))
fi
echo ""

# Check virtual environment
echo "Checking virtual environment..."
VENV_PATH="../../venv"
if [ -d "$VENV_PATH" ]; then
    echo -e "${GREEN}✓${NC} Virtual environment exists at $VENV_PATH"
    ((PASS++))
else
    echo -e "${YELLOW}⚠${NC} Virtual environment not found at $VENV_PATH"
    echo "  Run: python3 -m venv $VENV_PATH"
    ((FAIL++))
fi
echo ""

# Check core files
echo "Checking core files..."
check_file "main.py"
check_file "requirements.txt"
check_file "setup.sh"
check_file "__init__.py"
echo ""

# Check documentation
echo "Checking documentation..."
check_file "PRD.md"
check_file "planning.md"
check_file "tasks.md"
check_file "Claude.md"
check_file "README.md"
check_file "CHANGES_SUMMARY.md"
check_file "QUICK_REFERENCE.md"
check_file "PIPELINE_DIAGRAM.md"
check_file "FILES_COMPLETE_LIST.md"
echo ""

# Check config module
echo "Checking config module..."
check_file "config/__init__.py"
check_file "config/settings.py"
echo ""

# Check filters module
echo "Checking filters module..."
check_file "filters/__init__.py"
check_file "filters/base_filter.py"
check_file "filters/high_pass.py"
check_file "filters/low_pass.py"
check_file "filters/band_pass.py"
echo ""

# Check tasks module
echo "Checking tasks module..."
check_file "tasks/__init__.py"
check_file "tasks/fft_transform.py"
check_file "tasks/frequency_display.py"
check_file "tasks/filter_apply.py"
check_file "tasks/inverse_transform.py"
check_file "tasks/image_display.py"
echo ""

# Check utils module
echo "Checking utils module..."
check_file "utils/__init__.py"
check_file "utils/logger.py"
check_file "utils/path_handler.py"
check_file "utils/image_loader.py"
echo ""

# Check directories
echo "Checking directories..."
check_dir "input"
check_dir "output"
check_dir "log"
echo ""

# Check Python imports (if venv active)
if [ -n "$VIRTUAL_ENV" ]; then
    echo "Checking Python dependencies..."
    
    if python3 -c "import numpy" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} numpy"
        ((PASS++))
    else
        echo -e "${RED}✗${NC} numpy (not installed)"
        ((FAIL++))
    fi
    
    if python3 -c "import cv2" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} opencv-python"
        ((PASS++))
    else
        echo -e "${RED}✗${NC} opencv-python (not installed)"
        ((FAIL++))
    fi
    
    if python3 -c "import matplotlib" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} matplotlib"
        ((PASS++))
    else
        echo -e "${RED}✗${NC} matplotlib (not installed)"
        ((FAIL++))
    fi
    
    if python3 -c "import PIL" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Pillow"
        ((PASS++))
    else
        echo -e "${RED}✗${NC} Pillow (not installed)"
        ((FAIL++))
    fi
    
    if python3 -c "import scipy" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} scipy"
        ((PASS++))
    else
        echo -e "${RED}✗${NC} scipy (not installed)"
        ((FAIL++))
    fi
    echo ""
else
    echo -e "${YELLOW}⚠${NC} Virtual environment not active"
    echo "  Activate with: source ../../venv/bin/activate"
    echo "  Then run this script again to check dependencies"
    echo ""
fi

# Summary
echo "=========================================="
echo "Verification Summary"
echo "=========================================="
echo -e "${GREEN}Passed:${NC} $PASS"
echo -e "${RED}Failed:${NC} $FAIL"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Activate virtual environment: source ../../venv/bin/activate"
    echo "  2. Place image in input/: cp your_image.jpg input/"
    echo "  3. Run application: python main.py --input your_image.jpg --filter all"
    echo ""
    exit 0
else
    echo -e "${RED}✗ Some checks failed${NC}"
    echo ""
    echo "To fix issues:"
    echo "  1. Run setup script: ./setup.sh"
    echo "  2. Activate venv: source ../../venv/bin/activate"
    echo "  3. Install dependencies: pip install -r requirements.txt"
    echo "  4. Run this verification again"
    echo ""
    exit 1
fi