# Adetailer Integration

Цей документ описує інтеграцію з Adetailer для покращення реалістичності облич у згенерованих зображеннях.

## Огляд

Adetailer - це інструмент для автоматичного покращення деталей облич у зображеннях. Він використовує машинне навчання для виявлення облич та застосування покращень до їх деталей.

## Особливості

- **Автоматичне виявлення облич**: Використовує YOLOv8 модель для точного виявлення облич
- **Покращення деталей**: Застосовує спеціальні промпти для покращення якості облич
- **Налаштування параметрів**: Гнучкі налаштування для різних сценаріїв
- **Batch обробка**: Підтримка генерації множинних зображень
- **Інтеграція з FLUX API**: Повна інтеграція з існуючою системою

## Встановлення

1. Переконайтеся, що у вас встановлені всі залежності:
```bash
pip install -r requirements.txt
```

2. Налаштуйте API ключ:
```bash
export FLUX_API_KEY="your_api_key_here"
```

3. Помістіть вхідне зображення в `data/input/character.jpg`

## Використання

### Базове використання

```python
from src.flux_generator.core.adetailer import AdetailerGenerator

# Ініціалізація генератора
generator = AdetailerGenerator()

# Генерація одного зображення
output_path = generator.generate_with_adetailer()
print(f"Згенеровано: {output_path}")
```

### Batch генерація

```python
# Генерація множинних зображень
output_paths = generator.generate_multiple_with_adetailer(count=5)
for path in output_paths:
    print(f"Згенеровано: {path}")
```

### Налаштування параметрів

```python
# Оновлення налаштувань Adetailer
generator.update_adetailer_settings(
    confidence=0.5,
    denoising_strength=0.6,
    steps=30,
    cfg_scale=9.0,
    prompt="ultra detailed face, perfect skin texture"
)

# Генерація з кастомними налаштуваннями
adetailer_config = {
    'confidence': 0.4,
    'denoising_strength': 0.5,
    'steps': 25,
    'cfg_scale': 8.0
}

output_path = generator.generate_with_adetailer(
    prompt="A beautiful woman with realistic face details",
    seed=12345,
    adetailer_config=adetailer_config
)
```

## CLI Команди

### Генерація одного зображення

```bash
python -m src.flux_generator.cli.adetailer_commands generate \
    --prompt "A beautiful woman with realistic face details" \
    --seed 12345 \
    --confidence 0.4 \
    --denoising-strength 0.5 \
    --steps 25 \
    --cfg-scale 8.0
```

### Batch генерація

```bash
python -m src.flux_generator.cli.adetailer_commands batch \
    --count 5 \
    --start-seed 1000 \
    --confidence 0.3 \
    --denoising-strength 0.4
```

### Тестування з'єднання

```bash
python -m src.flux_generator.cli.adetailer_commands test
```

### Налаштування параметрів

```bash
python -m src.flux_generator.cli.adetailer_commands configure \
    --confidence 0.5 \
    --denoising-strength 0.6 \
    --steps 30 \
    --cfg-scale 9.0 \
    --prompt "ultra detailed face, perfect skin texture"
```

## Shell Скрипти

### Запуск генерації

```bash
# Генерація одного зображення
./scripts/run_adetailer.sh

# Batch генерація
./scripts/run_adetailer_batch.sh
```

## Параметри Adetailer

### Основні параметри

| Параметр | Тип | За замовчуванням | Опис |
|----------|-----|------------------|------|
| `enabled` | bool | `True` | Включити/виключити Adetailer |
| `model` | str | `"face_yolov8n.pt"` | Модель для виявлення облич |
| `confidence` | float | `0.3` | Впевненість виявлення (0.0-1.0) |
| `dilation` | int | `4` | Фактор розширення |
| `denoising_strength` | float | `0.4` | Сила шумоподавлення (0.0-1.0) |

### Параметри генерації

| Параметр | Тип | За замовчуванням | Опис |
|----------|-----|------------------|------|
| `prompt` | str | `"beautiful face, detailed eyes, perfect skin, high quality"` | Промпт для покращення облич |
| `negative_prompt` | str | `"blurry, low quality, distorted, deformed"` | Негативний промпт |
| `steps` | int | `20` | Кількість кроків генерації |
| `cfg_scale` | float | `7.0` | CFG масштаб |
| `sampler` | str | `"DPM++ 2M Karras"` | Семплер |
| `width` | int | `512` | Ширина для обробки облич |
| `height` | int | `512` | Висота для обробки облич |

## Рекомендації

### Для портретів

```python
adetailer_config = {
    'confidence': 0.4,
    'denoising_strength': 0.5,
    'steps': 25,
    'cfg_scale': 8.0,
    'prompt': 'beautiful face, detailed eyes, perfect skin, high quality, ultra realistic'
}
```

### Для групових фото

```python
adetailer_config = {
    'confidence': 0.3,
    'denoising_strength': 0.4,
    'steps': 20,
    'cfg_scale': 7.0,
    'prompt': 'detailed faces, natural skin, clear eyes'
}
```

### Для художніх портретів

```python
adetailer_config = {
    'confidence': 0.5,
    'denoising_strength': 0.6,
    'steps': 30,
    'cfg_scale': 9.0,
    'prompt': 'artistic face, detailed features, perfect composition'
}
```

## Приклади

Дивіться `examples/generate_adetailer_example.py` для повних прикладів використання.

## Тестування

Запустіть тести:

```bash
pytest tests/test_adetailer.py -v
```

## Структура файлів

```
src/flux_generator/
├── core/
│   └── adetailer.py              # Основний модуль Adetailer
├── cli/
│   └── adetailer_commands.py     # CLI команди
bin/
├── generate_adetailer.py         # Скрипт генерації
└── generate_adetailer_batch.py   # Скрипт batch генерації
scripts/
├── run_adetailer.sh              # Shell скрипт
└── run_adetailer_batch.sh        # Shell скрипт batch
examples/
└── generate_adetailer_example.py # Приклади використання
tests/
└── test_adetailer.py             # Тести
docs/
└── ADETAILER_INTEGRATION.md      # Ця документація
```

## Troubleshooting

### Проблеми з виявленням облич

- Збільшіть `confidence` до 0.4-0.5
- Переконайтеся, що обличчя добре видно на вхідному зображенні
- Спробуйте різні значення `dilation`

### Проблеми з якістю

- Збільшіть `steps` до 25-30
- Збільшіть `cfg_scale` до 8.0-9.0
- Налаштуйте `denoising_strength` (0.3-0.6)

### Проблеми з API

- Перевірте API ключ
- Перевірте з'єднання з інтернетом
- Спробуйте зменшити кількість запитів

## Ліцензія

Цей модуль використовується під тією ж ліцензією, що й основний проект. 