# FLUX API Image Generator

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python package for generating realistic images using BFL.ai FLUX API. This project creates high-quality portraits while preserving facial features and body structure from an input image.

## 🌟 Features

- 🎨 Generate realistic portraits using FLUX API
- 🔧 Customizable prompts and parameters
- 📁 Organized file structure with proper Python packaging
- 🐍 Modern Python project structure
- 🔒 Secure API key management
- 📊 Batch image generation
- 🧪 Built-in API testing
- 📚 Comprehensive documentation

## 📋 Requirements

- Python 3.8+
- BFL.ai API key
- Input image `character.jpg`

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/ElinaKlymovska/flux-image-generator.git
cd flux-image-generator
```

### 2. Install Dependencies

```bash
# Using the provided script (recommended)
./scripts/run.sh

# Or manually
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure API Key

```bash
cp env.example .env
# Edit .env and add your BFL_API_KEY
```

### 4. Run Generation

```bash
python main.py
```

## 📁 Project Structure

```
flux-image-generator/
├── src/
│   └── flux_generator/
│       ├── __init__.py          # Package initialization
│       ├── generator.py         # Main generator class
│       └── test_api.py          # API testing utilities
├── data/
│   ├── input/
│   │   └── character.jpg        # Input image
│   └── output/                  # Generated images
├── scripts/
│   ├── run.sh                   # Quick start script
│   └── run_manual.sh            # Manual setup script
├── docs/
│   └── README.md                # Detailed documentation
├── tests/                       # Test files
├── main.py                      # Entry point
├── requirements.txt             # Python dependencies
├── setup.py                     # Package setup
├── pyproject.toml              # Modern Python packaging
├── env.example                 # Environment template
└── README.md                   # This file
```

## 🎯 Usage

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
    "prompt": "ultra-realistic portrait of a woman, soft natural lighting",
    "input_image": "data/input/character.jpg",
    "seed": 1234,
    "aspect_ratio": "2:3",
    "output_format": "jpeg"
}
```

## ⚙️ Configuration

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

## 🧪 Testing

```bash
# Test API connection
python src/flux_generator/test_api.py

# Run all tests (when implemented)
python -m pytest tests/
```

## 🔧 Development

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

## 📊 Generated Images

Images are saved in `data/output/` with names:
- `woman_00_seed1000.jpg`
- `woman_01_seed1001.jpg`
- `woman_02_seed1002.jpg`
- etc.

## 🚨 Troubleshooting

### API Key Issues
- Ensure your API key is correct and active
- Check that `.env` file exists and contains `BFL_API_KEY`
- Verify API key format (no quotes needed)

### Network Issues
- Check internet connection
- API has rate limits - wait between requests
- Generation may take 10-15 minutes for 15 images

### Python Environment Issues
```bash
# Use virtual environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📚 Documentation

For detailed documentation, see [docs/README.md](docs/README.md).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [BFL.ai](https://bfl.ai) for providing the FLUX API
- Python community for excellent tools and libraries

---

## 🇺🇦 Ukrainian Version

### Опис

Цей проєкт генерує 15+ реалістичних зображень жінки, зберігаючи риси обличчя та фігуру з вхідного зображення `character.jpg`. Використовується стиль ultra-realistic з м'яким природним освітленням та нейтральним фоном.

### Швидкий запуск

```bash
# Клонування та налаштування
git clone https://github.com/ElinaKlymovska/flux-image-generator.git
cd flux-image-generator

# Встановлення залежностей
./scripts/run.sh

# Налаштування API ключа
cp env.example .env
# Відредагуйте .env та додайте ваш API ключ

# Запуск генерації
python main.py
```

### Отримання API ключа

1. Зареєструйтесь на [BFL.ai](https://bfl.ai)
2. Перейдіть до розділу API Keys
3. Створіть новий API ключ
4. Додайте ключ до файлу `.env`

### Вирішення проблем

- Переконайтеся в правильності API ключа
- Використовуйте віртуальне середовище
- Перевірте інтернет-з'єднання
- Генерація може зайняти 10-15 хвилин 