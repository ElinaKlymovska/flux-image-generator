"""
Adetailer Integration for FLUX Image Generator.

This module provides enhanced face detail generation using Adetailer.
"""

import time
from pathlib import Path
from typing import Optional, List, Dict, Any
import base64
import glob

from .base import BaseGenerator
from ..api.models import GenerationRequest
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


class AdetailerGenerator(BaseGenerator):
    """Enhanced FLUX Image Generator with Adetailer integration."""
    
    def __init__(self, output_subdir: str = "adetailer", api_key: Optional[str] = None):
        """Initialize Adetailer generator."""
        super().__init__(output_subdir=output_subdir, api_key=api_key)
        self.adetailer_settings = AdetailerSettings()
        
        logger.info(f"Adetailer generator initialized with settings: {self.adetailer_settings.model}")

    def _prepare_request_data_from_file(self, image_path: Path) -> Dict[str, Any]:
        """Prepares common request data from an image file."""
        image_info = ImageUtils.get_image_info(image_path)
        return {
            "image_data": ImageUtils.encode_image_to_base64(image_path),
            "aspect_ratio": f"{image_info['width']}:{image_info['height']}"
        }

    def process_directory_images(
        self, 
        input_dir: Optional[Path] = None,
        output_dir: Optional[Path] = None,
        file_pattern: str = "*.jpg",
        adetailer_config: Optional[Dict[str, Any]] = None,
        output_suffix: str = "_adetailer"
    ) -> List[Path]:
        """
        Process all images in the specified directory with Adetailer enhancement.
        
        Args:
            input_dir: Directory with images to process (default: data/output)
            output_dir: Directory to save processed images (default: data/adetailer_processed)
            file_pattern: File pattern to match (default: "*.jpg")
            adetailer_config: Custom Adetailer settings
            output_suffix: Suffix for processed files
            
        Returns:
            List of paths to processed images
        """
        # Use output directory if not specified
        if input_dir is None:
            input_dir = self.settings.paths.output_dir
        
        # Create output directory for Adetailer processed images
        if output_dir is None:
            output_dir = Path("data") / "adetailer_processed"
        
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
        
        if not image_files:
            logger.warning(f"No images found in {input_dir} with pattern {file_pattern}")
            return []
        
        logger.info(f"Found {len(image_files)} images to process with Adetailer")
        logger.info(f"Output directory: {output_dir}")
        logger.info(f"Using Adetailer parameters: {adetailer_config is not None}")
        
        processed_images = []
        
        for i, image_path in enumerate(image_files, 1):
            image_path = Path(image_path)
            logger.info(f"Processing image {i}/{len(image_files)}: {image_path.name}")
            
            try:
                # Process single image
                processed_path = self._process_single_image(
                    image_path, 
                    output_dir, 
                    output_suffix,
                    adetailer_config is not None
                )
                
                if processed_path:
                    processed_images.append(processed_path)
                    logger.info(f"Successfully processed: {processed_path.name}")
                else:
                    logger.warning(f"Failed to process: {image_path.name}")
                    
            except Exception as e:
                logger.error(f"Error processing {image_path.name}: {e}")
        
        return processed_images
    
    def process_single_image(
        self,
        image_path: Path,
        output_dir: Optional[Path] = None,
        adetailer_config: Optional[Dict[str, Any]] = None,
        output_suffix: str = "_adetailer"
    ) -> Optional[Path]:
        """
        Process a single image with Adetailer enhancement.
        
        Args:
            image_path: Path to the image to process
            output_dir: Directory to save processed image (default: data/adetailer_processed)
            adetailer_config: Custom Adetailer settings
            output_suffix: Suffix for processed file
            
        Returns:
            Path to processed image or None if failed
        """
        # Create output directory if not specified
        if output_dir is None:
            output_dir = Path("data") / "adetailer_processed"
        
        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Update Adetailer settings if provided
        if adetailer_config:
            for key, value in adetailer_config.items():
                if hasattr(self.adetailer_settings, key):
                    setattr(self.adetailer_settings, key, value)
        
        # Check if input image exists
        if not image_path.exists():
            logger.error(f"Input image not found: {image_path}")
            return None
        
        logger.info(f"Processing single image: {image_path.name}")
        
        try:
            return self._process_single_image(
                image_path, 
                output_dir, 
                output_suffix,
                adetailer_config is not None
            )
        except Exception as e:
            logger.error(f"Error processing {image_path.name}: {e}")
            return None
    
    def _process_single_image(
        self, 
        image_path: Path, 
        output_dir: Path,
        output_suffix: str,
        use_adetailer: bool = True
    ) -> Optional[Path]:
        """Internal method to process a single image."""
        try:
            # Create generation request
            if use_adetailer:
                request = self._create_adetailer_request_from_file(image_path)
            else:
                request = self._create_standard_request_from_file(image_path)
            
            # Generate output filename
            stem = image_path.stem
            extension = image_path.suffix
            output_filename = f"{stem}{output_suffix}{extension}"
            output_path = output_dir / output_filename

            # Execute generation
            return self._execute_generation(request, output_path)

        except Exception as e:
            logger.error(f"Error processing image: {e}")
            return None
    
    def _create_adetailer_request_from_file(
        self, 
        image_path: Path
    ) -> GenerationRequest:
        """Create Adetailer request from image file."""
        request_data = self._prepare_request_data_from_file(image_path)

        # Create Adetailer parameters
        adetailer_params = {
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
        
        return GenerationRequest(
            prompt="Portrait enhancement with detailed face features",
            input_image=request_data["image_data"],
            aspect_ratio=request_data["aspect_ratio"],
            output_format=self.settings.generation.default_output_format,
            adetailer=adetailer_params
        )
    
    def _create_standard_request_from_file(
        self, 
        image_path: Path
    ) -> GenerationRequest:
        """Create standard request from image file."""
        request_data = self._prepare_request_data_from_file(image_path)
        
        return GenerationRequest(
            prompt="Portrait enhancement with improved details",
            input_image=request_data["image_data"],
            aspect_ratio=request_data["aspect_ratio"],
            output_format=self.settings.generation.default_output_format
        )
    
    def update_adetailer_settings(self, **kwargs) -> None:
        """Update Adetailer settings."""
        for key, value in kwargs.items():
            if hasattr(self.adetailer_settings, key):
                setattr(self.adetailer_settings, key, value)
    
    def get_generator_info(self) -> Dict[str, Any]:
        """Get information about the generator."""
        return {
            "name": "AdetailerGenerator",
            "type": "adetailer",
            "description": "Enhanced FLUX Image Generator with Adetailer integration",
            "adetailer_model": self.adetailer_settings.model,
            "adetailer_enabled": self.adetailer_settings.enabled,
            "input_image": str(self.input_image),
            "output_dir": str(self.output_dir)
        } 