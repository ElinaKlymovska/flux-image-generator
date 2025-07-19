# FLUX API Image Generator

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python package for generating realistic images using BFL.ai FLUX API. This project creates high-quality portraits while preserving facial features and body structure from an input image.

## 🌟 Features

- 🎨 Generate realistic portraits using FLUX API
- 🔧 Customizable prompts and parameters
- 📁 Clean and organized project structure
- 🐍 Modern Python packaging
- 🔒 Secure API key management
- 📊 Batch image generation
- 🧪 Built-in API testing

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

## 📁 Project Structure

```
SenteticData/
├── src/
│   └── flux_generator/          # Main package
│       ├── api/                 # API client and models
│       ├── cli/                 # Command line interface
│       ├── config/              # Configuration and prompts
│       ├── core/                # Core generation logic
│       └── utils/               # Utilities
├── bin/                         # Entry point scripts
│   ├── main.py                  # Basic generator
│   ├── enhanced_main.py         # Enhanced generator
│   ├── generate_portrait_variations.py
│   ├── generate_all_variations.py
│   └── prompt_tester_main.py
├── data/
│   ├── input/                   # Input images
│   └── output/                  # Generated images
├── scripts/                     # Run scripts
├── examples/                    # Usage examples
├── tests/                       # Test files
├── config/                      # Configuration files
│   └── project/                 # Project configuration
│       ├── setup.py
│       ├── pyproject.toml
│       └── env.example
├── requirements.txt
└── README.md
```

## 🎯 Usage Examples

### Basic Usage

```python
from src.flux_generator.core.generator import FluxImageGenerator

# Create generator instance
generator = FluxImageGenerator()

# Generate images
generator.generate_images(5)
```

### Enhanced Usage

```python
from src.flux_generator.core.enhanced import EnhancedFluxGenerator

# Create enhanced generator
generator = EnhancedFluxGenerator()

# Generate portrait variations
summary = generator.generate_all_variations_summary(
    count_per_variation=1,
    include_qualities=["standard", "creative"]
)
```

## 🎨 Available Styles

- **Ultra Realistic** - Фотореалістичний портрет
- **Cinematic** - Кінематографічний стиль
- **Artistic** - Художній стиль
- **Fashion** - Модний портрет
- **Vintage** - Вінтажний стиль
- **Modern** - Сучасний мінімалістичний
- **Dramatic** - Драматичний стиль
- **Soft & Dreamy** - М'який мрійливий
- **Fantasy** - Фентезі стиль
- **Sci-Fi** - Науково-фантастичний
- **Film Noir** - Фільм-нуар
- **Impressionist** - Імпресіоністичний

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](docs/LICENSE) file for details. 