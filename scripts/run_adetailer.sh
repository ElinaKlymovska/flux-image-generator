#!/bin/bash

# Adetailer Image Generation Script
# This script generates images with enhanced face details using Adetailer

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

# Check if output directory exists
mkdir -p data/output

# Run Adetailer generation
print_status "Starting Adetailer image generation..."
python bin/generate_adetailer.py

if [ $? -eq 0 ]; then
    print_success "Adetailer generation completed successfully!"
    print_status "Check the data/output directory for generated images"
else
    print_error "Adetailer generation failed!"
    exit 1
fi 