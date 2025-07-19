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
    
    def get_available_presets(self) -> List[Dict[str, str]]:
        """Get list of available rotation presets."""
        return self.prompt_config.list_available_presets()
    
    def get_preset_info(self, preset: str) -> Dict[str, Any]:
        """Get detailed information about a specific preset."""
        return self.prompt_config.get_preset_config(preset, "portrait", "high")
    
    def generate_rotation_with_custom_preset(
        self,
        angle: str,
        preset: str,
        custom_prompt: str,
        seed: Optional[int] = None
    ) -> Optional[Path]:
        """Generate rotation with custom preset and prompt."""
        return self.generate_rotation_with_preset(
            angle=angle,
            preset=preset,
            seed=seed,
            custom_prompt=custom_prompt
        )
    
    def generate_single_rotation(
        self,
        angle: str,
        style: str = "ultra_realistic",
        seed: Optional[int] = None,
        custom_prompt: Optional[str] = None,
        use_preset: bool = True
    ) -> Optional[Path]:
        """Generate a single rotation image using Black Forest Labs best practices."""
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
                # Fallback to original method
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
            
            # Create generation request
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
    
    def generate_rotation_with_preset(
        self,
        angle: str,
        preset: str,
        seed: Optional[int] = None,
        custom_prompt: Optional[str] = None
    ) -> Optional[Path]:
        """Generate rotation image using specific preset."""
        seed = seed or self.settings.generation.default_seed
        
        logger.info(f"Generating rotation image: {angle} with preset: {preset}")
        
        try:
            # Get preset configuration
            config = self.prompt_config.get_preset_config(preset, "portrait", "high")
            
            # Use custom prompt or preset prompt
            if custom_prompt:
                prompt = f"{custom_prompt}, {config['prompt']}"
            else:
                prompt = config["prompt"]
            
            # Get quality settings from preset
            quality_settings = config["quality_settings"].copy()
            quality_settings.pop("description", None)
            
            # Create generation request
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
                    base_name=f"rotation_{angle}_{preset}",
                    index=0,
                    seed=seed,
                    extension="jpg"
                )
                
                # Save image
                output_path = self.output_dir / filename
                ImageUtils.save_image_data(response.image_data, output_path)
                
                logger.info(f"Generated rotation image with preset saved: {output_path}")
                return output_path
            else:
                logger.error(f"Rotation generation with preset failed: {response.error_message}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating rotation image with preset: {e}")
            return None
    
    def generate_character_consistent_rotation(
        self,
        angles: List[str],
        base_prompt: str = "portrait of a woman",
        seed: Optional[int] = None,
        use_presets: bool = True
    ) -> Dict[str, Optional[Path]]:
        """Generate character-consistent rotation sequence using Black Forest Labs best practices."""
        seed = seed or self.settings.generation.default_seed
        
        logger.info(f"Generating character-consistent rotation for angles: {angles}")
        logger.info(f"Base prompt: {base_prompt}")
        
        results = {}
        successful_count = 0
        
        for i, angle in enumerate(angles):
            current_seed = seed + i
            logger.info(f"Generating rotation {i + 1}/{len(angles)}: {angle}")
            
            try:
                # Create character-consistent prompt
                rotation_info = self.rotation_prompts[angle]
                character_prompt = f"{base_prompt}, {rotation_info['prompt']}"
                
                if use_presets and "preset" in rotation_info:
                    output_path = self.generate_rotation_with_preset(
                        angle=angle,
                        preset=rotation_info["preset"],
                        seed=current_seed,
                        custom_prompt=base_prompt
                    )
                else:
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
                
                # Small delay between requests for better API stability
                if i < len(angles) - 1:
                    time.sleep(3)
                    
            except Exception as e:
                logger.error(f"Error in rotation generation {i + 1}/{len(angles)}: {e}")
                results[angle] = None
        
        logger.info(f"Character-consistent rotation completed: {successful_count}/{len(angles)} images generated")
        return results
    
    def generate_full_rotation(
        self,
        angles: Optional[List[str]] = None,
        style: str = "ultra_realistic",
        start_seed: Optional[int] = None,
        custom_prompt: Optional[str] = None,
        use_presets: bool = True
    ) -> Dict[str, Optional[Path]]:
        """Generate full rotation sequence with character consistency."""
        angles = angles or list(self.rotation_prompts.keys())
        start_seed = start_seed or self.settings.generation.default_seed
        
        logger.info(f"Starting full rotation generation: {len(angles)} angles")
        logger.info(f"Using presets: {use_presets}")
        
        if use_presets:
            # Use character-consistent rotation with presets
            return self.generate_character_consistent_rotation(
                angles=angles,
                base_prompt=custom_prompt or "portrait of a woman",
                seed=start_seed,
                use_presets=True
            )
        else:
            # Fallback to original method
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
                        custom_prompt=custom_prompt,
                        use_preset=False
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
                    logger.error(f"Error in rotation generation {i + 1}/{len(angles)}: {e}")
                    results[angle] = None
            
            logger.info(f"Full rotation generation completed: {successful_count}/{len(angles)} images generated")
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