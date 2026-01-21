#!/bin/bash
# Setup script for Image Frequency Filter Application
# Author: Yair Levi
# Run this script from the project directory

set -e  # Exit on error

echo "=========================================="
echo "Image Frequency Filter - Setup Script"
echo "=========================================="

# Get project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/../../venv"

echo "Project directory: $PROJECT_DIR"
echo "Virtual environment: $VENV_DIR"

# Create directory structure
echo ""
echo "Creating directory structure..."
mkdir -p "$PROJECT_DIR/input"
mkdir -p "$PROJECT_DIR/output"
mkdir -p "$PROJECT_DIR/log"
mkdir -p "$PROJECT_DIR/tasks"
mkdir -p "$PROJECT_DIR/filters"
mkdir -p "$PROJECT_DIR/utils"
mkdir -p "$PROJECT_DIR/config"

echo "✓ Directories created"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo ""
    echo "Creating virtual environment at $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
    echo "✓ Virtual environment created"
else
    echo ""
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"
echo "✓ Virtual environment activated"

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing requirements..."
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    pip install -r "$PROJECT_DIR/requirements.txt"
    echo "✓ Requirements installed"
else
    echo "⚠ requirements.txt not found, skipping package installation"
fi

# Make main.py executable
chmod +x "$PROJECT_DIR/main.py"

echo ""
echo "=========================================="
echo "Setup completed successfully!"
echo "=========================================="
echo ""
echo "To activate the virtual environment manually:"
echo "  source $VENV_DIR/bin/activate"
echo ""
echo "To run the application:"
echo "  python main.py --input <image_file> --filter all"
echo ""
echo "For help:"
echo "  python main.py --help"
echo ""