"""
Tests for Adetailer integration.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from src.flux_generator.core.adetailer import AdetailerGenerator, AdetailerSettings
from src.flux_generator.api.models import GenerationResponse


class TestAdetailerSettings:
    """Test AdetailerSettings class."""
    
    def test_default_settings(self):
        """Test default Adetailer settings."""
        settings = AdetailerSettings()
        
        assert settings.enabled is True
        assert settings.model == "face_yolov8n.pt"
        assert settings.confidence == 0.3
        assert settings.dilation == 4
        assert settings.denoising_strength == 0.4
        assert "beautiful face" in settings.prompt
        assert "blurry" in settings.negative_prompt
        assert settings.steps == 20
        assert settings.cfg_scale == 7.0
        assert settings.sampler == "DPM++ 2M Karras"
        assert settings.width == 512
        assert settings.height == 512


class TestAdetailerGenerator:
    """Test AdetailerGenerator class."""
    
    @pytest.fixture
    def mock_api_client(self):
        """Mock API client."""
        mock_client = Mock()
        mock_client.test_connection.return_value = True
        return mock_client
    
    @pytest.fixture
    def mock_settings(self):
        """Mock settings."""
        mock_settings = Mock()
        mock_settings.validate.return_value = True
        mock_settings.paths.input_dir = Path("data/input")
        mock_settings.paths.output_dir = Path("data/output")
        return mock_settings
    
    @pytest.fixture
    def mock_prompt_config(self):
        """Mock prompt config."""
        mock_config = Mock()
        mock_config.PROMPTS = {
            "ultra_realistic": {"prompt": "test prompt"}
        }
        return mock_config
    
    @patch('src.flux_generator.core.adetailer.ImageUtils')
    @patch('src.flux_generator.core.adetailer.settings')
    @patch('src.flux_generator.core.adetailer.PromptConfig')
    @patch('src.flux_generator.core.adetailer.FluxAPIClient')
    def test_init_success(
        self, 
        mock_api_client_class, 
        mock_prompt_config_class, 
        mock_settings, 
        mock_image_utils
    ):
        """Test successful initialization."""
        # Setup mocks
        mock_api_client_class.return_value = Mock()
        mock_prompt_config_class.return_value = Mock()
        mock_image_utils.find_input_image.return_value = Path("data/input/character.jpg")
        
        # Create generator
        generator = AdetailerGenerator()
        
        # Assertions
        assert generator.api_client is not None
        assert generator.settings is not None
        assert generator.prompt_config is not None
        assert generator.adetailer_settings is not None
        assert isinstance(generator.adetailer_settings, AdetailerSettings)
    
    @patch('src.flux_generator.core.adetailer.ImageUtils')
    @patch('src.flux_generator.core.adetailer.settings')
    @patch('src.flux_generator.core.adetailer.PromptConfig')
    @patch('src.flux_generator.core.adetailer.FluxAPIClient')
    def test_init_no_input_image(
        self, 
        mock_api_client_class, 
        mock_prompt_config_class, 
        mock_settings, 
        mock_image_utils
    ):
        """Test initialization with no input image."""
        # Setup mocks
        mock_api_client_class.return_value = Mock()
        mock_prompt_config_class.return_value = Mock()
        mock_image_utils.find_input_image.return_value = None
        
        # Test that FileNotFoundError is raised
        with pytest.raises(FileNotFoundError):
            AdetailerGenerator()
    
    @patch('src.flux_generator.core.adetailer.ImageUtils')
    @patch('src.flux_generator.core.adetailer.settings')
    @patch('src.flux_generator.core.adetailer.PromptConfig')
    @patch('src.flux_generator.core.adetailer.FluxAPIClient')
    def test_generate_with_adetailer_success(
        self, 
        mock_api_client_class, 
        mock_prompt_config_class, 
        mock_settings, 
        mock_image_utils
    ):
        """Test successful generation with Adetailer."""
        # Setup mocks
        mock_client = Mock()
        mock_client.generate_image.return_value = GenerationResponse.success_response(
            image_data=b"fake_image_data"
        )
        mock_api_client_class.return_value = mock_client
        
        mock_prompt_config = Mock()
        mock_prompt_config.PROMPTS = {
            "ultra_realistic": {"prompt": "test prompt"}
        }
        mock_prompt_config_class.return_value = mock_prompt_config
        
        mock_image_utils.find_input_image.return_value = Path("data/input/character.jpg")
        mock_image_utils.generate_filename.return_value = "test_image.jpg"
        mock_image_utils.save_image_data.return_value = None
        
        # Create generator
        generator = AdetailerGenerator()
        
        # Test generation
        result = generator.generate_with_adetailer()
        
        # Assertions
        assert result is not None
        assert isinstance(result, Path)
    
    @patch('src.flux_generator.core.adetailer.ImageUtils')
    @patch('src.flux_generator.core.adetailer.settings')
    @patch('src.flux_generator.core.adetailer.PromptConfig')
    @patch('src.flux_generator.core.adetailer.FluxAPIClient')
    def test_generate_with_adetailer_failure(
        self, 
        mock_api_client_class, 
        mock_prompt_config_class, 
        mock_settings, 
        mock_image_utils
    ):
        """Test generation failure with Adetailer."""
        # Setup mocks
        mock_client = Mock()
        mock_client.generate_image.return_value = GenerationResponse.error_response(
            "Generation failed"
        )
        mock_api_client_class.return_value = mock_client
        
        mock_prompt_config = Mock()
        mock_prompt_config.PROMPTS = {
            "ultra_realistic": {"prompt": "test prompt"}
        }
        mock_prompt_config_class.return_value = mock_prompt_config
        
        mock_image_utils.find_input_image.return_value = Path("data/input/character.jpg")
        
        # Create generator
        generator = AdetailerGenerator()
        
        # Test generation
        result = generator.generate_with_adetailer()
        
        # Assertions
        assert result is None
    
    @patch('src.flux_generator.core.adetailer.ImageUtils')
    @patch('src.flux_generator.core.adetailer.settings')
    @patch('src.flux_generator.core.adetailer.PromptConfig')
    @patch('src.flux_generator.core.adetailer.FluxAPIClient')
    def test_update_adetailer_settings(
        self, 
        mock_api_client_class, 
        mock_prompt_config_class, 
        mock_settings, 
        mock_image_utils
    ):
        """Test updating Adetailer settings."""
        # Setup mocks
        mock_api_client_class.return_value = Mock()
        mock_prompt_config_class.return_value = Mock()
        mock_image_utils.find_input_image.return_value = Path("data/input/character.jpg")
        
        # Create generator
        generator = AdetailerGenerator()
        
        # Update settings
        generator.update_adetailer_settings(
            confidence=0.5,
            denoising_strength=0.6,
            steps=30
        )
        
        # Assertions
        assert generator.adetailer_settings.confidence == 0.5
        assert generator.adetailer_settings.denoising_strength == 0.6
        assert generator.adetailer_settings.steps == 30
    
    @patch('src.flux_generator.core.adetailer.ImageUtils')
    @patch('src.flux_generator.core.adetailer.settings')
    @patch('src.flux_generator.core.adetailer.PromptConfig')
    @patch('src.flux_generator.core.adetailer.FluxAPIClient')
    def test_test_connection(
        self, 
        mock_api_client_class, 
        mock_prompt_config_class, 
        mock_settings, 
        mock_image_utils
    ):
        """Test connection testing."""
        # Setup mocks
        mock_client = Mock()
        mock_client.test_connection.return_value = True
        mock_api_client_class.return_value = mock_client
        
        mock_prompt_config_class.return_value = Mock()
        mock_image_utils.find_input_image.return_value = Path("data/input/character.jpg")
        
        # Create generator
        generator = AdetailerGenerator()
        
        # Test connection
        result = generator.test_connection()
        
        # Assertions
        assert result is True
        mock_client.test_connection.assert_called_once()
    
    @patch('src.flux_generator.core.adetailer.ImageUtils')
    @patch('src.flux_generator.core.adetailer.settings')
    @patch('src.flux_generator.core.adetailer.PromptConfig')
    @patch('src.flux_generator.core.adetailer.FluxAPIClient')
    def test_get_input_image_info(
        self, 
        mock_api_client_class, 
        mock_prompt_config_class, 
        mock_settings, 
        mock_image_utils
    ):
        """Test getting input image info."""
        # Setup mocks
        mock_api_client_class.return_value = Mock()
        mock_prompt_config_class.return_value = Mock()
        mock_image_utils.find_input_image.return_value = Path("data/input/character.jpg")
        mock_image_utils.get_image_info.return_value = {
            'path': 'data/input/character.jpg',
            'width': 512,
            'height': 768,
            'format': 'JPEG'
        }
        
        # Create generator
        generator = AdetailerGenerator()
        
        # Get image info
        result = generator.get_input_image_info()
        
        # Assertions
        assert result['path'] == 'data/input/character.jpg'
        assert result['width'] == 512
        assert result['height'] == 768
        assert result['format'] == 'JPEG'
        mock_image_utils.get_image_info.assert_called_once()


if __name__ == '__main__':
    pytest.main([__file__]) 