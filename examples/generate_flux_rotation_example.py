#!/usr/bin/env python3
"""
Example script for FLUX 1.1 [pro] Character Rotation Generator.

This example demonstrates how to use the FluxProRotationGenerator class
to generate character rotation images programmatically.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from flux_generator.utils.logger import get_logger

# Import the generator class
sys.path.insert(0, str(Path(__file__).parent.parent / "bin"))
from generate_flux_rotation import FluxProRotationGenerator

logger = get_logger(__name__)


def main():
    """Example usage of FluxProRotationGenerator."""
    
    # Configuration
    API_KEY = "your_flux_api_key_here"  # Replace with your actual API key
    INPUT_IMAGE = "/Users/ElinaKlymovska/CursorIA/Art/SenteticData/data/input/character.jpg"
    OUTPUT_DIR = "example_rotation_output"
    SEED = 123456
    
    # Define rotation angles
    angles = [10, 20, 30, 45, 60, 90, 135, 180]
    
    try:
        # Initialize the generator
        logger.info("Initializing FLUX 1.1 [pro] Rotation Generator...")
        generator = FluxProRotationGenerator(
            api_key=API_KEY,
            output_dir=OUTPUT_DIR
        )
        
        # Test API connection
        logger.info("Testing API connection...")
        if not generator.test_connection():
            logger.error("API connection test failed. Please check your API key.")
            return 1
        
        logger.info("API connection test successful!")
        
        # Check if input image exists
        input_image_path = Path(INPUT_IMAGE)
        if not input_image_path.exists():
            logger.error(f"Input image not found: {input_image_path}")
            return 1
        
        # Generate all rotations
        logger.info("Starting rotation generation...")
        results = generator.generate_all_rotations(
            angles=angles,
            input_image_path=input_image_path,
            seed=SEED
        )
        
        # Print results
        successful = sum(1 for r in results.values() if r is not None)
        total = len(results)
        
        logger.info(f"\n{'='*50}")
        logger.info("GENERATION RESULTS")
        logger.info(f"{'='*50}")
        logger.info(f"Total angles: {total}")
        logger.info(f"Successful: {successful}")
        logger.info(f"Failed: {total - successful}")
        
        if successful > 0:
            logger.info("\nGenerated files:")
            for angle, result in results.items():
                if result:
                    logger.info(f"  ✅ rotation_{angle}.jpg")
                else:
                    logger.info(f"  ❌ rotation_{angle}.jpg (failed)")
        
        if successful == total:
            logger.info("\n🎉 All rotations generated successfully!")
            return 0
        else:
            logger.warning(f"\n⚠️ {total - successful} rotations failed")
            return 1
            
    except Exception as e:
        logger.error(f"Error in example: {e}")
        return 1


if __name__ == "__main__":
    print("FLUX 1.1 [pro] Character Rotation Generator Example")
    print("=" * 50)
    print("This example demonstrates how to use the FluxProRotationGenerator class.")
    print("Make sure to:")
    print("1. Replace 'your_flux_api_key_here' with your actual FLUX API key")
    print("2. Ensure the input image exists at the specified path")
    print("3. Have sufficient API credits for generation")
    print()
    
    sys.exit(main()) 