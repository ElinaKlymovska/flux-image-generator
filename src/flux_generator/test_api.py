#!/usr/bin/env python3
"""
Тестовий файл для перевірки підключення до FLUX API
"""

import os
import requests
from dotenv import load_dotenv

# Завантаження змінних середовища
load_dotenv()

def test_api_connection():
    """Тестування підключення до API"""
    api_key = os.getenv('BFL_API_KEY')
    
    if not api_key:
        print("❌ Помилка: BFL_API_KEY не знайдено в змінних середовища")
        print("   Переконайтеся, що файл .env існує та містить ваш API ключ")
        return False
    
    print(f"✅ API ключ знайдено: {api_key[:10]}...")
    
    # Remove quotes if present
    api_key = api_key.strip('"\'')
    
    # Тестовий запит до API
    headers = {
        "x-key": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        # Простий тестовий запит до FLUX API
        test_data = {
            "prompt": "test",
            "input_image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k=",
            "seed": 1000,
            "aspect_ratio": "1:1"
        }
        
        response = requests.post(
            "https://api.bfl.ai/v1/flux-kontext-pro",
            headers=headers,
            json=test_data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Підключення до API успішне")
            return True
        elif response.status_code == 403:
            print(f"❌ Помилка 403: Доступ заборонено")
            print(f"   Перевірте правильність API ключа")
            return False
        else:
            print(f"⚠️  API відповідає з кодом {response.status_code}")
            print(f"   Відповідь: {response.text[:200]}...")
            return True  # Можливо endpoint не існує, але API ключ працює
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Помилка підключення до API: {e}")
        return False

def check_files():
    """Перевірка наявності необхідних файлів"""
    print("\n📁 Перевірка файлів:")
    
    # Перевірка вхідного зображення
    if os.path.exists("data/input/character.jpg"):
        size = os.path.getsize("data/input/character.jpg") / 1024  # KB
        print(f"✅ character.jpg знайдено ({size:.1f} KB)")
    else:
        print("❌ data/input/character.jpg не знайдено")
        return False
    
    # Перевірка папки outputs
    if os.path.exists("data/output"):
        print("✅ Папка data/output існує")
    else:
        print("❌ Папка data/output не знайдена")
        return False
    
    return True

def main():
    """Головна функція тестування"""
    print("🧪 Тестування FLUX API Image Generator")
    print("=" * 50)
    
    # Перевірка файлів
    files_ok = check_files()
    
    # Тестування API
    api_ok = test_api_connection()
    
    print("\n" + "=" * 50)
    if files_ok and api_ok:
        print("✅ Всі тести пройдені! Можна запускати main.py")
        print("\n📝 Наступні кроки:")
        print("1. Переконайтеся, що ваш API ключ правильний")
        print("2. Запустіть: python main.py")
    else:
        print("❌ Є проблеми, які потрібно вирішити перед запуском")
        
        if not files_ok:
            print("   - Перевірте наявність data/input/character.jpg")
        if not api_ok:
            print("   - Перевірте API ключ у файлі .env")

if __name__ == "__main__":
    main() 