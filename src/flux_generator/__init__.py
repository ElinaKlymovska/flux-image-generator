"""
FLUX API Image Generator Package

A Python package for generating realistic images using BFL.ai FLUX API.
"""

# Core functionality
from .core.base import BaseGenerator
from .core.generator import FluxImageGenerator
from .core.enhanced import EnhancedFluxGenerator
from .core.rotation import CharacterRotationGenerator
from .core.adetailer import AdetailerGenerator

# API components
from .api.base import BaseAPIClient, BaseRequest, BaseResponse, APIError
from .api.client import FluxAPIClient
from .api.models import GenerationRequest, GenerationResponse

# Configuration
from .config.base import BaseConfig, EnvironmentConfig, PathConfig
from .config.settings import Settings, settings
from .config.prompts import PromptConfig

# Utilities
from .utils.base import BaseUtils, ImageProcessor, LoggerManager, FileUtils
from .utils.image import ImageUtils
from .utils.logger import setup_logger, get_logger

__version__ = "2.0.0"
__author__ = "Elina Klymovska"
__email__ = "elina.klymovska@gmail.com"

__all__ = [
    # Core classes
    "BaseGenerator",
    "FluxImageGenerator",
    "EnhancedFluxGenerator",
    "CharacterRotationGenerator",
    "AdetailerGenerator",
    
    # API components
    "BaseAPIClient",
    "BaseRequest", 
    "BaseResponse",
    "APIError",
    "FluxAPIClient",
    "GenerationRequest",
    "GenerationResponse",
    
    # Configuration
    "BaseConfig",
    "EnvironmentConfig",
    "PathConfig",
    "Settings",
    "settings",
    "PromptConfig",
    
    # Utilities
    "BaseUtils",
    "ImageProcessor",
    "LoggerManager",
    "FileUtils",
    "ImageUtils",
    "setup_logger",
    "get_logger",
] 