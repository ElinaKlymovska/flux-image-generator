"""
Image utilities for FLUX Image Generator.
"""

import base64
from pathlib import Path
from typing import Optional, Tuple
import hashlib


class ImageUtils:
    """Utility class for image operations."""
    
    @staticmethod
    def encode_image_to_base64(image_path: Path) -> str:
        """Encode image file to base64 string."""
        if not image_path.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        with open(image_path, "rb") as f:
            image_data = f.read()
        
        # Determine MIME type
        mime_type = "image/jpeg"  # Default
        if image_path.suffix.lower() in [".png"]:
            mime_type = "image/png"
        elif image_path.suffix.lower() in [".gif"]:
            mime_type = "image/gif"
        elif image_path.suffix.lower() in [".webp"]:
            mime_type = "image/webp"
        
        # Encode to base64
        encoded_image = base64.b64encode(image_data).decode("utf-8")
        return f"data:{mime_type};base64,{encoded_image}"
    
    @staticmethod
    def decode_base64_to_image(base64_string: str, output_path: Path) -> None:
        """Decode base64 string to image file."""
        try:
            # Remove data URL prefix if present
            if base64_string.startswith("data:"):
                # Extract base64 part
                base64_data = base64_string.split(",", 1)[1]
            else:
                base64_data = base64_string
            
            # Decode base64
            image_data = base64.b64decode(base64_data)
            
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write image data
            with open(output_path, "wb") as f:
                f.write(image_data)
                
        except Exception as e:
            raise ValueError(f"Failed to decode base64 image: {e}")
    
    @staticmethod
    def save_image_data(image_data: bytes, output_path: Path) -> None:
        """Save image data to file."""
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "wb") as f:
            f.write(image_data)
    
    @staticmethod
    def get_image_hash(image_path: Path) -> str:
        """Get MD5 hash of image file."""
        if not image_path.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        hash_md5 = hashlib.md5()
        with open(image_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        
        return hash_md5.hexdigest()
    
    @staticmethod
    def get_image_info(image_path: Path) -> dict:
        """Get basic information about image file."""
        if not image_path.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        stat = image_path.stat()
        
        return {
            "path": str(image_path),
            "size_bytes": stat.st_size,
            "size_mb": round(stat.st_size / (1024 * 1024), 2),
            "extension": image_path.suffix.lower(),
            "hash": ImageUtils.get_image_hash(image_path)
        }
    
    @staticmethod
    def generate_filename(
        base_name: str = "woman",
        index: int = 0,
        seed: int = 1000,
        extension: str = "jpg"
    ) -> str:
        """Generate standardized filename for generated images."""
        return f"{base_name}_{index:02d}_seed{seed}.{extension}"
    
    @staticmethod
    def find_input_image(input_dir: Path, filename: str = "character.jpg") -> Optional[Path]:
        """Find input image in directory."""
        image_path = input_dir / filename
        
        if image_path.exists():
            return image_path
        
        # Try alternative extensions
        for ext in [".png", ".jpeg", ".webp"]:
            alt_path = input_dir / f"{filename.rsplit('.', 1)[0]}{ext}"
            if alt_path.exists():
                return alt_path
        
        return None 