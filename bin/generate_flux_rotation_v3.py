#!/usr/bin/env python3
"""
FLUX 1.1 [pro] Character Rotation Generator Script (Version 3).

This script generates character images from different rotation angles using the FLUX API
with ultra and raw mode enabled, by extending the existing API client.
"""

import sys
import argparse
import time
import requests
from pathlib import Path
from typing import List, Optional

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from flux_generator.api.client import FluxAPIClient
from flux_generator.api.models import GenerationRequest, GenerationResponse
from flux_generator.config.settings import settings
from flux_generator.utils.logger import get_logger

logger = get_logger(__name__)


class FluxProAPIClient(FluxAPIClient):
    """Extended FLUX API client with ultra and raw mode support."""
    
    def generate_image_with_ultra_raw(self, request: GenerationRequest) -> GenerationResponse:
        """Generate image using FLUX API with ultra and raw mode enabled."""
        for attempt in range(self.max_retries):
            try:
                # Use session for better connection handling
                session = requests.Session()
                session.headers.update(self.headers)
                
                # Get the base request data
                request_data = request.to_dict()
                
                # Add ultra and raw parameters
                request_data["ultra"] = True
                request_data["raw"] = True
                
                # Submit generation request
                logger.info(f"🚀 Submitting generation request with ultra and raw mode (attempt {attempt + 1}/{self.max_retries})...")
                response = session.post(
                    f"{self.base_url}/flux-kontext-pro",
                    headers=self.headers,
                    json=request_data,
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    # Parse response to get polling URL
                    try:
                        result = response.json()
                        polling_url = result.get('polling_url')
                        
                        if not polling_url:
                            return GenerationResponse.error_response("No polling URL in response")
                        
                        # Poll for completion
                        logger.info("🔄 Waiting for generation to complete...")
                        final_result = self.poll_generation_status(polling_url)
                        
                        # Extract image URL from result
                        result_data = final_result.get('result', {})
                        image_url = result_data.get('sample')
                        
                        if not image_url:
                            return GenerationResponse.error_response("No image URL in result")
                        
                        # Download image
                        logger.info("📥 Downloading generated image...")
                        image_data = self.download_image(image_url)
                        
                        if image_data:
                            logger.info("✅ Image generated successfully!")
                            return GenerationResponse.success_response(
                                image_data=image_data,
                                request_id=final_result.get('id')
                            )
                        else:
                            return GenerationResponse.error_response("Failed to download image")
                            
                    except Exception as e:
                        return GenerationResponse.error_response(f"Invalid response: {e}")
                        
                else:
                    error_msg = f"API returned status {response.status_code}"
                    try:
                        error_data = response.json()
                        error_msg = error_data.get("error", error_msg)
                    except:
                        pass
                    
                    if response.status_code == 403:
                        raise Exception("Access denied. Check API key.")
                    elif response.status_code >= 500:
                        # Server error, retry
                        if attempt < self.max_retries - 1:
                            logger.warning(f"⚠️ Server error, retrying in {self.retry_delay} seconds...")
                            time.sleep(self.retry_delay)
                            continue
                    
                    return GenerationResponse.error_response(error_msg)
                    
            except requests.exceptions.Timeout:
                if attempt < self.max_retries - 1:
                    logger.warning(f"⚠️ Request timeout, retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                    continue
                return GenerationResponse.error_response("Request timeout")
                
            except requests.exceptions.ConnectionError as e:
                if attempt < self.max_retries - 1:
                    logger.warning(f"⚠️ Connection error: {e}, retrying in {self.retry_delay * 2} seconds...")
                    time.sleep(self.retry_delay * 2)  # Longer delay for connection issues
                    continue
                return GenerationResponse.error_response(f"Connection failed: {e}")
                
            except requests.exceptions.RequestException as e:
                if attempt < self.max_retries - 1:
                    logger.warning(f"⚠️ Request failed: {e}, retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                    continue
                return GenerationResponse.error_response(f"Request failed: {e}")
        
        return GenerationResponse.error_response("Max retries exceeded")


class FluxProRotationGeneratorV3:
    """Generator for character rotation using FLUX API with ultra and raw mode."""
    
    def __init__(self, api_key: str, output_dir: str = "rotation_output"):
        """Initialize the generator."""
        self.api_key = api_key.strip('"\'')
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize the extended API client
        self.client = FluxProAPIClient(api_key=self.api_key)
    
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
            # Create prompt
            prompt = self.create_rotation_prompt(angle)
            
            logger.info(f"Generating rotation for {angle} degrees...")
            logger.info(f"Prompt: {prompt}")
            
            # Create generation request
            request = GenerationRequest.from_image_file(
                prompt=prompt,
                image_path=input_image_path,
                seed=seed,
                aspect_ratio="2:3",
                output_format="jpeg"
            )
            
            # Generate image using the extended client with ultra and raw mode
            response = self.client.generate_image_with_ultra_raw(request)
            
            if response.success and response.image_data:
                logger.info(f"✅ Successfully generated image for {angle} degrees")
                return response.image_data
            else:
                logger.error(f"❌ Failed to generate image for {angle} degrees: {response.error_message}")
                return None
            
        except Exception as e:
            logger.error(f"Error generating rotation for {angle} degrees: {e}")
            return None
    
    def test_connection(self) -> bool:
        """Test API connection."""
        return self.client.test_connection()
    
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
    parser = argparse.ArgumentParser(description="Generate character rotation images using FLUX API with ultra and raw mode")
    
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
        help="FLUX API key (will use environment variable if not provided)"
    )
    
    parser.add_argument(
        "--test-connection",
        action="store_true",
        help="Test API connection before generation"
    )
    
    args = parser.parse_args()
    
    try:
        # Get API key from argument or environment
        api_key = args.api_key
        if not api_key:
            import os
            api_key = os.getenv("BFL_API_KEY") or os.getenv("FLUX_API_KEY")
            if not api_key:
                logger.error("API key is required. Provide --api-key or set BFL_API_KEY/FLUX_API_KEY environment variable.")
                return 1
        
        # Initialize generator
        generator = FluxProRotationGeneratorV3(
            api_key=api_key,
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