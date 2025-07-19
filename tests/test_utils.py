"""
Tests for utility functions.
"""

import pytest
from pathlib import Path
import base64

from src.flux_generator.utils.image import ImageUtils


class TestImageUtils:
    """Test ImageUtils class."""
    
    def test_encode_image_to_base64(self, sample_image):
        """Test image encoding to base64."""
        encoded = ImageUtils.encode_image_to_base64(sample_image)
        
        assert encoded.startswith("data:image/jpeg;base64,")
        assert len(encoded) > 100  # Should have some content
    
    def test_encode_nonexistent_image(self, temp_dir):
        """Test encoding non-existent image."""
        nonexistent_image = temp_dir / "nonexistent.jpg"
        
        with pytest.raises(FileNotFoundError):
            ImageUtils.encode_image_to_base64(nonexistent_image)
    
    def test_decode_base64_to_image(self, temp_dir):
        """Test base64 decoding to image."""
        # Create test base64 string
        test_data = b"test image data"
        base64_string = f"data:image/jpeg;base64,{base64.b64encode(test_data).decode()}"
        
        output_path = temp_dir / "decoded.jpg"
        ImageUtils.decode_base64_to_image(base64_string, output_path)
        
        assert output_path.exists()
        with open(output_path, "rb") as f:
            assert f.read() == test_data
    
    def test_save_image_data(self, temp_dir):
        """Test saving image data."""
        test_data = b"test image data"
        output_path = temp_dir / "saved.jpg"
        
        ImageUtils.save_image_data(test_data, output_path)
        
        assert output_path.exists()
        with open(output_path, "rb") as f:
            assert f.read() == test_data
    
    def test_get_image_hash(self, sample_image):
        """Test image hash generation."""
        hash_value = ImageUtils.get_image_hash(sample_image)
        
        assert isinstance(hash_value, str)
        assert len(hash_value) == 32  # MD5 hash length
    
    def test_get_image_info(self, sample_image):
        """Test image info retrieval."""
        info = ImageUtils.get_image_info(sample_image)
        
        assert "path" in info
        assert "size_bytes" in info
        assert "size_mb" in info
        assert "extension" in info
        assert "hash" in info
        
        assert info["path"] == str(sample_image)
        assert info["extension"] == ".jpg"
        assert info["size_bytes"] > 0
    
    def test_generate_filename(self):
        """Test filename generation."""
        filename = ImageUtils.generate_filename("test", 5, 1234, "jpg")
        
        assert filename == "test_05_seed1234.jpg"
    
    def test_find_input_image(self, temp_dir, sample_image):
        """Test input image finding."""
        # Test with existing image
        found_image = ImageUtils.find_input_image(temp_dir, sample_image.name)
        assert found_image == sample_image
        
        # Test with non-existent image
        found_image = ImageUtils.find_input_image(temp_dir, "nonexistent.jpg")
        assert found_image is None 