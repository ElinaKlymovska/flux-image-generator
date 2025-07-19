#!/usr/bin/env python3
"""
Prompt Tester Main - Automated Testing of Multiple Prompts with Rotation
Головний скрипт для автоматичного тестування промптів з обертанням
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from flux_generator import PromptTester

def show_menu():
    """Показати головне меню"""
    print("\n🧪 Prompt Tester for FLUX API Image Generator")
    print("=" * 60)
    print("1. Показати всі промпти")
    print("2. Показати кути обертання")
    print("3. Тестувати один промпт")
    print("4. Тестувати всі промпти (105 зображень)")
    print("5. Тестувати вибрані промпти")
    print("6. Показати статистику")
    print("7. Вихід")
    print("=" * 60)

def show_prompts(tester):
    """Показати всі промпти"""
    print("\n📝 Всі промпти для тестування:")
    tester.list_prompts()

def show_rotations(tester):
    """Показати кути обертання"""
    print("\n🔄 Кути обертання:")
    tester.list_rotations()

def test_single_prompt(tester):
    """Тестування одного промпту"""
    print("\n🎯 Тестування одного промпту")
    
    # Показати доступні промпти
    tester.list_prompts()
    
    # Вибір промпту
    try:
        choice = int(input("\nВиберіть номер промпту (1-15): ")) - 1
        if choice < 0 or choice >= len(tester.test_prompts):
            print("❌ Невірний номер промпту")
            return
    except ValueError:
        print("❌ Введіть число")
        return
    
    prompt = tester.test_prompts[choice]
    
    # Підтвердження
    print(f"\n🎨 Обраний промпт: {prompt['name']}")
    print(f"📝 Опис: {prompt['description']}")
    print(f"🔄 Буде згенеровано {len(tester.rotation_angles)} зображень")
    
    confirm = input("\nПродовжити? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ Скасовано")
        return
    
    # Тестування
    tester.test_prompt(prompt)

def test_all_prompts(tester):
    """Тестування всіх промптів"""
    total_images = len(tester.test_prompts) * len(tester.rotation_angles)
    
    print(f"\n⚠️  УВАГА: Тестування всіх промптів")
    print(f"📊 Кількість промптів: {len(tester.test_prompts)}")
    print(f"🔄 Кути обертання: {len(tester.rotation_angles)}")
    print(f"📸 Всього зображень: {total_images}")
    print(f"⏱️  Приблизний час: {total_images * 2} хвилин")
    print(f"💰 API кредити: {total_images} запитів")
    
    confirm = input("\nПродовжити? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ Скасовано")
        return
    
    # Запуск тестування
    tester.test_all_prompts()

def test_selected_prompts(tester):
    """Тестування вибраних промптів"""
    print("\n🎯 Тестування вибраних промптів")
    
    # Показати доступні промпти
    tester.list_prompts()
    
    # Вибір промптів
    selection = input("\nВведіть номери промптів через кому (наприклад: 1,3,5): ").strip()
    
    try:
        indices = [int(x.strip()) - 1 for x in selection.split(",")]
        selected_prompts = [tester.test_prompts[i] for i in indices if 0 <= i < len(tester.test_prompts)]
        
        if not selected_prompts:
            print("❌ Не вибрано жодного валідного промпту")
            return
        
        total_images = len(selected_prompts) * len(tester.rotation_angles)
        
        print(f"\n📋 Обрані промпти:")
        for prompt in selected_prompts:
            print(f"  • {prompt['name']}: {prompt['description']}")
        
        print(f"\n📊 Всього зображень: {total_images}")
        
        confirm = input("\nПродовжити? (y/N): ").strip().lower()
        if confirm != 'y':
            print("❌ Скасовано")
            return
        
        # Тестування вибраних промптів
        for i, prompt in enumerate(selected_prompts):
            print(f"\n{'='*60}")
            print(f"📋 Промпт {i+1}/{len(selected_prompts)}: {prompt['name']}")
            print(f"{'='*60}")
            
            tester.test_prompt(prompt)
            
            # Пауза між промптами
            if i < len(selected_prompts) - 1:
                print(f"\n⏳ Пауза 10 секунд...")
                import time
                time.sleep(10)
        
        print(f"\n🎉 === ТЕСТУВАННЯ ЗАВЕРШЕНО ===")
        
    except ValueError:
        print("❌ Невірний формат введення")

def show_statistics(tester):
    """Показати статистику"""
    print("\n📊 Статистика тестування")
    print("=" * 40)
    
    # Інформація про промпти
    print(f"📝 Кількість промптів: {len(tester.test_prompts)}")
    print(f"🔄 Кути обертання: {len(tester.rotation_angles)}")
    print(f"📸 Зображень на промпт: {len(tester.rotation_angles)}")
    print(f"📊 Всього зображень: {len(tester.test_prompts) * len(tester.rotation_angles)}")
    
    # Інформація про папки датасетів
    datasets_dir = Path(__file__).parent.parent / "data/output/datasets"
    if datasets_dir.exists():
        datasets = list(datasets_dir.glob("*"))
        print(f"📁 Існуючих датасетів: {len(datasets)}")
        
        if datasets:
            print("\n📋 Останні датасети:")
            for dataset in sorted(datasets, key=lambda x: x.stat().st_mtime, reverse=True)[:5]:
                print(f"  • {dataset.name}")
    else:
        print("📁 Датасети ще не створені")

def main():
    """Головна функція"""
    print("🚀 Prompt Tester - Starting...")
    
    try:
        # Перевірка наявності вхідного зображення
        input_image = Path(__file__).parent.parent / "data/input/character.jpg"
        print(f"🔍 Checking input image: {input_image}")
        
        if not input_image.exists():
            print("❌ Помилка: Файл data/input/character.jpg не знайдено")
            return
        
        print("✅ Input image found")
        
        # Створення тестера
        print("🔧 Creating prompt tester...")
        tester = PromptTester()
        print("✅ Prompt tester created successfully")
        
        # Інтерактивне меню
        while True:
            show_menu()
            choice = input("Виберіть опцію (1-7): ").strip()
            
            if choice == "1":
                show_prompts(tester)
            
            elif choice == "2":
                show_rotations(tester)
            
            elif choice == "3":
                test_single_prompt(tester)
            
            elif choice == "4":
                test_all_prompts(tester)
            
            elif choice == "5":
                test_selected_prompts(tester)
            
            elif choice == "6":
                show_statistics(tester)
            
            elif choice == "7":
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