"""
Prompt Tester for FLUX Image Generator.

This module provides automated testing of different prompts with character rotation.
"""

import time
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

from ..config.settings import settings
from ..api.client import FluxAPIClient
from ..api.models import GenerationRequest, GenerationResponse
from ..utils.logger import get_logger
from ..utils.image import ImageUtils

logger = get_logger(__name__)


class PromptTester:
    """Automated prompt testing with character rotation."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize prompt tester."""
        self.api_client = FluxAPIClient(api_key)
        self.settings = settings
        
        # Validate settings
        self.settings.validate()
        
        # Find input image
        self.input_image = ImageUtils.find_input_image(self.settings.paths.input_dir)
        if not self.input_image:
            raise FileNotFoundError(
                f"Input image not found in {self.settings.paths.input_dir}. "
                "Please place character.jpg in the input directory."
            )
        
        # Setup datasets directory
        self.datasets_dir = self.settings.paths.output_dir / "datasets"
        self.datasets_dir.mkdir(parents=True, exist_ok=True)
        
        # Test prompts
        self.test_prompts = [
            "ultra-realistic portrait of a woman, soft natural lighting, neutral background, high quality, detailed facial features, professional photography, 8k resolution",
            "cinematic portrait of a woman, dramatic lighting, shallow depth of field, film grain, professional cinematography, moody atmosphere, high contrast, golden hour",
            "artistic portrait of a woman, painterly style, soft brushstrokes, artistic lighting, creative composition, masterpiece quality, fine art photography, oil painting effect",
            "fashion portrait of a woman, studio lighting, professional makeup, elegant pose, high fashion photography, magazine quality, sophisticated style, editorial look",
            "vintage portrait of a woman, retro style, film photography, warm tones, nostalgic atmosphere, classic beauty, timeless elegance, 1950s aesthetic",
            "modern portrait of a woman, contemporary style, clean composition, minimalist background, sharp details, professional headshot quality, urban aesthetic",
            "dramatic portrait of a woman, intense lighting, strong shadows, emotional expression, powerful composition, artistic photography, chiaroscuro lighting",
            "soft dreamy portrait of a woman, gentle lighting, soft focus, ethereal atmosphere, romantic mood, delicate beauty, pastel tones, bokeh background",
            "professional corporate portrait of a woman, business attire, clean background, confident expression, executive headshot, modern office setting, professional lighting",
            "creative artistic portrait of a woman, abstract background, artistic composition, creative lighting, modern art style, contemporary photography, experimental",
            "elegant sophisticated portrait of a woman, luxury setting, refined beauty, high-end fashion, premium quality, sophisticated lighting, exclusive atmosphere",
            "natural outdoor portrait of a woman, natural lighting, outdoor setting, environmental portrait, nature background, organic beauty, environmental photography",
            "studio professional portrait of a woman, controlled lighting, studio background, professional equipment, commercial photography, advertising quality",
            "expressive character portrait of a woman, strong personality, character study, emotional depth, psychological portrait, human interest, documentary style",
            "contemporary urban portrait of a woman, city background, modern lifestyle, urban aesthetic, street photography style, contemporary culture, metropolitan"
        ]
        
        # Rotation angles
        self.rotation_angles = [0, 10, 30, 45, 60, 90, 180]
        
        logger.info(f"Initialized prompt tester with {len(self.test_prompts)} test prompts")
    
    def create_generation_request(
        self, 
        prompt: str, 
        seed: int, 
        rotation: int = 0
    ) -> GenerationRequest:
        """Create generation request with rotation."""
        # Add rotation information to prompt
        rotation_prompt = ""
        if rotation > 0:
            rotation_prompt = f", rotated {rotation} degrees, different angle view"
        
        full_prompt = prompt + rotation_prompt
        
        return GenerationRequest.from_image_file(
            prompt=full_prompt,
            image_path=self.input_image,
            seed=seed,
            aspect_ratio="2:3",
            output_format="jpeg",
            prompt_upsampling=True,
            safety_tolerance=2
        )
    
    def create_dataset_folder(self, prompt_name: str) -> Path:
        """Create dataset folder for prompt."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = f"{prompt_name}_{timestamp}"
        dataset_path = self.datasets_dir / folder_name
        dataset_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Created dataset folder: {dataset_path}")
        return dataset_path
    
    def generate_single_image(
        self, 
        prompt: str, 
        rotation: int, 
        seed: int, 
        dataset_path: Path
    ) -> Optional[Path]:
        """Generate a single test image."""
        try:
            # Create request
            request = self.create_generation_request(prompt, seed, rotation)
            
            # Generate image
            response = self.api_client.generate_image(request)
            
            if response.success and response.image_data:
                # Generate filename
                filename = f"test_{seed:04d}_rot{rotation:03d}.jpg"
                output_path = dataset_path / filename
                
                # Save image
                ImageUtils.save_image_data(response.image_data, output_path)
                
                logger.info(f"Generated test image: {output_path}")
                return output_path
            else:
                logger.error(f"Generation failed: {response.error_message}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating test image: {e}")
            return None
    
    def test_prompt(self, prompt: str, count: int = 1) -> List[Path]:
        """Test a single prompt with all rotations."""
        logger.info(f"Testing prompt: {prompt[:50]}...")
        
        # Create dataset folder
        prompt_name = f"prompt_{hash(prompt) % 10000:04d}"
        dataset_path = self.create_dataset_folder(prompt_name)
        
        generated_images = []
        successful_count = 0
        
        for rotation in self.rotation_angles:
            for i in range(count):
                seed = 1000 + i
                
                logger.info(f"Generating rotation {rotation}°, image {i + 1}/{count}")
                
                output_path = self.generate_single_image(prompt, rotation, seed, dataset_path)
                
                if output_path:
                    generated_images.append(output_path)
                    successful_count += 1
                
                # Small delay between requests
                time.sleep(2)
        
        logger.info(f"Prompt test completed: {successful_count} images generated")
        return generated_images
    
    def test_all_prompts(self, images_per_prompt: int = 1) -> Dict[str, List[Path]]:
        """Test all prompts."""
        logger.info(f"Testing all {len(self.test_prompts)} prompts")
        
        results = {}
        total_generated = 0
        
        for i, prompt in enumerate(self.test_prompts, 1):
            logger.info(f"Testing prompt {i}/{len(self.test_prompts)}")
            
            images = self.test_prompt(prompt, count=images_per_prompt)
            results[f"prompt_{i:02d}"] = images
            total_generated += len(images)
            
            logger.info(f"Generated {len(images)} images for prompt {i}")
        
        logger.info(f"All prompts tested: {total_generated} total images generated")
        return results
    
    def test_connection(self) -> bool:
        """Test API connection."""
        try:
            return self.api_client.test_connection()
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False 