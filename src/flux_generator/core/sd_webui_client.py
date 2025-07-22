"""
Stable Diffusion WebUI Client with Adetailer support.
"""

import base64
import requests
import time
from pathlib import Path
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class SDWebUIClient:
    """Client for Stable Diffusion WebUI API with Adetailer support."""
    
    def __init__(self, base_url: str = "http://localhost:7860"):
        self.base_url = base_url.rstrip('/')
        self.api_url = f"{self.base_url}/sdapi/v1"
        
    def test_connection(self) -> bool:
        """Test connection to SD WebUI."""
        try:
            response = requests.get(f"{self.api_url}/progress", timeout=10)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    def process_image_with_adetailer(
        self,
        image_path: Path,
        prompt: str = "beautiful face, detailed eyes, perfect skin, high quality",
        negative_prompt: str = "",
        adetailer_config: Optional[Dict[str, Any]] = None
    ) -> Optional[bytes]:
        """Process image with Adetailer using SD WebUI."""
        
        # Default Adetailer settings
        default_config = {
            "model": "face_yolov8n.pt",
            "confidence": 0.3,
            "dilation": 4,
            "denoising_strength": 0.4,
            "steps": 20,
            "cfg_scale": 7.0,
            "sampler": "DPM++ 2M Karras",
            "width": 512,
            "height": 512
        }
        
        if adetailer_config:
            default_config.update(adetailer_config)
        
        try:
            # Read and encode image
            with open(image_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode()
            
            # Prepare payload
            payload = {
                "init_images": [image_data],
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "steps": default_config["steps"],
                "cfg_scale": default_config["cfg_scale"],
                "sampler_name": default_config["sampler"],
                "width": default_config["width"],
                "height": default_config["height"],
                "denoising_strength": default_config["denoising_strength"],
                "adetailer": {
                    "args": [
                        True,  # enabled
                        default_config["model"],
                        default_config["confidence"],
                        default_config["dilation"],
                        default_config["denoising_strength"],
                        prompt,  # adetailer prompt
                        negative_prompt,  # adetailer negative prompt
                        default_config["steps"],
                        default_config["cfg_scale"],
                        default_config["sampler"],
                        default_config["width"],
                        default_config["height"]
                    ]
                }
            }
            
            # Send request
            logger.info(f"Processing {image_path.name} with Adetailer...")
            response = requests.post(f"{self.api_url}/img2img", json=payload, timeout=120)
            
            if response.status_code == 200:
                result = response.json()
                if "images" in result and result["images"]:
                    # Decode the first image
                    image_data = base64.b64decode(result["images"][0])
                    logger.info(f"Successfully processed {image_path.name}")
                    return image_data
                else:
                    logger.error(f"No image returned for {image_path.name}")
                    return None
            else:
                logger.error(f"API error for {image_path.name}: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error processing {image_path.name}: {e}")
            return None
    
    def process_multiple_images(
        self,
        image_paths: List[Path],
        output_dir: Path,
        prompt: str = "beautiful face, detailed eyes, perfect skin, high quality",
        negative_prompt: str = "",
        adetailer_config: Optional[Dict[str, Any]] = None,
        output_suffix: str = "_adetailer"
    ) -> List[Path]:
        """Process multiple images with Adetailer."""
        
        if not self.test_connection():
            logger.error("Cannot connect to SD WebUI")
            return []
        
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)
        
        processed_paths = []
        successful_count = 0
        
        for i, image_path in enumerate(image_paths, 1):
            logger.info(f"Processing {i}/{len(image_paths)}: {image_path.name}")
            
            try:
                # Process image
                processed_image_data = self.process_image_with_adetailer(
                    image_path, prompt, negative_prompt, adetailer_config
                )
                
                if processed_image_data:
                    # Save processed image
                    output_filename = f"{image_path.stem}{output_suffix}{image_path.suffix}"
                    output_path = output_dir / output_filename
                    
                    with open(output_path, "wb") as f:
                        f.write(processed_image_data)
                    
                    processed_paths.append(output_path)
                    successful_count += 1
                    logger.info(f"Saved: {output_filename}")
                else:
                    logger.warning(f"Failed to process: {image_path.name}")
                
                # Small delay between requests
                if i < len(image_paths):
                    time.sleep(2)
                    
            except Exception as e:
                logger.error(f"Error processing {image_path.name}: {e}")
        
        logger.info(f"Processing completed: {successful_count}/{len(image_paths)} images")
        return processed_paths 