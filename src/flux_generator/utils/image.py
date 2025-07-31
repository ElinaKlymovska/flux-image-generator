"""
Image utilities for FLUX Image Generator.
"""

from pathlib import Path
from typing import Optional

from .base import ImageProcessor, FileUtils


class ImageUtils:
    """Utility class for image operations."""
    
    @staticmethod
    def encode_image_to_base64(image_path: Path) -> str:
        """Encode image file to base64 string."""
        return ImageProcessor.encode_to_base64(image_path)
    
    @staticmethod
    def decode_base64_to_image(base64_string: str, output_path: Path) -> None:
        """Decode base64 string to image file."""
        ImageProcessor.decode_from_base64(base64_string, output_path)
    
    @staticmethod
    def save_image_data(image_data: bytes, output_path: Path) -> None:
        """Save image data to file."""
        ImageProcessor.save_image_data(image_data, output_path)
    
    @staticmethod
    def get_image_hash(image_path: Path) -> str:
        """Get MD5 hash of image file."""
        return ImageProcessor.get_image_hash(image_path)
    
    @staticmethod
    def get_image_info(image_path: Path) -> dict:
        """Get basic information about image file."""
        return ImageProcessor.get_image_info(image_path)
    
    @staticmethod
    def find_input_image(input_dir: Path, filename: str = "character.jpg") -> Optional[Path]:
        """Find input image in directory."""
        return FileUtils.find_file_in_directory(
            input_dir, 
            filename, 
            extensions=["", ".png", ".jpeg", ".webp"]
        )
    
    @staticmethod
    def generate_filename(
        base_name: str,
        index: int = 0,
        seed: Optional[int] = None,
        extension: str = "jpg"
    ) -> str:
        """Generate filename with optional seed."""
        return FileUtils.generate_filename(base_name, index, seed, extension) 