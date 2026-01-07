#!/bin/bash
# Installation script for DeepFake Detection Tool
# Author: Yair Levi

set -e

echo "=================================="
echo "DeepFake Detector Installation"
echo "=================================="

# Check if running in WSL
if ! grep -qEi "(Microsoft|WSL)" /proc/version &> /dev/null; then
    echo "Warning: This script is designed for WSL (Windows Subsystem for Linux)"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Detect available Python version
echo "Detecting Python version..."
if command -v python3.12 &> /dev/null; then
    PYTHON_CMD=python3.12
    PYTHON_VERSION="3.12"
elif command -v python3.11 &> /dev/null; then
    PYTHON_CMD=python3.11
    PYTHON_VERSION="3.11"
elif command -v python3.10 &> /dev/null; then
    PYTHON_CMD=python3.10
    PYTHON_VERSION="3.10"
elif command -v python3.9 &> /dev/null; then
    PYTHON_CMD=python3.9
    PYTHON_VERSION="3.9"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
    PYTHON_VERSION=$($PYTHON_CMD --version | cut -d' ' -f2 | cut -d'.' -f1,2)
else
    echo "Error: Python 3.9+ not found"
    exit 1
fi

echo "Found Python $PYTHON_VERSION at $PYTHON_CMD"

# Update system packages
echo "Updating system packages..."
sudo apt update

# Install system dependencies
echo "Installing system dependencies..."
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev \
    cmake \
    build-essential \
    libopenblas-dev \
    liblapack-dev

# Navigate to virtual environment directory
echo "Setting up virtual environment..."
cd ../..

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    $PYTHON_CMD -m venv venv
    echo "Virtual environment created at: $(pwd)/venv"
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Navigate back to project directory
cd Lesson26/Lesson26_DeepFake

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating project directories..."
mkdir -p log
mkdir -p models
mkdir -p tests

# Create .gitkeep files for empty directories
touch log/.gitkeep
touch models/.gitkeep

# Install package in development mode
echo "Installing package in development mode..."
pip install -e .

# Verify installation
echo ""
echo "Verifying installation..."
python -c "import deepfake_detector; print(f'Package version: {deepfake_detector.__version__}')"

echo ""
echo "=================================="
echo "Installation Complete!"
echo "=================================="
echo ""
echo "To activate the virtual environment:"
echo "  source ../../venv/bin/activate"
echo ""
echo "To run the detector:"
echo "  python -m deepfake_detector.main <video_file>"
echo ""
echo "Or use the command:"
echo "  deepfake-detect <video_file>"
echo ""
echo "For help:"
echo "  python -m deepfake_detector.main --help"
echo "=================================="
