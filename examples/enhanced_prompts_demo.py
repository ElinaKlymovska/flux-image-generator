#!/usr/bin/env python3
"""
Демонстрація вдосконаленої системи промптів FLUX Image Generator
Показує прецизійні технічні параметри та контекстуальні use cases
"""

import sys
from pathlib import Path

# Додаємо src до шляху для імпорту
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from flux_generator.config.prompts import PromptConfig
from flux_generator.core.enhanced import EnhancedFluxGenerator
from flux_generator.utils.logger import setup_logger

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
        "wedding photography"
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
        ("focus", "emotional")
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

def demo_enhanced_generator():
    """Демонстрація роботи з enhanced генератором"""
    print("🚀 Демонстрація роботи з Enhanced Generator")
    print("=" * 60)
    
    try:
        generator = EnhancedFluxGenerator()
        
        # Показуємо поточну конфігурацію
        config = generator.get_current_config()
        print(f"Поточна конфігурація:")
        print(f"  Стиль: {config['style_name']}")
        print(f"  Аспект: {config['aspect_ratio']}")
        print(f"  Use Case: {config['use_case']}")
        print(f"  Технічні характеристики: {config['technical_specs']}")
        print()
        
        # Демонструємо зміну стилю
        print("Зміна стилю на 'cinematic':")
        generator.set_style("cinematic")
        style_info = generator.get_style_info()
        print(f"  Новий стиль: {style_info['name']}")
        print(f"  Use Case: {style_info['use_case']}")
        print()
        
        # Пошук стилів за use case
        print("Пошук fashion стилів:")
        fashion_styles = generator.find_styles_by_use_case("fashion")
        for style in fashion_styles:
            print(f"  📸 {style['name']}: {style['description']}")
        print()
        
    except Exception as e:
        print(f"❌ Помилка при роботі з генератором: {e}")

def demo_prompt_comparison():
    """Демонстрація порівняння промптів"""
    print("📊 Демонстрація порівняння промптів")
    print("=" * 60)
    
    styles_to_compare = ["ultra_realistic", "cinematic", "artistic"]
    
    for style in styles_to_compare:
        config = PromptConfig.get_prompt_config(style)
        print(f"🎨 {config['style_name']}:")
        print(f"   Use Case: {config['use_case']}")
        print(f"   Освітлення: {config['technical_specs']['lighting']}")
        print(f"   Фон: {config['technical_specs']['background']}")
        print(f"   Фокус: {config['technical_specs']['focus']}")
        print(f"   Якість: {config['technical_specs']['quality']}")
        print()

def demo_quality_settings():
    """Демонстрація налаштувань якості"""
    print("⭐ Демонстрація налаштувань якості")
    print("=" * 60)
    
    qualities = PromptConfig.list_available_qualities()
    for quality in qualities:
        print(f"🔧 {quality['key']}: {quality['description']}")

def main():
    """Головна функція демонстрації"""
    print("🎭 FLUX Image Generator - Enhanced Prompts Demo")
    print("=" * 80)
    print("Демонстрація вдосконаленої системи промптів з прецизійними параметрами")
    print("та контекстуальними use cases")
    print()
    
    # Налаштування логування
    setup_logger(level="INFO")
    
    try:
        # Демонстрації
        demo_style_information()
        demo_use_case_search()
        demo_technical_specs_search()
        demo_quality_settings()
        demo_prompt_comparison()
        demo_enhanced_generator()
        
        print("✅ Демонстрація завершена успішно!")
        print()
        print("💡 Поради для використання:")
        print("  1. Використовуйте --use-case для пошуку стилів за призначенням")
        print("  2. Використовуйте --technical-spec для пошуку за технічними характеристиками")
        print("  3. Всі стилі мають уніфіковану роздільну здатність 8K")
        print("  4. Кожен стиль оптимізований для конкретних use cases")
        
    except Exception as e:
        print(f"❌ Помилка під час демонстрації: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 