"""
Enhanced FLUX Image Generator.

This module provides enhanced image generation with multiple styles and configurations.
"""

import time
from pathlib import Path
from typing import Optional, List, Dict, Any

from ..config.settings import settings
from ..config.prompts import PromptConfig
from ..api.client import FluxAPIClient
from ..api.models import GenerationRequest, GenerationResponse
from ..utils.logger import get_logger
from ..utils.image import ImageUtils

logger = get_logger(__name__)


class EnhancedFluxGenerator:
    """Enhanced FLUX Image Generator with multiple styles."""
    
    def __init__(self, output_subdir: str = "enhanced", api_key: Optional[str] = None):
        """Initialize enhanced generator."""
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
        self.output_dir = self.settings.paths.output_dir / output_subdir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Current settings
        self.current_style = "ultra_realistic"
        self.current_aspect = "portrait"
        self.current_quality = "high"
        
        logger.info(f"Initialized enhanced generator with output dir: {self.output_dir}")
    
    def set_style(self, style: str) -> None:
        """Set generation style."""
        if style not in self.prompt_config.PROMPTS:
            available = list(self.prompt_config.PROMPTS.keys())
            raise ValueError(f"Unknown style: {style}. Available: {available}")
        self.current_style = style
        logger.info(f"Style set to: {style}")
    
    def get_style_info(self) -> Dict[str, Any]:
        """Get detailed information about current style."""
        return self.prompt_config.get_style_info(self.current_style)
    
    def find_styles_by_use_case(self, use_case: str) -> List[Dict[str, Any]]:
        """Find styles suitable for specific use case."""
        return self.prompt_config.get_prompt_by_use_case(use_case)
    
    def find_styles_by_technical_spec(self, spec_type: str, spec_value: str) -> List[Dict[str, Any]]:
        """Find styles matching technical specifications."""
        return self.prompt_config.get_prompt_by_technical_spec(spec_type, spec_value)
    
    def set_aspect_ratio(self, aspect: str) -> None:
        """Set aspect ratio."""
        if aspect not in self.prompt_config.ASPECT_RATIOS:
            available = list(self.prompt_config.ASPECT_RATIOS.keys())
            raise ValueError(f"Unknown aspect: {aspect}. Available: {available}")
        self.current_aspect = aspect
        logger.info(f"Aspect ratio set to: {aspect}")
    
    def set_quality(self, quality: str) -> None:
        """Set generation quality."""
        if quality not in self.prompt_config.QUALITY_SETTINGS:
            available = list(self.prompt_config.QUALITY_SETTINGS.keys())
            raise ValueError(f"Unknown quality: {quality}. Available: {available}")
        self.current_quality = quality
        logger.info(f"Quality set to: {quality}")
    
    def get_current_config(self) -> Dict[str, Any]:
        """Get current configuration."""
        return self.prompt_config.get_prompt_config(
            self.current_style,
            self.current_aspect,
            self.current_quality
        )
    
    def generate_single_image(
        self, 
        seed: Optional[int] = None,
        custom_prompt: Optional[str] = None
    ) -> Optional[Path]:
        """Generate a single image."""
        seed = seed or self.settings.generation.default_seed
        config = self.get_current_config()
        
        logger.info(f"Generating image with seed {seed}, style: {config['style_name']}")
        
        try:
            # Use custom prompt or default
            prompt = custom_prompt if custom_prompt else config["prompt"]
            
            # Create generation request
            quality_settings = config["quality_settings"].copy()
            # Remove description as it's not a valid parameter for GenerationRequest
            quality_settings.pop("description", None)
            
            request = GenerationRequest.from_image_file(
                prompt=prompt,
                image_path=self.input_image,
                seed=seed,
                aspect_ratio=config["aspect_ratio"],
                output_format="jpeg",
                **quality_settings
            )
            
            # Generate image
            response = self.api_client.generate_image(request)
            
            if response.success and response.image_data:
                # Generate filename
                filename = ImageUtils.generate_filename(
                    base_name=f"{self.current_style}_woman",
                    index=0,
                    seed=seed,
                    extension="jpg"
                )
                
                # Save image
                output_path = self.output_dir / filename
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
        custom_prompt: Optional[str] = None
    ) -> List[Path]:
        """Generate multiple images."""
        count = count or 5
        start_seed = start_seed or self.settings.generation.default_seed
        
        logger.info(f"Starting generation of {count} images with style: {self.current_style}")
        
        generated_images = []
        successful_count = 0
        
        for i in range(count):
            seed = start_seed + i
            logger.info(f"Generating image {i + 1}/{count} with seed {seed}")
            
            try:
                output_path = self.generate_single_image(seed, custom_prompt)
                
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
    
    def generate_style_comparison(
        self, 
        styles: Optional[List[str]] = None, 
        count_per_style: int = 2
    ) -> Dict[str, List[Path]]:
        """Generate comparison across multiple styles."""
        styles = styles or ["ultra_realistic", "cinematic", "artistic"]
        
        logger.info(f"Generating style comparison: {styles}")
        
        results = {}
        
        for style in styles:
            logger.info(f"Generating {count_per_style} images in {style} style")
            
            # Set style
            self.set_style(style)
            
            # Generate images
            images = self.generate_images(count=count_per_style)
            results[style] = images
            
            logger.info(f"Generated {len(images)} images for {style} style")
        
        return results
    
    def generate_from_preset(
        self, 
        preset: str, 
        count: int = 1,
        start_seed: Optional[int] = None
    ) -> List[Path]:
        """Generate images using a preset configuration."""
        logger.info(f"Generating {count} images using preset: {preset}")
        
        start_seed = start_seed or self.settings.generation.default_seed
        config = self.prompt_config.get_preset_config(preset, self.current_aspect, self.current_quality)
        
        generated_images = []
        successful_count = 0
        
        for i in range(count):
            seed = start_seed + i
            logger.info(f"Generating image {i + 1}/{count} with seed {seed}")
            
            try:
                # Create generation request
                quality_settings = config["quality_settings"].copy()
                # Remove description as it's not a valid parameter for GenerationRequest
                quality_settings.pop("description", None)
                
                request = GenerationRequest.from_image_file(
                    prompt=config["prompt"],
                    image_path=self.input_image,
                    seed=seed,
                    aspect_ratio=config["aspect_ratio"],
                    output_format="jpeg",
                    **quality_settings
                )
                
                # Generate image
                response = self.api_client.generate_image(request)
                
                if response.success and response.image_data:
                    # Generate filename
                    filename = ImageUtils.generate_filename(
                        base_name=f"preset_{preset}",
                        index=i,
                        seed=seed,
                        extension="jpg"
                    )
                    
                    # Save image
                    output_path = self.output_dir / filename
                    ImageUtils.save_image_data(response.image_data, output_path)
                    
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
        
        logger.info(f"Preset generation completed: {successful_count}/{count} images generated")
        return generated_images
    
    def list_available_styles(self) -> List[Dict[str, str]]:
        """List available styles."""
        return self.prompt_config.list_available_styles()
    
    def list_available_aspects(self) -> Dict[str, str]:
        """List available aspect ratios."""
        return self.prompt_config.list_available_aspects()
    
    def list_available_qualities(self) -> List[str]:
        """List available quality settings."""
        return self.prompt_config.list_available_qualities()
    
    def test_connection(self) -> bool:
        """Test API connection."""
        try:
            return self.api_client.test_connection()
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False 