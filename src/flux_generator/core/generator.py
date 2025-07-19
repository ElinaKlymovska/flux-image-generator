"""
Basic FLUX Image Generator.

This module provides the core image generation functionality.
"""

import time
from pathlib import Path
from typing import Optional, List

from ..config.settings import settings
from ..config.prompts import PromptConfig
from ..api.client import FluxAPIClient
from ..api.models import GenerationRequest, GenerationResponse
from ..utils.logger import get_logger
from ..utils.image import ImageUtils

logger = get_logger(__name__)


class FluxImageGenerator:
    """Basic FLUX Image Generator."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize generator."""
        self.api_client = FluxAPIClient(api_key)
        self.settings = settings
        self.prompt_config = PromptConfig()
        
        # Validate settings
        self.settings.validate()
        
        # Find input image
        self.input_image = ImageUtils.find_input_image(self.settings.paths.input_dir)
        if not self.input_image:
            raise FileNotFoundError(
                f"Input image not found in {self.settings.paths.input_dir}. "
                "Please place character.jpg in the input directory."
            )
        
        logger.info(f"Initialized generator with input image: {self.input_image}")
    
    def generate_single_image(
        self, 
        prompt: Optional[str] = None,
        seed: Optional[int] = None,
        aspect_ratio: Optional[str] = None,
        output_format: Optional[str] = None
    ) -> Optional[Path]:
        """Generate a single image."""
        # Use defaults if not provided
        prompt = prompt or self.prompt_config.PROMPTS["ultra_realistic"]["prompt"]
        seed = seed or self.settings.generation.default_seed
        aspect_ratio = aspect_ratio or self.settings.generation.default_aspect_ratio
        output_format = output_format or self.settings.generation.default_output_format
        
        logger.info(f"Generating image with seed {seed}")
        
        try:
            # Create generation request
            request = GenerationRequest.from_image_file(
                prompt=prompt,
                image_path=self.input_image,
                seed=seed,
                aspect_ratio=aspect_ratio,
                output_format=output_format
            )
            
            # Generate image
            response = self.api_client.generate_image(request)
            
            if response.success and response.image_data:
                # Generate filename
                filename = ImageUtils.generate_filename(
                    base_name="woman",
                    index=0,
                    seed=seed,
                    extension=output_format
                )
                
                # Save image
                output_path = self.settings.paths.output_dir / filename
                ImageUtils.save_image_data(response.image_data, output_path)
                
                logger.info(f"Generated image saved: {output_path}")
                return output_path
            else:
                logger.error(f"Generation failed: {response.error_message}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return None
    
    def generate_images(
        self, 
        count: Optional[int] = None,
        start_seed: Optional[int] = None,
        prompt: Optional[str] = None,
        aspect_ratio: Optional[str] = None,
        output_format: Optional[str] = None
    ) -> List[Path]:
        """Generate multiple images."""
        count = count or self.settings.generation.default_count
        start_seed = start_seed or self.settings.generation.default_seed
        
        logger.info(f"Starting generation of {count} images")
        
        generated_images = []
        successful_count = 0
        
        for i in range(count):
            seed = start_seed + i
            logger.info(f"Generating image {i + 1}/{count} with seed {seed}")
            
            try:
                output_path = self.generate_single_image(
                    prompt=prompt,
                    seed=seed,
                    aspect_ratio=aspect_ratio,
                    output_format=output_format
                )
                
                if output_path:
                    generated_images.append(output_path)
                    successful_count += 1
                    logger.info(f"Successfully generated image {i + 1}/{count}")
                else:
                    logger.warning(f"Failed to generate image {i + 1}/{count}")
                
                # Small delay between requests
                if i < count - 1:
                    time.sleep(2)
                    
            except Exception as e:
                logger.error(f"Error in generation {i + 1}/{count}: {e}")
        
        logger.info(f"Generation completed: {successful_count}/{count} images generated")
        return generated_images
    
    def test_connection(self) -> bool:
        """Test API connection."""
        try:
            return self.api_client.test_connection()
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    def get_input_image_info(self) -> dict:
        """Get information about input image."""
        return ImageUtils.get_image_info(self.input_image) 