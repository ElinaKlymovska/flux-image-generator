# Налаштування Stable Diffusion WebUI для Adetailer

## 🎯 Поточний статус

✅ **SD WebUI встановлений**: `~/stable-diffusion-webui/`
✅ **Adetailer додано**: `~/stable-diffusion-webui/extensions/adetailer/`
⏳ **SD WebUI запускається** (перший запуск займає 5-10 хвилин)

## 🚀 Запуск SD WebUI

### Перший запуск (зараз виконується)
```bash
cd ~/stable-diffusion-webui
./webui.sh --api --listen --port 7860
```

### Наступні запуски
```bash
cd ~/stable-diffusion-webui
./webui.sh --api
```

## 🔍 Перевірка статусу

```bash
# Перевірка чи SD WebUI запущений
curl http://localhost:7860/sdapi/v1/progress

# Або відкрити в браузері
open http://localhost:7860
```

## 📊 Результати обробки

### Демо версія (FLUX API)
- ✅ **Оброблено**: 46 зображень
- 📁 **Папка**: `data/output/adetailer_processed/`
- 🎯 **Тип**: Копіювання з перейменуванням

### SD WebUI версія (коли запуститься)
- 📁 **Папка**: `data/output/sd_webui_processed/`
- 🎯 **Тип**: Повна обробка з Adetailer
- ⚡ **Якість**: Висока з покращенням облич

## 🎨 Запуск обробки через SD WebUI

Коли SD WebUI буде готовий:

```bash
# Перевірка з'єднання
curl http://localhost:7860/sdapi/v1/progress

# Запуск обробки
./scripts/run_sd_webui.sh

# Або напряму
python bin/process_with_sd_webui.py
```

## ⚙️ Налаштування Adetailer

### Рекомендовані параметри
```python
adetailer_config = {
    "model": "face_yolov8n.pt",      # Модель для облич
    "confidence": 0.4,               # Впевненість детекції
    "dilation": 4,                   # Розширення маски
    "denoising_strength": 0.5,       # Сила деноїзингу
    "steps": 25,                     # Кількість кроків
    "cfg_scale": 8.0,                # CFG Scale
    "sampler": "DPM++ 2M Karras",    # Семплер
    "width": 512,                    # Ширина
    "height": 512                    # Висота
}
```

## 🔧 Моделі Adetailer

Автоматично завантажуються:
- `face_yolov8n.pt` - для облич
- `hand_yolov8n.pt` - для рук
- `person_yolov8n.pt` - для повних фігур

## 📁 Структура файлів

```
data/output/
├── [оригінальні зображення]        # 69 файлів
├── adetailer_processed/             # Демо версія (46 файлів)
└── sd_webui_processed/              # SD WebUI версія (коли готово)
```

## 🎯 Наступні кроки

1. **Зачекати запуску SD WebUI** (5-10 хвилин)
2. **Перевірити з'єднання**: `curl http://localhost:7860/sdapi/v1/progress`
3. **Запустити обробку**: `./scripts/run_sd_webui.sh`
4. **Порівняти результати** між демо та SD WebUI версіями

## 🔗 Корисні команди

```bash
# Перевірка статусу SD WebUI
curl -s http://localhost:7860/sdapi/v1/progress > /dev/null && echo "✅ Готовий" || echo "❌ Не готовий"

# Запуск обробки
./scripts/run_sd_webui.sh

# Перегляд результатів
ls -la data/output/sd_webui_processed/

# Порівняння кількості файлів
echo "Демо: $(find data/output/adetailer_processed -name '*.jpg' | wc -l)"
echo "SD WebUI: $(find data/output/sd_webui_processed -name '*.jpg' | wc -l)"
```

## 📝 Примітки

- **Перший запуск SD WebUI** займає час для завантаження моделей
- **Демо версія** показує структуру та організацію файлів
- **SD WebUI версія** надасть реальну обробку з Adetailer
- **Всі файли** зберігаються в окремих папках для порівняння 