# FLUX API Image Generator

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python package for generating realistic images using BFL.ai FLUX API. This project creates high-quality portraits while preserving facial features and body structure from an input image.

## 🌟 Features

- 🎨 Generate realistic portraits using FLUX API
- 🔄 **Character rotation with 12 different angles**
- 🎭 **Adetailer integration for enhanced face details**
- 🔧 Customizable prompts and parameters
- 📁 Clean and organized project structure
- 🐍 Modern Python packaging
- 🔒 Secure API key management
- 📊 Batch image generation
- 🧪 Built-in API testing
- 🎯 360-degree character sequences

## 📋 Requirements

- Python 3.8+
- BFL.ai API key
- Input image `character.jpg`

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone repository
git clone https://github.com/ElinaKlymovska/flux-image-generator.git
cd SenteticData

# Install dependencies
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
# Set your API key
export BFL_API_KEY='your_api_key_here'
```

### 3. Run Generation

**Portrait Variations** (Recommended):
```bash
python bin/generate_portrait_variations.py
# Generates 24 images: 12 styles × 2 qualities
```

**Basic Generator**:
```bash
python bin/main.py
```

**Enhanced Generator**:
```bash
python bin/enhanced_main.py
```

**Prompt Tester**:
```bash
python bin/prompt_tester_main.py
```

**All Variations**:
```bash
python bin/generate_all_variations.py
```

**Character Rotation**:
```bash
# Basic 4-angle rotation
python bin/generate_rotation.py --angles front left back right

# 360-degree sequence (8 steps)
python bin/generate_rotation.py --steps 8 --style cinematic

# Custom prompt with rotation
python bin/generate_rotation.py --custom-prompt "wearing red dress" --style fashion

# Enhanced rotation with Black Forest Labs presets (recommended)
python bin/generate_rotation.py --angles front left back right --use-presets

# Character-consistent rotation with custom base prompt
python bin/generate_rotation.py --angles front left back right --custom-prompt "portrait of a woman with long brown hair"

# List available rotation presets
python bin/generate_rotation.py --list-presets

# Show preset details
python bin/generate_rotation.py --preset-info rotation_front
```

**Flux Rotation (Advanced)**:
```bash
python bin/generate_flux_rotation_v3.py
```

**Adetailer Processing**:
```bash
# FLUX API Adetailer (Recommended - Works perfectly)
python bin/process_with_flux_adetailer.py

# Or use the script
./scripts/run_flux_adetailer.sh

# SD WebUI Adetailer (Requires SD WebUI setup)
python bin/process_with_sd_webui.py
```

## 📁 Project Structure

```
SenteticData/
├── bin/                          # Main executable scripts
│   ├── main.py                   # Basic image generator
│   ├── enhanced_main.py          # Enhanced generator with more options
│   ├── generate_portrait_variations.py  # Portrait variations generator
│   ├── generate_all_variations.py       # All variations generator
│   ├── generate_rotation.py             # Character rotation
│   ├── generate_flux_rotation_v3.py     # Advanced flux rotation
│   ├── prompt_tester_main.py            # Prompt testing utility
│   ├── process_with_flux_adetailer.py   # FLUX API Adetailer processing
│   └── process_with_sd_webui.py         # SD WebUI Adetailer processing
├── src/                          # Core package source code
│   └── flux_generator/
│       ├── api/                  # API client and models
│       ├── cli/                  # Command line interface
│       ├── config/               # Configuration and prompts
│       ├── core/                 # Core generation logic
│       └── utils/                # Utility functions
├── config/                       # Configuration files
│   └── config.yaml              # Main configuration
├── data/                         # Data directories
│   ├── input/                   # Input images
│   └── output/                  # Generated images
├── scripts/                      # Shell scripts for automation
│   ├── run_flux_adetailer.sh     # FLUX Adetailer processing
├── requirements.txt              # Python dependencies
├── pyproject.toml               # Project configuration
├── setup.py                     # Package setup
├── LICENSE                       # MIT License
└── README.md                     # This file
```

## 🔧 Configuration

The main configuration is in `config/config.yaml`:

```yaml
api:
  base_url: "https://api.bfl.ai/v1"
  timeout: 300
  max_retries: 3
  retry_delay: 5

generation:
  default_count: 15
  default_seed: 1000
  default_aspect_ratio: "2:3"
  default_output_format: "jpeg"
  default_quality: "high"
  default_style: "realistic"
```

## 🎨 Usage Examples

### Basic Image Generation

```python
from src.flux_generator.core.generator import FluxImageGenerator

# Initialize generator
generator = FluxImageGenerator()

# Generate single image
output_path = generator.generate_single_image(
    prompt="portrait of a beautiful woman",
    seed=1000
)
```

### Character Rotation

```python
from src.flux_generator.core.rotation import FluxRotationGenerator

# Initialize rotation generator
rotation_gen = FluxRotationGenerator()

# Generate rotation sequence
output_paths = rotation_gen.generate_rotation_sequence(
    angles=["front", "left", "back", "right"],
    style="cinematic"
)
```

### Adetailer Processing

```python
from src.flux_generator.core.adetailer import AdetailerProcessor

# Initialize adetailer processor
processor = AdetailerProcessor()

# Process image with adetailer
processed_path = processor.process_image(
    input_path="path/to/image.jpg",
    strength=0.8
)
```

## 🛠️ Development

### Installing in Development Mode

```bash
pip install -e .
```

### Running Tests

```bash
python -m pytest tests/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For support and questions, please open an issue on GitHub. 