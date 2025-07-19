"""
FLUX API Image Generator Package

A Python package for generating realistic images using BFL.ai FLUX API.
"""

from .generator import FluxImageGenerator
from .enhanced_generator import EnhancedFluxGenerator
from .prompts import PromptConfig
from .prompt_tester import PromptTester

__version__ = "1.0.0"
__author__ = "Elina Klymovska"
__email__ = "elina.klymovska@gmail.com"

__all__ = ["FluxImageGenerator", "EnhancedFluxGenerator", "PromptConfig", "PromptTester"] 