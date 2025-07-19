#!/bin/bash

# Prompt Tester Runner
# Скрипт для запуску автоматичного тестування промптів

echo "🧪 Prompt Tester for FLUX API Image Generator"
echo "============================================="

# Перевірка наявності віртуального середовища
if [ ! -d "venv" ]; then
    echo "❌ Віртуальне середовище не знайдено. Створюю..."
    python3 -m venv venv
fi

# Активація віртуального середовища
echo "🔧 Активація віртуального середовища..."
source venv/bin/activate

# Перевірка залежностей
echo "📦 Перевірка залежностей..."
pip install -e . > /dev/null 2>&1

# Перевірка наявності вхідного зображення
if [ ! -f "data/input/character.jpg" ]; then
    echo "❌ Помилка: Файл data/input/character.jpg не знайдено"
    echo "   Переконайтеся, що зображення знаходиться в папці data/input/"
    exit 1
fi

# Перевірка API ключа
if [ ! -f ".env" ]; then
    echo "❌ Помилка: Файл .env не знайдено"
    echo "   Скопіюйте env.example в .env та додайте ваш API ключ"
    exit 1
fi

echo "✅ Всі перевірки пройдені"
echo "🚀 Запуск Prompt Tester..."
echo ""

# Запуск тестування промптів
python prompt_tester_main.py 