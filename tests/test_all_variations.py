#!/usr/bin/env python3
"""
Test All Variations Functionality

This script tests the all variations generation functionality with a small subset.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from flux_generator.core.enhanced import EnhancedFluxGenerator
from flux_generator.utils.logger import get_logger

logger = get_logger(__name__)


def test_all_variations_functionality():
    """Test the all variations functionality with a small subset."""
    
    # Check for API key
    api_key = os.getenv("FLUX_API_KEY")
    if not api_key:
        logger.error("FLUX_API_KEY environment variable not set")
        logger.info("Please set your API key: export FLUX_API_KEY='your_api_key_here'")
        return False
    
    try:
        # Initialize generator
        logger.info("Initializing Enhanced FLUX Generator for testing...")
        generator = EnhancedFluxGenerator(output_subdir="test_all_variations")
        
        # Test connection
        logger.info("Testing API connection...")
        if not generator.test_connection():
            logger.error("Failed to connect to FLUX API")
            return False
        
        logger.info("Connection successful!")
        
        # Test with a small subset
        logger.info("Testing with a small subset of variations...")
        
        # Test: 2 styles × 2 aspects × 2 qualities = 8 variations
        summary = generator.generate_all_variations_summary(
            count_per_variation=1,
            start_seed=9999,
            include_styles=["ultra_realistic", "cinematic"],
            include_aspects=["portrait", "square"],
            include_qualities=["high", "standard"]
        )
        
        # Print results
        stats = summary["statistics"]
        print("\n" + "="*50)
        print("TEST RESULTS")
        print("="*50)
        print(f"Total variations attempted: {stats['total_variations']}")
        print(f"Successful variations: {stats['successful_variations']}")
        print(f"Total images attempted: {stats['total_images']}")
        print(f"Successful images: {stats['successful_images']}")
        print(f"Success rate (variations): {stats['success_rate_variations']}")
        print(f"Success rate (images): {stats['success_rate_images']}")
        print("="*50)
        
        # Print detailed results
        print("\nDETAILED RESULTS:")
        print("-" * 30)
        
        results = summary["results"]
        for style in results:
            print(f"\nStyle: {style}")
            for aspect in results[style]:
                print(f"  Aspect: {aspect}")
                for quality in results[style][aspect]:
                    images = results[style][aspect][quality]
                    status = "✓" if images else "✗"
                    print(f"    {quality}: {status} ({len(images)} images)")
                    if images:
                        for img_path in images:
                            print(f"      - {img_path.name}")
        
        # Test successful
        if stats['successful_variations'] > 0:
            logger.info("Test completed successfully!")
            return True
        else:
            logger.warning("Test completed but no images were generated")
            return False
        
    except Exception as e:
        logger.error(f"Error during test: {e}")
        return False


def test_custom_prompt():
    """Test all variations with custom prompt."""
    
    api_key = os.getenv("FLUX_API_KEY")
    if not api_key:
        logger.error("FLUX_API_KEY environment variable not set")
        return False
    
    try:
        generator = EnhancedFluxGenerator(output_subdir="test_custom_prompt")
        
        if not generator.test_connection():
            logger.error("Failed to connect to FLUX API")
            return False
        
        logger.info("Testing with custom prompt...")
        
        custom_prompt = "Beautiful portrait of a woman with blue eyes"
        summary = generator.generate_all_variations_summary(
            count_per_variation=1,
            start_seed=8888,
            include_styles=["ultra_realistic"],
            include_aspects=["portrait"],
            include_qualities=["high"],
            custom_prompt=custom_prompt
        )
        
        stats = summary["statistics"]
        print(f"\nCustom prompt test: {stats['successful_images']}/{stats['total_images']} images generated")
        
        return stats['successful_images'] > 0
        
    except Exception as e:
        logger.error(f"Error in custom prompt test: {e}")
        return False


if __name__ == "__main__":
    print("Testing All Variations Functionality")
    print("=" * 40)
    
    # Run tests
    test1_success = test_all_variations_functionality()
    test2_success = test_custom_prompt()
    
    print("\n" + "="*40)
    print("TEST SUMMARY")
    print("="*40)
    print(f"Basic functionality test: {'✓ PASS' if test1_success else '✗ FAIL'}")
    print(f"Custom prompt test: {'✓ PASS' if test2_success else '✗ FAIL'}")
    
    if test1_success and test2_success:
        print("\n🎉 All tests passed! The all variations functionality is working correctly.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the logs for details.")
        sys.exit(1) 