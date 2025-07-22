#!/usr/bin/env python3
"""
Adetailer Image Generation Script.

This script generates images with enhanced face details using Adetailer.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from flux_generator.core.adetailer import AdetailerGenerator
from flux_generator.utils.logger import get_logger

logger = get_logger(__name__)


def main():
    """Main function for Adetailer generation."""
    try:
        # Initialize Adetailer generator
        generator = AdetailerGenerator()
        
        # Test connection
        if not generator.test_connection():
            print("❌ Failed to connect to FLUX API. Check your API key.")
            return 1
        
        print("✅ Connected to FLUX API successfully!")
        
        # Get input image info
        image_info = generator.get_input_image_info()
        print(f"📸 Input image: {image_info['path']}")
        print(f"📏 Size: {image_info['width']}x{image_info['height']}")
        
        # Show Adetailer settings
        print("\n🔧 Adetailer Settings:")
        print(f"  Model: {generator.adetailer_settings.model}")
        print(f"  Confidence: {generator.adetailer_settings.confidence}")
        print(f"  Denoising Strength: {generator.adetailer_settings.denoising_strength}")
        print(f"  Steps: {generator.adetailer_settings.steps}")
        print(f"  CFG Scale: {generator.adetailer_settings.cfg_scale}")
        print(f"  Sampler: {generator.adetailer_settings.sampler}")
        
        # Generate single image with Adetailer
        print("\n🚀 Starting Adetailer generation...")
        output_path = generator.generate_with_adetailer()
        
        if output_path:
            print(f"✅ Adetailer enhanced image generated: {output_path}")
            return 0
        else:
            print("❌ Failed to generate Adetailer enhanced image")
            return 1
            
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Main error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 