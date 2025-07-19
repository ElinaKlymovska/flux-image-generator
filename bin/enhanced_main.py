#!/usr/bin/env python3
"""
Enhanced FLUX API Image Generator - Main Entry Point
Покращена версія генератора з інтерактивним вибором стилів
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from flux_generator import EnhancedFluxGenerator

def show_menu():
    """Показати головне меню"""
    print("\n🎨 Enhanced FLUX API Image Generator")
    print("=" * 50)
    print("1. Показати доступні стилі")
    print("2. Генерація з одним стилем")
    print("3. Порівняння стилів")
    print("4. Кастомний промпт")
    print("5. Налаштування")
    print("6. Вихід")
    print("=" * 50)

def show_styles(generator):
    """Показати доступні стилі"""
    print("\n🎨 Доступні стилі:")
    generator.list_available_styles()
    print("\n📐 Доступні аспекти:")
    generator.list_available_aspects()
    print("\n⭐ Доступні якості:")
    generator.list_available_qualities()

def single_style_generation(generator):
    """Генерація з одним стилем"""
    print("\n🎯 Генерація з одним стилем")
    
    # Показати доступні стилі
    generator.list_available_styles()
    
    # Вибір стилю
    style = input("\nВиберіть стиль (або Enter для realistic): ").strip().lower()
    if not style:
        style = "realistic"
    
    try:
        generator.set_style(style)
    except ValueError as e:
        print(f"❌ {e}")
        return
    
    # Вибір аспекту
    generator.list_available_aspects()
    aspect = input("Виберіть аспект (або Enter для portrait): ").strip().lower()
    if not aspect:
        aspect = "portrait"
    
    try:
        generator.set_aspect_ratio(aspect)
    except ValueError as e:
        print(f"❌ {e}")
        return
    
    # Вибір якості
    generator.list_available_qualities()
    quality = input("Виберіть якість (або Enter для standard): ").strip().lower()
    if not quality:
        quality = "standard"
    
    try:
        generator.set_quality(quality)
    except ValueError as e:
        print(f"❌ {e}")
        return
    
    # Кількість зображень
    try:
        count = int(input("Кількість зображень (або Enter для 3): ") or "3")
    except ValueError:
        count = 3
    
    # Генерація
    print(f"\n🚀 Запуск генерації...")
    generator.generate_images(count)

def style_comparison(generator):
    """Порівняння стилів"""
    print("\n🔄 Порівняння стилів")
    
    # Показати доступні стилі
    generator.list_available_styles()
    
    # Вибір стилів
    styles_input = input("\nВиберіть стилі через кому (або Enter для realistic,cinematic,artistic): ").strip()
    if not styles_input:
        styles = ["realistic", "cinematic", "artistic"]
    else:
        styles = [s.strip().lower() for s in styles_input.split(",")]
    
    # Кількість зображень на стиль
    try:
        count_per_style = int(input("Кількість зображень на стиль (або Enter для 2): ") or "2")
    except ValueError:
        count_per_style = 2
    
    # Генерація
    print(f"\n🚀 Запуск порівняння стилів...")
    generator.generate_style_comparison(styles, count_per_style)

def custom_prompt_generation(generator):
    """Генерація з кастомним промптом"""
    print("\n✍️ Кастомний промпт")
    
    # Вибір стилю як бази
    generator.list_available_styles()
    style = input("\nВиберіть базовий стиль (або Enter для realistic): ").strip().lower()
    if not style:
        style = "realistic"
    
    try:
        generator.set_style(style)
    except ValueError as e:
        print(f"❌ {e}")
        return
    
    # Кастомний промпт
    custom_prompt = input("Введіть ваш кастомний промпт: ").strip()
    if not custom_prompt:
        print("❌ Промпт не може бути порожнім")
        return
    
    # Кількість зображень
    try:
        count = int(input("Кількість зображень (або Enter для 2): ") or "2")
    except ValueError:
        count = 2
    
    # Генерація
    print(f"\n🚀 Запуск генерації з кастомним промптом...")
    generator.generate_images(count, custom_prompt)

def settings_menu(generator):
    """Меню налаштувань"""
    while True:
        print("\n⚙️ Налаштування")
        print("1. Змінити стиль")
        print("2. Змінити аспект")
        print("3. Змінити якість")
        print("4. Показати поточні налаштування")
        print("5. Назад")
        
        choice = input("Виберіть опцію: ").strip()
        
        if choice == "1":
            generator.list_available_styles()
            style = input("Виберіть новий стиль: ").strip().lower()
            try:
                generator.set_style(style)
                print(f"✅ Стиль змінено на: {style}")
            except ValueError as e:
                print(f"❌ {e}")
        
        elif choice == "2":
            generator.list_available_aspects()
            aspect = input("Виберіть новий аспект: ").strip().lower()
            try:
                generator.set_aspect_ratio(aspect)
                print(f"✅ Аспект змінено на: {aspect}")
            except ValueError as e:
                print(f"❌ {e}")
        
        elif choice == "3":
            generator.list_available_qualities()
            quality = input("Виберіть нову якість: ").strip().lower()
            try:
                generator.set_quality(quality)
                print(f"✅ Якість змінено на: {quality}")
            except ValueError as e:
                print(f"❌ {e}")
        
        elif choice == "4":
            config = generator.get_current_config()
            print(f"\n📋 Поточні налаштування:")
            print(f"🎨 Стиль: {config['style_name']}")
            print(f"📐 Аспект: {config['aspect_ratio']}")
            print(f"⭐ Якість: {generator.current_quality}")
            print(f"📝 Промпт: {config['prompt'][:100]}...")
        
        elif choice == "5":
            break
        
        else:
            print("❌ Невірний вибір")

def main():
    """Головна функція"""
    print("🚀 Enhanced FLUX API Image Generator - Starting...")
    
    try:
        # Перевірка наявності вхідного зображення
        input_image = Path(__file__).parent.parent / "data/input/character.jpg"
        print(f"🔍 Checking input image: {input_image}")
        
        if not input_image.exists():
            print("❌ Помилка: Файл data/input/character.jpg не знайдено")
            return
        
        print("✅ Input image found")
        
        # Створення покращеного генератора
        print("🔧 Creating enhanced generator...")
        generator = EnhancedFluxGenerator()
        print("✅ Enhanced generator created successfully")
        
        # Інтерактивне меню
        while True:
            show_menu()
            choice = input("Виберіть опцію (1-6): ").strip()
            
            if choice == "1":
                show_styles(generator)
            
            elif choice == "2":
                single_style_generation(generator)
            
            elif choice == "3":
                style_comparison(generator)
            
            elif choice == "4":
                custom_prompt_generation(generator)
            
            elif choice == "5":
                settings_menu(generator)
            
            elif choice == "6":
                print("👋 До побачення!")
                break
            
            else:
                print("❌ Невірний вибір. Спробуйте ще раз.")
            
            input("\nНатисніть Enter для продовження...")
        
    except ValueError as e:
        print(f"❌ Помилка конфігурації: {e}")
    except Exception as e:
        print(f"❌ Неочікувана помилка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 