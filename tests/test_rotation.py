"""
Tests for Character Rotation Generator.

This module contains tests for the rotation functionality.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from flux_generator.core.rotation import CharacterRotationGenerator, RotationAngle
from flux_generator.api.models import GenerationResponse


class TestRotationAngle:
    """Test RotationAngle enum."""
    
    def test_rotation_angles(self):
        """Test that all rotation angles are available."""
        angles = [angle.value for angle in RotationAngle]
        expected_angles = [
            "front", "front_left", "left", "back_left", "back",
            "back_right", "right", "front_right", "three_quarter_left",
            "three_quarter_right", "profile_left", "profile_right"
        ]
        
        assert len(angles) == len(expected_angles)
        for angle in expected_angles:
            assert angle in angles


class TestCharacterRotationGenerator:
    """Test CharacterRotationGenerator class."""
    
    @pytest.fixture
    def mock_api_client(self):
        """Mock API client."""
        mock_client = Mock()
        mock_client.test_connection.return_value = True
        
        # Mock successful generation response
        mock_response = Mock(spec=GenerationResponse)
        mock_response.success = True
        mock_response.image_data = b"fake_image_data"
        mock_response.error_message = None
        mock_client.generate_image.return_value = mock_response
        
        return mock_client
    
    @pytest.fixture
    def mock_input_image(self, tmp_path):
        """Create mock input image."""
        input_dir = tmp_path / "input"
        input_dir.mkdir()
        input_image = input_dir / "character.jpg"
        input_image.write_bytes(b"fake_input_image")
        return input_image
    
    @pytest.fixture
    def generator(self, mock_api_client, mock_input_image, tmp_path):
        """Create generator instance with mocked dependencies."""
        with patch('flux_generator.core.rotation.FluxAPIClient', return_value=mock_api_client):
            with patch('flux_generator.core.rotation.ImageUtils.find_input_image', return_value=mock_input_image):
                with patch('flux_generator.core.rotation.settings') as mock_settings:
                    mock_settings.paths.input_dir = mock_input_image.parent
                    mock_settings.paths.output_dir = tmp_path / "output"
                    mock_settings.generation.default_seed = 1001
                    mock_settings.validate.return_value = None
                    
                    generator = CharacterRotationGenerator(output_subdir="test_rotation")
                    generator.api_client = mock_api_client
                    return generator
    
    def test_initialization(self, generator):
        """Test generator initialization."""
        assert generator is not None
        assert hasattr(generator, 'rotation_prompts')
        assert len(generator.rotation_prompts) > 0
    
    def test_get_rotation_angles(self, generator):
        """Test getting available rotation angles."""
        angles = generator.get_rotation_angles()
        assert isinstance(angles, list)
        assert len(angles) > 0
        assert "front" in angles
        assert "left" in angles
        assert "right" in angles
        assert "back" in angles
    
    def test_get_rotation_info(self, generator):
        """Test getting rotation angle information."""
        info = generator.get_rotation_info("front")
        assert isinstance(info, dict)
        assert "name" in info
        assert "prompt" in info
        assert "description" in info
        assert info["name"] == "Front View"
    
    def test_get_rotation_info_invalid(self, generator):
        """Test getting rotation info for invalid angle."""
        with pytest.raises(ValueError, match="Unknown rotation angle"):
            generator.get_rotation_info("invalid_angle")
    
    def test_test_connection(self, generator):
        """Test connection testing."""
        result = generator.test_connection()
        assert result is True
        generator.api_client.test_connection.assert_called_once()
    
    def test_generate_single_rotation(self, generator):
        """Test single rotation generation."""
        with patch('flux_generator.core.rotation.ImageUtils.save_image_data'):
            with patch('flux_generator.core.rotation.ImageUtils.generate_filename', return_value="test_image.jpg"):
                result = generator.generate_single_rotation("front", "ultra_realistic", 1001)
                
                assert result is not None
                assert isinstance(result, Path)
                generator.api_client.generate_image.assert_called_once()
    
    def test_generate_single_rotation_invalid_angle(self, generator):
        """Test single rotation generation with invalid angle."""
        with pytest.raises(ValueError, match="Unknown rotation angle"):
            generator.generate_single_rotation("invalid_angle")
    
    def test_generate_full_rotation(self, generator):
        """Test full rotation generation."""
        angles = ["front", "left", "right"]
        
        with patch('flux_generator.core.rotation.ImageUtils.save_image_data'):
            with patch('flux_generator.core.rotation.ImageUtils.generate_filename', return_value="test_image.jpg"):
                with patch('flux_generator.core.rotation.time.sleep'):  # Mock sleep
                    results = generator.generate_full_rotation(angles, "ultra_realistic", 1001)
                    
                    assert isinstance(results, dict)
                    assert len(results) == len(angles)
                    assert all(angle in results for angle in angles)
                    assert all(isinstance(path, Path) for path in results.values() if path is not None)
    
    def test_generate_360_degree_sequence(self, generator):
        """Test 360-degree sequence generation."""
        with patch('flux_generator.core.rotation.ImageUtils.save_image_data'):
            with patch('flux_generator.core.rotation.ImageUtils.generate_filename', return_value="test_image.jpg"):
                with patch('flux_generator.core.rotation.time.sleep'):  # Mock sleep
                    results = generator.generate_360_degree_sequence(steps=4, style="ultra_realistic", start_seed=1001)
                    
                    assert isinstance(results, list)
                    assert len(results) == 4
                    assert all(isinstance(path, Path) for path in results if path is not None)
    
    def test_generate_360_degree_sequence_invalid_steps(self, generator):
        """Test 360-degree sequence with invalid steps."""
        with pytest.raises(ValueError, match="Steps must be between 4 and 12"):
            generator.generate_360_degree_sequence(steps=3)
        
        with pytest.raises(ValueError, match="Steps must be between 4 and 12"):
            generator.generate_360_degree_sequence(steps=13)
    
    def test_generate_rotation_comparison(self, generator):
        """Test rotation comparison generation."""
        angles = ["front", "left"]
        styles = ["ultra_realistic", "cinematic"]
        
        with patch('flux_generator.core.rotation.ImageUtils.save_image_data'):
            with patch('flux_generator.core.rotation.ImageUtils.generate_filename', return_value="test_image.jpg"):
                with patch('flux_generator.core.rotation.time.sleep'):  # Mock sleep
                    results = generator.generate_rotation_comparison(angles, styles, 1001)
                    
                    assert isinstance(results, dict)
                    assert len(results) == len(styles)
                    for style in styles:
                        assert style in results
                        assert len(results[style]) == len(angles)
    
    def test_custom_sequence_creation(self, generator):
        """Test custom sequence creation."""
        # Test 5 steps
        sequence = generator._create_custom_sequence(5)
        assert len(sequence) == 5
        assert "front" in sequence
        assert "left" in sequence
        assert "back" in sequence
        assert "right" in sequence
    
    def test_generation_failure_handling(self, generator):
        """Test handling of generation failures."""
        # Mock failed response
        failed_response = Mock(spec=GenerationResponse)
        failed_response.success = False
        failed_response.image_data = None
        failed_response.error_message = "Generation failed"
        generator.api_client.generate_image.return_value = failed_response
        
        with patch('flux_generator.core.rotation.ImageUtils.save_image_data'):
            with patch('flux_generator.core.rotation.ImageUtils.generate_filename', return_value="test_image.jpg"):
                result = generator.generate_single_rotation("front")
                
                assert result is None
    
    def test_api_exception_handling(self, generator):
        """Test handling of API exceptions."""
        generator.api_client.generate_image.side_effect = Exception("API Error")
        
        with patch('flux_generator.core.rotation.ImageUtils.save_image_data'):
            with patch('flux_generator.core.rotation.ImageUtils.generate_filename', return_value="test_image.jpg"):
                result = generator.generate_single_rotation("front")
                
                assert result is None
    
    def test_preset_functionality(self, generator):
        """Test preset-related functionality."""
        # Test getting available presets
        presets = generator.get_available_presets()
        assert isinstance(presets, list)
        assert len(presets) > 0
        
        # Check that presets have required structure
        for preset in presets:
            assert "key" in preset
            assert "name" in preset
            assert isinstance(preset["key"], str)
            assert isinstance(preset["name"], str)
        
        # Test getting preset info
        preset_info = generator.get_preset_info("rotation_front")
        assert isinstance(preset_info, dict)
        assert "prompt" in preset_info
        assert "preset_name" in preset_info
        assert "description" in preset_info
        assert "use_case" in preset_info
        assert "technical_specs" in preset_info
    
    def test_rotation_prompts_with_presets(self, generator):
        """Test that rotation prompts include preset information."""
        for angle, prompt_info in generator.rotation_prompts.items():
            assert "preset" in prompt_info
            assert isinstance(prompt_info["preset"], str)
            assert prompt_info["preset"].startswith("rotation_")
    
    def test_character_consistent_rotation(self, generator):
        """Test character-consistent rotation generation."""
        angles = ["front", "left"]
        
        with patch('flux_generator.core.rotation.ImageUtils.save_image_data'):
            with patch('flux_generator.core.rotation.ImageUtils.generate_filename', return_value="test_image.jpg"):
                with patch('flux_generator.core.rotation.time.sleep'):  # Mock sleep
                    results = generator.generate_character_consistent_rotation(
                        angles=angles,
                        base_prompt="portrait of a woman with brown hair",
                        use_presets=True
                    )
                    
                    assert isinstance(results, dict)
                    assert len(results) == len(angles)
                    assert all(angle in results for angle in angles)
    
    def test_generate_rotation_with_preset(self, generator):
        """Test rotation generation with specific preset."""
        with patch('flux_generator.core.rotation.ImageUtils.save_image_data'):
            with patch('flux_generator.core.rotation.ImageUtils.generate_filename', return_value="test_image.jpg"):
                result = generator.generate_rotation_with_preset(
                    angle="front",
                    preset="rotation_front",
                    custom_prompt="portrait of a woman",
                    seed=1001
                )
                
                assert result is not None
                assert isinstance(result, Path)
                generator.api_client.generate_image.assert_called_once()
    
    def test_generate_rotation_with_custom_preset(self, generator):
        """Test rotation generation with custom preset."""
        with patch('flux_generator.core.rotation.ImageUtils.save_image_data'):
            with patch('flux_generator.core.rotation.ImageUtils.generate_filename', return_value="test_image.jpg"):
                result = generator.generate_rotation_with_custom_preset(
                    angle="front",
                    preset="rotation_front",
                    custom_prompt="portrait of a woman in red dress",
                    seed=1001
                )
                
                assert result is not None
                assert isinstance(result, Path)
    
    def test_full_rotation_with_presets(self, generator):
        """Test full rotation generation with presets enabled."""
        angles = ["front", "left", "right"]
        
        with patch('flux_generator.core.rotation.ImageUtils.save_image_data'):
            with patch('flux_generator.core.rotation.ImageUtils.generate_filename', return_value="test_image.jpg"):
                with patch('flux_generator.core.rotation.time.sleep'):  # Mock sleep
                    results = generator.generate_full_rotation(
                        angles=angles,
                        custom_prompt="portrait of a woman",
                        use_presets=True
                    )
                    
                    assert isinstance(results, dict)
                    assert len(results) == len(angles)
                    assert all(angle in results for angle in angles)
    
    def test_full_rotation_without_presets(self, generator):
        """Test full rotation generation with presets disabled."""
        angles = ["front", "left", "right"]
        
        with patch('flux_generator.core.rotation.ImageUtils.save_image_data'):
            with patch('flux_generator.core.rotation.ImageUtils.generate_filename', return_value="test_image.jpg"):
                with patch('flux_generator.core.rotation.time.sleep'):  # Mock sleep
                    results = generator.generate_full_rotation(
                        angles=angles,
                        style="ultra_realistic",
                        custom_prompt="portrait of a woman",
                        use_presets=False
                    )
                    
                    assert isinstance(results, dict)
                    assert len(results) == len(angles)
                    assert all(angle in results for angle in angles) 
    
    def test_rotation_prompts_structure(self, generator):
        """Test that rotation prompts have correct structure."""
        for angle, prompt_info in generator.rotation_prompts.items():
            assert isinstance(angle, str)
            assert isinstance(prompt_info, dict)
            assert "name" in prompt_info
            assert "prompt" in prompt_info
            assert "description" in prompt_info
            assert isinstance(prompt_info["name"], str)
            assert isinstance(prompt_info["prompt"], str)
            assert isinstance(prompt_info["description"], str)
    
    def test_rotation_prompts_content(self, generator):
        """Test that rotation prompts contain expected content."""
        # Check specific angles
        front_info = generator.rotation_prompts["front"]
        assert "Front" in front_info["name"]
        assert "front-facing" in front_info["prompt"].lower()
        
        left_info = generator.rotation_prompts["left"]
        assert "Left" in left_info["name"]
        assert "left" in left_info["prompt"].lower()
        
        back_info = generator.rotation_prompts["back"]
        assert "Back" in back_info["name"]
        assert "back" in back_info["prompt"].lower() 