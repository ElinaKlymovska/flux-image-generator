"""
Test configuration and fixtures.
"""

import pytest
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def temp_dir():
    """Create temporary directory for tests."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_image(temp_dir):
    """Create a sample image file for testing."""
    image_path = temp_dir / "test_image.jpg"
    
    # Create a minimal JPEG file
    with open(image_path, "wb") as f:
        # Minimal JPEG header
        f.write(b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\x27 ,#\x1c\x1c(7),01444\x1f\x27=9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9")
    
    return image_path


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    class MockSettings:
        api_key = "test_api_key"
        api = type('obj', (object,), {
            'base_url': 'https://api.test.com',
            'timeout': 30,
            'max_retries': 2,
            'retry_delay': 1
        })()
        generation = type('obj', (object,), {
            'default_count': 5,
            'default_seed': 1000,
            'default_aspect_ratio': '2:3',
            'default_output_format': 'jpeg',
            'default_quality': 'standard',
            'default_style': 'realistic'
        })()
        paths = type('obj', (object,), {
            'input_dir': Path('/tmp/input'),
            'output_dir': Path('/tmp/output'),
            'config_dir': Path('/tmp/config')
        })()
        
        def validate(self):
            return True
    
    return MockSettings() 