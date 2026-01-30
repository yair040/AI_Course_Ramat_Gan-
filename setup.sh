#!/bin/bash
# Gmail Event Scanner - Initial Setup Script
# Author: Yair Levi
# This script helps with first-time setup

set -e  # Exit on error

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "================================================================"
echo "Gmail Event Scanner - Initial Setup"
echo "Author: Yair Levi"
echo "================================================================"
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${BLUE}Current directory: $SCRIPT_DIR${NC}"
echo ""

# Step 1: Rename gitignore.txt to .gitignore
echo -e "${YELLOW}Step 1: Setting up .gitignore${NC}"
if [ -f "gitignore.txt" ]; then
    mv gitignore.txt .gitignore
    echo -e "${GREEN}✓ Renamed gitignore.txt to .gitignore${NC}"
elif [ -f ".gitignore" ]; then
    echo -e "${GREEN}✓ .gitignore already exists${NC}"
else
    echo -e "${RED}✗ Warning: gitignore.txt not found${NC}"
fi
echo ""

# Step 2: Create required directories
echo -e "${YELLOW}Step 2: Creating required directories${NC}"

if [ ! -d "credentials" ]; then
    mkdir -p credentials
    echo -e "${GREEN}✓ Created credentials/ directory${NC}"
else
    echo -e "${GREEN}✓ credentials/ directory exists${NC}"
fi

if [ ! -d "log" ]; then
    mkdir -p log
    echo -e "${GREEN}✓ Created log/ directory${NC}"
else
    echo -e "${GREEN}✓ log/ directory exists${NC}"
fi
echo ""

# Step 3: Create Anthropic API Key directory
echo -e "${YELLOW}Step 3: Creating Anthropic API Key directory${NC}"
API_KEY_DIR="$SCRIPT_DIR/Anthropic_API_Key"
if [ ! -d "$API_KEY_DIR" ]; then
    mkdir -p "$API_KEY_DIR"
    echo -e "${GREEN}✓ Created ./Anthropic_API_Key/ directory${NC}"
else
    echo -e "${GREEN}✓ ./Anthropic_API_Key/ directory exists${NC}"
fi
echo ""

# Step 4: Check for virtual environment
echo -e "${YELLOW}Step 4: Checking virtual environment${NC}"
VENV_DIR="$SCRIPT_DIR/../../venv"
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Virtual environment not found at ../../venv/${NC}"
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    cd "$SCRIPT_DIR/../.."
    python3 -m venv venv
    echo -e "${GREEN}✓ Created virtual environment${NC}"
    cd "$SCRIPT_DIR"
else
    echo -e "${GREEN}✓ Virtual environment exists${NC}"
fi
echo ""

# Step 5: Verify .gitignore is working
echo -e "${YELLOW}Step 5: Verifying .gitignore configuration${NC}"
if [ -f ".gitignore" ]; then
    if grep -q "credentials/" .gitignore && grep -q "Anthropic_API_Key" .gitignore; then
        echo -e "${GREEN}✓ .gitignore properly configured${NC}"
    else
        echo -e "${RED}✗ Warning: .gitignore may be missing critical entries${NC}"
    fi
else
    echo -e "${RED}✗ Error: .gitignore not found${NC}"
fi
echo ""

# Step 6: Check for credentials
echo -e "${YELLOW}Step 6: Checking for credentials${NC}"

if [ -f "credentials/credentials.json" ]; then
    echo -e "${GREEN}✓ Google credentials.json found${NC}"
    # Check permissions
    PERMS=$(stat -c "%a" credentials/credentials.json 2>/dev/null || stat -f "%A" credentials/credentials.json 2>/dev/null)
    if [ "$PERMS" != "600" ]; then
        echo -e "${YELLOW}  Setting permissions to 600...${NC}"
        chmod 600 credentials/credentials.json
        echo -e "${GREEN}  ✓ Permissions updated${NC}"
    else
        echo -e "${GREEN}  ✓ Permissions correct (600)${NC}"
    fi
else
    echo -e "${RED}✗ credentials/credentials.json NOT FOUND${NC}"
    echo -e "${YELLOW}  Action: Download from Google Cloud Console${NC}"
fi

if [ -f "$API_KEY_DIR/api_key.dat" ]; then
    echo -e "${GREEN}✓ Anthropic API key found${NC}"
    # Check permissions
    PERMS=$(stat -c "%a" "$API_KEY_DIR/api_key.dat" 2>/dev/null || stat -f "%A" "$API_KEY_DIR/api_key.dat" 2>/dev/null)
    if [ "$PERMS" != "600" ]; then
        echo -e "${YELLOW}  Setting permissions to 600...${NC}"
        chmod 600 "$API_KEY_DIR/api_key.dat"
        echo -e "${GREEN}  ✓ Permissions updated${NC}"
    else
        echo -e "${GREEN}  ✓ Permissions correct (600)${NC}"
    fi
else
    echo -e "${RED}✗ Anthropic API key NOT FOUND${NC}"
    echo -e "${YELLOW}  Action: Create $API_KEY_DIR/api_key.dat${NC}"
fi
echo ""

# Step 7: Make run.sh executable
echo -e "${YELLOW}Step 7: Making run.sh executable${NC}"
if [ -f "run.sh" ]; then
    chmod +x run.sh
    echo -e "${GREEN}✓ run.sh is now executable${NC}"
else
    echo -e "${RED}✗ run.sh not found${NC}"
fi
echo ""

# Summary
echo "================================================================"
echo -e "${BLUE}Setup Summary${NC}"
echo "================================================================"
echo ""

# Check what's ready
READY=true

if [ ! -f ".gitignore" ]; then
    echo -e "${RED}✗ .gitignore missing${NC}"
    READY=false
else
    echo -e "${GREEN}✓ .gitignore configured${NC}"
fi

if [ ! -d "$VENV_DIR" ]; then
    echo -e "${RED}✗ Virtual environment missing${NC}"
    READY=false
else
    echo -e "${GREEN}✓ Virtual environment ready${NC}"
fi

if [ ! -f "credentials/credentials.json" ]; then
    echo -e "${RED}✗ Google credentials missing${NC}"
    READY=false
else
    echo -e "${GREEN}✓ Google credentials present${NC}"
fi

if [ ! -f "$API_KEY_DIR/api_key.dat" ]; then
    echo -e "${RED}✗ Anthropic API key missing${NC}"
    READY=false
else
    echo -e "${GREEN}✓ Anthropic API key present${NC}"
fi

echo ""

if [ "$READY" = true ]; then
    echo -e "${GREEN}================================================================${NC}"
    echo -e "${GREEN}✓ Setup Complete! Ready to run.${NC}"
    echo -e "${GREEN}================================================================${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Activate virtual environment: source ../../venv/bin/activate"
    echo "2. Install dependencies: pip install -r requirements.txt"
    echo "3. Configure config.yaml"
    echo "4. Run the application: ./run.sh"
else
    echo -e "${YELLOW}================================================================${NC}"
    echo -e "${YELLOW}⚠ Setup Incomplete - Action Required${NC}"
    echo -e "${YELLOW}================================================================${NC}"
    echo ""
    echo "Please complete the missing steps above."
    echo "See INSTALLATION_GUIDE.md for detailed instructions."
fi

echo ""
echo "For help:"
echo "  - Quick setup: SETUP.md"
echo "  - Full guide: INSTALLATION_GUIDE.md"
echo "  - Security: SECURITY.md"
echo ""
