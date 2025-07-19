#!/usr/bin/env python3
"""
FLUX 1.1 [pro] Character Rotation Generator Script.

This script generates character images from different rotation angles using the FLUX 1.1 [pro] API
with ultra and raw mode enabled.
"""

import sys
import argparse
import requests
import base64
import time
import json
from pathlib import Path
from typing import List, Optional

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from flux_generator.utils.logger import get_logger

logger = get_logger(__name__)


class FluxProRotationGenerator:
    """Generator for character rotation using FLUX 1.1 [pro] API."""
    
    def __init__(self, api_key: str, output_dir: str = "rotation_output"):
        """Initialize the generator."""
        self.api_key = api_key.strip('"\'')
        self.api_endpoint = "https://api.bfl.ai/v1/flux-1.1-pro-ultra"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.headers = {
            "x-key": self.api_key,
            "Content-Type": "application/json"
        }
    
    def encode_image(self, image_path: Path) -> str:
        """Encode image to base64."""
        if not image_path.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        with open(image_path, "rb") as f:
            image_data = f.read()
        
        # Determine MIME type
        mime_type = "image/jpeg"  # Default
        if image_path.suffix.lower() in [".png"]:
            mime_type = "image/png"
        
        # Encode to base64
        encoded_image = base64.b64encode(image_data).decode("utf-8")
        return f"data:{mime_type};base64,{encoded_image}"
    
    def create_rotation_prompt(self, angle: int) -> str:
        """Create prompt for specific rotation angle."""
        if angle == 0:
            direction = "facing forward"
        elif angle == 180:
            direction = "facing away, back turned"
        elif angle < 90:
            direction = f"rotated {angle} degrees to the right"
        elif angle == 90:
            direction = "facing 90 degrees to the right"
        elif angle < 180:
            direction = f"rotated {angle} degrees to the right"
        else:
            direction = f"rotated {angle} degrees to the right"
        
        return (
            f"A realistic portrait of the same woman as in the input image, {direction}, "
            f"keeping her facial features and body unchanged, consistent lighting and style, "
            f"ultra realistic, high detail, studio lighting"
        )
    
    def generate_rotation_image(self, angle: int, input_image_path: Path, seed: int = 123456) -> Optional[bytes]:
        """Generate a single rotation image."""
        try:
            # Encode input image
            encoded_image = self.encode_image(input_image_path)
            
            # Create prompt
            prompt = self.create_rotation_prompt(angle)
            
            # Prepare request data
            request_data = {
                "prompt": prompt,
                "input_image": encoded_image,
                "seed": seed,
                "ultra": True,
                "raw": True,
                "aspect_ratio": "2:3",
                "output_format": "jpeg"
            }
            
            logger.info(f"Generating rotation for {angle} degrees...")
            logger.info(f"Prompt: {prompt}")
            
            # Make API request
            response = requests.post(
                self.api_endpoint,
                headers=self.headers,
                json=request_data,
                timeout=600  # 10 minutes timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Check if we need to poll for completion
                if "polling_url" in result:
                    logger.info("Generation in progress, polling for completion...")
                    final_result = self.poll_generation_status(result["polling_url"])
                    
                    if final_result and "result" in final_result:
                        image_url = final_result["result"].get("image_url")
                        if image_url:
                            return self.download_image(image_url)
                else:
                    # Direct response with image data
                    if "image_url" in result:
                        return self.download_image(result["image_url"])
                    elif "image_data" in result:
                        return base64.b64decode(result["image_data"])
            
            logger.error(f"API request failed with status {response.status_code}: {response.text}")
            return None
            
        except Exception as e:
            logger.error(f"Error generating rotation for {angle} degrees: {e}")
            return None
    
    def poll_generation_status(self, polling_url: str) -> Optional[dict]:
        """Poll generation status until completion."""
        max_attempts = 180  # Maximum 15 minutes (180 * 5 seconds)
        attempt = 0
        
        while attempt < max_attempts:
            try:
                response = requests.get(polling_url, headers=self.headers, timeout=60)
                
                if response.status_code == 200:
                    result = response.json()
                    status = result.get('status')
                    
                    if status == 'completed' or status == 'Ready':
                        logger.info("Generation completed!")
                        return result
                    elif status == 'failed':
                        logger.error(f"Generation failed: {result.get('error', 'Unknown error')}")
                        return None
                    elif status == 'processing' or status == 'Pending':
                        logger.info(f"🔄 Processing... (attempt {attempt + 1}/{max_attempts})")
                        time.sleep(5)
                    else:
                        logger.info(f"ℹ️ Status: {status}")
                        time.sleep(5)
                else:
                    logger.error(f"❌ HTTP {response.status_code} error while polling status")
                    time.sleep(5)
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"❌ Network error while polling: {e}")
                time.sleep(10)
            
            attempt += 1
        
        logger.error(f"❌ Generation timeout exceeded after {attempt} attempts")
        return None
    
    def download_image(self, image_url: str) -> Optional[bytes]:
        """Download image from URL."""
        try:
            response = requests.get(image_url, timeout=30)
            
            if response.status_code == 200:
                return response.content
            else:
                logger.error(f"❌ Failed to download image: HTTP {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Download error: {e}")
            return None
    
    def test_connection(self) -> bool:
        """Test API connection."""
        try:
            # Simple test request
            test_data = {
                "prompt": "test",
                "input_image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k=",
                "seed": 1000,
                "ultra": True,
                "raw": True
            }
            
            response = requests.post(
                self.api_endpoint,
                headers=self.headers,
                json=test_data,
                timeout=10
            )
            
            # If we get any response (even error), the API key is working
            if response.status_code in [200, 400, 422]:  # Success or validation errors
                return True
            elif response.status_code == 403:
                logger.error("Access denied. Check API key.")
                return False
            else:
                return True
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    def generate_all_rotations(self, angles: List[int], input_image_path: Path, seed: int = 123456) -> dict:
        """Generate images for all specified angles."""
        results = {}
        
        logger.info(f"Starting rotation generation for angles: {angles}")
        logger.info(f"Input image: {input_image_path}")
        logger.info(f"Seed: {seed}")
        logger.info(f"Output directory: {self.output_dir}")
        
        for angle in angles:
            logger.info(f"\n{'='*50}")
            logger.info(f"Processing angle: {angle} degrees")
            logger.info(f"{'='*50}")
            
            # Generate image
            image_data = self.generate_rotation_image(angle, input_image_path, seed)
            
            if image_data:
                # Save image
                output_filename = f"rotation_{angle}.jpg"
                output_path = self.output_dir / output_filename
                
                with open(output_path, "wb") as f:
                    f.write(image_data)
                
                logger.info(f"✅ Successfully generated: {output_filename}")
                results[angle] = output_path
            else:
                logger.error(f"❌ Failed to generate image for {angle} degrees")
                results[angle] = None
        
        return results


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Generate character rotation images using FLUX 1.1 [pro] API")
    
    parser.add_argument(
        "--angles",
        nargs="+",
        type=int,
        default=[10, 20, 30, 45, 60, 90, 135, 180],
        help="Rotation angles to generate (default: 10 20 30 45 60 90 135 180)"
    )
    
    parser.add_argument(
        "--input-image",
        default="/Users/ElinaKlymovska/CursorIA/Art/SenteticData/data/input/character.jpg",
        help="Path to input character image"
    )
    
    parser.add_argument(
        "--seed",
        type=int,
        default=123456,
        help="Seed for generation (default: 123456)"
    )
    
    parser.add_argument(
        "--output-dir",
        default="rotation_output",
        help="Output directory for generated images"
    )
    
    parser.add_argument(
        "--api-key",
        required=True,
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
        generator = FluxProRotationGenerator(
            api_key=args.api_key,
            output_dir=args.output_dir
        )
        
        # Test connection if requested
        if args.test_connection:
            logger.info("Testing API connection...")
            if not generator.test_connection():
                logger.error("API connection test failed")
                return 1
            logger.info("API connection test successful")
        
        # Check input image
        input_image_path = Path(args.input_image)
        if not input_image_path.exists():
            logger.error(f"Input image not found: {input_image_path}")
            return 1
        
        # Generate all rotations
        results = generator.generate_all_rotations(
            angles=args.angles,
            input_image_path=input_image_path,
            seed=args.seed
        )
        
        # Summary
        successful = sum(1 for r in results.values() if r is not None)
        total = len(results)
        
        logger.info(f"\n{'='*50}")
        logger.info("GENERATION SUMMARY")
        logger.info(f"{'='*50}")
        logger.info(f"Total angles: {total}")
        logger.info(f"Successful: {successful}")
        logger.info(f"Failed: {total - successful}")
        logger.info(f"Output directory: {generator.output_dir}")
        
        if successful > 0:
            logger.info("\nGenerated files:")
            for angle, result in results.items():
                if result:
                    logger.info(f"  rotation_{angle}.jpg")
        
        if successful == total:
            logger.info("\n🎉 All rotations generated successfully!")
            return 0
        else:
            logger.warning(f"\n⚠️ {total - successful} rotations failed")
            return 1
        
    except Exception as e:
        logger.error(f"Error in rotation generation: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 