# Enhanced FLUX API Image Generator - Features

## 🎨 Overview

Enhanced FLUX API Image Generator - це покращена версія базового генератора з підтримкою різних стилів, аспектів та якостей генерації. Вона дозволяє створювати більш різноманітні та якісні зображення.

## 🚀 New Features

### 1. Multiple Styles
Підтримка 8 різних стилів генерації:

- **Ultra Realistic** - Фотореалістичний портрет з природним освітленням
- **Cinematic** - Кінематографічний стиль з драматичним освітленням
- **Artistic** - Художній стиль з живописними ефектами
- **Fashion** - Модний портрет в стилі fashion фотографії
- **Vintage** - Вінтажний стиль з ретро атмосферою
- **Modern** - Сучасний мінімалістичний стиль
- **Dramatic** - Драматичний стиль з сильними контрастами
- **Soft & Dreamy** - М'який мрійливий стиль з ефірною атмосферою

### 2. Aspect Ratios
Підтримка різних співвідношень сторін:

- **Portrait** (2:3) - Вертикальний формат
- **Square** (1:1) - Квадратний формат
- **Landscape** (3:2) - Горизонтальний формат
- **Wide** (16:9) - Широкий формат

### 3. Quality Settings
Три рівні якості генерації:

- **Standard** - Базова якість
- **High** - Висока якість з upsampling
- **Creative** - Творчий режим з більшою свободою

### 4. Interactive Interface
Інтерактивне меню з можливістю:

- Вибору стилів та налаштувань
- Порівняння різних стилів
- Використання кастомних промптів
- Налаштування параметрів

## 📁 File Structure

```
src/flux_generator/
├── generator.py              # Базовий генератор
├── enhanced_generator.py     # Покращений генератор
├── prompts.py               # Конфігурація промптів
└── test_api.py              # Тестування API

enhanced_main.py              # Інтерактивний інтерфейс
```

## 🎯 Usage Examples

### Basic Usage

```python
from flux_generator import EnhancedFluxGenerator

# Створення генератора
generator = EnhancedFluxGenerator()

# Встановлення стилю
generator.set_style("cinematic")
generator.set_aspect_ratio("portrait")
generator.set_quality("high")

# Генерація зображень
generator.generate_images(5)
```

### Style Comparison

```python
# Порівняння різних стилів
generator.generate_style_comparison(
    styles=["realistic", "cinematic", "artistic"],
    count_per_style=2
)
```

### Custom Prompts

```python
# Генерація з кастомним промптом
custom_prompt = "portrait of a woman in a magical forest, fantasy style"
generator.generate_images(3, custom_prompt)
```

## 🎨 Style Details

### Ultra Realistic
```
ultra-realistic portrait of a woman, soft natural lighting, neutral background, 
high quality, detailed facial features, professional photography, 8k resolution
```
**Призначення**: Фотореалістичні портрети для професійного використання

### Cinematic
```
cinematic portrait of a woman, dramatic lighting, shallow depth of field, 
film grain, professional cinematography, moody atmosphere, high contrast
```
**Призначення**: Кінематографічні портрети з драматичним освітленням

### Artistic
```
artistic portrait of a woman, painterly style, soft brushstrokes, 
artistic lighting, creative composition, masterpiece quality, fine art photography
```
**Призначення**: Художні портрети з живописними ефектами

### Fashion
```
fashion portrait of a woman, studio lighting, professional makeup, 
elegant pose, high fashion photography, magazine quality, sophisticated style
```
**Призначення**: Модні портрети для fashion індустрії

### Vintage
```
vintage portrait of a woman, retro style, film photography, 
warm tones, nostalgic atmosphere, classic beauty, timeless elegance
```
**Призначення**: Вінтажні портрети з ретро атмосферою

### Modern
```
modern portrait of a woman, contemporary style, clean composition, 
minimalist background, sharp details, professional headshot quality
```
**Призначення**: Сучасні мінімалістичні портрети

### Dramatic
```
dramatic portrait of a woman, intense lighting, strong shadows, 
emotional expression, powerful composition, artistic photography
```
**Призначення**: Драматичні портрети з сильними контрастами

### Soft & Dreamy
```
soft dreamy portrait of a woman, gentle lighting, soft focus, 
ethereal atmosphere, romantic mood, delicate beauty, pastel tones
```
**Призначення**: М'які мрійливі портрети з ефірною атмосферою

## ⚙️ Configuration

### Quality Settings

| Setting | prompt_upsampling | safety_tolerance | Description |
|---------|------------------|------------------|-------------|
| Standard | False | 2 | Базова якість, безпечний режим |
| High | True | 1 | Висока якість з upsampling |
| Creative | True | 3 | Творчий режим з більшою свободою |

### Aspect Ratios

| Ratio | Dimensions | Use Case |
|-------|------------|----------|
| 2:3 | Portrait | Вертикальні портрети |
| 1:1 | Square | Квадратні зображення |
| 3:2 | Landscape | Горизонтальні зображення |
| 16:9 | Wide | Широкі зображення |

## 🎯 Best Practices

### 1. Style Selection
- **Realistic**: Для професійних портретів
- **Cinematic**: Для драматичних ефектів
- **Artistic**: Для творчих проектів
- **Fashion**: Для модної фотографії
- **Vintage**: Для ретро стилю
- **Modern**: Для сучасних проектів
- **Dramatic**: Для емоційних портретів
- **Soft**: Для романтичних зображень

### 2. Quality Settings
- **Standard**: Для швидкого тестування
- **High**: Для фінальних результатів
- **Creative**: Для експериментів

### 3. Aspect Ratios
- **Portrait**: Найкраще для портретів
- **Square**: Для соціальних мереж
- **Landscape**: Для широких зображень
- **Wide**: Для кінематографічних ефектів

## 🔧 Advanced Usage

### Custom Prompt Creation

```python
# Створення власного промпту на основі існуючого стилю
base_config = PromptConfig.get_prompt_config("realistic")
custom_prompt = base_config["prompt"] + ", wearing a red dress, outdoor setting"

generator.generate_images(2, custom_prompt)
```

### Batch Processing

```python
# Генерація зображень у різних стилях
styles = ["realistic", "cinematic", "artistic"]
for style in styles:
    generator.set_style(style)
    generator.generate_images(3)
```

### Configuration Management

```python
# Збереження та відновлення конфігурації
config = generator.get_current_config()
print(f"Current style: {config['style_name']}")
print(f"Current aspect: {config['aspect_ratio']}")
```

## 🚨 Troubleshooting

### Common Issues

1. **Style not found**: Перевірте правильність назви стилю
2. **Aspect ratio error**: Використовуйте тільки підтримувані аспекти
3. **Quality setting invalid**: Використовуйте standard, high або creative

### Performance Tips

1. **Use appropriate quality**: Standard для тестування, High для фінальних результатів
2. **Limit batch size**: Генеруйте не більше 5-10 зображень за раз
3. **Monitor API limits**: Дотримуйтесь лімітів API

## 📊 Output Organization

Покращений генератор зберігає зображення в окремій папці:

```
data/output/enhanced/
├── realistic_2000.jpg
├── realistic_2001.jpg
├── cinematic_2002.jpg
├── artistic_2003.jpg
└── ...
```

## 🔄 Migration from Basic Generator

Для переходу з базового генератора:

```python
# Старий код
from flux_generator import FluxImageGenerator
generator = FluxImageGenerator()
generator.generate_images(15)

# Новий код
from flux_generator import EnhancedFluxGenerator
generator = EnhancedFluxGenerator()
generator.set_style("realistic")  # Еквівалент базовому
generator.generate_images(15)
``` 