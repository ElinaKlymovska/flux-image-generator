# Stable Diffusion WebUI Integration with Adetailer

Цей документ описує як інтегрувати наш проект з Stable Diffusion WebUI для обробки зображень з Adetailer.

## 🎯 Огляд

Stable Diffusion WebUI (Automatic1111) - це найпопулярніший інструмент для роботи зі Stable Diffusion, який має повну підтримку Adetailer для покращення облич.

## 📋 Вимоги

- Python 3.8+
- Git
- CUDA-сумісна GPU (рекомендовано)
- Мінімум 8GB VRAM для роботи з Adetailer

## 🚀 Встановлення Stable Diffusion WebUI

### 1. Клонування репозиторію

```bash
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui
cd stable-diffusion-webui
```

### 2. Встановлення Adetailer

```bash
git clone https://github.com/Bing-su/adetailer extensions/adetailer
```

### 3. Запуск з API

```bash
./webui.sh --api
```

Або для Windows:
```bash
webui.bat --api
```

## 🔧 Налаштування

### Моделі для Adetailer

За замовчуванням використовується `face_yolov8n.pt`. Додаткові моделі можна завантажити:

- `face_yolov8n.pt` - швидка модель для облич
- `face_yolov8s.pt` - середня швидкість та якість
- `face_yolov8m.pt` - повільна, але висока якість
- `hand_yolov8n.pt` - для рук
- `person_yolov8n.pt` - для повних фігур

### Параметри Adetailer

```python
adetailer_config = {
    "model": "face_yolov8n.pt",      # Модель детекції
    "confidence": 0.3,               # Впевненість детекції (0.1-1.0)
    "dilation": 4,                   # Розширення маски (0-10)
    "denoising_strength": 0.4,       # Сила деноїзингу (0.1-1.0)
    "steps": 20,                     # Кількість кроків
    "cfg_scale": 7.0,                # CFG Scale
    "sampler": "DPM++ 2M Karras",    # Семплер
    "width": 512,                    # Ширина
    "height": 512                    # Висота
}
```

## 💻 Використання

### Через Python

```python
from src.flux_generator.core.sd_webui_client import SDWebUIClient

# Ініціалізація клієнта
client = SDWebUIClient("http://localhost:7860")

# Перевірка з'єднання
if not client.test_connection():
    print("SD WebUI не запущений")
    exit(1)

# Обробка одного зображення
from pathlib import Path
image_path = Path("data/output/image.jpg")

processed_data = client.process_image_with_adetailer(
    image_path=image_path,
    prompt="beautiful face, detailed eyes, perfect skin",
    adetailer_config={
        "confidence": 0.4,
        "denoising_strength": 0.5,
        "steps": 25
    }
)

# Збереження результату
if processed_data:
    with open("enhanced_image.jpg", "wb") as f:
        f.write(processed_data)
```

### Обробка множинних зображень

```python
from pathlib import Path

# Знаходження всіх зображень
input_dir = Path("data/output")
image_files = list(input_dir.rglob("*.jpg")) + list(input_dir.rglob("*.png"))

# Обробка
output_dir = Path("data/output/sd_webui_processed")
processed_paths = client.process_multiple_images(
    image_paths=image_files,
    output_dir=output_dir,
    prompt="beautiful face, detailed eyes, perfect skin, high quality",
    negative_prompt="blurry, low quality, distorted",
    adetailer_config={
        "model": "face_yolov8n.pt",
        "confidence": 0.4,
        "denoising_strength": 0.5,
        "steps": 25,
        "cfg_scale": 8.0
    },
    output_suffix="_adetailer"
)

print(f"Оброблено {len(processed_paths)} зображень")
```

### Через скрипти

```bash
# Запуск обробки
./scripts/run_sd_webui.sh

# Або напряму
python bin/process_with_sd_webui.py
```

## 📁 Структура файлів

```
src/flux_generator/core/
└── sd_webui_client.py          # Клієнт для SD WebUI API

bin/
└── process_with_sd_webui.py    # Скрипт обробки

scripts/
└── run_sd_webui.sh            # Shell скрипт

data/output/
├── [оригінальні зображення]
└── sd_webui_processed/         # Оброблені зображення
    ├── image1_adetailer.jpg
    ├── image2_adetailer.jpg
    └── ...
```

## ⚙️ Налаштування параметрів

### Рекомендовані налаштування для облич

```python
# Для портретів
portrait_config = {
    "model": "face_yolov8n.pt",
    "confidence": 0.3,
    "dilation": 4,
    "denoising_strength": 0.4,
    "steps": 20,
    "cfg_scale": 7.0,
    "prompt": "beautiful face, detailed eyes, perfect skin, high quality"
}

# Для високої якості
high_quality_config = {
    "model": "face_yolov8s.pt",
    "confidence": 0.4,
    "dilation": 6,
    "denoising_strength": 0.5,
    "steps": 30,
    "cfg_scale": 8.0,
    "prompt": "ultra realistic face, detailed facial features, perfect skin texture"
}
```

## 🔍 Діагностика проблем

### SD WebUI не запущений

```bash
# Перевірка статусу
curl http://localhost:7860/sdapi/v1/progress

# Запуск з API
./webui.sh --api --listen
```

### Помилки Adetailer

1. **Модель не знайдена**: Завантажте модель в `models/adetailer/`
2. **Недостатньо VRAM**: Зменшіть розмір зображення або використовуйте CPU
3. **Повільна обробка**: Використовуйте меншу модель або зменшіть кількість кроків

### Логування

```python
import logging
logging.basicConfig(level=logging.INFO)

# Детальне логування
client = SDWebUIClient("http://localhost:7860")
```

## 🚀 Оптимізація продуктивності

### Для швидкої обробки

```python
fast_config = {
    "model": "face_yolov8n.pt",
    "confidence": 0.3,
    "steps": 15,
    "width": 512,
    "height": 512
}
```

### Для високої якості

```python
quality_config = {
    "model": "face_yolov8s.pt",
    "confidence": 0.4,
    "steps": 30,
    "width": 768,
    "height": 768
}
```

## 🔗 Корисні посилання

- [Stable Diffusion WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- [Adetailer Extension](https://github.com/Bing-su/adetailer)
- [SD WebUI API Documentation](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/API)
- [Adetailer Documentation](https://github.com/Bing-su/adetailer/wiki)

## 📝 Примітки

1. **Приватність**: SD WebUI працює локально, ваші зображення не передаються стороннім сервісам
2. **Продуктивність**: Швидкість обробки залежить від вашої GPU
3. **Якість**: Більше кроків = краща якість, але повільніша обробка
4. **Моделі**: Різні моделі Adetailer оптимізовані для різних типів об'єктів 