# Prompt Tester - Automated Testing System

## 🧪 Overview

Prompt Tester - це автоматизована система для тестування різних промптів з обертанням персонажа. Вона створює організовані датасети з 15 різними промптами та 7 кутами обертання (0°, 10°, 30°, 45°, 60°, 90°, 180°).

## 🎯 Features

### 1. 15 Pre-defined Prompts
Система включає 15 різноманітних промптів:

1. **ultra_realistic** - Ультрареалістичний портрет
2. **cinematic_dramatic** - Кінематографічний драматичний
3. **artistic_painterly** - Художній живописний
4. **fashion_editorial** - Модний редакційний
5. **vintage_retro** - Вінтажний ретро
6. **modern_minimalist** - Сучасний мінімалістичний
7. **dramatic_emotional** - Драматичний емоційний
8. **soft_dreamy** - М'який мрійливий
9. **professional_corporate** - Професійний корпоративний
10. **creative_artistic** - Творчий художній
11. **elegant_sophisticated** - Елегантний вишуканий
12. **natural_outdoor** - Природний зовнішній
13. **studio_professional** - Студійний професійний
14. **expressive_character** - Експресивний характерний
15. **contemporary_urban** - Сучасний міський

### 2. Rotation Angles
Кути обертання персонажа:
- **0°** - Фронтальний вигляд
- **10°** - Легке обертання
- **30°** - Помірне обертання
- **45°** - Півоборот
- **60°** - Сильне обертання
- **90°** - Профіль
- **180°** - Повний оберт

### 3. Organized Dataset Structure
Кожен промпт створює окрему папку з метаданими:

```
data/output/datasets/
├── ultra_realistic_20241201_143022/
│   ├── metadata.json
│   ├── ultra_realistic_rotation000_seed5000.jpg
│   ├── ultra_realistic_rotation010_seed5001.jpg
│   ├── ultra_realistic_rotation030_seed5002.jpg
│   ├── ultra_realistic_rotation045_seed5003.jpg
│   ├── ultra_realistic_rotation060_seed5004.jpg
│   ├── ultra_realistic_rotation090_seed5005.jpg
│   └── ultra_realistic_rotation180_seed5006.jpg
├── cinematic_dramatic_20241201_143156/
│   ├── metadata.json
│   └── ...
└── ...
```

## 🚀 Usage

### Interactive Mode

```bash
# Запуск інтерактивного режиму
python prompt_tester_main.py

# Або через скрипт
./scripts/run_prompt_tester.sh
```

### Programmatic Usage

```python
from flux_generator import PromptTester

# Створення тестера
tester = PromptTester()

# Тестування одного промпту
prompt = tester.test_prompts[0]  # ultra_realistic
tester.test_prompt(prompt)

# Тестування всіх промптів
tester.test_all_prompts()
```

## 📊 Dataset Information

### Metadata Structure

```json
{
  "prompt_name": "ultra_realistic",
  "created_at": "2024-12-01T14:30:22.123456",
  "total_images": 7,
  "rotation_angles": [0, 10, 30, 45, 60, 90, 180],
  "prompt_text": "ultra-realistic portrait of a woman, soft natural lighting..."
}
```

### File Naming Convention

```
{prompt_name}_rotation{angle:03d}_seed{seed}.jpg
```

Приклади:
- `ultra_realistic_rotation000_seed5000.jpg`
- `cinematic_dramatic_rotation045_seed5003.jpg`
- `artistic_painterly_rotation180_seed5006.jpg`

## 🎨 Prompt Details

### 1. Ultra Realistic
```
ultra-realistic portrait of a woman, soft natural lighting, neutral background, 
high quality, detailed facial features, professional photography, 8k resolution
```
**Призначення**: Базовий фотореалістичний портрет

### 2. Cinematic Dramatic
```
cinematic portrait of a woman, dramatic lighting, shallow depth of field, 
film grain, professional cinematography, moody atmosphere, high contrast, golden hour
```
**Призначення**: Кінематографічні ефекти

### 3. Artistic Painterly
```
artistic portrait of a woman, painterly style, soft brushstrokes, 
artistic lighting, creative composition, masterpiece quality, fine art photography, oil painting effect
```
**Призначення**: Художній стиль

### 4. Fashion Editorial
```
fashion portrait of a woman, studio lighting, professional makeup, 
elegant pose, high fashion photography, magazine quality, sophisticated style, editorial look
```
**Призначення**: Модна фотографія

### 5. Vintage Retro
```
vintage portrait of a woman, retro style, film photography, 
warm tones, nostalgic atmosphere, classic beauty, timeless elegance, 1950s aesthetic
```
**Призначення**: Ретро стиль

### 6. Modern Minimalist
```
modern portrait of a woman, contemporary style, clean composition, 
minimalist background, sharp details, professional headshot quality, urban aesthetic
```
**Призначення**: Сучасний мінімалізм

### 7. Dramatic Emotional
```
dramatic portrait of a woman, intense lighting, strong shadows, 
emotional expression, powerful composition, artistic photography, chiaroscuro lighting
```
**Призначення**: Емоційні портрети

### 8. Soft Dreamy
```
soft dreamy portrait of a woman, gentle lighting, soft focus, 
ethereal atmosphere, romantic mood, delicate beauty, pastel tones, bokeh background
```
**Призначення**: Мрійливі портрети

### 9. Professional Corporate
```
professional corporate portrait of a woman, business attire, clean background, 
confident expression, executive headshot, modern office setting, professional lighting
```
**Призначення**: Корпоративні портрети

### 10. Creative Artistic
```
creative artistic portrait of a woman, abstract background, artistic composition, 
creative lighting, modern art style, contemporary photography, experimental
```
**Призначення**: Творчі експерименти

### 11. Elegant Sophisticated
```
elegant sophisticated portrait of a woman, luxury setting, refined beauty, 
high-end fashion, premium quality, sophisticated lighting, exclusive atmosphere
```
**Призначення**: Вишукані портрети

### 12. Natural Outdoor
```
natural outdoor portrait of a woman, natural lighting, outdoor setting, 
environmental portrait, nature background, organic beauty, environmental photography
```
**Призначення**: Природні портрети

### 13. Studio Professional
```
studio professional portrait of a woman, controlled lighting, studio background, 
professional equipment, commercial photography, advertising quality
```
**Призначення**: Студійна фотографія

### 14. Expressive Character
```
expressive character portrait of a woman, strong personality, character study, 
emotional depth, psychological portrait, human interest, documentary style
```
**Призначення**: Характерні портрети

### 15. Contemporary Urban
```
contemporary urban portrait of a woman, city background, modern lifestyle, 
urban aesthetic, street photography style, contemporary culture, metropolitan
```
**Призначення**: Міські портрети

## ⚙️ Configuration

### Rotation Enhancement
Кожен промпт автоматично доповнюється інформацією про обертання:

```python
# Оригінальний промпт
"ultra-realistic portrait of a woman..."

# З обертанням 45°
"ultra-realistic portrait of a woman..., rotated 45 degrees, different angle view"
```

### Quality Settings
- **prompt_upsampling**: True
- **safety_tolerance**: 2
- **aspect_ratio**: "2:3"
- **output_format**: "jpeg"

## 📈 Statistics

### Full Dataset
- **Промптів**: 15
- **Кутів обертання**: 7
- **Зображень на промпт**: 7
- **Всього зображень**: 105
- **Приблизний час**: 3.5 години
- **API запитів**: 105

### Single Prompt
- **Зображень**: 7
- **Приблизний час**: 14 хвилин
- **API запитів**: 7

## 🎯 Best Practices

### 1. Testing Strategy
- **Почати з одного промпту** для тестування
- **Використовувати вибрані промпти** для економії часу
- **Повне тестування** тільки для фінальної валідації

### 2. Resource Management
- **Моніторинг API лімітів** - 105 запитів за раз
- **Паузи між промптами** - 10 секунд
- **Паузи між зображеннями** - 3 секунди

### 3. Dataset Organization
- **Унікальні seed** для кожного промпту
- **Timestamp в назві папки** для версіонування
- **Метадані** для відстеження

## 🔧 Advanced Usage

### Custom Rotation Angles

```python
# Зміна кутів обертання
tester.rotation_angles = [0, 15, 30, 45, 60, 75, 90, 135, 180]
```

### Custom Prompts

```python
# Додавання власного промпту
custom_prompt = {
    "name": "custom_style",
    "prompt": "your custom prompt here",
    "description": "Your description"
}
tester.test_prompts.append(custom_prompt)
```

### Batch Processing

```python
# Тестування тільки певних промптів
selected_prompts = [
    tester.test_prompts[0],  # ultra_realistic
    tester.test_prompts[2],  # artistic_painterly
    tester.test_prompts[7]   # soft_dreamy
]

for prompt in selected_prompts:
    tester.test_prompt(prompt)
```

## 🚨 Troubleshooting

### Common Issues

1. **API Rate Limits**: Система автоматично обробляє помилки 429
2. **Network Timeouts**: Автоматичні повторні спроби
3. **Disk Space**: Перевірте вільне місце для 105 зображень

### Performance Tips

1. **Use SSD**: Швидше збереження файлів
2. **Stable Internet**: Стабільне з'єднання для API
3. **Monitor Resources**: Слідкуйте за використанням API

## 📊 Output Analysis

### Dataset Comparison
Порівняння результатів між різними промптами:

```python
# Аналіз метаданих
import json
from pathlib import Path

datasets_dir = Path("data/output/datasets")
for dataset in datasets_dir.glob("*"):
    with open(dataset / "metadata.json") as f:
        metadata = json.load(f)
        print(f"{metadata['prompt_name']}: {metadata['total_images']} images")
```

### Quality Assessment
- **Консистентність** між кутами обертання
- **Якість** різних стилів
- **Відповідність** промпту до результату

## 🔄 Integration

### With Enhanced Generator

```python
from flux_generator import EnhancedFluxGenerator, PromptTester

# Використання результатів тестування
tester = PromptTester()
enhanced = EnhancedFluxGenerator()

# Тестування промпту
tester.test_prompt(tester.test_prompts[0])

# Використання в enhanced generator
enhanced.set_style("realistic")
enhanced.generate_images(5)
```

### With Basic Generator

```python
from flux_generator import FluxImageGenerator, PromptTester

# Порівняння результатів
basic = FluxImageGenerator()
tester = PromptTester()

# Генерація базового набору
basic.generate_images(15)

# Тестування покращених промптів
tester.test_all_prompts()
``` 