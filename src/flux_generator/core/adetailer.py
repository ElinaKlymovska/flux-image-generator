"""
Adetailer Integration for FLUX Image Generator.

This module provides enhanced face detail generation using Adetailer.
"""

import time
from pathlib import Path
from typing import Optional, List, Dict, Any
import base64
import json
import glob

from ..config.settings import settings
from ..config.prompts import PromptConfig
from ..api.client import FluxAPIClient
from ..api.models import GenerationRequest, GenerationResponse
from ..utils.logger import get_logger
from ..utils.image import ImageUtils

logger = get_logger(__name__)


class AdetailerSettings:
    """Settings for Adetailer processing."""
    
    def __init__(self):
        self.enabled = True
        self.model = "face_yolov8n.pt"  # Face detection model
        self.confidence = 0.3  # Detection confidence
        self.dilation = 4  # Dilation factor
        self.denoising_strength = 0.4  # Denoising strength
        self.prompt = "beautiful face, detailed eyes, perfect skin, high quality"
        self.negative_prompt = "blurry, low quality, distorted, deformed"
        self.steps = 20  # Number of steps
        self.cfg_scale = 7.0  # CFG scale
        self.sampler = "DPM++ 2M Karras"  # Sampler
        self.width = 512  # Width for face processing
        self.height = 512  # Height for face processing


class AdetailerGenerator:
    """Enhanced FLUX Image Generator with Adetailer integration."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Adetailer generator."""
        self.api_client = FluxAPIClient(api_key)
        self.settings = settings
        self.prompt_config = PromptConfig()
        self.adetailer_settings = AdetailerSettings()
        
        # Validate settings
        self.settings.validate()
        
        # Find input image
        self.input_image = ImageUtils.find_input_image(self.settings.paths.input_dir)
        if not self.input_image:
            raise FileNotFoundError(
                f"Input image not found in {self.settings.paths.input_dir}. "
                "Please place character.jpg in the input directory."
            )
        
        logger.info(f"Initialized Adetailer generator with input image: {self.input_image}")
    
    def process_existing_images(
        self, 
        input_dir: Optional[Path] = None,
        output_dir: Optional[Path] = None,
        file_pattern: str = "*.jpg",
        adetailer_config: Optional[Dict[str, Any]] = None,
        output_suffix: str = "_adetailer"
    ) -> List[Path]:
        """Process existing images in output directory with Adetailer enhancement."""
        # Use output directory if not specified
        if input_dir is None:
            input_dir = self.settings.paths.output_dir
        
        # Create output directory for Adetailer processed images
        if output_dir is None:
            output_dir = self.settings.paths.output_dir / "adetailer_processed"
        
        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Update Adetailer settings if provided
        if adetailer_config:
            for key, value in adetailer_config.items():
                if hasattr(self.adetailer_settings, key):
                    setattr(self.adetailer_settings, key, value)
        
        # Find all images in the directory
        image_pattern = str(input_dir / file_pattern)
        image_files = glob.glob(image_pattern)
        
        # Also check for PNG files
        png_pattern = str(input_dir / "*.png")
        png_files = glob.glob(png_pattern)
        image_files.extend(png_files)
        
        if not image_files:
            logger.warning(f"No images found in {input_dir} with pattern {file_pattern}")
            return []
        
        logger.info(f"Found {len(image_files)} images to process with Adetailer")
        logger.info(f"Output directory: {output_dir}")
        
        processed_images = []
        successful_count = 0
        
        for i, image_path in enumerate(image_files, 1):
            image_path = Path(image_path)
            logger.info(f"Processing image {i}/{len(image_files)}: {image_path.name}")
            
            try:
                # Process single image with Adetailer
                enhanced_path = self._process_single_existing_image(
                    image_path, 
                    output_dir,
                    output_suffix
                )
                
                if enhanced_path:
                    processed_images.append(enhanced_path)
                    successful_count += 1
                    logger.info(f"Successfully processed: {enhanced_path.name}")
                else:
                    logger.warning(f"Failed to process: {image_path.name}")
                
                # Small delay between requests
                if i < len(image_files):
                    time.sleep(2)
                    
            except Exception as e:
                logger.error(f"Error processing {image_path.name}: {e}")
        
        logger.info(f"Adetailer processing completed: {successful_count}/{len(image_files)} images processed")
        logger.info(f"Enhanced images saved to: {output_dir}")
        return processed_images
    
    def _process_single_existing_image(
        self, 
        image_path: Path, 
        output_dir: Path,
        output_suffix: str
    ) -> Optional[Path]:
        """Process a single existing image with Adetailer enhancement."""
        try:
            # Create Adetailer request
            adetailer_request = self._create_adetailer_request_from_file(
                image_path
            )
            
            # Send to API with Adetailer parameters
            response = self.api_client.generate_image(adetailer_request)
            
            if response.success and response.image_data:
                # Generate filename for enhanced image
                stem = image_path.stem
                suffix = image_path.suffix
                enhanced_filename = f"{stem}{output_suffix}{suffix}"
                
                # Save enhanced image to output directory
                output_path = output_dir / enhanced_filename
                ImageUtils.save_image_data(response.image_data, output_path)
                
                return output_path
            else:
                logger.error(f"Adetailer enhancement failed for {image_path.name}: {response.error_message}")
                return None
                
        except Exception as e:
            logger.error(f"Error processing {image_path.name}: {e}")
            return None
    
    def _create_adetailer_request_from_file(
        self, 
        image_path: Path
    ) -> GenerationRequest:
        """Create generation request with Adetailer parameters from existing file."""
        # Read image
        with open(image_path, "rb") as f:
            image_data = f.read()
        
        # Determine MIME type
        mime_type = "image/jpeg"
        if image_path.suffix.lower() in [".png"]:
            mime_type = "image/png"
        
        # Encode to base64
        encoded_image = base64.b64encode(image_data).decode("utf-8")
        input_image = f"data:{mime_type};base64,{encoded_image}"
        
        # Create enhanced prompt with face details
        enhanced_prompt = f"{self.adetailer_settings.prompt}, ultra realistic face, detailed facial features"
        
        # Create request with Adetailer parameters
        request = GenerationRequest(
            prompt=enhanced_prompt,
            input_image=input_image,
            seed=1000,  # Default seed for processing
            aspect_ratio="1:1",  # Square for face processing
            output_format=image_path.suffix[1:] if image_path.suffix else "jpeg"
        )
        
        # Add Adetailer-specific parameters to the request
        request_dict = request.to_dict()
        request_dict.update({
            "adetailer": {
                "enabled": self.adetailer_settings.enabled,
                "model": self.adetailer_settings.model,
                "confidence": self.adetailer_settings.confidence,
                "dilation": self.adetailer_settings.dilation,
                "denoising_strength": self.adetailer_settings.denoising_strength,
                "prompt": self.adetailer_settings.prompt,
                "negative_prompt": self.adetailer_settings.negative_prompt,
                "steps": self.adetailer_settings.steps,
                "cfg_scale": self.adetailer_settings.cfg_scale,
                "sampler": self.adetailer_settings.sampler,
                "width": self.adetailer_settings.width,
                "height": self.adetailer_settings.height
            }
        })
        
        return request
    
    def process_specific_images(
        self, 
        image_paths: List[Path],
        output_dir: Optional[Path] = None,
        adetailer_config: Optional[Dict[str, Any]] = None,
        output_suffix: str = "_adetailer"
    ) -> List[Path]:
        """Process specific images with Adetailer enhancement."""
        # Create output directory for Adetailer processed images
        if output_dir is None:
            output_dir = self.settings.paths.output_dir / "adetailer_processed"
        
        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Update Adetailer settings if provided
        if adetailer_config:
            for key, value in adetailer_config.items():
                if hasattr(self.adetailer_settings, key):
                    setattr(self.adetailer_settings, key, value)
        
        logger.info(f"Processing {len(image_paths)} specific images with Adetailer")
        logger.info(f"Output directory: {output_dir}")
        
        processed_images = []
        successful_count = 0
        
        for i, image_path in enumerate(image_paths, 1):
            logger.info(f"Processing image {i}/{len(image_paths)}: {image_path.name}")
            
            try:
                # Process single image with Adetailer
                enhanced_path = self._process_single_existing_image(
                    image_path, 
                    output_dir,
                    output_suffix
                )
                
                if enhanced_path:
                    processed_images.append(enhanced_path)
                    successful_count += 1
                    logger.info(f"Successfully processed: {enhanced_path.name}")
                else:
                    logger.warning(f"Failed to process: {image_path.name}")
                
                # Small delay between requests
                if i < len(image_paths):
                    time.sleep(2)
                    
            except Exception as e:
                logger.error(f"Error processing {image_path.name}: {e}")
        
        logger.info(f"Adetailer processing completed: {successful_count}/{len(image_paths)} images processed")
        logger.info(f"Enhanced images saved to: {output_dir}")
        return processed_images

    def generate_with_adetailer(
        self, 
        prompt: Optional[str] = None,
        seed: Optional[int] = None,
        aspect_ratio: Optional[str] = None,
        output_format: Optional[str] = None,
        adetailer_config: Optional[Dict[str, Any]] = None
    ) -> Optional[Path]:
        """Generate image with Adetailer face enhancement."""
        # Use defaults if not provided
        prompt = prompt or self.prompt_config.PROMPTS["ultra_realistic"]["prompt"]
        seed = seed or self.settings.generation.default_seed
        aspect_ratio = aspect_ratio or self.settings.generation.default_aspect_ratio
        output_format = output_format or self.settings.generation.default_output_format
        
        # Update Adetailer settings if provided
        if adetailer_config:
            for key, value in adetailer_config.items():
                if hasattr(self.adetailer_settings, key):
                    setattr(self.adetailer_settings, key, value)
        
        logger.info(f"Generating image with Adetailer using seed {seed}")
        
        try:
            # Step 1: Generate base image
            logger.info("Step 1: Generating base image...")
            base_request = GenerationRequest.from_image_file(
                prompt=prompt,
                image_path=self.input_image,
                seed=seed,
                aspect_ratio=aspect_ratio,
                output_format=output_format
            )
            
            base_response = self.api_client.generate_image(base_request)
            
            if not base_response.success or not base_response.image_data:
                logger.error(f"Base generation failed: {base_response.error_message}")
                return None
            
            # Save base image temporarily
            base_filename = ImageUtils.generate_filename(
                base_name="base_woman",
                index=0,
                seed=seed,
                extension=output_format
            )
            base_path = self.settings.paths.output_dir / base_filename
            ImageUtils.save_image_data(base_response.image_data, base_path)
            
            logger.info(f"Base image saved: {base_path}")
            
            # Step 2: Apply Adetailer processing
            logger.info("Step 2: Applying Adetailer face enhancement...")
            enhanced_path = self._apply_adetailer_enhancement(
                base_path, 
                seed, 
                output_format
            )
            
            if enhanced_path:
                logger.info(f"Adetailer enhanced image saved: {enhanced_path}")
                # Remove base image
                base_path.unlink(missing_ok=True)
                return enhanced_path
            else:
                logger.warning("Adetailer enhancement failed, returning base image")
                return base_path
                
        except Exception as e:
            logger.error(f"Error in Adetailer generation: {e}")
            return None
    
    def _apply_adetailer_enhancement(
        self, 
        base_image_path: Path, 
        seed: int, 
        output_format: str
    ) -> Optional[Path]:
        """Apply Adetailer enhancement to the base image."""
        try:
            # Create Adetailer request
            adetailer_request = self._create_adetailer_request(
                base_image_path, 
                seed, 
                output_format
            )
            
            # Send to API with Adetailer parameters
            response = self.api_client.generate_image(adetailer_request)
            
            if response.success and response.image_data:
                # Generate filename for enhanced image
                filename = ImageUtils.generate_filename(
                    base_name="adetailer_woman",
                    index=0,
                    seed=seed,
                    extension=output_format
                )
                
                # Save enhanced image
                output_path = self.settings.paths.output_dir / filename
                ImageUtils.save_image_data(response.image_data, output_path)
                
                return output_path
            else:
                logger.error(f"Adetailer enhancement failed: {response.error_message}")
                return None
                
        except Exception as e:
            logger.error(f"Error applying Adetailer enhancement: {e}")
            return None
    
    def _create_adetailer_request(
        self, 
        base_image_path: Path, 
        seed: int, 
        output_format: str
    ) -> GenerationRequest:
        """Create generation request with Adetailer parameters."""
        # Read base image
        with open(base_image_path, "rb") as f:
            image_data = f.read()
        
        # Determine MIME type
        mime_type = "image/jpeg"
        if base_image_path.suffix.lower() in [".png"]:
            mime_type = "image/png"
        
        # Encode to base64
        encoded_image = base64.b64encode(image_data).decode("utf-8")
        input_image = f"data:{mime_type};base64,{encoded_image}"
        
        # Create enhanced prompt with face details
        enhanced_prompt = f"{self.adetailer_settings.prompt}, ultra realistic face, detailed facial features"
        
        # Create request with Adetailer parameters
        request = GenerationRequest(
            prompt=enhanced_prompt,
            input_image=input_image,
            seed=seed,
            aspect_ratio="1:1",  # Square for face processing
            output_format=output_format
        )
        
        # Add Adetailer-specific parameters to the request
        request_dict = request.to_dict()
        request_dict.update({
            "adetailer": {
                "enabled": self.adetailer_settings.enabled,
                "model": self.adetailer_settings.model,
                "confidence": self.adetailer_settings.confidence,
                "dilation": self.adetailer_settings.dilation,
                "denoising_strength": self.adetailer_settings.denoising_strength,
                "prompt": self.adetailer_settings.prompt,
                "negative_prompt": self.adetailer_settings.negative_prompt,
                "steps": self.adetailer_settings.steps,
                "cfg_scale": self.adetailer_settings.cfg_scale,
                "sampler": self.adetailer_settings.sampler,
                "width": self.adetailer_settings.width,
                "height": self.adetailer_settings.height
            }
        })
        
        return request
    
    def generate_multiple_with_adetailer(
        self, 
        count: Optional[int] = None,
        start_seed: Optional[int] = None,
        prompt: Optional[str] = None,
        aspect_ratio: Optional[str] = None,
        output_format: Optional[str] = None,
        adetailer_config: Optional[Dict[str, Any]] = None
    ) -> List[Path]:
        """Generate multiple images with Adetailer enhancement."""
        count = count or self.settings.generation.default_count
        start_seed = start_seed or self.settings.generation.default_seed
        
        logger.info(f"Starting Adetailer generation of {count} images")
        
        generated_images = []
        successful_count = 0
        
        for i in range(count):
            seed = start_seed + i
            logger.info(f"Generating Adetailer image {i + 1}/{count} with seed {seed}")
            
            try:
                output_path = self.generate_with_adetailer(
                    prompt=prompt,
                    seed=seed,
                    aspect_ratio=aspect_ratio,
                    output_format=output_format,
                    adetailer_config=adetailer_config
                )
                
                if output_path:
                    generated_images.append(output_path)
                    successful_count += 1
                    logger.info(f"Successfully generated Adetailer image {i + 1}/{count}")
                else:
                    logger.warning(f"Failed to generate Adetailer image {i + 1}/{count}")
                
                # Small delay between requests
                if i < count - 1:
                    time.sleep(3)
                    
            except Exception as e:
                logger.error(f"Error in Adetailer generation {i + 1}/{count}: {e}")
        
        logger.info(f"Adetailer generation completed: {successful_count}/{count} images generated")
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
    
    def update_adetailer_settings(self, **kwargs) -> None:
        """Update Adetailer settings."""
        for key, value in kwargs.items():
            if hasattr(self.adetailer_settings, key):
                setattr(self.adetailer_settings, key, value)
                logger.info(f"Updated Adetailer setting {key}: {value}")
            else:
                logger.warning(f"Unknown Adetailer setting: {key}") 