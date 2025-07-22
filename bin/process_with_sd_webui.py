#!/usr/bin/env python3
"""
Process Images with Stable Diffusion WebUI and Adetailer.

This script processes existing images using SD WebUI with Adetailer support.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from flux_generator.core.sd_webui_client import SDWebUIClient
from flux_generator.utils.logger import get_logger

logger = get_logger(__name__)


def main():
    """Main function for processing images with SD WebUI and Adetailer."""
    try:
        # Initialize SD WebUI client
        client = SDWebUIClient("http://localhost:7860")
        
        # Test connection
        if not client.test_connection():
            print("❌ Failed to connect to Stable Diffusion WebUI.")
            print("💡 Make sure SD WebUI is running with --api flag:")
            print("   ./webui.sh --api")
            return 1
        
        print("✅ Connected to Stable Diffusion WebUI successfully!")
        
        # Find all images in output directory
        input_dir = Path("data/output")
        image_files = list(input_dir.rglob("*.jpg")) + list(input_dir.rglob("*.png"))
        
        if not image_files:
            print("❌ No images found in data/output directory")
            return 1
        
        print(f"📁 Found {len(image_files)} images to process")
        
        # Define output directory
        output_dir = Path("data/output/sd_webui_processed")
        print(f"📁 Output directory: {output_dir}")
        
        # Adetailer configuration
        adetailer_config = {
            "model": "face_yolov8n.pt",
            "confidence": 0.4,
            "dilation": 4,
            "denoising_strength": 0.5,
            "steps": 25,
            "cfg_scale": 8.0,
            "sampler": "DPM++ 2M Karras",
            "width": 512,
            "height": 512
        }
        
        print("\n🔧 Adetailer Settings:")
        for key, value in adetailer_config.items():
            print(f"  {key}: {value}")
        
        # Process images
        print("\n🚀 Starting SD WebUI processing with Adetailer...")
        processed_paths = client.process_multiple_images(
            image_paths=image_files,
            output_dir=output_dir,
            prompt="beautiful face, detailed eyes, perfect skin, high quality, ultra realistic",
            negative_prompt="blurry, low quality, distorted",
            adetailer_config=adetailer_config,
            output_suffix="_adetailer"
        )
        
        if processed_paths:
            print(f"\n✅ Successfully processed {len(processed_paths)} images:")
            for i, path in enumerate(processed_paths, 1):
                print(f"  {i}. {path.name}")
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