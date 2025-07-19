#!/usr/bin/env python3
"""
Test Portrait Setup Script

This script tests the setup for portrait generation without requiring API key.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from flux_generator.config.prompts import PromptConfig
from flux_generator.utils.logger import get_logger

logger = get_logger(__name__)


def main():
    """Test portrait generation setup."""
    
    print("="*60)
    print("PORTRAIT GENERATION SETUP TEST")
    print("="*60)
    
    # Test 1: Check available styles
    print("\n1. Available Styles:")
    styles = PromptConfig.list_available_styles()
    print(f"   Total styles: {len(styles)}")
    for style in styles:
        print(f"   - {style['name']} ({style['key']})")
    
    # Test 2: Check aspect ratios
    print("\n2. Aspect Ratios:")
    aspects = PromptConfig.list_available_aspects()
    print(f"   Portrait aspect: {aspects.get('portrait', 'Not found')}")
    
    # Test 3: Check qualities
    print("\n3. Available Qualities:")
    qualities = PromptConfig.list_available_qualities()
    print(f"   Total qualities: {len(qualities)}")
    for quality in qualities:
        print(f"   - {quality['key']}: {quality['description']}")
    
    # Test 4: Calculate total variations
    total_variations = len(styles) * len(qualities)
    print(f"\n4. Total Portrait Variations:")
    print(f"   {len(styles)} styles × {len(qualities)} qualities = {total_variations} variations")
    
    # Test 5: Check input image
    print("\n5. Input Image Check:")
    input_path = Path("data/input/character.jpg")
    if input_path.exists():
        print(f"   ✓ Input image found: {input_path}")
        print(f"   Size: {input_path.stat().st_size / 1024:.1f} KB")
    else:
        print(f"   ✗ Input image not found: {input_path}")
    
    # Test 6: Check API key
    print("\n6. API Key Check:")
    api_key = os.getenv("FLUX_API_KEY") or os.getenv("BFL_API_KEY")
    if api_key:
        print(f"   ✓ API key found: {api_key[:8]}...")
    else:
        print("   ✗ API key not found")
        print("   Please set one of:")
        print("   - export FLUX_API_KEY='your_api_key_here'")
        print("   - export BFL_API_KEY='your_api_key_here'")
    
    # Test 7: Check output directory
    print("\n7. Output Directory Check:")
    output_dir = Path("data/output/portrait_variations")
    if output_dir.exists():
        print(f"   ✓ Output directory exists: {output_dir}")
    else:
        print(f"   ⚠ Output directory will be created: {output_dir}")
    
    print("\n" + "="*60)
    print("SETUP TEST COMPLETED")
    print("="*60)
    
    if api_key and input_path.exists():
        print("\n✅ Ready to generate portrait variations!")
        print("Run: python generate_portrait_variations.py")
    else:
        print("\n❌ Setup incomplete. Please fix the issues above.")
    
    return True


if __name__ == "__main__":
    main() 