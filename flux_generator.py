#!/usr/bin/env python3
"""
FLUX Image Generator - Main Entry Point

A unified CLI interface for the FLUX Image Generator.
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from flux_generator.cli.commands import main

if __name__ == "__main__":
    main() 