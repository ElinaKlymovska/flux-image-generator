#!/bin/bash

# FLUX 1.1 [pro] Character Rotation Generator Script (Version 3)
# This script generates character images from different rotation angles using FLUX API with ultra and raw mode

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BIN_DIR="$PROJECT_DIR/bin"

# Default values
ANGLES="10 20 30 45 60 90 135 180"
INPUT_IMAGE="/Users/ElinaKlymovska/CursorIA/Art/SenteticData/data/input/character.jpg"
SEED=123456
OUTPUT_DIR="rotation_output"
API_KEY=""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -a, --angles ANGLE1 ANGLE2 ...  Rotation angles to generate (default: 10 20 30 45 60 90 135 180)"
    echo "  -i, --input-image PATH          Input character image path"
    echo "  -s, --seed SEED                 Seed for generation (default: 123456)"
    echo "  -o, --output-dir DIR            Output directory (default: rotation_output)"
    echo "  -k, --api-key KEY               FLUX API key (will use environment variable if not provided)"
    echo "  -t, --test-connection           Test API connection before generation"
    echo "  -h, --help                      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0"
    echo "  $0 -a 45 90 135 -s 999999"
    echo "  $0 -i /path/to/character.jpg -o my_rotations"
    echo "  $0 -k YOUR_API_KEY -t"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -a|--angles)
            ANGLES="$2"
            shift 2
            ;;
        -i|--input-image)
            INPUT_IMAGE="$2"
            shift 2
            ;;
        -s|--seed)
            SEED="$2"
            shift 2
            ;;
        -o|--output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -k|--api-key)
            API_KEY="$2"
            shift 2
            ;;
        -t|--test-connection)
            TEST_CONNECTION="--test-connection"
            shift
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Check if Python script exists
PYTHON_SCRIPT="$BIN_DIR/generate_flux_rotation_v3.py"
if [[ ! -f "$PYTHON_SCRIPT" ]]; then
    print_error "Python script not found: $PYTHON_SCRIPT"
    exit 1
fi

# Check if input image exists
if [[ ! -f "$INPUT_IMAGE" ]]; then
    print_error "Input image not found: $INPUT_IMAGE"
    exit 1
fi

# Print configuration
print_info "FLUX 1.1 [pro] Character Rotation Generator (Version 3)"
print_info "====================================================="
print_info "Angles: $ANGLES"
print_info "Input image: $INPUT_IMAGE"
print_info "Seed: $SEED"
print_info "Output directory: $OUTPUT_DIR"
if [[ -n "$API_KEY" ]]; then
    print_info "API key: ${API_KEY:0:8}..."
else
    print_info "API key: Will use environment variable (BFL_API_KEY)"
fi

# Activate virtual environment if it exists
if [[ -d "$PROJECT_DIR/venv" ]]; then
    print_info "Activating virtual environment..."
    source "$PROJECT_DIR/venv/bin/activate"
fi

# Run the Python script
print_info "Starting generation..."
cd "$PROJECT_DIR"

python "$PYTHON_SCRIPT" \
    --angles $ANGLES \
    --input-image "$INPUT_IMAGE" \
    --seed "$SEED" \
    --output-dir "$OUTPUT_DIR" \
    ${API_KEY:+--api-key "$API_KEY"} \
    $TEST_CONNECTION

# Check exit status
if [[ $? -eq 0 ]]; then
    print_success "Rotation generation completed successfully!"
    print_info "Generated images saved in: $OUTPUT_DIR"
    
    # Show generated files
    if [[ -d "$OUTPUT_DIR" ]]; then
        print_info "Generated files:"
        for file in "$OUTPUT_DIR"/rotation_*.jpg; do
            if [[ -f "$file" ]]; then
                filename=$(basename "$file")
                filesize=$(ls -lh "$file" | awk '{print $5}')
                print_info "  $filename ($filesize)"
            fi
        done
    fi
else
    print_error "Rotation generation failed!"
    exit 1
fi 