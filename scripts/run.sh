#!/bin/bash

echo "🚀 FLUX API Image Generator"
echo "=========================="

# Перевірка наявності Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 не знайдено. Встановіть Python 3.7+"
    exit 1
fi

# Перевірка наявності вхідного зображення
if [ ! -f "character.jpg" ]; then
    echo "❌ Файл character.jpg не знайдено"
    exit 1
fi

# Перевірка наявності .env файлу
if [ ! -f ".env" ]; then
    echo "⚠️  Файл .env не знайдено"
    echo "📝 Створюю .env з прикладу..."
    cp config/project/env.example .env
    echo "✅ Файл .env створено. Будь ласка, додайте ваш API ключ:"
    echo "   nano .env"
    exit 1
fi

# Створення та активація віртуального середовища
echo "🐍 Створення віртуального середовища..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Віртуальне середовище створено"
else
    echo "✅ Віртуальне середовище вже існує"
fi

# Активація віртуального середовища
echo "🔧 Активація віртуального середовища..."
source venv/bin/activate

# Встановлення залежностей
echo "📦 Встановлення залежностей..."
pip install -r requirements.txt

# Тестування API
echo "🧪 Тестування підключення до API..."
python bin/prompt_tester_main.py

echo ""
echo "🎯 Запуск генерації..."
cd "$(dirname "$0")/.."
python bin/main.py

# Деактивація віртуального середовища
deactivate 