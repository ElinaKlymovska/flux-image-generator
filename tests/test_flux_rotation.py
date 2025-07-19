#!/usr/bin/env python3
"""
Test script for FLUX 1.1 [pro] Character Rotation Generator.

This script tests the basic functionality of the FluxProRotationGenerator class.
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch, mock_open

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Import the generator class
sys.path.insert(0, str(Path(__file__).parent.parent / "bin"))
from generate_flux_rotation import FluxProRotationGenerator


class TestFluxProRotationGenerator(unittest.TestCase):
    """Test cases for FluxProRotationGenerator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.api_key = "test_api_key"
        self.output_dir = "test_output"
        self.generator = FluxProRotationGenerator(
            api_key=self.api_key,
            output_dir=self.output_dir
        )
    
    def test_init(self):
        """Test generator initialization."""
        self.assertEqual(self.generator.api_key, self.api_key)
        self.assertEqual(self.generator.api_endpoint, "https://api.flux.run/generate/flux-1.1-pro-ultra")
        self.assertEqual(self.generator.output_dir, Path(self.output_dir))
        self.assertEqual(self.generator.headers["x-key"], self.api_key)
        self.assertEqual(self.generator.headers["Content-Type"], "application/json")
    
    def test_encode_image(self):
        """Test image encoding functionality."""
        # Create a mock image file
        mock_image_path = Path("test_image.jpg")
        mock_image_data = b"fake_image_data"
        
        with patch("builtins.open", mock_open(read_data=mock_image_data)):
            with patch("pathlib.Path.exists", return_value=True):
                encoded = self.generator.encode_image(mock_image_path)
                
                self.assertTrue(encoded.startswith("data:image/jpeg;base64,"))
                # The base64 part should be the encoded mock data
                import base64
                expected_encoded = base64.b64encode(mock_image_data).decode("utf-8")
                self.assertIn(expected_encoded, encoded)
    
    def test_encode_image_not_found(self):
        """Test image encoding with non-existent file."""
        mock_image_path = Path("nonexistent.jpg")
        
        with patch("pathlib.Path.exists", return_value=False):
            with self.assertRaises(FileNotFoundError):
                self.generator.encode_image(mock_image_path)
    
    def test_create_rotation_prompt(self):
        """Test prompt creation for different angles."""
        # Test 0 degrees
        prompt_0 = self.generator.create_rotation_prompt(0)
        self.assertIn("facing forward", prompt_0)
        
        # Test 45 degrees
        prompt_45 = self.generator.create_rotation_prompt(45)
        self.assertIn("rotated 45 degrees to the right", prompt_45)
        
        # Test 90 degrees
        prompt_90 = self.generator.create_rotation_prompt(90)
        self.assertIn("facing 90 degrees to the right", prompt_90)
        
        # Test 180 degrees
        prompt_180 = self.generator.create_rotation_prompt(180)
        self.assertIn("facing away, back turned", prompt_180)
        
        # All prompts should contain key elements
        for prompt in [prompt_0, prompt_45, prompt_90, prompt_180]:
            self.assertIn("realistic portrait", prompt)
            self.assertIn("same woman", prompt)
            self.assertIn("ultra realistic", prompt)
            self.assertIn("studio lighting", prompt)
    
    @patch('requests.post')
    def test_test_connection_success(self, mock_post):
        """Test successful API connection test."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        result = self.generator.test_connection()
        self.assertTrue(result)
        
        # Verify the request was made correctly
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertEqual(call_args[0][0], self.generator.api_endpoint)
        self.assertEqual(call_args[1]['headers'], self.generator.headers)
    
    @patch('requests.post')
    def test_test_connection_failure(self, mock_post):
        """Test failed API connection test."""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_post.return_value = mock_response
        
        result = self.generator.test_connection()
        self.assertFalse(result)
    
    @patch('requests.post')
    def test_generate_rotation_image_success(self, mock_post):
        """Test successful image generation."""
        # Mock the API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "polling_url": "https://api.flux.run/poll/123"
        }
        mock_post.return_value = mock_response
        
        # Mock the polling response
        with patch.object(self.generator, 'poll_generation_status') as mock_poll:
            mock_poll.return_value = {
                "result": {
                    "image_url": "https://example.com/image.jpg"
                }
            }
            
            # Mock the download
            with patch.object(self.generator, 'download_image') as mock_download:
                mock_download.return_value = b"fake_image_data"
                
                # Mock the image encoding
                with patch.object(self.generator, 'encode_image') as mock_encode:
                    mock_encode.return_value = "data:image/jpeg;base64,fake"
                    
                    result = self.generator.generate_rotation_image(
                        angle=45,
                        input_image_path=Path("test.jpg"),
                        seed=123456
                    )
                    
                    self.assertEqual(result, b"fake_image_data")
    
    def test_generate_all_rotations(self):
        """Test generating all rotations."""
        angles = [10, 45, 90]
        input_path = Path("test.jpg")
        seed = 123456
        
        # Mock the generate_rotation_image method
        with patch.object(self.generator, 'generate_rotation_image') as mock_generate:
            mock_generate.side_effect = [
                b"image_data_1",  # 10 degrees
                None,             # 45 degrees (failed)
                b"image_data_3"   # 90 degrees
            ]
            
            # Mock file operations
            with patch("builtins.open", mock_open()):
                results = self.generator.generate_all_rotations(
                    angles=angles,
                    input_image_path=input_path,
                    seed=seed
                )
                
                # Check results
                self.assertEqual(len(results), 3)
                self.assertIsNotNone(results[10])
                self.assertIsNone(results[45])
                self.assertIsNotNone(results[90])
                
                # Verify generate_rotation_image was called for each angle
                self.assertEqual(mock_generate.call_count, 3)


if __name__ == "__main__":
    # Run tests
    unittest.main(verbosity=2) 