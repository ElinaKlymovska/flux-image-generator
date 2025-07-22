#!/bin/bash

# Process Existing Images with Adetailer Script
# This script processes existing images in the output directory with Adetailer face enhancement

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
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

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_warning "Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
print_status "Installing/upgrading dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check if input image exists
if [ ! -f "data/input/character.jpg" ]; then
    print_error "Input image not found at data/input/character.jpg"
    print_status "Please place your character image in the data/input directory"
    exit 1
fi

# Check if output directory exists and has images
if [ ! -d "data/output" ]; then
    print_error "Output directory does not exist: data/output"
    print_status "Please generate some images first or create the output directory"
    exit 1
fi

# Check if there are images in output directory
image_count=$(find data/output -name "*.jpg" -o -name "*.png" | wc -l)
if [ "$image_count" -eq 0 ]; then
    print_warning "No images found in data/output directory"
    print_status "Please generate some images first or check the output directory"
    exit 1
fi

print_status "Found $image_count images in output directory"

# Run Adetailer processing
print_status "Starting Adetailer processing of existing images..."
python bin/process_existing_with_adetailer.py

if [ $? -eq 0 ]; then
    print_success "Adetailer processing completed successfully!"
    print_status "Check the data/output directory for enhanced images (with _adetailer suffix)"
else
    print_error "Adetailer processing failed!"
    exit 1
fi 