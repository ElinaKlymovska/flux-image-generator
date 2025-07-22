#!/usr/bin/env python3
"""
Example usage of Adetailer Image Generator.

This example demonstrates how to use the Adetailer generator for enhanced face details.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from flux_generator.core.adetailer import AdetailerGenerator
from flux_generator.utils.logger import get_logger

logger = get_logger(__name__)


def example_single_generation():
    """Example of single image generation with Adetailer."""
    print("=== Single Image Generation with Adetailer ===")
    
    try:
        # Initialize generator
        generator = AdetailerGenerator()
        
        # Test connection
        if not generator.test_connection():
            print("❌ Connection failed")
            return
        
        print("✅ Connection successful")
        
        # Custom Adetailer settings
        adetailer_config = {
            'confidence': 0.4,  # Higher confidence for better detection
            'denoising_strength': 0.5,  # Stronger denoising
            'steps': 25,  # More steps for better quality
            'cfg_scale': 8.0,  # Higher CFG for more detail
            'prompt': 'beautiful face, detailed eyes, perfect skin, high quality, ultra realistic'
        }
        
        # Generate image
        output_path = generator.generate_with_adetailer(
            prompt="A beautiful woman with realistic face details",
            seed=12345,
            aspect_ratio="2:3",
            output_format="jpeg",
            adetailer_config=adetailer_config
        )
        
        if output_path:
            print(f"✅ Generated: {output_path}")
        else:
            print("❌ Generation failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def example_batch_generation():
    """Example of batch image generation with Adetailer."""
    print("\n=== Batch Image Generation with Adetailer ===")
    
    try:
        # Initialize generator
        generator = AdetailerGenerator()
        
        # Test connection
        if not generator.test_connection():
            print("❌ Connection failed")
            return
        
        print("✅ Connection successful")
        
        # Custom Adetailer settings for batch
        adetailer_config = {
            'confidence': 0.3,  # Standard confidence
            'denoising_strength': 0.4,  # Standard denoising
            'steps': 20,  # Standard steps
            'cfg_scale': 7.0,  # Standard CFG
            'prompt': 'beautiful face, detailed eyes, perfect skin, high quality'
        }
        
        # Generate multiple images
        output_paths = generator.generate_multiple_with_adetailer(
            count=3,  # Generate 3 images
            start_seed=1000,
            prompt="A beautiful woman with enhanced face details",
            aspect_ratio="2:3",
            output_format="jpeg",
            adetailer_config=adetailer_config
        )
        
        if output_paths:
            print(f"✅ Generated {len(output_paths)} images:")
            for i, path in enumerate(output_paths, 1):
                print(f"  {i}. {path}")
        else:
            print("❌ No images generated")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def example_custom_settings():
    """Example of customizing Adetailer settings."""
    print("\n=== Custom Adetailer Settings ===")
    
    try:
        # Initialize generator
        generator = AdetailerGenerator()
        
        # Update Adetailer settings
        generator.update_adetailer_settings(
            confidence=0.5,
            denoising_strength=0.6,
            steps=30,
            cfg_scale=9.0,
            sampler="Euler a",
            prompt="ultra detailed face, perfect skin texture, realistic eyes, high resolution",
            negative_prompt="blurry, low quality, distorted, deformed, ugly"
        )
        
        print("✅ Settings updated successfully")
        
        # Show current settings
        print("\nCurrent Adetailer Settings:")
        print(f"  Confidence: {generator.adetailer_settings.confidence}")
        print(f"  Denoising Strength: {generator.adetailer_settings.denoising_strength}")
        print(f"  Steps: {generator.adetailer_settings.steps}")
        print(f"  CFG Scale: {generator.adetailer_settings.cfg_scale}")
        print(f"  Sampler: {generator.adetailer_settings.sampler}")
        print(f"  Prompt: {generator.adetailer_settings.prompt}")
        print(f"  Negative Prompt: {generator.adetailer_settings.negative_prompt}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Main function to run all examples."""
    print("🚀 Adetailer Generator Examples")
    print("=" * 50)
    
    # Run examples
    example_single_generation()
    example_batch_generation()
    example_custom_settings()
    
    print("\n✅ All examples completed!")


if __name__ == "__main__":
    main() 