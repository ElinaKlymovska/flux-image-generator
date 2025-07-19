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
        "--use-presets",
        action="store_true",
        default=True,
        help="Use rotation presets for better character consistency (default: True)"
    )
    
    parser.add_argument(
        "--no-presets",
        action="store_true",
        help="Disable presets and use original method"
    )
    
    parser.add_argument(
        "--list-presets",
        action="store_true",
        help="List available rotation presets"
    )
    
    parser.add_argument(
        "--preset-info",
        help="Show detailed information about a specific preset"
    )
    
    parser.add_argument(
        "--character-consistent",
        action="store_true",
        default=True,
        help="Use character-consistent rotation (default: True)"
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
        
        # Handle special commands
        if args.list_presets:
            logger.info("Available rotation presets:")
            presets = generator.get_available_presets()
            for preset in presets:
                logger.info(f"  {preset['key']}: {preset['name']}")
            return 0
        
        if args.preset_info:
            try:
                preset_info = generator.get_preset_info(args.preset_info)
                logger.info(f"Preset: {args.preset_info}")
                logger.info(f"Name: {preset_info['preset_name']}")
                logger.info(f"Description: {preset_info['description']}")
                logger.info(f"Use case: {preset_info['use_case']}")
                logger.info(f"Technical specs: {preset_info['technical_specs']}")
                logger.info(f"Prompt: {preset_info['prompt']}")
                return 0
            except ValueError as e:
                logger.error(f"Error getting preset info: {e}")
                return 1
        
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
        
        # Determine if presets should be used
        use_presets = args.use_presets and not args.no_presets
        
        if args.steps:
            # Generate 360-degree sequence
            logger.info(f"Generating 360-degree sequence with {args.steps} steps")
            logger.info(f"Using presets: {use_presets}")
            
            if use_presets:
                # Use character-consistent rotation
                angles = generator._create_custom_sequence(args.steps)
                results = generator.generate_character_consistent_rotation(
                    angles=angles,
                    base_prompt=args.custom_prompt or "portrait of a woman",
                    start_seed=args.start_seed,
                    use_presets=True
                )
                successful = sum(1 for r in results.values() if r is not None)
            else:
                # Use original method
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
            logger.info(f"Using presets: {use_presets}")
            
            results = generator.generate_full_rotation(
                angles=args.angles,
                style=args.style,
                start_seed=args.start_seed,
                custom_prompt=args.custom_prompt,
                use_presets=use_presets
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