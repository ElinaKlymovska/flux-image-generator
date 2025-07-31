"""
Base Generator Class for FLUX API.

This module provides the base class with common functionality
shared across all generator classes.
"""

import time
from pathlib import Path
from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod

from ..config.settings import settings
from ..config.prompts import PromptConfig
from ..api.client import FluxAPIClient
from ..api.models import GenerationRequest
from ..utils.logger import get_logger
from ..utils.image import ImageUtils

logger = get_logger(__name__)


class BaseGenerator(ABC):
    """Base class for all FLUX generators with common functionality."""
    
    def __init__(self, output_subdir: Optional[str] = None, api_key: Optional[str] = None):
        """Initialize base generator."""
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
        
        # Setup output directory
        if output_subdir:
            self.output_dir = self.settings.paths.output_dir / output_subdir
            self.output_dir.mkdir(parents=True, exist_ok=True)
        else:
            self.output_dir = self.settings.paths.output_dir
        
        logger.info(f"Initialized {self.__class__.__name__} with input image: {self.input_image}")
        if output_subdir:
            logger.info(f"Output directory: {self.output_dir}")
    
    def _execute_generation(self, request: GenerationRequest, output_path: Path) -> Optional[Path]:
        """Executes the image generation request and saves the result."""
        try:
            logger.info(f"Executing generation request for {output_path.name}")
            response = self.api_client.generate_image(request)
            
            if response.success and response.image_data:
                ImageUtils.save_image_data(response.image_data, output_path)
                logger.info(f"Generated image saved: {output_path}")
                return output_path
            else:
                logger.error(f"Generation failed for {output_path.name}: {response.error_message}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating image for {output_path.name}: {e}")
            return None

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
    
    def generate_single_image(
        self,
        prompt: str,
        seed: Optional[int] = None,
        aspect_ratio: Optional[str] = None,
        output_format: Optional[str] = None,
        base_name: str = "image",
        **kwargs
    ) -> Optional[Path]:
        """Generate a single image with common logic."""
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
                output_format=output_format,
                **kwargs
            )
            
            # Generate filename and execute
            filename = ImageUtils.generate_filename(
                base_name=base_name,
                index=0,
                seed=seed,
                extension=output_format
            )
            output_path = self.output_dir / filename
            return self._execute_generation(request, output_path)
            
        except Exception as e:
            logger.error(f"Error preparing generation request: {e}")
            return None
    
    def generate_multiple_images(
        self,
        count: int,
        prompt: str,
        start_seed: Optional[int] = None,
        aspect_ratio: Optional[str] = None,
        output_format: Optional[str] = None,
        base_name: str = "image",
        delay_between_requests: int = 2,
        **kwargs
    ) -> List[Path]:
        """Generate multiple images with common logic."""
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
                    output_format=output_format,
                    base_name=f"{base_name}_{i+1}",
                    **kwargs
                )
                
                if output_path:
                    generated_images.append(output_path)
                    successful_count += 1
                    logger.info(f"Successfully generated image {i + 1}/{count}")
                else:
                    logger.warning(f"Failed to generate image {i + 1}/{count}")
                
                # Delay between requests
                if i < count - 1:
                    time.sleep(delay_between_requests)
                    
            except Exception as e:
                logger.error(f"Error in generation {i + 1}/{count}: {e}")
        
        logger.info(f"Generation completed: {successful_count}/{count} images generated")
        return generated_images
    
    @abstractmethod
    def get_generator_info(self) -> Dict[str, Any]:
        """Get information about the specific generator implementation."""
        pass 