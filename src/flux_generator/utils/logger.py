"""
Logging utilities for FLUX Image Generator.
"""

from pathlib import Path
from typing import Optional

from .base import LoggerManager


def setup_logger(
    name: str = "flux_generator",
    level: str = "INFO",
    log_file: Optional[Path] = None,
    format_string: Optional[str] = None
):
    """Setup logger with console and file handlers."""
    return LoggerManager.setup_logger(name, level, log_file, format_string)


def get_logger(name: str = "flux_generator"):
    """Get existing logger or create new one."""
    return LoggerManager.get_logger(name) 