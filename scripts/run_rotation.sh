#!/bin/bash

# Character Rotation Generator Script
# This script generates character images from different rotation angles

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}=== Character Rotation Generator ===${NC}"
echo -e "${BLUE}Project directory: ${PROJECT_DIR}${NC}"

# Check if virtual environment exists
if [ -d "$PROJECT_DIR/venv" ]; then
    echo -e "${GREEN}Activating virtual environment...${NC}"
    source "$PROJECT_DIR/venv/bin/activate"
else
    echo -e "${YELLOW}Virtual environment not found. Using system Python.${NC}"
fi

# Check if input image exists
INPUT_DIR="$PROJECT_DIR/data/input"
if [ ! -f "$INPUT_DIR/character.jpg" ] && [ ! -f "$INPUT_DIR/character.png" ]; then
    echo -e "${RED}Error: Input image not found in $INPUT_DIR${NC}"
    echo -e "${YELLOW}Please place character.jpg or character.png in the input directory.${NC}"
    exit 1
fi

# Default values
ANGLES="front left back right"
STYLE="ultra_realistic"
STEPS=""
START_SEED=1001
CUSTOM_PROMPT=""
OUTPUT_DIR="rotation"
API_KEY=""
TEST_CONNECTION=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --angles)
            ANGLES="$2"
            shift 2
            ;;
        --style)
            STYLE="$2"
            shift 2
            ;;
        --steps)
            STEPS="$2"
            shift 2
            ;;
        --start-seed)
            START_SEED="$2"
            shift 2
            ;;
        --custom-prompt)
            CUSTOM_PROMPT="$2"
            shift 2
            ;;
        --output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --api-key)
            API_KEY="$2"
            shift 2
            ;;
        --test-connection)
            TEST_CONNECTION=true
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --angles ANGLE1 ANGLE2...    Rotation angles to generate (default: front left back right)"
            echo "  --style STYLE                Generation style (default: ultra_realistic)"
            echo "  --steps N                    Number of steps for 360-degree sequence (4-12)"
            echo "  --start-seed SEED            Starting seed for generation (default: 1001)"
            echo "  --custom-prompt PROMPT       Custom prompt to add to rotation"
            echo "  --output-dir DIR             Output subdirectory (default: rotation)"
            echo "  --api-key KEY                FLUX API key"
            echo "  --test-connection            Test API connection before generation"
            echo "  --help                       Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0 --angles front left back right"
            echo "  $0 --steps 8 --style cinematic"
            echo "  $0 --custom-prompt 'wearing red dress' --style fashion"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Build command
CMD="python $PROJECT_DIR/bin/generate_rotation.py"

if [ -n "$ANGLES" ]; then
    CMD="$CMD --angles $ANGLES"
fi

if [ -n "$STYLE" ]; then
    CMD="$CMD --style $STYLE"
fi

if [ -n "$STEPS" ]; then
    CMD="$CMD --steps $STEPS"
fi

if [ -n "$START_SEED" ]; then
    CMD="$CMD --start-seed $START_SEED"
fi

if [ -n "$CUSTOM_PROMPT" ]; then
    CMD="$CMD --custom-prompt '$CUSTOM_PROMPT'"
fi

if [ -n "$OUTPUT_DIR" ]; then
    CMD="$CMD --output-dir $OUTPUT_DIR"
fi

if [ -n "$API_KEY" ]; then
    CMD="$CMD --api-key $API_KEY"
fi

if [ "$TEST_CONNECTION" = true ]; then
    CMD="$CMD --test-connection"
fi

# Show configuration
echo -e "${BLUE}Configuration:${NC}"
echo -e "  Style: ${GREEN}$STYLE${NC}"
if [ -n "$STEPS" ]; then
    echo -e "  Steps: ${GREEN}$STEPS${NC}"
else
    echo -e "  Angles: ${GREEN}$ANGLES${NC}"
fi
echo -e "  Start seed: ${GREEN}$START_SEED${NC}"
if [ -n "$CUSTOM_PROMPT" ]; then
    echo -e "  Custom prompt: ${GREEN}$CUSTOM_PROMPT${NC}"
fi
echo -e "  Output directory: ${GREEN}$OUTPUT_DIR${NC}"
if [ "$TEST_CONNECTION" = true ]; then
    echo -e "  Test connection: ${GREEN}Yes${NC}"
fi

echo ""
echo -e "${BLUE}Starting rotation generation...${NC}"

# Execute command
eval $CMD

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Rotation generation completed successfully!${NC}"
    echo -e "${BLUE}Check output in: $PROJECT_DIR/data/output/$OUTPUT_DIR${NC}"
else
    echo -e "${RED}Rotation generation failed!${NC}"
    exit 1
fi 