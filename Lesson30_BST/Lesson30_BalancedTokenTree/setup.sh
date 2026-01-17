#!/bin/bash
# Setup script for Balanced Token Tree
# Author: Yair Levi

set -e  # Exit on error

echo "=================================="
echo "Balanced Token Tree - Setup"
echo "=================================="
echo ""

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found"
    echo "Please run this script from the project root directory"
    exit 1
fi

echo "Step 1: Creating virtual environment..."
cd ../..
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists at ../../venv/"
    read -p "Do you want to recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
        echo "✓ Virtual environment recreated"
    else
        echo "✓ Using existing virtual environment"
    fi
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

echo ""
echo "Step 2: Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

echo ""
echo "Step 3: Upgrading pip..."
pip install --upgrade pip --quiet
echo "✓ pip upgraded"

echo ""
echo "Step 4: Installing dependencies..."
cd Lesson30/Lesson30_BalancedTokenTree
pip install -r requirements.txt
echo "✓ Dependencies installed"

echo ""
echo "Step 5: Verifying installation..."
python3 -c "import matplotlib; import numpy; print('✓ All dependencies available')"

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "To run the program:"
echo "  cd balanced_token_tree"
echo "  python3 main.py --seed 42"
echo ""
echo "Or use the quick command:"
echo "  python3 -m balanced_token_tree.main --seed 42"
echo ""
echo "Virtual environment is located at: ../../venv/"
echo "Remember to activate it: source ../../venv/bin/activate"
echo ""
