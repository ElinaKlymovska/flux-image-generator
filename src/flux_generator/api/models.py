"""
Data models for FLUX API integration.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from pathlib import Path
import base64


@dataclass
class GenerationRequest:
    """Request model for image generation."""
    prompt: str
    input_image: str  # Base64 encoded image
    seed: int = 1000
    aspect_ratio: str = "2:3"
    output_format: str = "jpeg"
    prompt_upsampling: bool = False
    safety_tolerance: int = 2
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API request."""
        return {
            "prompt": self.prompt,
            "input_image": self.input_image,
            "seed": self.seed,
            "aspect_ratio": self.aspect_ratio,
            "output_format": self.output_format,
            "prompt_upsampling": self.prompt_upsampling,
            "safety_tolerance": self.safety_tolerance
        }
    
    @classmethod
    def from_image_file(cls, prompt: str, image_path: Path, **kwargs) -> "GenerationRequest":
        """Create request from image file."""
        if not image_path.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        # Read and encode image
        with open(image_path, "rb") as f:
            image_data = f.read()
        
        # Determine MIME type
        mime_type = "image/jpeg"  # Default
        if image_path.suffix.lower() in [".png"]:
            mime_type = "image/png"
        
        # Encode to base64
        encoded_image = base64.b64encode(image_data).decode("utf-8")
        input_image = f"data:{mime_type};base64,{encoded_image}"
        
        return cls(prompt=prompt, input_image=input_image, **kwargs)


@dataclass
class GenerationResponse:
    """Response model for image generation."""
    success: bool
    image_data: Optional[bytes] = None
    image_url: Optional[str] = None
    error_message: Optional[str] = None
    request_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    @classmethod
    def success_response(cls, image_data: bytes, **kwargs) -> "GenerationResponse":
        """Create success response."""
        return cls(success=True, image_data=image_data, **kwargs)
    
    @classmethod
    def error_response(cls, error_message: str, **kwargs) -> "GenerationResponse":
        """Create error response."""
        return cls(success=False, error_message=error_message, **kwargs)


@dataclass
class APIError:
    """API error model."""
    status_code: int
    message: str
    details: Optional[Dict[str, Any]] = None
    
    def __str__(self) -> str:
        return f"API Error {self.status_code}: {self.message}" 