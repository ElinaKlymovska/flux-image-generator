# Enhanced FLUX Image Generator - Precision-Focused Prompts

## Огляд

Вдосконалена система промптів для FLUX Image Generator, що реалізує дві ключові стратегії:

1. **Precision-Focused Style Prompts** - уніфіковані технічні параметри для консистентної якості
2. **Context-Enriched Artistic Style Prompts** - контекстуальні анотації для цілеспрямованої генерації

## Ключові Покращення

### 1. Прецизійні Технічні Параметри

Кожен стиль тепер включає:
- **Уніфіковану роздільну здатність**: 8K для всіх стилів
- **Специфічне освітлення**: точний тип освітлення для кожного стилю
- **Детальні характеристики фону**: від нейтрального до кінематографічного
- **Фокус на ключових елементах**: від гіпер-деталізованих облич до емоційного виразу
- **Якісні стандарти**: від RAW до кінематографічної якості

### 2. Контекстуальні Use Cases

Кожен стиль має чітко визначені сценарії використання:

- **Ultra Realistic**: Professional headshots, corporate profiles, high-end fashion catalogs
- **Cinematic**: Movie posters, film promotional materials, dramatic storytelling
- **Artistic**: Art galleries, creative portfolios, luxury brand campaigns
- **Fashion**: Fashion magazines, luxury brand campaigns, runway presentations
- **Vintage**: Vintage fashion advertising, themed editorial spreads, heritage campaigns

## Доступні Стилі

### Ultra Realistic
- **Технічні характеристики**: 8K, soft natural lighting, neutral seamless background
- **Фокус**: hyper-detailed facial features, RAW image quality
- **Use Case**: Professional headshots, corporate profiles, medical aesthetics

### Cinematic
- **Технічні характеристики**: 8K, dramatic lighting, cinematic depth
- **Фокус**: emotional expression, film grain effect
- **Use Case**: Movie posters, film promotions, entertainment portfolios

### Artistic
- **Технічні характеристики**: 8K, artistic lighting, creative composition
- **Фокус**: painterly style, masterpiece quality
- **Use Case**: Art galleries, creative portfolios, luxury campaigns

### Fashion
- **Технічні характеристики**: 8K, studio lighting, editorial background
- **Фокус**: fashion presentation, magazine quality
- **Use Case**: Fashion magazines, luxury brands, runway presentations

### Vintage
- **Технічні характеристики**: 8K, retro film lighting, nostalgic background
- **Фокус**: classic beauty, heritage quality
- **Use Case**: Vintage advertising, themed editorials, heritage campaigns

### Modern
- **Технічні характеристики**: 8K, contemporary lighting, minimalist background
- **Фокус**: clean composition, professional quality
- **Use Case**: Tech profiles, modern brands, contemporary art

### Dramatic
- **Технічні характеристики**: 8K, intense lighting, dramatic background
- **Фокус**: emotional expression, theatrical quality
- **Use Case**: Theater productions, dramatic advertising, artistic exhibitions

### Soft & Dreamy
- **Технічні характеристики**: 8K, gentle lighting, ethereal background
- **Фокус**: delicate beauty, dreamlike quality
- **Use Case**: Romance novels, wedding photography, beauty campaigns

### Fantasy
- **Технічні характеристики**: 8K, ethereal lighting, mystical background
- **Фокус**: otherworldly beauty, enchanted quality
- **Use Case**: Fantasy books, gaming characters, mystical campaigns

### Sci-Fi
- **Технічні характеристики**: 8K, futuristic lighting, high tech background
- **Фокус**: technological beauty, advanced quality
- **Use Case**: Sci-fi entertainment, tech branding, futuristic products

### Film Noir
- **Технічні характеристики**: 8K, film noir lighting, mysterious background
- **Фокус**: monochromatic beauty, classic quality
- **Use Case**: Classic cinema, mystery marketing, vintage detective stories

### Impressionist
- **Технічні характеристики**: 8K, natural lighting, outdoor background
- **Фокус**: painterly beauty, artistic quality
- **Use Case**: Art exhibitions, cultural campaigns, natural products

## CLI Команди

### Перегляд доступних стилів
```bash
python -m flux_generator enhanced --list-styles
```

### Пошук стилів за use case
```bash
python -m flux_generator enhanced --use-case "fashion magazine"
```

### Пошук стилів за технічними характеристиками
```bash
python -m flux_generator enhanced --technical-spec "lighting:dramatic"
```

### Детальна інформація про стиль
```bash
python -m flux_generator enhanced --style-info "cinematic"
```

### Генерація з конкретним стилем
```bash
python -m flux_generator enhanced --style "ultra_realistic" --count 3
```

### Порівняння стилів
```bash
python -m flux_generator enhanced --compare --count 2
```

## Програмний API

### Отримання конфігурації стилю
```python
from flux_generator.config.prompts import PromptConfig

config = PromptConfig.get_prompt_config(
    style="cinematic",
    aspect_ratio="portrait",
    quality="high"
)

print(f"Prompt: {config['prompt']}")
print(f"Use Case: {config['use_case']}")
print(f"Technical Specs: {config['technical_specs']}")
```

### Пошук стилів за use case
```python
matching_styles = PromptConfig.get_prompt_by_use_case("fashion")
for style in matching_styles:
    print(f"{style['name']}: {style['use_case']}")
```

### Пошук за технічними характеристиками
```python
matching_styles = PromptConfig.get_prompt_by_technical_spec("lighting", "dramatic")
for style in matching_styles:
    print(f"{style['name']}: {style['technical_specs']}")
```

## Enhanced Generator

### Робота з enhanced генератором
```python
from flux_generator.core.enhanced import EnhancedFluxGenerator

generator = EnhancedFluxGenerator()

# Встановлення стилю
generator.set_style("cinematic")

# Отримання інформації про поточний стиль
style_info = generator.get_style_info()
print(f"Current style: {style_info['name']}")
print(f"Use case: {style_info['use_case']}")

# Пошук стилів за use case
fashion_styles = generator.find_styles_by_use_case("fashion")
print(f"Found {len(fashion_styles)} fashion styles")

# Генерація зображень
images = generator.generate_images(count=3)
```

## Якісні Налаштування

### Standard
- **prompt_upsampling**: False
- **safety_tolerance**: 2
- **Призначення**: General use

### High
- **prompt_upsampling**: True
- **safety_tolerance**: 1
- **Призначення**: Professional use

### Creative
- **prompt_upsampling**: True
- **safety_tolerance**: 3
- **Призначення**: Artistic projects

### Ultra
- **prompt_upsampling**: True
- **safety_tolerance**: 0
- **Призначення**: Premium applications

## Аспектні Співвідношення

- **portrait**: 2:3
- **square**: 1:1
- **landscape**: 3:2
- **wide**: 16:9
- **ultra_wide**: 21:9

## Переваги Нової Системи

1. **Консистентність**: Уніфіковані технічні параметри забезпечують стабільну якість
2. **Цілеспрямованість**: Use cases допомагають вибрати правильний стиль для проекту
3. **Гнучкість**: Можливість пошуку за різними критеріями
4. **Професійність**: Прецизійні параметри для професійних результатів
5. **Зручність**: CLI команди для швидкого доступу до функціональності

## Приклади Використання

### Для Fashion Magazine
```bash
python -m flux_generator enhanced --use-case "fashion magazine"
# Рекомендує: fashion, ultra_realistic, artistic
```

### Для Movie Poster
```bash
python -m flux_generator enhanced --use-case "movie poster"
# Рекомендує: cinematic, dramatic, noir
```

### Для Tech Company Profile
```bash
python -m flux_generator enhanced --use-case "tech company"
# Рекомендує: modern, ultra_realistic
```

### Для Art Gallery
```bash
python -m flux_generator enhanced --use-case "art gallery"
# Рекомендує: artistic, impressionist, fantasy
``` 