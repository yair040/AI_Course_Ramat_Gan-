#!/bin/bash
# Gmail Event Scanner - Run Script
# Author: Yair Levi

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Virtual environment path (relative to project)
VENV_PATH="$SCRIPT_DIR/../../venv"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "======================================================================"
echo "Gmail Event Scanner & Calendar Integration"
echo "Author: Yair Levi"
echo "======================================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo -e "${RED}Error: Virtual environment not found at $VENV_PATH${NC}"
    echo "Please create it first:"
    echo "  cd ../.."
    echo "  python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source "$VENV_PATH/bin/activate"

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to activate virtual environment${NC}"
    exit 1
fi

echo -e "${GREEN}Virtual environment activated${NC}"
echo ""

# Change to project directory
cd "$SCRIPT_DIR"

# Check if config.yaml exists
if [ ! -f "config.yaml" ]; then
    echo -e "${RED}Error: config.yaml not found${NC}"
    echo "Please create and configure config.yaml before running"
    exit 1
fi

# Check if credentials directory exists
if [ ! -d "credentials" ]; then
    echo -e "${RED}Error: credentials/ directory not found${NC}"
    echo "Please create credentials/ and add your Google API credentials"
    exit 1
fi

# Run the application
echo -e "${YELLOW}Starting application...${NC}"
echo ""
python main.py

# Capture exit code
EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}Application exited successfully${NC}"
else
    echo -e "${RED}Application exited with error code $EXIT_CODE${NC}"
fi

# Deactivate virtual environment
deactivate

exit $EXIT_CODE
