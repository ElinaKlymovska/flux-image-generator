#!/usr/bin/env python3
"""
Character Rotation Generator Script.

This script generates character images from different rotation angles.
"""

import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from flux_generator.core.rotation import CharacterRotationGenerator, RotationAngle
from flux_generator.utils.logger import get_logger

logger = get_logger(__name__)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Generate character rotation images")
    
    parser.add_argument(
        "--angles",
        nargs="+",
        choices=[angle.value for angle in RotationAngle],
        default=["front", "left", "back", "right"],
        help="Rotation angles to generate"
    )
    
    parser.add_argument(
        "--style",
        default="ultra_realistic",
        help="Generation style"
    )
    
    parser.add_argument(
        "--steps",
        type=int,
        choices=[4, 5, 6, 7, 8, 9, 10, 11, 12],
        help="Number of steps for 360-degree sequence"
    )
    
    parser.add_argument(
        "--start-seed",
        type=int,
        default=1001,
        help="Starting seed for generation"
    )
    
    parser.add_argument(
        "--custom-prompt",
        help="Custom prompt to add to rotation"
    )
    
    parser.add_argument(
        "--output-dir",
        default="rotation",
        help="Output subdirectory"
    )
    
    parser.add_argument(
        "--api-key",
        help="FLUX API key"
    )
    
    parser.add_argument(
        "--test-connection",
        action="store_true",
        help="Test API connection before generation"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize generator
        generator = CharacterRotationGenerator(
            output_subdir=args.output_dir,
            api_key=args.api_key
        )
        
        # Test connection if requested
        if args.test_connection:
            logger.info("Testing API connection...")
            if not generator.test_connection():
                logger.error("API connection test failed")
                return 1
            logger.info("API connection test successful")
        
        # Get input image info
        image_info = generator.get_input_image_info()
        logger.info(f"Input image: {image_info}")
        
        if args.steps:
            # Generate 360-degree sequence
            logger.info(f"Generating 360-degree sequence with {args.steps} steps")
            results = generator.generate_360_degree_sequence(
                steps=args.steps,
                style=args.style,
                start_seed=args.start_seed,
                custom_prompt=args.custom_prompt
            )
            
            successful = sum(1 for r in results if r is not None)
            logger.info(f"Generated {successful}/{len(results)} images")
            
        else:
            # Generate specific angles
            logger.info(f"Generating rotation images for angles: {args.angles}")
            results = generator.generate_full_rotation(
                angles=args.angles,
                style=args.style,
                start_seed=args.start_seed,
                custom_prompt=args.custom_prompt
            )
            
            successful = sum(1 for r in results.values() if r is not None)
            logger.info(f"Generated {successful}/{len(results)} images")
        
        logger.info("Rotation generation completed successfully!")
        return 0
        
    except Exception as e:
        logger.error(f"Error in rotation generation: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 