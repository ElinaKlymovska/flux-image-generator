"""
Character Rotation Generator for FLUX API.

This module provides functionality to generate character images from different angles
and perspectives, creating a 360-degree view of the character.
"""

import time
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from enum import Enum

from ..config.settings import settings
from ..config.prompts import PromptConfig
from ..api.client import FluxAPIClient
from ..api.models import GenerationRequest, GenerationResponse
from ..utils.logger import get_logger
from ..utils.image import ImageUtils

logger = get_logger(__name__)


class RotationAngle(Enum):
    """Predefined rotation angles."""
    FRONT = "front"
    FRONT_LEFT = "front_left"
    LEFT = "left"
    BACK_LEFT = "back_left"
    BACK = "back"
    BACK_RIGHT = "back_right"
    RIGHT = "right"
    FRONT_RIGHT = "front_right"
    THREE_QUARTER_LEFT = "three_quarter_left"
    THREE_QUARTER_RIGHT = "three_quarter_right"
    PROFILE_LEFT = "profile_left"
    PROFILE_RIGHT = "profile_right"


class CharacterRotationGenerator:
    """Generator for character rotation images."""
    
    def __init__(self, output_subdir: str = "rotation", api_key: Optional[str] = None):
        """Initialize rotation generator."""
        self.api_client = FluxAPIClient(api_key)
        self.settings = settings
        self.prompt_config = PromptConfig()
        
        # Validate settings
        self.settings.validate()
        
        # Find input image
        self.input_image = ImageUtils.find_input_image(self.settings.paths.input_dir)
        if not self.input_image:
            raise FileNotFoundError(
                f"Input image not found in {self.settings.paths.input_dir}. "
                "Please place character.jpg in the input directory."
            )
        
        # Setup output directory
        self.output_dir = self.settings.paths.output_dir / output_subdir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Rotation angle configurations
        self.rotation_prompts = self._create_rotation_prompts()
        
        logger.info(f"Initialized rotation generator with output dir: {self.output_dir}")
    
    def _create_rotation_prompts(self) -> Dict[str, Dict[str, str]]:
        """Create rotation-specific prompts."""
        return {
            RotationAngle.FRONT.value: {
                "name": "Front View",
                "prompt": "Front-facing portrait of a woman, direct eye contact, symmetrical composition, professional headshot angle, neutral expression, 8K resolution, perfect lighting from front",
                "description": "Прямий фронтальний ракурс"
            },
            RotationAngle.FRONT_LEFT.value: {
                "name": "Front-Left View",
                "prompt": "Slightly turned left portrait of a woman, gentle head rotation, natural pose, soft lighting, 8K resolution, three-quarter front view",
                "description": "Легкий поворот вліво"
            },
            RotationAngle.LEFT.value: {
                "name": "Left View",
                "prompt": "Left-facing portrait of a woman, head turned 45 degrees left, elegant pose, side lighting, 8K resolution, dynamic composition",
                "description": "Поворот на 45° вліво"
            },
            RotationAngle.BACK_LEFT.value: {
                "name": "Back-Left View",
                "prompt": "Back-left view of a woman, head turned 90 degrees left, elegant neck line, dramatic side lighting, 8K resolution, sophisticated angle",
                "description": "Поворот на 90° вліво"
            },
            RotationAngle.BACK.value: {
                "name": "Back View",
                "prompt": "Back view of a woman, elegant neck and shoulder line, sophisticated back lighting, 8K resolution, artistic rear composition",
                "description": "Вид ззаду"
            },
            RotationAngle.BACK_RIGHT.value: {
                "name": "Back-Right View",
                "prompt": "Back-right view of a woman, head turned 90 degrees right, elegant neck line, dramatic side lighting, 8K resolution, sophisticated angle",
                "description": "Поворот на 90° вправо"
            },
            RotationAngle.RIGHT.value: {
                "name": "Right View",
                "prompt": "Right-facing portrait of a woman, head turned 45 degrees right, elegant pose, side lighting, 8K resolution, dynamic composition",
                "description": "Поворот на 45° вправо"
            },
            RotationAngle.FRONT_RIGHT.value: {
                "name": "Front-Right View",
                "prompt": "Slightly turned right portrait of a woman, gentle head rotation, natural pose, soft lighting, 8K resolution, three-quarter front view",
                "description": "Легкий поворот вправо"
            },
            RotationAngle.THREE_QUARTER_LEFT.value: {
                "name": "Three-Quarter Left",
                "prompt": "Three-quarter left view of a woman, head turned 30 degrees left, classic portrait angle, professional lighting, 8K resolution, timeless composition",
                "description": "Три чверті вліво"
            },
            RotationAngle.THREE_QUARTER_RIGHT.value: {
                "name": "Three-Quarter Right",
                "prompt": "Three-quarter right view of a woman, head turned 30 degrees right, classic portrait angle, professional lighting, 8K resolution, timeless composition",
                "description": "Три чверті вправо"
            },
            RotationAngle.PROFILE_LEFT.value: {
                "name": "Left Profile",
                "prompt": "Left profile portrait of a woman, pure side view, elegant profile line, dramatic side lighting, 8K resolution, classic profile composition",
                "description": "Профіль вліво"
            },
            RotationAngle.PROFILE_RIGHT.value: {
                "name": "Right Profile",
                "prompt": "Right profile portrait of a woman, pure side view, elegant profile line, dramatic side lighting, 8K resolution, classic profile composition",
                "description": "Профіль вправо"
            }
        }
    
    def get_rotation_angles(self) -> List[str]:
        """Get list of available rotation angles."""
        return list(self.rotation_prompts.keys())
    
    def get_rotation_info(self, angle: str) -> Dict[str, str]:
        """Get information about specific rotation angle."""
        if angle not in self.rotation_prompts:
            available = list(self.rotation_prompts.keys())
            raise ValueError(f"Unknown rotation angle: {angle}. Available: {available}")
        return self.rotation_prompts[angle]
    
    def generate_single_rotation(
        self,
        angle: str,
        style: str = "ultra_realistic",
        seed: Optional[int] = None,
        custom_prompt: Optional[str] = None
    ) -> Optional[Path]:
        """Generate a single rotation image."""
        if angle not in self.rotation_prompts:
            available = list(self.rotation_prompts.keys())
            raise ValueError(f"Unknown rotation angle: {angle}. Available: {available}")
        
        seed = seed or self.settings.generation.default_seed
        rotation_info = self.rotation_prompts[angle]
        
        logger.info(f"Generating rotation image: {angle} with seed {seed}")
        
        try:
            # Combine rotation prompt with style
            base_prompt = rotation_info["prompt"]
            style_config = self.prompt_config.get_prompt_config(style, "portrait", "high")
            
            # Use custom prompt or combine rotation with style
            if custom_prompt:
                prompt = f"{custom_prompt}, {rotation_info['prompt']}"
            else:
                prompt = f"{base_prompt}, {style_config['prompt']}"
            
            # Create generation request
            quality_settings = style_config["quality_settings"].copy()
            quality_settings.pop("description", None)
            
            request = GenerationRequest.from_image_file(
                prompt=prompt,
                image_path=self.input_image,
                seed=seed,
                aspect_ratio="2:3",  # Portrait for rotation
                output_format="jpeg",
                **quality_settings
            )
            
            # Generate image
            response = self.api_client.generate_image(request)
            
            if response.success and response.image_data:
                # Generate filename
                filename = ImageUtils.generate_filename(
                    base_name=f"rotation_{angle}",
                    index=0,
                    seed=seed,
                    extension="jpg"
                )
                
                # Save image
                output_path = self.output_dir / filename
                ImageUtils.save_image_data(response.image_data, output_path)
                
                logger.info(f"Generated rotation image saved: {output_path}")
                return output_path
            else:
                logger.error(f"Rotation generation failed: {response.error_message}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating rotation image: {e}")
            return None
    
    def generate_full_rotation(
        self,
        angles: Optional[List[str]] = None,
        style: str = "ultra_realistic",
        start_seed: Optional[int] = None,
        custom_prompt: Optional[str] = None
    ) -> Dict[str, Optional[Path]]:
        """Generate full rotation sequence."""
        angles = angles or list(self.rotation_prompts.keys())
        start_seed = start_seed or self.settings.generation.default_seed
        
        logger.info(f"Starting full rotation generation: {len(angles)} angles")
        
        results = {}
        successful_count = 0
        
        for i, angle in enumerate(angles):
            seed = start_seed + i
            logger.info(f"Generating rotation {i + 1}/{len(angles)}: {angle}")
            
            try:
                output_path = self.generate_single_rotation(
                    angle=angle,
                    style=style,
                    seed=seed,
                    custom_prompt=custom_prompt
                )
                
                results[angle] = output_path
                if output_path:
                    successful_count += 1
                    logger.info(f"Successfully generated rotation: {angle}")
                else:
                    logger.warning(f"Failed to generate rotation: {angle}")
                
                # Small delay between requests
                if i < len(angles) - 1:
                    time.sleep(2)
                    
            except Exception as e:
                logger.error(f"Error in rotation {angle}: {e}")
                results[angle] = None
        
        logger.info(f"Rotation generation completed: {successful_count}/{len(angles)} images generated")
        return results
    
    def generate_rotation_comparison(
        self,
        angles: List[str],
        styles: List[str],
        seed: Optional[int] = None
    ) -> Dict[str, Dict[str, Optional[Path]]]:
        """Generate rotation comparison across multiple styles."""
        logger.info(f"Generating rotation comparison: {len(angles)} angles x {len(styles)} styles")
        
        results = {}
        total_generated = 0
        total_successful = 0
        
        for style in styles:
            results[style] = {}
            logger.info(f"Generating rotations for style: {style}")
            
            for angle in angles:
                try:
                    output_path = self.generate_single_rotation(
                        angle=angle,
                        style=style,
                        seed=seed
                    )
                    
                    results[style][angle] = output_path
                    total_generated += 1
                    if output_path:
                        total_successful += 1
                    
                    # Small delay between requests
                    time.sleep(2)
                    
                except Exception as e:
                    logger.error(f"Error generating {style}/{angle}: {e}")
                    results[style][angle] = None
                    total_generated += 1
        
        logger.info(f"Rotation comparison completed: {total_successful}/{total_generated} images generated")
        return results
    
    def generate_360_degree_sequence(
        self,
        steps: int = 8,
        style: str = "ultra_realistic",
        start_seed: Optional[int] = None,
        custom_prompt: Optional[str] = None
    ) -> List[Optional[Path]]:
        """Generate 360-degree rotation sequence with custom steps."""
        if steps < 4 or steps > 12:
            raise ValueError("Steps must be between 4 and 12")
        
        # Define rotation sequence based on steps
        if steps == 4:
            sequence = ["front", "left", "back", "right"]
        elif steps == 6:
            sequence = ["front", "front_left", "left", "back_left", "back", "right"]
        elif steps == 8:
            sequence = ["front", "front_left", "left", "back_left", "back", "back_right", "right", "front_right"]
        elif steps == 12:
            sequence = list(self.rotation_prompts.keys())
        else:
            # Custom sequence
            sequence = self._create_custom_sequence(steps)
        
        logger.info(f"Generating 360-degree sequence: {steps} steps")
        
        results = []
        start_seed = start_seed or self.settings.generation.default_seed
        
        for i, angle in enumerate(sequence):
            seed = start_seed + i
            logger.info(f"Generating step {i + 1}/{steps}: {angle}")
            
            try:
                output_path = self.generate_single_rotation(
                    angle=angle,
                    style=style,
                    seed=seed,
                    custom_prompt=custom_prompt
                )
                
                results.append(output_path)
                
                # Small delay between requests
                if i < steps - 1:
                    time.sleep(2)
                    
            except Exception as e:
                logger.error(f"Error in step {i + 1}: {e}")
                results.append(None)
        
        successful_count = sum(1 for r in results if r is not None)
        logger.info(f"360-degree sequence completed: {successful_count}/{steps} images generated")
        return results
    
    def _create_custom_sequence(self, steps: int) -> List[str]:
        """Create custom rotation sequence for given number of steps."""
        # Map steps to available angles
        angle_mapping = {
            5: ["front", "front_left", "left", "back", "right"],
            7: ["front", "front_left", "left", "back_left", "back", "right", "front_right"],
            9: ["front", "front_left", "left", "back_left", "back", "back_right", "right", "front_right", "three_quarter_left"],
            10: ["front", "front_left", "left", "back_left", "back", "back_right", "right", "front_right", "three_quarter_left", "three_quarter_right"],
            11: ["front", "front_left", "left", "back_left", "back", "back_right", "right", "front_right", "three_quarter_left", "three_quarter_right", "profile_left"]
        }
        
        return angle_mapping.get(steps, list(self.rotation_prompts.keys())[:steps])
    
    def test_connection(self) -> bool:
        """Test API connection."""
        try:
            return self.api_client.test_connection()
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    def get_input_image_info(self) -> dict:
        """Get information about input image."""
        return ImageUtils.get_image_info(self.input_image) 