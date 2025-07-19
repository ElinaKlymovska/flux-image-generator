#!/usr/bin/env python3
"""
Generate All Variations Script

This script generates images for all possible combinations of styles, aspects, and qualities.
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from flux_generator.core.enhanced import EnhancedFluxGenerator
from flux_generator.utils.logger import get_logger

logger = get_logger(__name__)


def main():
    """Main function to generate all variations."""
    
    # Check for API key
    api_key = os.getenv("FLUX_API_KEY")
    if not api_key:
        logger.error("FLUX_API_KEY environment variable not set")
        logger.info("Please set your API key: export FLUX_API_KEY='your_api_key_here'")
        return False
    
    try:
        # Initialize generator
        logger.info("Initializing Enhanced FLUX Generator...")
        generator = EnhancedFluxGenerator(output_subdir="all_variations")
        
        # Test connection
        logger.info("Testing API connection...")
        if not generator.test_connection():
            logger.error("Failed to connect to FLUX API")
            return False
        
        logger.info("Connection successful!")
        
        # Get available options
        styles = generator.list_available_styles()
        aspects = generator.list_available_aspects()
        qualities = generator.list_available_qualities()
        
        logger.info(f"Available styles: {len(styles)}")
        logger.info(f"Available aspects: {len(aspects)}")
        logger.info(f"Available qualities: {len(qualities)}")
        
        # Calculate total variations (only working qualities)
        working_qualities = ["standard", "creative"]
        total_variations = len(styles) * len(aspects) * len(working_qualities)
        logger.info(f"Total possible variations (working qualities): {total_variations}")
        
        # Ask user for confirmation
        print("\n" + "="*60)
        print("GENERATE ALL VARIATIONS")
        print("="*60)
        print(f"Styles: {len(styles)}")
        print(f"Aspects: {len(aspects)}")
        print(f"Working qualities: {len(working_qualities)} (standard, creative)")
        print(f"Total variations: {total_variations}")
        print(f"Images per variation: 1")
        print(f"Total images to generate: {total_variations}")
        print("="*60)
        
        response = input("\nDo you want to proceed? (y/N): ").strip().lower()
        if response not in ['y', 'yes']:
            logger.info("Generation cancelled by user")
            return False
        
        # Generate all variations
        logger.info("Starting generation of ALL variations...")
        
        summary = generator.generate_all_variations_summary(
            count_per_variation=1,
            start_seed=1000,
            custom_prompt=None,  # Use default prompts for each style
            include_qualities=["standard", "creative"]  # Only working qualities
        )
        
        # Print results
        print("\n" + "="*60)
        print("GENERATION COMPLETED")
        print("="*60)
        
        stats = summary["statistics"]
        print(f"Total variations attempted: {stats['total_variations']}")
        print(f"Successful variations: {stats['successful_variations']}")
        print(f"Total images attempted: {stats['total_images']}")
        print(f"Successful images: {stats['successful_images']}")
        print(f"Success rate (variations): {stats['success_rate_variations']}")
        print(f"Success rate (images): {stats['success_rate_images']}")
        print("="*60)
        
        # Save results to file
        results_file = Path(__file__).parent.parent / "all_variations_results.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, default=str)
        
        logger.info(f"Results saved to: {results_file}")
        
        # Print detailed results
        print("\nDETAILED RESULTS:")
        print("-" * 40)
        
        results = summary["results"]
        for style in results:
            print(f"\nStyle: {style}")
            for aspect in results[style]:
                print(f"  Aspect: {aspect}")
                for quality in results[style][aspect]:
                    images = results[style][aspect][quality]
                    status = "✓" if images else "✗"
                    print(f"    {quality}: {status} ({len(images)} images)")
        
        return True
        
    except Exception as e:
        logger.error(f"Error during generation: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 