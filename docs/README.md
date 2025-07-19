# FLUX API Image Generator - Documentation

## Overview

FLUX API Image Generator is a Python package for generating realistic images using BFL.ai FLUX API. It provides a simple interface for creating high-quality portraits with customizable parameters.

## Features

- 🎨 Generate realistic portraits using FLUX API
- 🔧 Customizable prompts and parameters
- 📁 Organized file structure
- 🐍 Python package with proper structure
- 🔒 Secure API key management
- 📊 Batch image generation

## Installation

### Prerequisites

- Python 3.8 or higher
- BFL.ai API key

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/flux-image-generator.git
cd flux-image-generator
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure API key:
```bash
cp env.example .env
# Edit .env and add your BFL_API_KEY
```

## Usage

### Basic Usage

```python
from flux_generator import FluxImageGenerator

# Create generator instance
generator = FluxImageGenerator()

# Generate 15 images
generator.generate_images(15)
```

### Command Line

```bash
# Run the main script
python main.py

# Or use the provided scripts
./scripts/run.sh
```

### Custom Parameters

```python
# Create custom generation request
request_data = {
    "prompt": "your custom prompt here",
    "input_image": "path/to/input/image.jpg",
    "seed": 1234,
    "aspect_ratio": "1:1",
    "output_format": "jpeg"
}
```

## Project Structure

```
flux-image-generator/
├── src/
│   └── flux_generator/
│       ├── __init__.py
│       ├── generator.py
│       └── test_api.py
├── data/
│   ├── input/
│   │   └── character.jpg
│   └── output/
├── scripts/
│   ├── run.sh
│   └── run_manual.sh
├── docs/
├── tests/
├── main.py
├── requirements.txt
├── setup.py
├── pyproject.toml
└── README.md
```

## Configuration

### Environment Variables

- `BFL_API_KEY`: Your BFL.ai API key

### API Parameters

- `prompt`: Text description for image generation
- `input_image`: Base64 encoded input image
- `seed`: Random seed for reproducible results
- `aspect_ratio`: Image aspect ratio (e.g., "2:3", "1:1")
- `output_format`: Output format ("jpeg", "png")
- `prompt_upsampling`: Enable prompt upsampling
- `safety_tolerance`: Safety tolerance level

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Code Formatting

```bash
black src/
flake8 src/
```

### Building Package

```bash
python setup.py build
pip install -e .
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support

For support, please open an issue on GitHub or contact the maintainers. 