#!/usr/bin/env python3
"""
FLUX API Image Generator - Main Entry Point
Генерація реалістичних зображень жінки за допомогою BFL.ai FLUX API
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from flux_generator import FluxImageGenerator

def main():
    """Головна функція"""
    print("🚀 FLUX API Image Generator - Starting...")
    
    try:
        # Перевірка наявності вхідного зображення
        input_image = Path("data/input/character.jpg")
        print(f"🔍 Checking input image: {input_image}")
        
        if not input_image.exists():
            print("❌ Помилка: Файл data/input/character.jpg не знайдено")
            return
        
        print("✅ Input image found")
        
        # Створення генератора
        print("🔧 Creating generator...")
        generator = FluxImageGenerator()
        print("✅ Generator created successfully")
        
        # Генерація 15 зображень
        print("🎯 Starting image generation...")
        generator.generate_images(15)
        
    except ValueError as e:
        print(f"❌ Помилка конфігурації: {e}")
    except Exception as e:
        print(f"❌ Неочікувана помилка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 