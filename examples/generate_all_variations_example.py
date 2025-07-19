#!/usr/bin/env python3
"""
Example: Generate All Variations

This example demonstrates how to generate images for all possible combinations
of styles, aspects, and qualities.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from flux_generator.core.enhanced import EnhancedFluxGenerator
from flux_generator.utils.logger import get_logger

logger = get_logger(__name__)


def example_generate_all_variations():
    """Example of generating all variations."""
    
    # Check for API key
    api_key = os.getenv("FLUX_API_KEY")
    if not api_key:
        logger.error("FLUX_API_KEY environment variable not set")
        return
    
    try:
        # Initialize generator
        generator = EnhancedFluxGenerator(output_subdir="example_all_variations")
        
        # Test connection
        if not generator.test_connection():
            logger.error("Failed to connect to FLUX API")
            return
        
        logger.info("Connection successful!")
        
        # Example 1: Generate all variations (this will be a lot!)
        logger.info("Example 1: Generating ALL variations...")
        
        # This will generate: 12 styles × 5 aspects × 2 qualities = 120 images
        summary = generator.generate_all_variations_summary(
            count_per_variation=1,
            start_seed=1000,
            include_qualities=["standard", "creative"]  # Only working qualities
        )
        
        print(f"Generated {summary['statistics']['successful_images']} images")
        
        # Example 2: Generate only specific styles
        logger.info("Example 2: Generating only specific styles...")
        
        specific_styles = ["ultra_realistic", "cinematic", "artistic"]
        summary2 = generator.generate_all_variations_summary(
            count_per_variation=1,
            start_seed=2000,
            include_styles=specific_styles
        )
        
        print(f"Generated {summary2['statistics']['successful_images']} images for specific styles")
        
        # Example 3: Generate only specific aspects
        logger.info("Example 3: Generating only specific aspects...")
        
        specific_aspects = ["portrait", "square"]
        summary3 = generator.generate_all_variations_summary(
            count_per_variation=1,
            start_seed=3000,
            include_aspects=specific_aspects
        )
        
        print(f"Generated {summary3['statistics']['successful_images']} images for specific aspects")
        
        # Example 4: Generate with custom prompt
        logger.info("Example 4: Generating with custom prompt...")
        
        custom_prompt = "Beautiful portrait of a woman with blue eyes and golden hair"
        summary4 = generator.generate_all_variations_summary(
            count_per_variation=1,
            start_seed=4000,
            include_styles=["ultra_realistic", "cinematic"],
            include_aspects=["portrait"],
            include_qualities=["high"],
            custom_prompt=custom_prompt
        )
        
        print(f"Generated {summary4['statistics']['successful_images']} images with custom prompt")
        
        # Example 5: Generate multiple images per variation
        logger.info("Example 5: Generating multiple images per variation...")
        
        summary5 = generator.generate_all_variations_summary(
            count_per_variation=3,  # 3 images per variation
            start_seed=5000,
            include_styles=["ultra_realistic"],
            include_aspects=["portrait"],
            include_qualities=["standard", "creative"]
        )
        
        print(f"Generated {summary5['statistics']['successful_images']} images (3 per variation)")
        
    except Exception as e:
        logger.error(f"Error in example: {e}")


def example_analyze_results():
    """Example of analyzing generation results."""
    
    api_key = os.getenv("FLUX_API_KEY")
    if not api_key:
        logger.error("FLUX_API_KEY environment variable not set")
        return
    
    try:
        generator = EnhancedFluxGenerator(output_subdir="analysis_example")
        
        # Generate a small set for analysis
        summary = generator.generate_all_variations_summary(
            count_per_variation=1,
            start_seed=6000,
            include_styles=["ultra_realistic", "cinematic"],
            include_aspects=["portrait", "square"],
            include_qualities=["high"]
        )
        
        # Analyze results
        results = summary["results"]
        stats = summary["statistics"]
        
        print("\n=== ANALYSIS RESULTS ===")
        print(f"Total variations: {stats['total_variations']}")
        print(f"Successful variations: {stats['successful_variations']}")
        print(f"Success rate: {stats['success_rate_variations']}")
        
        # Analyze by style
        print("\n=== BY STYLE ===")
        for style in results:
            style_success = 0
            style_total = 0
            for aspect in results[style]:
                for quality in results[style][aspect]:
                    style_total += 1
                    if results[style][aspect][quality]:
                        style_success += 1
            print(f"{style}: {style_success}/{style_total} ({style_success/style_total*100:.1f}%)")
        
        # Analyze by aspect
        print("\n=== BY ASPECT ===")
        aspects = {}
        for style in results:
            for aspect in results[style]:
                if aspect not in aspects:
                    aspects[aspect] = {"success": 0, "total": 0}
                for quality in results[style][aspect]:
                    aspects[aspect]["total"] += 1
                    if results[style][aspect][quality]:
                        aspects[aspect]["success"] += 1
        
        for aspect, data in aspects.items():
            success_rate = data["success"] / data["total"] * 100
            print(f"{aspect}: {data['success']}/{data['total']} ({success_rate:.1f}%)")
        
    except Exception as e:
        logger.error(f"Error in analysis example: {e}")


if __name__ == "__main__":
    print("FLUX Image Generator - All Variations Examples")
    print("=" * 50)
    
    # Run examples
    example_generate_all_variations()
    example_analyze_results()
    
    print("\nExamples completed!") 