"""
Base Configuration Class for FLUX Image Generator.

This module provides base classes for configuration management
to reduce code duplication across settings and prompts.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod
import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class BaseConfig(ABC):
    """Base class for configuration management."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize base configuration."""
        self.config_path = config_path
        self._config_data: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from file."""
        if self.config_path and self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self._config_data = yaml.safe_load(f) or {}
            except Exception as e:
                print(f"Warning: Could not load config from {self.config_path}: {e}")
                self._config_data = {}
    
    def save_config(self, config_path: Optional[Path] = None) -> None:
        """Save configuration to file."""
        save_path = config_path or self.config_path
        if save_path:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            with open(save_path, 'w', encoding='utf-8') as f:
                yaml.dump(self._config_data, f, default_flow_style=False, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config_data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self._config_data[key] = value
    
    def validate(self) -> bool:
        """Validate configuration."""
        return True
    
    @abstractmethod
    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        pass


class EnvironmentConfig:
    """Environment variable configuration helper."""
    
    @staticmethod
    def get_api_key() -> Optional[str]:
        """Get API key from environment variables."""
        return os.getenv("FLUX_API_KEY") or os.getenv("BFL_API_KEY")
    
    @staticmethod
    def get_base_dir() -> Path:
        """Get base directory from environment or current working directory."""
        base_dir = os.getenv("FLUX_BASE_DIR")
        return Path(base_dir) if base_dir else Path.cwd()
    
    @staticmethod
    def get_log_level() -> str:
        """Get log level from environment."""
        return os.getenv("FLUX_LOG_LEVEL", "INFO").upper()
    
    @staticmethod
    def get_timeout() -> int:
        """Get timeout from environment."""
        return int(os.getenv("FLUX_TIMEOUT", "600"))
    
    @staticmethod
    def get_max_retries() -> int:
        """Get max retries from environment."""
        return int(os.getenv("FLUX_MAX_RETRIES", "5"))


class PathConfig:
    """Path configuration helper."""
    
    def __init__(self, base_dir: Optional[Path] = None):
        """Initialize path configuration."""
        self.base_dir = base_dir or EnvironmentConfig.get_base_dir()
        self._setup_paths()
    
    def _setup_paths(self) -> None:
        """Setup all required paths."""
        self.input_dir = self.base_dir / "data" / "input"
        self.output_dir = self.base_dir / "data" / "output"
        self.config_dir = self.base_dir / "config"
        self.logs_dir = self.base_dir / "logs"
        
        # Create directories
        for path in [self.input_dir, self.output_dir, self.config_dir, self.logs_dir]:
            path.mkdir(parents=True, exist_ok=True)
    
    def get_subdir(self, subdir_name: str) -> Path:
        """Get subdirectory path."""
        subdir = self.output_dir / subdir_name
        subdir.mkdir(parents=True, exist_ok=True)
        return subdir
    
    def find_input_image(self, filename: str = "character.jpg") -> Optional[Path]:
        """Find input image in input directory."""
        image_path = self.input_dir / filename
        
        if image_path.exists():
            return image_path
        
        # Try alternative extensions
        for ext in [".png", ".jpeg", ".webp"]:
            alt_path = self.input_dir / f"{filename.rsplit('.', 1)[0]}{ext}"
            if alt_path.exists():
                return alt_path
        
        return None 