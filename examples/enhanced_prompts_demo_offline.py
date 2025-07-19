#!/usr/bin/env python3
"""
Офлайн демонстрація вдосконаленої системи промптів FLUX Image Generator
Показує прецизійні технічні параметри та контекстуальні use cases без API
"""

import sys
from pathlib import Path

# Додаємо src до шляху для імпорту
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from flux_generator.config.prompts import PromptConfig

def demo_style_information():
    """Демонстрація детальної інформації про стилі"""
    print("🎨 Демонстрація детальної інформації про стилі")
    print("=" * 60)
    
    # Показуємо всі доступні стилі з use cases
    styles = PromptConfig.list_available_styles()
    print(f"Доступно стилів: {len(styles)}")
    print()
    
    for style in styles:
        print(f"📸 {style['name']} ({style['key']})")
        print(f"   Опис: {style['description']}")
        print(f"   Use Case: {style['use_case']}")
        print()

def demo_use_case_search():
    """Демонстрація пошуку за use case"""
    print("🔍 Демонстрація пошуку за use case")
    print("=" * 60)
    
    use_cases = [
        "fashion magazine",
        "movie poster", 
        "art gallery",
        "tech company",
        "wedding photography",
        "fantasy book",
        "sci-fi entertainment",
        "vintage advertising"
    ]
    
    for use_case in use_cases:
        print(f"Пошук стилів для: '{use_case}'")
        matching_styles = PromptConfig.get_prompt_by_use_case(use_case)
        
        if matching_styles:
            for style in matching_styles:
                print(f"  ✅ {style['name']}: {style['description']}")
        else:
            print(f"  ❌ Стилі не знайдено")
        print()

def demo_technical_specs_search():
    """Демонстрація пошуку за технічними характеристиками"""
    print("⚙️ Демонстрація пошуку за технічними характеристиками")
    print("=" * 60)
    
    specs_to_search = [
        ("lighting", "dramatic"),
        ("background", "cinematic"),
        ("quality", "RAW"),
        ("focus", "emotional"),
        ("lighting", "ethereal"),
        ("background", "mystical"),
        ("quality", "masterpiece")
    ]
    
    for spec_type, spec_value in specs_to_search:
        print(f"Пошук стилів з {spec_type} = '{spec_value}':")
        matching_styles = PromptConfig.get_prompt_by_technical_spec(spec_type, spec_value)
        
        if matching_styles:
            for style in matching_styles:
                print(f"  ✅ {style['name']}: {style['technical_specs']}")
        else:
            print(f"  ❌ Стилі не знайдено")
        print()

def demo_prompt_comparison():
    """Демонстрація порівняння промптів"""
    print("📊 Демонстрація порівняння промптів")
    print("=" * 60)
    
    styles_to_compare = ["ultra_realistic", "cinematic", "artistic", "fantasy", "sci_fi"]
    
    for style in styles_to_compare:
        config = PromptConfig.get_prompt_config(style)
        print(f"🎨 {config['style_name']}:")
        print(f"   Use Case: {config['use_case']}")
        print(f"   Освітлення: {config['technical_specs']['lighting']}")
        print(f"   Фон: {config['technical_specs']['background']}")
        print(f"   Фокус: {config['technical_specs']['focus']}")
        print(f"   Якість: {config['technical_specs']['quality']}")
        print(f"   Промпт: {config['prompt'][:100]}...")
        print()

def demo_quality_settings():
    """Демонстрація налаштувань якості"""
    print("⭐ Демонстрація налаштувань якості")
    print("=" * 60)
    
    qualities = PromptConfig.list_available_qualities()
    for quality in qualities:
        print(f"🔧 {quality['key']}: {quality['description']}")

def demo_style_details():
    """Демонстрація детальної інформації про конкретні стилі"""
    print("🔬 Демонстрація детальної інформації про стилі")
    print("=" * 60)
    
    styles_to_show = ["ultra_realistic", "cinematic", "fantasy", "sci_fi", "noir"]
    
    for style in styles_to_show:
        try:
            info = PromptConfig.get_style_info(style)
            print(f"📸 {info['name']} ({style})")
            print(f"   Опис: {info['description']}")
            print(f"   Use Case: {info['use_case']}")
            print(f"   Технічні характеристики:")
            for key, value in info['technical_specs'].items():
                print(f"     {key}: {value}")
            print(f"   Повний промпт: {info['prompt']}")
            print()
        except ValueError as e:
            print(f"❌ Помилка для стилю {style}: {e}")

def demo_cli_commands():
    """Демонстрація CLI команд"""
    print("💻 Демонстрація CLI команд")
    print("=" * 60)
    
    commands = [
        "python -m flux_generator enhanced --list-styles",
        "python -m flux_generator enhanced --use-case 'fashion magazine'",
        "python -m flux_generator enhanced --technical-spec 'lighting:dramatic'",
        "python -m flux_generator enhanced --style-info 'cinematic'",
        "python -m flux_generator enhanced --style 'fantasy' --count 3",
        "python -m flux_generator enhanced --compare --count 2"
    ]
    
    for i, command in enumerate(commands, 1):
        print(f"{i}. {command}")
    print()

def demo_programmatic_api():
    """Демонстрація програмного API"""
    print("🔧 Демонстрація програмного API")
    print("=" * 60)
    
    print("1. Отримання конфігурації стилю:")
    config = PromptConfig.get_prompt_config("cinematic")
    print(f"   Стиль: {config['style_name']}")
    print(f"   Use Case: {config['use_case']}")
    print(f"   Технічні характеристики: {config['technical_specs']}")
    print()
    
    print("2. Пошук стилів за use case:")
    fashion_styles = PromptConfig.get_prompt_by_use_case("fashion")
    for style in fashion_styles:
        print(f"   {style['name']}: {style['use_case']}")
    print()
    
    print("3. Пошук за технічними характеристиками:")
    dramatic_styles = PromptConfig.get_prompt_by_technical_spec("lighting", "dramatic")
    for style in dramatic_styles:
        print(f"   {style['name']}: {style['technical_specs']}")
    print()

def demo_enhancement_comparison():
    """Демонстрація порівняння до/після вдосконалення"""
    print("📈 Порівняння до/після вдосконалення")
    print("=" * 60)
    
    print("ДО вдосконалення:")
    print("  ❌ Всі промпти зафіксовані на 'portrait of a woman'")
    print("  ❌ Базові технічні параметри")
    print("  ❌ Відсутні use cases")
    print("  ❌ 8 стилів")
    print("  ❌ Прості промпти")
    print()
    
    print("ПІСЛЯ вдосконалення:")
    print("  ✅ Різноманітність об'єктів та стилів")
    print("  ✅ Прецизійні технічні параметри (8K, специфічне освітлення)")
    print("  ✅ Контекстуальні use cases для кожного стилю")
    print("  ✅ 12 стилів з новими: Fantasy, Sci-Fi, Film Noir, Impressionist")
    print("  ✅ Детальні промпти з технічними специфікаціями")
    print("  ✅ Пошук за use case та технічними характеристиками")
    print("  ✅ Уніфіковані якісні стандарти")
    print()

def main():
    """Головна функція демонстрації"""
    print("🎭 FLUX Image Generator - Enhanced Prompts Demo (Offline)")
    print("=" * 80)
    print("Демонстрація вдосконаленої системи промптів з прецизійними параметрами")
    print("та контекстуальними use cases (без підключення до API)")
    print()
    
    try:
        # Демонстрації
        demo_style_information()
        demo_use_case_search()
        demo_technical_specs_search()
        demo_quality_settings()
        demo_prompt_comparison()
        demo_style_details()
        demo_cli_commands()
        demo_programmatic_api()
        demo_enhancement_comparison()
        
        print("✅ Офлайн демонстрація завершена успішно!")
        print()
        print("💡 Ключові переваги нової системи:")
        print("  1. Прецизійні технічні параметри для консистентної якості")
        print("  2. Контекстуальні use cases для цілеспрямованої генерації")
        print("  3. Розширена різноманітність стилів (12 замість 8)")
        print("  4. Зручні CLI команди для пошуку та фільтрації")
        print("  5. Програмний API для інтеграції")
        print("  6. Уніфіковані якісні стандарти (8K для всіх стилів)")
        print()
        print("🚀 Готово до використання з реальним API!")
        
    except Exception as e:
        print(f"❌ Помилка під час демонстрації: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 