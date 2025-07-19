#!/usr/bin/env python3
"""
Enhanced Character Rotation Generator Example.

This example demonstrates the new rotation capabilities with Black Forest Labs best practices.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from flux_generator.core.rotation import CharacterRotationGenerator
from flux_generator.utils.logger import get_logger

logger = get_logger(__name__)


def main():
    """Main function demonstrating enhanced rotation capabilities."""
    
    print("🎭 Enhanced Character Rotation Generator Example")
    print("=" * 50)
    
    try:
        # Initialize generator
        generator = CharacterRotationGenerator(output_subdir="enhanced_rotation")
        
        # Test connection
        print("\n🔍 Testing API connection...")
        if not generator.test_connection():
            print("❌ API connection failed")
            return 1
        print("✅ API connection successful")
        
        # Show available presets
        print("\n📋 Available rotation presets:")
        presets = generator.get_available_presets()
        for preset in presets:
            print(f"  • {preset['key']}: {preset['name']}")
        
        # Show preset details
        print("\n📖 Preset details (rotation_front):")
        preset_info = generator.get_preset_info("rotation_front")
        print(f"  Name: {preset_info['preset_name']}")
        print(f"  Description: {preset_info['description']}")
        print(f"  Use case: {preset_info['use_case']}")
        print(f"  Technical specs: {preset_info['technical_specs']}")
        
        # Generate character-consistent rotation
        print("\n🎯 Generating character-consistent rotation sequence...")
        angles = ["front", "left", "back", "right"]
        
        results = generator.generate_character_consistent_rotation(
            angles=angles,
            base_prompt="portrait of a woman with long brown hair and green eyes",
            seed=1001,
            use_presets=True
        )
        
        successful = sum(1 for r in results.values() if r is not None)
        print(f"✅ Generated {successful}/{len(results)} character-consistent images")
        
        # Generate with custom preset
        print("\n🎨 Generating with custom preset...")
        custom_result = generator.generate_rotation_with_custom_preset(
            angle="front",
            preset="rotation_front",
            custom_prompt="portrait of a woman wearing a red dress",
            seed=2001
        )
        
        if custom_result:
            print(f"✅ Custom preset generation successful: {custom_result}")
        else:
            print("❌ Custom preset generation failed")
        
        # Generate full rotation with presets
        print("\n🔄 Generating full rotation with presets...")
        full_results = generator.generate_full_rotation(
            angles=["front", "left", "back", "right"],
            custom_prompt="portrait of a woman in professional attire",
            use_presets=True
        )
        
        successful_full = sum(1 for r in full_results.values() if r is not None)
        print(f"✅ Full rotation with presets: {successful_full}/{len(full_results)} images")
        
        print("\n🎉 Enhanced rotation example completed successfully!")
        return 0
        
    except Exception as e:
        logger.error(f"Error in enhanced rotation example: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
