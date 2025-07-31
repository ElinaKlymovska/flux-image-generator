"""
Character Rotation Generator for FLUX API.

This module provides functionality to generate character images from different angles
and perspectives, creating a 360-degree view of the character.
"""

import time
from pathlib import Path
from typing import Optional, List, Dict, Any
from enum import Enum

from .base import BaseGenerator
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


class CharacterRotationGenerator(BaseGenerator):
    """Generator for character rotation images."""
    
    def __init__(self, output_subdir: str = "rotation", api_key: Optional[str] = None):
        """Initialize rotation generator."""
        super().__init__(output_subdir=output_subdir, api_key=api_key)
        
        # Rotation angle configurations
        self.rotation_prompts = self._create_rotation_prompts()
        
        logger.info(f"Rotation generator initialized with {len(self.rotation_prompts)} rotation angles")
    
    def _create_rotation_prompts(self) -> Dict[str, Dict[str, str]]:
        """Create rotation-specific prompts using Black Forest Labs best practices."""
        return {
            RotationAngle.FRONT.value: {
                "name": "Front View",
                "prompt": "Front-facing portrait of a woman, direct eye contact, symmetrical composition, professional headshot angle, neutral expression, 8K resolution, perfect lighting from front, maintain exact facial features, eye color, hairstyle, and distinctive characteristics while preserving identity",
                "description": "Прямий фронтальний ракурс з збереженням ідентичності",
                "preset": "rotation_front"
            },
            RotationAngle.FRONT_LEFT.value: {
                "name": "Front-Left View",
                "prompt": "Slightly turned left portrait of a woman, gentle head rotation, natural pose, soft lighting, 8K resolution, three-quarter front view, maintain exact facial features, eye color, hairstyle, and distinctive characteristics while preserving identity",
                "description": "Легкий поворот вліво з збереженням ідентичності",
                "preset": "rotation_three_quarter_left"
            },
            RotationAngle.LEFT.value: {
                "name": "Left View",
                "prompt": "Left-facing portrait of a woman, head turned 45 degrees left, elegant pose, side lighting, 8K resolution, dynamic composition, maintain exact facial features, hairstyle, and distinctive characteristics while preserving identity",
                "description": "Поворот на 45° вліво з збереженням ідентичності",
                "preset": "rotation_left"
            },
            RotationAngle.BACK_LEFT.value: {
                "name": "Back-Left View",
                "prompt": "Back-left view of a woman, head turned 90 degrees left, elegant neck line, dramatic side lighting, 8K resolution, sophisticated angle, maintain exact hairstyle and distinctive features from behind",
                "description": "Поворот на 90° вліво з збереженням характерних рис",
                "preset": "rotation_back"
            },
            RotationAngle.BACK.value: {
                "name": "Back View",
                "prompt": "Back view of a woman, elegant neck and shoulder line, sophisticated back lighting, 8K resolution, artistic rear composition, maintain exact hairstyle and distinctive features from behind",
                "description": "Вид ззаду з збереженням характерних рис",
                "preset": "rotation_back"
            },
            RotationAngle.BACK_RIGHT.value: {
                "name": "Back-Right View",
                "prompt": "Back-right view of a woman, head turned 90 degrees right, elegant neck line, dramatic side lighting, 8K resolution, sophisticated angle, maintain exact hairstyle and distinctive features from behind",
                "description": "Поворот на 90° вправо з збереженням характерних рис",
                "preset": "rotation_back"
            },
            RotationAngle.RIGHT.value: {
                "name": "Right View",
                "prompt": "Right-facing portrait of a woman, head turned 45 degrees right, elegant pose, side lighting, 8K resolution, dynamic composition, maintain exact facial features, hairstyle, and distinctive characteristics while preserving identity",
                "description": "Поворот на 45° вправо з збереженням ідентичності",
                "preset": "rotation_right"
            },
            RotationAngle.FRONT_RIGHT.value: {
                "name": "Front-Right View",
                "prompt": "Slightly turned right portrait of a woman, gentle head rotation, natural pose, soft lighting, 8K resolution, three-quarter front view, maintain exact facial features, eye color, hairstyle, and distinctive characteristics while preserving identity",
                "description": "Легкий поворот вправо з збереженням ідентичності",
                "preset": "rotation_three_quarter_right"
            },
            RotationAngle.THREE_QUARTER_LEFT.value: {
                "name": "Three-Quarter Left",
                "prompt": "Three-quarter left view of a woman, head turned 30 degrees left, classic portrait angle, professional lighting, 8K resolution, timeless composition, maintain exact facial features, eye color, and distinctive characteristics while preserving identity",
                "description": "Три чверті вліво з збереженням ідентичності",
                "preset": "rotation_three_quarter_left"
            },
            RotationAngle.THREE_QUARTER_RIGHT.value: {
                "name": "Three-Quarter Right",
                "prompt": "Three-quarter right view of a woman, head turned 30 degrees right, classic portrait angle, professional lighting, 8K resolution, timeless composition, maintain exact facial features, eye color, and distinctive characteristics while preserving identity",
                "description": "Три чверті вправо з збереженням ідентичності",
                "preset": "rotation_three_quarter_right"
            },
            RotationAngle.PROFILE_LEFT.value: {
                "name": "Left Profile",
                "prompt": "Left profile portrait of a woman, pure side view, elegant profile line, dramatic side lighting, 8K resolution, classic profile composition, maintain exact facial profile and distinctive features",
                "description": "Профіль вліво з збереженням профілю обличчя",
                "preset": "rotation_profile_left"
            },
            RotationAngle.PROFILE_RIGHT.value: {
                "name": "Right Profile",
                "prompt": "Right profile portrait of a woman, pure side view, elegant profile line, dramatic side lighting, 8K resolution, classic profile composition, maintain exact facial profile and distinctive features",
                "description": "Профіль вправо з збереженням профілю обличчя",
                "preset": "rotation_profile_right"
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
        seed: Optional[int] = None,
        custom_prompt: Optional[str] = None,
        use_preset: bool = True
    ) -> Optional[Path]:
        """Generate a single rotation image."""
        if angle not in self.rotation_prompts:
            available = list(self.rotation_prompts.keys())
            raise ValueError(f"Unknown rotation angle: {angle}. Available: {available}")
        
        seed = seed or self.settings.generation.default_seed
        rotation_info = self.rotation_prompts[angle]
        
        logger.info(f"Generating rotation image: {angle} with seed {seed}")
        
        try:
            if use_preset and "preset" in rotation_info:
                # Use preset configuration for better character consistency
                preset_name = rotation_info["preset"]
                config = self.prompt_config.get_preset_config(preset_name, "portrait", "high")
                
                # Use custom prompt or preset prompt
                if custom_prompt:
                    prompt = f"{custom_prompt}, {rotation_info['prompt']}"
                else:
                    prompt = config["prompt"]
                
                # Get quality settings from preset
                quality_settings = config["quality_settings"].copy()
                quality_settings.pop("description", None)
                
                logger.info(f"Using preset: {preset_name} for angle: {angle}")
                
            else:
                # Fallback to basic prompt
                prompt = custom_prompt or rotation_info["prompt"]
                quality_settings = {
                    "steps": 20,
                    "cfg_scale": 7.0,
                    "scheduler": "euler_a"
                }
            
            # Use base class method for generation
            return super().generate_single_image(
                prompt=prompt,
                seed=seed,
                aspect_ratio="2:3",  # Portrait for rotation
                output_format="jpeg",
                base_name=f"rotation_{angle}",
                **quality_settings
            )
                
        except Exception as e:
            logger.error(f"Error generating rotation image: {e}")
            return None
    
    def generate_rotation_sequence(
        self,
        angles: Optional[List[str]] = None,
        base_prompt: str = "portrait of a woman",
        start_seed: Optional[int] = None,
        use_presets: bool = True,
        delay_between_requests: int = 3
    ) -> Dict[str, Optional[Path]]:
        """Generate rotation sequence with character consistency."""
        angles = angles or list(self.rotation_prompts.keys())
        start_seed = start_seed or self.settings.generation.default_seed
        
        logger.info(f"Generating rotation sequence: {len(angles)} angles")
        logger.info(f"Base prompt: {base_prompt}")
        logger.info(f"Using presets: {use_presets}")
        
        results = {}
        successful_count = 0
        
        for i, angle in enumerate(angles):
            current_seed = start_seed + i
            logger.info(f"Generating rotation {i + 1}/{len(angles)}: {angle}")
            
            try:
                output_path = self.generate_single_rotation(
                    angle=angle,
                    seed=current_seed,
                    custom_prompt=base_prompt,
                    use_preset=use_presets
                )
                
                results[angle] = output_path
                if output_path:
                    successful_count += 1
                    logger.info(f"Successfully generated rotation: {angle}")
                else:
                    logger.warning(f"Failed to generate rotation: {angle}")
                
                # Delay between requests for better API stability
                if i < len(angles) - 1:
                    time.sleep(delay_between_requests)
                    
            except Exception as e:
                logger.error(f"Error in rotation generation {i + 1}/{len(angles)}: {e}")
                results[angle] = None
        
        logger.info(f"Rotation sequence completed: {successful_count}/{len(angles)} images generated")
        return results
    
    def generate_360_degree_sequence(
        self,
        steps: int = 8,
        base_prompt: str = "portrait of a woman",
        start_seed: Optional[int] = None,
        use_presets: bool = True
    ) -> List[Optional[Path]]:
        """Generate 360-degree rotation sequence with custom steps."""
        if steps < 4 or steps > 12:
            raise ValueError("Steps must be between 4 and 12")
        
        # Define rotation sequence based on steps
        sequence_mapping = {
            4: ["front", "left", "back", "right"],
            5: ["front", "front_left", "left", "back", "right"],
            6: ["front", "front_left", "left", "back_left", "back", "right"],
            7: ["front", "front_left", "left", "back_left", "back", "right", "front_right"],
            8: ["front", "front_left", "left", "back_left", "back", "back_right", "right", "front_right"],
            9: ["front", "front_left", "left", "back_left", "back", "back_right", "right", "front_right", "three_quarter_left"],
            10: ["front", "front_left", "left", "back_left", "back", "back_right", "right", "front_right", "three_quarter_left", "three_quarter_right"],
            11: ["front", "front_left", "left", "back_left", "back", "back_right", "right", "front_right", "three_quarter_left", "three_quarter_right", "profile_left"],
            12: list(self.rotation_prompts.keys())
        }
        
        sequence = sequence_mapping.get(steps, list(self.rotation_prompts.keys())[:steps])
        
        logger.info(f"Generating 360-degree sequence: {steps} steps")
        
        # Use the main rotation sequence method
        results_dict = self.generate_rotation_sequence(
            angles=sequence,
            base_prompt=base_prompt,
            start_seed=start_seed,
            use_presets=use_presets
        )
        
        # Convert to list format for backward compatibility
        results = [results_dict.get(angle) for angle in sequence]
        
        successful_count = sum(1 for r in results if r is not None)
        logger.info(f"360-degree sequence completed: {successful_count}/{steps} images generated")
        return results
    
    def get_generator_info(self) -> Dict[str, Any]:
        """Get information about the generator."""
        return {
            "name": "CharacterRotationGenerator",
            "type": "rotation",
            "description": "Character Rotation Generator for 360-degree views",
            "rotation_angles": len(self.rotation_prompts),
            "available_angles": list(self.rotation_prompts.keys()),
            "input_image": str(self.input_image),
            "output_dir": str(self.output_dir)
        }
    
