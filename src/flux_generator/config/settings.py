"""
Settings and configuration management for FLUX Image Generator.
"""

import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field
import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class APISettings:
    """API configuration settings."""
    base_url: str = "https://api.bfl.ai/v1"
    timeout: int = 600  # Increased timeout to 10 minutes
    max_retries: int = 5  # Increased retries
    retry_delay: int = 10  # Increased delay between retries


@dataclass
class GenerationSettings:
    """Image generation settings."""
    default_count: int = 15
    default_seed: int = 1000
    default_aspect_ratio: str = "2:3"
    default_output_format: str = "jpeg"
    default_quality: str = "high"
    default_style: str = "realistic"


@dataclass
class PathSettings:
    """Path configuration settings."""
    base_dir: Path = field(default_factory=lambda: Path.cwd())
    input_dir: Path = field(init=False)
    output_dir: Path = field(init=False)
    config_dir: Path = field(init=False)
    
    def __post_init__(self):
        self.input_dir = self.base_dir / "data" / "input"
        self.output_dir = self.base_dir / "data" / "output"
        self.config_dir = self.base_dir / "config"


@dataclass
class Settings:
    """Main settings class."""
    api_key: Optional[str] = None
    api: APISettings = field(default_factory=APISettings)
    generation: GenerationSettings = field(default_factory=GenerationSettings)
    paths: PathSettings = field(default_factory=PathSettings)
    
    def __post_init__(self):
        # Load API key from environment
        if not self.api_key:
            self.api_key = os.getenv("FLUX_API_KEY") or os.getenv("BFL_API_KEY")
        
        # Create directories if they don't exist
        self.paths.input_dir.mkdir(parents=True, exist_ok=True)
        self.paths.output_dir.mkdir(parents=True, exist_ok=True)
        self.paths.config_dir.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def from_file(cls, config_path: Optional[Path] = None) -> "Settings":
        """Load settings from YAML file."""
        if config_path is None:
            config_path = Path.cwd() / "config" / "config.yaml"
        
        settings = cls()
        
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
                
            if config_data:
                # Update API settings
                if 'api' in config_data:
                    api_data = config_data['api']
                    settings.api.base_url = api_data.get('base_url', settings.api.base_url)
                    settings.api.timeout = api_data.get('timeout', settings.api.timeout)
                    settings.api.max_retries = api_data.get('max_retries', settings.api.max_retries)
                    settings.api.retry_delay = api_data.get('retry_delay', settings.api.retry_delay)
                
                # Update generation settings
                if 'generation' in config_data:
                    gen_data = config_data['generation']
                    settings.generation.default_count = gen_data.get('default_count', settings.generation.default_count)
                    settings.generation.default_seed = gen_data.get('default_seed', settings.generation.default_seed)
                    settings.generation.default_aspect_ratio = gen_data.get('default_aspect_ratio', settings.generation.default_aspect_ratio)
                    settings.generation.default_output_format = gen_data.get('default_output_format', settings.generation.default_output_format)
                    settings.generation.default_quality = gen_data.get('default_quality', settings.generation.default_quality)
                    settings.generation.default_style = gen_data.get('default_style', settings.generation.default_style)
        
        return settings
    
    def save_to_file(self, config_path: Optional[Path] = None) -> None:
        """Save settings to YAML file."""
        if config_path is None:
            config_path = self.paths.config_dir / "config.yaml"
        
        config_data = {
            'api': {
                'base_url': self.api.base_url,
                'timeout': self.api.timeout,
                'max_retries': self.api.max_retries,
                'retry_delay': self.api.retry_delay,
            },
            'generation': {
                'default_count': self.generation.default_count,
                'default_seed': self.generation.default_seed,
                'default_aspect_ratio': self.generation.default_aspect_ratio,
                'default_output_format': self.generation.default_output_format,
                'default_quality': self.generation.default_quality,
                'default_style': self.generation.default_style,
            }
        }
        
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f, default_flow_style=False, indent=2)
    
    def validate(self) -> bool:
        """Validate settings."""
        if not self.api_key:
            raise ValueError("API key is required. Set FLUX_API_KEY or BFL_API_KEY environment variable or configure it.")
        
        if not self.paths.input_dir.exists():
            raise ValueError(f"Input directory does not exist: {self.paths.input_dir}")
        
        return True


# Global settings instance
settings = Settings.from_file() 