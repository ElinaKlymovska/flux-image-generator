"""
Base Utilities for FLUX Image Generator.

This module provides base classes for utility functions
to reduce code duplication across image and logger utilities.
"""

import base64
import hashlib
import logging
import sys
from pathlib import Path
from typing import Optional, Dict, Any, Union
from abc import ABC, abstractmethod


class BaseUtils(ABC):
    """Base class for utility functions."""
    
    @staticmethod
    def ensure_directory(path: Path) -> None:
        """Ensure directory exists."""
        path.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def safe_file_operation(operation, *args, **kwargs):
        """Safely execute file operations with error handling."""
        try:
            return operation(*args, **kwargs)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {e}")
        except PermissionError as e:
            raise PermissionError(f"Permission denied: {e}")
        except Exception as e:
            raise Exception(f"File operation failed: {e}")


class ImageProcessor:
    """Base image processing utilities."""
    
    @staticmethod
    def encode_to_base64(image_path: Path) -> str:
        """Encode image file to base64 string."""
        if not image_path.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        with open(image_path, "rb") as f:
            image_data = f.read()
        
        # Determine MIME type
        mime_type = ImageProcessor._get_mime_type(image_path)
        
        # Encode to base64
        encoded_image = base64.b64encode(image_data).decode("utf-8")
        return f"data:{mime_type};base64,{encoded_image}"
    
    @staticmethod
    def decode_from_base64(base64_string: str, output_path: Path) -> None:
        """Decode base64 string to image file."""
        try:
            # Remove data URL prefix if present
            if base64_string.startswith("data:"):
                base64_data = base64_string.split(",", 1)[1]
            else:
                base64_data = base64_string
            
            # Decode base64
            image_data = base64.b64decode(base64_data)
            
            # Ensure output directory exists
            BaseUtils.ensure_directory(output_path.parent)
            
            # Write image data
            with open(output_path, "wb") as f:
                f.write(image_data)
                
        except Exception as e:
            raise ValueError(f"Failed to decode base64 image: {e}")
    
    @staticmethod
    def save_image_data(image_data: bytes, output_path: Path) -> None:
        """Save image data to file."""
        BaseUtils.ensure_directory(output_path.parent)
        
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
    def get_image_info(image_path: Path) -> Dict[str, Any]:
        """Get basic information about image file."""
        if not image_path.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        stat = image_path.stat()
        
        # Try to get image dimensions if PIL is available
        try:
            from PIL import Image
            with Image.open(image_path) as img:
                width, height = img.size
        except ImportError:
            # PIL not available, use default values
            width, height = 512, 512
        except Exception:
            # Any other error, use default values
            width, height = 512, 512
        
        return {
            "path": str(image_path),
            "size_bytes": stat.st_size,
            "size_mb": round(stat.st_size / (1024 * 1024), 2),
            "extension": image_path.suffix.lower(),
            "hash": ImageProcessor.get_image_hash(image_path),
            "width": width,
            "height": height
        }
    
    @staticmethod
    def _get_mime_type(image_path: Path) -> str:
        """Get MIME type for image file."""
        extension = image_path.suffix.lower()
        mime_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".webp": "image/webp",
            ".bmp": "image/bmp",
            ".tiff": "image/tiff"
        }
        return mime_types.get(extension, "image/jpeg")


class LoggerManager:
    """Base logger management utilities."""
    
    @staticmethod
    def setup_logger(
        name: str = "flux_generator",
        level: Union[str, int] = "INFO",
        log_file: Optional[Path] = None,
        format_string: Optional[str] = None
    ) -> logging.Logger:
        """Setup logger with console and file handlers."""
        
        # Convert string level to logging constant
        if isinstance(level, str):
            level = getattr(logging, level.upper(), logging.INFO)
        
        if format_string is None:
            format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        
        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        # Clear existing handlers
        logger.handlers.clear()
        
        # Create formatter
        formatter = logging.Formatter(format_string)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler (optional)
        if log_file:
            BaseUtils.ensure_directory(log_file.parent)
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        return logger
    
    @staticmethod
    def get_logger(name: str = "flux_generator") -> logging.Logger:
        """Get existing logger or create new one."""
        logger = logging.getLogger(name)
        
        if not logger.handlers:
            # Setup default logger if not configured
            logger = LoggerManager.setup_logger(name)
        
        return logger


class FileUtils:
    """File utility functions."""
    
    @staticmethod
    def find_file_in_directory(
        directory: Path, 
        filename: str, 
        extensions: Optional[list] = None
    ) -> Optional[Path]:
        """Find file in directory with optional extension variations."""
        if extensions is None:
            extensions = [""]  # No extension
        
        for ext in extensions:
            file_path = directory / f"{filename}{ext}"
            if file_path.exists():
                return file_path
        
        return None
    
    @staticmethod
    def generate_filename(
        base_name: str,
        index: int = 0,
        seed: Optional[int] = None,
        extension: str = "jpg"
    ) -> str:
        """Generate filename with optional seed."""
        if seed is not None:
            return f"{base_name}_{seed}.{extension}"
        elif index > 0:
            return f"{base_name}_{index}.{extension}"
        else:
            return f"{base_name}.{extension}"
    
    @staticmethod
    def ensure_extension(filename: str, extension: str) -> str:
        """Ensure filename has correct extension."""
        if not extension.startswith('.'):
            extension = '.' + extension
        
        if filename.endswith(extension):
            return filename
        else:
            return filename + extension 