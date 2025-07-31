"""
Data models for FLUX API integration.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from pathlib import Path

from .base import BaseRequest, BaseResponse, APIError
from ..utils.base import ImageProcessor


@dataclass
class GenerationRequest(BaseRequest):
    """Request model for image generation."""
    prompt: str
    input_image: str  # Base64 encoded image
    seed: int = 1000
    aspect_ratio: str = "2:3"
    output_format: str = "jpeg"
    prompt_upsampling: bool = False
    safety_tolerance: int = 2
    
    @classmethod
    def from_image_file(cls, prompt: str, image_path: Path, **kwargs) -> "GenerationRequest":
        """Create request from image file."""
        if not image_path.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        # Encode image to base64
        input_image = ImageProcessor.encode_to_base64(image_path)
        
        return cls(prompt=prompt, input_image=input_image, **kwargs)


class GenerationResponse(BaseResponse):
    """Response model for image generation."""
    
    def __init__(self, success: bool, image_data: Optional[bytes] = None, 
                 image_url: Optional[str] = None, error_message: Optional[str] = None,
                 request_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None):
        """Initialize GenerationResponse."""
        super().__init__(success=success)
        self.image_data = image_data
        self.image_url = image_url
        self.error_message = error_message
        self.request_id = request_id
        self.metadata = metadata 