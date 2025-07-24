#!/usr/bin/env python3
"""
FLUX API Adetailer Processing for 6 Images
Processes exactly 6 images with high-quality Adetailer-style enhancement
"""

import os
import sys
import time
import shutil
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from flux_generator.core.generator import FluxImageGenerator
from flux_generator.utils.logger import setup_logger

def main():
    """Process 6 images with FLUX API Adetailer enhancement"""
    
    # Setup logging
    logger = setup_logger(__name__)
    
    # Configuration
    input_dir = Path("data/output/woman")
    output_dir = Path("data/output/six_enhanced")
    output_dir.mkdir(exist_ok=True)
    
    # Get first 6 images from woman directory
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png']:
        image_files.extend(input_dir.glob(ext))
    
    # Sort and take first 6
    image_files = sorted(image_files)[:6]
    
    if not image_files:
        print("❌ No images found in input directory")
        return
    
    print(f"✅ Found {len(image_files)} images to process")
    print(f"📁 Input directory: {input_dir}")
    print(f"📁 Output directory: {output_dir}")
    
    # FLUX API Enhancement Settings
    enhancement_prompts = [
        "ultra detailed face, perfect skin texture, sharp eyes, detailed lips, professional portrait photography, 8k resolution",
        "cinematic lighting, dramatic shadows, high contrast, detailed facial features, professional studio lighting",
        "soft natural lighting, smooth skin, gentle shadows, elegant portrait, high quality photography",
        "artistic portrait, detailed facial features, creative lighting, professional photography, sharp focus"
    ]
    
    print(f"\n🔧 FLUX Enhancement Settings:")
    print(f"  Enhanced prompts: {len(enhancement_prompts)} variations")
    print(f"  Output directory: {output_dir}")
    print(f"  Processing first 6 images")
    
    print(f"\n🚀 Starting FLUX API enhancement processing...")
    
    # Test connection first
    try:
        test_generator = FluxImageGenerator()
        if test_generator.test_connection():
            print("✅ Connected to FLUX API successfully!")
        else:
            print("❌ Failed to connect to FLUX API")
            return
    except Exception as e:
        print(f"❌ Failed to connect to FLUX API: {e}")
        return
    
    successful = 0
    failed = 0
    
    for i, image_path in enumerate(image_files, 1):
        image_name = image_path.name
        print(f"\n📸 Processing {i}/6: {image_name}")
        
        try:
            # Copy current image to input directory for processing
            input_image_path = Path("data/input/character.jpg")
            shutil.copy2(image_path, input_image_path)
            
            # Initialize generator with current image
            generator = FluxImageGenerator()
            
            # Process with each enhancement prompt
            for prompt_idx, prompt in enumerate(enhancement_prompts, 1):
                try:
                    # Generate enhanced image
                    result_path = generator.generate_single_image(
                        prompt=prompt,
                        seed=2000 + i * 10 + prompt_idx
                    )
                    
                    if result_path and result_path.exists():
                        # Move to our output directory with custom name
                        output_filename = f"{image_path.stem}_enhanced_{prompt_idx}.jpg"
                        output_path = output_dir / output_filename
                        
                        shutil.move(str(result_path), str(output_path))
                        
                        print(f"  ✅ Enhanced variation {prompt_idx}/4: {output_filename}")
                        
                        # Small delay between requests
                        time.sleep(1)
                    else:
                        print(f"  ❌ Failed to generate variation {prompt_idx}")
                        failed += 1
                        
                except Exception as e:
                    print(f"  ❌ Error processing variation {prompt_idx}: {e}")
                    failed += 1
                    continue
            
            successful += 1
            print(f"✅ Successfully enhanced: {image_name}")
            
        except Exception as e:
            print(f"❌ Failed to enhance: {image_name}")
            print(f"   Error: {e}")
            failed += 1
            continue
    
    print(f"\n🎉 Processing completed!")
    print(f"✅ Successfully enhanced {successful}/6 images")
    print(f"❌ Failed: {failed} variations")
    print(f"📁 All enhanced images saved to: {output_dir}")
    
    # List generated files
    if output_dir.exists():
        generated_files = list(output_dir.glob("*.jpg"))
        print(f"\n📋 Generated files ({len(generated_files)} total):")
        for file in sorted(generated_files):
            print(f"  - {file.name}")

if __name__ == "__main__":
    main() 