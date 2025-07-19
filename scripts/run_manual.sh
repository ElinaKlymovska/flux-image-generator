#!/bin/bash

echo "🚀 FLUX API Image Generator (Manual Mode)"
echo "========================================="

# Перевірка наявності Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 не знайдено. Встановіть Python 3.7+"
    exit 1
fi

# Перевірка наявності вхідного зображення
if [ ! -f "data/input/character.jpg" ]; then
    echo "❌ Файл data/input/character.jpg не знайдено"
    exit 1
fi

# Перевірка наявності .env файлу
if [ ! -f ".env" ]; then
    echo "⚠️  Файл .env не знайдено"
    echo "📝 Створюю .env з прикладу..."
    cp env.example .env
    echo "✅ Файл .env створено. Будь ласка, додайте ваш API ключ:"
    echo "   nano .env"
    exit 1
fi

# Встановлення залежностей з флагом --user
echo "📦 Встановлення залежностей (користувацький режим)..."
pip3 install --user -r requirements.txt

# Тестування API
echo "🧪 Тестування підключення до API..."
cd "$(dirname "$0")/.."
python3 src/flux_generator/test_api.py

echo ""
echo "🎯 Запуск генерації..."
python3 main.py 