"""
Settings and configuration management for FLUX Image Generator.
"""

from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field

from .base import BaseConfig, EnvironmentConfig, PathConfig


@dataclass
class APISettings:
    """API configuration settings."""
    base_url: str = "https://api.bfl.ai/v1"
    timeout: int = field(default_factory=EnvironmentConfig.get_timeout)
    max_retries: int = field(default_factory=EnvironmentConfig.get_max_retries)
    retry_delay: int = 10
    polling_interval: int = 5  # seconds
    polling_timeout_attempts: int = 180  # 180 * 5s = 15 minutes


@dataclass
class GenerationSettings:
    """Image generation settings."""
    default_count: int = 15
    default_seed: int = 1000
    default_aspect_ratio: str = "2:3"
    default_output_format: str = "jpeg"
    default_quality: str = "high"
    default_style: str = "realistic"


class Settings(BaseConfig):
    """Main settings class."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize settings."""
        if config_path is None:
            path_config = PathConfig()
            config_path = path_config.config_dir / "config.yaml"
        
        super().__init__(config_path)
        
        # Initialize components
        self.paths = PathConfig()
        self.api = APISettings()
        self.generation = GenerationSettings()
        self.api_key = EnvironmentConfig.get_api_key()
        
        # Load from config file
        self._load_from_config()
        
        # Validate
        self.validate()
    
    def _load_from_config(self) -> None:
        """Load settings from configuration data."""
        if not self._config_data:
            return
        
        # Update API settings
        if 'api' in self._config_data:
            api_data = self._config_data['api']
            self.api.base_url = api_data.get('base_url', self.api.base_url)
            self.api.timeout = api_data.get('timeout', self.api.timeout)
            self.api.max_retries = api_data.get('max_retries', self.api.max_retries)
            self.api.retry_delay = api_data.get('retry_delay', self.api.retry_delay)
            self.api.polling_interval = api_data.get('polling_interval', self.api.polling_interval)
            self.api.polling_timeout_attempts = api_data.get('polling_timeout_attempts', self.api.polling_timeout_attempts)
        
        # Update generation settings
        if 'generation' in self._config_data:
            gen_data = self._config_data['generation']
            self.generation.default_count = gen_data.get('default_count', self.generation.default_count)
            self.generation.default_seed = gen_data.get('default_seed', self.generation.default_seed)
            self.generation.default_aspect_ratio = gen_data.get('default_aspect_ratio', self.generation.default_aspect_ratio)
            self.generation.default_output_format = gen_data.get('default_output_format', self.generation.default_output_format)
            self.generation.default_quality = gen_data.get('default_quality', self.generation.default_quality)
            self.generation.default_style = gen_data.get('default_style', self.generation.default_style)
    
    def validate(self) -> bool:
        """Validate settings."""
        if not self.api_key:
            raise ValueError("API key is required. Set FLUX_API_KEY or BFL_API_KEY environment variable or configure it.")
        
        if not self.paths.input_dir.exists():
            raise ValueError(f"Input directory does not exist: {self.paths.input_dir}")
        
        return True
    
    def get_default_config(self) -> dict:
        """Get default configuration."""
        return {
            'api': {
                'base_url': self.api.base_url,
                'timeout': self.api.timeout,
                'max_retries': self.api.max_retries,
                'retry_delay': self.api.retry_delay,
                'polling_interval': self.api.polling_interval,
                'polling_timeout_attempts': self.api.polling_timeout_attempts,
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
    
    def save_to_file(self, config_path: Optional[Path] = None) -> None:
        """Save settings to YAML file."""
        self._config_data = self.get_default_config()
        super().save_config(config_path)


# Global settings instance
settings = Settings() 