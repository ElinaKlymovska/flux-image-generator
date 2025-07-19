#!/bin/bash

# Run Portrait Variations Generation Script
# This script generates portrait images (2:3) for all 12 styles and all qualities

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  FLUX Image Generator - Portrait Only${NC}"
echo -e "${BLUE}========================================${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install requirements
echo -e "${YELLOW}Installing requirements...${NC}"
pip install -r requirements.txt

# Check if API key is set
if [ -z "$FLUX_API_KEY" ]; then
    echo -e "${RED}Error: FLUX_API_KEY environment variable is not set${NC}"
    echo -e "${YELLOW}Please set your API key:${NC}"
    echo -e "export FLUX_API_KEY='your_api_key_here'"
    exit 1
fi

# Check if input image exists
if [ ! -f "data/input/character.jpg" ]; then
    echo -e "${RED}Error: Input image not found${NC}"
    echo -e "${YELLOW}Please place character.jpg in data/input/ directory${NC}"
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p data/output/portrait_variations

echo -e "${GREEN}Starting generation of portrait variations...${NC}"
echo -e "${YELLOW}This will generate portrait images (2:3) for all 12 styles and all qualities${NC}"
echo ""

# Run the generation script
python bin/generate_portrait_variations.py

echo ""
echo -e "${GREEN}Generation completed!${NC}"
echo -e "${BLUE}Check data/output/portrait_variations/ for generated images${NC}"
echo -e "${BLUE}Check portrait_variations_results.json for detailed results${NC}" 