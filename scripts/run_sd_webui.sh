#!/bin/bash

# Process Images with Stable Diffusion WebUI and Adetailer
# This script processes existing images using SD WebUI with Adetailer support

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

# Check if SD WebUI is running
print_status "Checking SD WebUI connection..."
if ! curl -s http://localhost:7860/sdapi/v1/progress > /dev/null; then
    print_error "Stable Diffusion WebUI is not running on localhost:7860"
    print_status "Please start SD WebUI with API enabled:"
    echo "   cd /path/to/stable-diffusion-webui"
    echo "   ./webui.sh --api"
    echo ""
    print_status "Or install SD WebUI:"
    echo "   git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui"
    echo "   cd stable-diffusion-webui"
    echo "   git clone https://github.com/Bing-su/adetailer extensions/adetailer"
    echo "   ./webui.sh --api"
    exit 1
fi

print_success "SD WebUI is running and accessible!"

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

# Create sd_webui_processed directory
sd_output_dir="data/output/sd_webui_processed"
print_status "Creating output directory: $sd_output_dir"
mkdir -p "$sd_output_dir"

# Run SD WebUI processing
print_status "Starting SD WebUI processing with Adetailer..."
python bin/process_with_sd_webui.py

if [ $? -eq 0 ]; then
    print_success "SD WebUI processing completed successfully!"
    print_status "Enhanced images saved to: $sd_output_dir"
    
    # Show processed images count
    processed_count=$(find "$sd_output_dir" -name "*.jpg" -o -name "*.png" | wc -l)
    print_status "Processed $processed_count images with SD WebUI and Adetailer"
else
    print_error "SD WebUI processing failed!"
    exit 1
fi 