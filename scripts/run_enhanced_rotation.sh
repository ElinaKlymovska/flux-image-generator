#!/bin/bash

# Enhanced Character Rotation Script
# Uses Black Forest Labs best practices and presets

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🎭 Enhanced Character Rotation Generator${NC}"
echo -e "${BLUE}=====================================${NC}"

# Check if API key is set (only for generation commands)
check_api_key() {
    if [ -z "$BFL_API_KEY" ] && [ -z "$FLUX_API_KEY" ]; then
        echo -e "${RED}❌ Error: BFL_API_KEY or FLUX_API_KEY environment variable is required${NC}"
        exit 1
    fi
}

# Default values
ANGLES="front left back right"
STYLE="ultra_realistic"
STEPS=""
CUSTOM_PROMPT=""
USE_PRESETS=true
START_SEED=1001

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --help)
            echo "Enhanced Character Rotation Generator"
            echo ""
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --angles ANGLE1,ANGLE2,...  Rotation angles to generate (default: front,left,back,right)"
            echo "  --style STYLE               Generation style (default: ultra_realistic)"
            echo "  --steps N                   Generate 360-degree sequence with N steps"
            echo "  --custom-prompt PROMPT      Custom prompt for character description"
            echo "  --no-presets                Disable presets and use original method"
            echo "  --start-seed SEED           Starting seed for generation (default: 1001)"
            echo "  --test-connection           Test API connection before generation"
            echo "  --list-presets              List available rotation presets"
            echo "  --preset-info PRESET        Show detailed information about a preset"
            echo "  --help                      Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0 --angles front,left,back,right --custom-prompt 'portrait of a woman with brown hair'"
            echo "  $0 --steps 8 --custom-prompt 'portrait of a woman in professional attire'"
            echo "  $0 --list-presets"
            echo "  $0 --preset-info rotation_front"
            exit 0
            ;;
        --list-presets)
            echo -e "${YELLOW}📋 Available rotation presets:${NC}"
            python bin/generate_rotation.py --list-presets
            exit 0
            ;;
        --preset-info)
            echo -e "${YELLOW}📖 Preset information:${NC}"
            python bin/generate_rotation.py --preset-info "$2"
            exit 0
            ;;
        --test-connection)
            check_api_key
            echo -e "${YELLOW}🔍 Testing API connection...${NC}"
            python bin/test_connection.py
            exit $?
            ;;
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
        --custom-prompt)
            CUSTOM_PROMPT="$2"
            shift 2
            ;;
        --no-presets)
            USE_PRESETS=false
            shift
            ;;
        --start-seed)
            START_SEED="$2"
            shift 2
            ;;
        *)
            echo -e "${RED}❌ Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Check API key for generation commands
check_api_key

# Convert comma-separated angles to space-separated
ANGLES=$(echo "$ANGLES" | tr ',' ' ')

echo -e "${YELLOW}📋 Configuration:${NC}"
echo "  Angles: $ANGLES"
echo "  Style: $STYLE"
if [ -n "$STEPS" ]; then
    echo "  Steps: $STEPS"
fi
if [ -n "$CUSTOM_PROMPT" ]; then
    echo "  Custom prompt: $CUSTOM_PROMPT"
fi
echo "  Use presets: $USE_PRESETS"
echo "  Start seed: $START_SEED"

# Build command
CMD="python bin/generate_rotation.py"

if [ -n "$STEPS" ]; then
    CMD="$CMD --steps $STEPS"
else
    CMD="$CMD --angles $ANGLES"
fi

CMD="$CMD --style $STYLE --start-seed $START_SEED"

if [ -n "$CUSTOM_PROMPT" ]; then
    CMD="$CMD --custom-prompt '$CUSTOM_PROMPT'"
fi

if [ "$USE_PRESETS" = true ]; then
    CMD="$CMD --use-presets"
else
    CMD="$CMD --no-presets"
fi

echo -e "${YELLOW}🚀 Starting generation...${NC}"
echo "Command: $CMD"

# Execute the command
eval $CMD

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Enhanced rotation generation completed successfully!${NC}"
else
    echo -e "${RED}❌ Enhanced rotation generation failed${NC}"
    exit 1
fi 