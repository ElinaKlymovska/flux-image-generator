"""
FLUX API Image Generator Package

A Python package for generating realistic images using BFL.ai FLUX API.
"""

# Core functionality
from .core.generator import FluxImageGenerator
from .core.enhanced import EnhancedFluxGenerator
from .core.tester import PromptTester

# API components
from .api.client import FluxAPIClient
from .api.models import GenerationRequest, GenerationResponse, APIError

# Configuration
from .config.settings import Settings, settings
from .config.prompts import PromptConfig

# Utilities
from .utils.image import ImageUtils
from .utils.logger import setup_logger, get_logger

# CLI
from .cli.commands import main as cli_main

__version__ = "2.0.0"
__author__ = "Elina Klymovska"
__email__ = "elina.klymovska@gmail.com"

__all__ = [
    # Core classes
    "FluxImageGenerator",
    "EnhancedFluxGenerator", 
    "PromptTester",
    
    # API components
    "FluxAPIClient",
    "GenerationRequest",
    "GenerationResponse",
    "APIError",
    
    # Configuration
    "Settings",
    "settings",
    "PromptConfig",
    
    # Utilities
    "ImageUtils",
    "setup_logger",
    "get_logger",
    
    # CLI
    "cli_main"
] 