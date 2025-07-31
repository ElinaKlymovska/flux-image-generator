"""
Basic FLUX Image Generator.

This module provides the core image generation functionality.
"""

from pathlib import Path
from typing import Optional, List, Dict, Any

from .base import BaseGenerator
from ..utils.logger import get_logger

logger = get_logger(__name__)


class FluxImageGenerator(BaseGenerator):
    """Basic FLUX Image Generator."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize generator."""
        super().__init__(output_subdir=None, api_key=api_key)
    
    def generate_single_image(
        self, 
        prompt: Optional[str] = None,
        seed: Optional[int] = None,
        aspect_ratio: Optional[str] = None,
        output_format: Optional[str] = None
    ) -> Optional[Path]:
        """Generate a single image."""
        # Use defaults if not provided - safer prompt
        prompt = prompt or self.prompt_config.PROMPTS["safe_realistic"]["prompt"]
        
        return super().generate_single_image(
            prompt=prompt,
            seed=seed,
            aspect_ratio=aspect_ratio,
            output_format=output_format,
            base_name="woman"
        )
    
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
        prompt = prompt or self.prompt_config.PROMPTS["safe_realistic"]["prompt"]
        
        return super().generate_multiple_images(
            count=count,
            prompt=prompt,
            start_seed=start_seed,
            aspect_ratio=aspect_ratio,
            output_format=output_format,
            base_name="woman"
        )
    
    def get_generator_info(self) -> Dict[str, Any]:
        """Get information about the generator."""
        return {
            "name": "FluxImageGenerator",
            "type": "basic",
            "description": "Basic FLUX Image Generator with simple functionality",
            "input_image": str(self.input_image),
            "output_dir": str(self.output_dir)
        } 