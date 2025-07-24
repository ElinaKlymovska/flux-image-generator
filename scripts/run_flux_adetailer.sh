#!/bin/bash

# FLUX API Adetailer Processing Script
# This script processes images with FLUX API enhancement

echo "🎭 FLUX API Adetailer Processing"
echo "=================================="

# Check if we're in the right directory
if [ ! -f "bin/process_with_flux_adetailer.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Warning: Virtual environment not detected"
    echo "💡 Consider activating it: source venv/bin/activate"
fi

# Check if API key is set
if [ -z "$BFL_API_KEY" ]; then
    echo "⚠️  Warning: BFL_API_KEY not set"
    echo "💡 Set your API key: export BFL_API_KEY='your_api_key_here'"
fi

echo ""
echo "🚀 Starting FLUX API Adetailer processing..."
echo "📁 Input: data/output/ (all images)"
echo "📁 Output: data/output/flux_enhanced/"
echo ""

# Run the processing script
python bin/process_with_flux_adetailer.py

# Check exit status
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ FLUX Adetailer processing completed successfully!"
    echo "📁 Check results in: data/output/flux_enhanced/"
else
    echo ""
    echo "❌ FLUX Adetailer processing failed!"
    exit 1
fi 