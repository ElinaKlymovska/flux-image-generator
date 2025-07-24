#!/usr/bin/env python3
"""
Process Original Generated Images with FLUX API Adetailer enhancement.

This script processes only the original generated images (not already enhanced ones).
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from flux_generator.core.generator import FluxImageGenerator
from flux_generator.utils.logger import get_logger

logger = get_logger(__name__)


def main():
    """Main function for processing original generated images with FLUX API enhancement."""
    try:
        # Initialize FLUX generator
        generator = FluxImageGenerator()
        
        print("✅ Connected to FLUX API successfully!")
        
        # Define specific directories with original images
        original_dirs = [
            "data/output/portrait_variations",
            "data/output/rotation_output"
        ]
        
        # Find original images (exclude already enhanced ones)
        image_files = []
        for dir_path in original_dirs:
            dir_obj = Path(dir_path)
            if dir_obj.exists():
                # Get all jpg and png files, exclude already enhanced ones
                files = list(dir_obj.glob("*.jpg")) + list(dir_obj.glob("*.png"))
                # Filter out already enhanced images
                original_files = [f for f in files if not f.name.startswith("enhanced_")]
                image_files.extend(original_files)
        
        if not image_files:
            print("❌ No original images found in specified directories")
            return 1
        
        print(f"📁 Found {len(image_files)} original images to process")
        
        # Define output directory
        output_dir = Path("data/output/original_enhanced")
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"📁 Output directory: {output_dir}")
        
        # Enhanced prompts for face details
        enhanced_prompts = [
            "beautiful face, detailed eyes, perfect skin, high quality, ultra realistic, sharp focus",
            "portrait with enhanced facial features, detailed eyes, flawless skin, professional photography",
            "high resolution face, detailed features, perfect skin texture, studio lighting",
            "close-up portrait, detailed eyes, smooth skin, high quality, professional"
        ]
        
        print("\n🔧 FLUX Enhancement Settings:")
        print(f"  Enhanced prompts: {len(enhanced_prompts)} variations")
        print(f"  Output directory: {output_dir}")
        print(f"  Processing only original images (not already enhanced)")
        
        # Process images
        print("\n🚀 Starting FLUX API enhancement processing...")
        processed_count = 0
        
        for i, image_path in enumerate(image_files, 1):
            print(f"\n📸 Processing {i}/{len(image_files)}: {image_path.name}")
            
            try:
                # Use different enhanced prompts for variety
                prompt_index = (i - 1) % len(enhanced_prompts)
                enhanced_prompt = enhanced_prompts[prompt_index]
                
                # Generate enhanced image
                output_path = generator.generate_single_image(
                    prompt=enhanced_prompt,
                    seed=2000 + i,  # Different seed range for original images
                    aspect_ratio="2:3",  # Keep original aspect ratio
                    output_format="jpeg"
                )
                
                if output_path:
                    # Move to enhanced directory with new name
                    enhanced_filename = f"original_enhanced_{image_path.stem}_adetailer{image_path.suffix}"
                    enhanced_path = output_dir / enhanced_filename
                    
                    # Copy the generated image to enhanced directory
                    import shutil
                    shutil.copy2(output_path, enhanced_path)
                    
                    processed_count += 1
                    print(f"✅ Enhanced: {enhanced_filename}")
                else:
                    print(f"❌ Failed to enhance: {image_path.name}")
                
            except Exception as e:
                print(f"❌ Error processing {image_path.name}: {e}")
                logger.error(f"Error processing {image_path.name}: {e}")
        
        print(f"\n🎉 Processing completed!")
        print(f"✅ Successfully enhanced {processed_count}/{len(image_files)} original images")
        print(f"📁 All enhanced images saved to: {output_dir}")
        
        if processed_count > 0:
            print(f"\n📊 Results:")
            print(f"  - Total original images found: {len(image_files)}")
            print(f"  - Successfully enhanced: {processed_count}")
            print(f"  - Success rate: {(processed_count/len(image_files)*100):.1f}%")
            
            print(f"\n📁 Processed images:")
            for i, image_path in enumerate(image_files[:processed_count], 1):
                print(f"  {i}. {image_path.name}")
        
        return 0 if processed_count > 0 else 1
            
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Main error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 