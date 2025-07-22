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

# Or use the script:
./scripts/run_rotation.sh --steps 8 --style ultra_realistic
```

**Adetailer Face Enhancement**:
```bash
# Single image with Adetailer
python bin/generate_adetailer.py

# Batch generation with Adetailer
python bin/generate_adetailer_batch.py

# Process existing images with Adetailer
python bin/process_existing_with_adetailer.py

# CLI commands for Adetailer
python -m src.flux_generator.cli.adetailer_commands generate --confidence 0.4 --denoising-strength 0.5

# Process existing images via CLI
python -m src.flux_generator.cli.adetailer_commands process --confidence 0.4 --denoising-strength 0.5

# Or use the scripts:
./scripts/run_adetailer.sh
./scripts/run_adetailer_batch.sh
./scripts/run_process_existing.sh
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
│   ├── generate_rotation.py     # Character rotation generator
│   ├── generate_adetailer.py    # Adetailer face enhancement
│   ├── generate_adetailer_batch.py # Batch Adetailer generation
│   ├── process_existing_with_adetailer.py # Process existing images with Adetailer
│   └── prompt_tester_main.py
├── data/
│   ├── input/                   # Input images
│   └── output/                  # Generated images
├── scripts/                     # Run scripts
│   ├── run.sh                   # Basic generation
│   ├── run_enhanced.sh          # Enhanced generation
│   ├── run_portrait_variations.sh
│   ├── run_all_variations.sh
│   ├── run_rotation.sh          # Character rotation
│   ├── run_adetailer.sh         # Adetailer generation
│   ├── run_adetailer_batch.sh   # Batch Adetailer generation
│   ├── run_process_existing.sh  # Process existing images with Adetailer
│   └── run_prompt_tester.sh
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

### Character Rotation Usage

```python
from src.flux_generator.core.rotation import CharacterRotationGenerator

# Create rotation generator
generator = CharacterRotationGenerator()

# Generate 360-degree sequence
results = generator.generate_360_degree_sequence(
    steps=8,
    style="cinematic",
    start_seed=1001
)

# Generate specific angles
results = generator.generate_full_rotation(
    angles=["front", "left", "back", "right"],
    style="ultra_realistic"
)
```

### Adetailer Face Enhancement Usage

```python
from src.flux_generator.core.adetailer import AdetailerGenerator

# Create Adetailer generator
generator = AdetailerGenerator()

# Generate single image with enhanced face details
output_path = generator.generate_with_adetailer(
    prompt="A beautiful woman with realistic face details",
    seed=12345,
    adetailer_config={
        'confidence': 0.4,
        'denoising_strength': 0.5,
        'steps': 25,
        'cfg_scale': 8.0
    }
)

# Generate multiple images with Adetailer
output_paths = generator.generate_multiple_with_adetailer(
    count=5,
    start_seed=1000
)

# Update Adetailer settings
generator.update_adetailer_settings(
    confidence=0.5,
    denoising_strength=0.6,
    steps=30,
    cfg_scale=9.0
)

# Process existing images with Adetailer
output_paths = generator.process_existing_images(
    file_pattern="*.jpg",
    adetailer_config={
        'confidence': 0.4,
        'denoising_strength': 0.5,
        'steps': 25,
        'cfg_scale': 8.0
    },
    output_suffix="_adetailer"
)

# Process specific images
specific_images = [
    Path("data/output/woman_1000.jpg"),
    Path("data/output/woman_1001.jpg")
]
output_paths = generator.process_specific_images(
    image_paths=specific_images,
    adetailer_config={'confidence': 0.5, 'steps': 30},
    output_suffix="_enhanced"
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

## 🔄 Character Rotation Angles

- **Front** - Прямий фронтальний ракурс
- **Front-Left** - Легкий поворот вліво
- **Left** - Поворот на 45° вліво
- **Back-Left** - Поворот на 90° вліво
- **Back** - Вид ззаду
- **Back-Right** - Поворот на 90° вправо
- **Right** - Поворот на 45° вправо
- **Front-Right** - Легкий поворот вправо
- **Three-Quarter Left** - Три чверті вліво
- **Three-Quarter Right** - Три чверті вправо
- **Profile Left** - Профіль вліво
- **Profile Right** - Профіль вправо

### 🎯 Enhanced Rotation Features

**Black Forest Labs Best Practices Integration:**
- **Character Consistency**: Maintains facial features, hairstyle, and distinctive characteristics across all rotation angles
- **Preset System**: Specialized rotation presets optimized for FLUX.1 Kontext [pro] model
- **Identity Preservation**: Advanced prompts that preserve character identity during rotation
- **Professional Quality**: 8K resolution with optimized lighting and composition for each angle

**Available Rotation Presets:**
- `rotation_front` - Front view with identity preservation
- `rotation_left` - Left view with character consistency
- `rotation_right` - Right view with character consistency
- `rotation_back` - Back view with distinctive features preservation
- `rotation_profile_left` - Left profile with facial profile preservation
- `rotation_profile_right` - Right profile with facial profile preservation
- `rotation_three_quarter_left` - Three-quarter left with identity preservation
- `rotation_three_quarter_right` - Three-quarter right with identity preservation

**Usage Examples:**
```python
# Character-consistent rotation with presets
generator = CharacterRotationGenerator()
results = generator.generate_character_consistent_rotation(
    angles=["front", "left", "back", "right"],
    base_prompt="portrait of a woman with long brown hair and green eyes",
    use_presets=True
)

# Generate with specific preset
result = generator.generate_rotation_with_preset(
    angle="front",
    preset="rotation_front",
    custom_prompt="portrait of a woman wearing a red dress"
)
```

## 🎭 Adetailer Face Enhancement

The Adetailer integration provides enhanced face detail generation for more realistic portraits:

### Key Features
- **Automatic Face Detection**: Uses YOLOv8 model for precise face detection
- **Enhanced Detail Processing**: Applies specialized prompts for face quality improvement
- **Configurable Parameters**: Flexible settings for different scenarios
- **Batch Processing**: Support for multiple image generation
- **FLUX API Integration**: Full integration with existing system

### Adetailer Parameters
- **Confidence**: Face detection confidence (0.0-1.0)
- **Denoising Strength**: Noise reduction strength (0.0-1.0)
- **Steps**: Number of generation steps
- **CFG Scale**: CFG scale for detail control
- **Sampler**: Generation sampler type
- **Face Enhancement Prompt**: Specialized prompts for face improvement

### Recommended Settings
```python
# For portraits
adetailer_config = {
    'confidence': 0.4,
    'denoising_strength': 0.5,
    'steps': 25,
    'cfg_scale': 8.0,
    'prompt': 'beautiful face, detailed eyes, perfect skin, high quality, ultra realistic'
}

# For group photos
adetailer_config = {
    'confidence': 0.3,
    'denoising_strength': 0.4,
    'steps': 20,
    'cfg_scale': 7.0,
    'prompt': 'detailed faces, natural skin, clear eyes'
}
```

For detailed documentation, see [ADETAILER_INTEGRATION.md](docs/ADETAILER_INTEGRATION.md).

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](docs/LICENSE) file for details. 