#!/usr/bin/env python3
"""
Process Existing Images with Adetailer Script.

This script processes existing images in the output directory with Adetailer face enhancement.
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
    """Main function for processing existing images with Adetailer."""
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
        
        # Custom Adetailer settings for processing existing images
        adetailer_config = {
            'confidence': 0.4,  # Higher confidence for better detection
            'denoising_strength': 0.5,  # Stronger denoising
            'steps': 25,  # More steps for better quality
            'cfg_scale': 8.0,  # Higher CFG for more detail
            'prompt': 'beautiful face, detailed eyes, perfect skin, high quality, ultra realistic'
        }
        
        # Define output directory
        output_dir = Path("data/output/adetailer_processed")
        print(f"\n📁 Output directory: {output_dir}")
        
        # Process existing images
        print("\n🚀 Starting Adetailer processing of existing images...")
        output_paths = generator.process_existing_images(
            file_pattern="*.jpg",  # Process all JPG files
            output_dir=output_dir,
            adetailer_config=adetailer_config,
            output_suffix="_adetailer"
        )
        
        if output_paths:
            print(f"\n✅ Successfully processed {len(output_paths)} images:")
            for i, path in enumerate(output_paths, 1):
                print(f"  {i}. {path}")
            print(f"\n📁 All enhanced images saved to: {output_dir}")
            return 0
        else:
            print("❌ No images were processed")
            return 1
            
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Main error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 