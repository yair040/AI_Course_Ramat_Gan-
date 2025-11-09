#!/bin/bash
# Setup script for PCA and t-SNE Text Vectorization System

set -e  # Exit on error

echo "=========================================="
echo "PCA and t-SNE Setup Script"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping..."
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing dependencies..."
echo "Note: This may take several minutes (downloading ~500MB)"
pip install -r requirements.txt

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To run the program, execute:"
echo "  python main.py"
echo ""
echo "To run individual tasks:"
echo "  python task1_generate.py"
echo "  python task2_vectorize.py"
echo "  python task3_manual_pca.py"
echo "  python task4_sklearn_pca.py"
echo "  python task5_tsne.py"
echo ""
echo "For more information, see README.md"
echo "=========================================="
