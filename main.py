#!/usr/bin/env python3
"""
🎨 SenteticData - Об'єднаний генератор зображень з FLUX API
Головна команда для всіх функцій проекту
"""

import sys
import os
import argparse
from pathlib import Path
from typing import List, Optional

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from flux_generator import EnhancedFluxGenerator, FluxImageGenerator
from flux_generator.core.rotation import CharacterRotationGenerator
from flux_generator.utils.logger import get_logger

logger = get_logger(__name__)


class SenteticDataGenerator:
    """Головний клас для об'єднаної логіки проекту"""
    
    def __init__(self):
        """Ініціалізація генератора"""
        self.enhanced_generator = None
        self.rotation_generator = None
        self.flux_generator = None
        
    def initialize_generators(self):
        """Ініціалізація всіх генераторів"""
        try:
            self.enhanced_generator = EnhancedFluxGenerator()
            self.rotation_generator = CharacterRotationGenerator()
            self.flux_generator = FluxImageGenerator()
            return True
        except Exception as e:
            logger.error(f"Помилка ініціалізації генераторів: {e}")
            return False
    
    def test_connection(self) -> bool:
        """Тестування з'єднання з API"""
        if not self.enhanced_generator:
            return False
        return self.enhanced_generator.test_connection()
    
    def show_main_menu(self):
        """Показати головне меню"""
        print("\n🎨 SenteticData - Об'єднаний генератор зображень")
        print("=" * 60)
        print("1. 🎯 Генерація з одним стилем")
        print("2. 🔄 Порівняння стилів")
        print("3. ✍️ Кастомний промпт")
        print("4. 🌀 Генерація ротації персонажа")
        print("5. 📸 Генерація варіацій портретів")
        print("6. 🔧 Обробка зображень (Adetailer)")
        print("7. ⚙️ Налаштування")
        print("8. 📋 Інформація про стилі")
        print("9. 🚀 Швидка генерація (всі функції)")
        print("0. 👋 Вихід")
        print("=" * 60)
    
    def single_style_generation(self):
        """Генерація з одним стилем"""
        print("\n🎯 Генерація з одним стилем")
        
        # Показати доступні стилі
        self.enhanced_generator.list_available_styles()
        
        # Вибір стилю
        style = input("\nВиберіть стиль (або Enter для realistic): ").strip().lower()
        if not style:
            style = "realistic"
        
        try:
            self.enhanced_generator.set_style(style)
        except ValueError as e:
            print(f"❌ {e}")
            return
        
        # Вибір аспекту
        self.enhanced_generator.list_available_aspects()
        aspect = input("Виберіть аспект (або Enter для portrait): ").strip().lower()
        if not aspect:
            aspect = "portrait"
        
        try:
            self.enhanced_generator.set_aspect_ratio(aspect)
        except ValueError as e:
            print(f"❌ {e}")
            return
        
        # Вибір якості
        self.enhanced_generator.list_available_qualities()
        quality = input("Виберіть якість (або Enter для standard): ").strip().lower()
        if not quality:
            quality = "standard"
        
        try:
            self.enhanced_generator.set_quality(quality)
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
        self.enhanced_generator.generate_images(count)
    
    def style_comparison(self):
        """Порівняння стилів"""
        print("\n🔄 Порівняння стилів")
        
        # Показати доступні стилі
        self.enhanced_generator.list_available_styles()
        
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
        self.enhanced_generator.generate_style_comparison(styles, count_per_style)
    
    def custom_prompt_generation(self):
        """Генерація з кастомним промптом"""
        print("\n✍️ Кастомний промпт")
        
        # Вибір стилю як бази
        self.enhanced_generator.list_available_styles()
        style = input("\nВиберіть базовий стиль (або Enter для realistic): ").strip().lower()
        if not style:
            style = "realistic"
        
        try:
            self.enhanced_generator.set_style(style)
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
        self.enhanced_generator.generate_images(count, custom_prompt)
    
    def character_rotation_generation(self):
        """Генерація ротації персонажа"""
        print("\n🌀 Генерація ротації персонажа")
        
        print("Виберіть тип ротації:")
        print("1. Базові кути (front, left, back, right)")
        print("2. 360° послідовність")
        print("3. Кастомні кути")
        
        choice = input("Виберіть опцію (1-3): ").strip()
        
        if choice == "1":
            angles = ["front", "left", "back", "right"]
            steps = None
        elif choice == "2":
            try:
                steps = int(input("Кількість кроків для 360° (або Enter для 8): ") or "8")
                angles = None
            except ValueError:
                steps = 8
                angles = None
        elif choice == "3":
            angles_input = input("Введіть кути через кому (наприклад: 10,45,90,180): ").strip()
            angles = [angle.strip() for angle in angles_input.split(",")]
            steps = None
        else:
            print("❌ Невірний вибір")
            return
        
        # Стиль
        style = input("Виберіть стиль (або Enter для ultra_realistic): ").strip()
        if not style:
            style = "ultra_realistic"
        
        # Кастомний промпт
        custom_prompt = input("Кастомний промпт (або Enter для пропуску): ").strip()
        if not custom_prompt:
            custom_prompt = None
        
        # Генерація
        print(f"\n🚀 Запуск генерації ротації...")
        
        if steps:
            results = self.rotation_generator.generate_360_degree_sequence(
                steps=steps,
                style=style,
                start_seed=1001,
                custom_prompt=custom_prompt
            )
        else:
            results = self.rotation_generator.generate_full_rotation(
                angles=angles,
                style=style,
                start_seed=1001,
                custom_prompt=custom_prompt
            )
        
        successful = sum(1 for r in results.values() if r is not None) if isinstance(results, dict) else sum(1 for r in results if r is not None)
        total = len(results)
        print(f"✅ Згенеровано {successful}/{total} зображень ротації")
    
    def portrait_variations_generation(self):
        """Генерація варіацій портретів"""
        print("\n📸 Генерація варіацій портретів")
        
        print("Це згенерує портрети для всіх стилів та якостей.")
        confirm = input("Продовжити? (y/N): ").strip().lower()
        
        if confirm not in ['y', 'yes']:
            print("❌ Скасовано")
            return
        
        print(f"\n🚀 Запуск генерації варіацій портретів...")
        
        summary = self.enhanced_generator.generate_all_variations_summary(
            count_per_variation=1,
            start_seed=1000,
            custom_prompt=None,
            include_aspects=["portrait"]
        )
        
        stats = summary["statistics"]
        print(f"\n📊 Результати:")
        print(f"  - Всього варіацій: {stats['total_variations']}")
        print(f"  - Успішних: {stats['successful_variations']}")
        print(f"  - Всього зображень: {stats['total_images']}")
        print(f"  - Успішних зображень: {stats['successful_images']}")
    
    def process_images_adetailer(self):
        """Обробка зображень з Adetailer"""
        print("\n🔧 Обробка зображень (Adetailer)")
        
        print("Виберіть тип обробки:")
        print("1. Всі зображення в data/output")
        print("2. Тільки оригінальні зображення")
        print("3. Зображення ротації")
        print("4. Перші 6 зображень")
        
        choice = input("Виберіть опцію (1-4): ").strip()
        
        if choice == "1":
            self._process_all_images()
        elif choice == "2":
            self._process_original_images()
        elif choice == "3":
            self._process_rotation_images()
        elif choice == "4":
            self._process_six_images()
        else:
            print("❌ Невірний вибір")
    
    def _process_all_images(self):
        """Обробка всіх зображень"""
        input_dir = Path("data/output")
        image_files = list(input_dir.rglob("*.jpg")) + list(input_dir.rglob("*.png"))
        
        if not image_files:
            print("❌ Не знайдено зображень в data/output")
            return
        
        print(f"📁 Знайдено {len(image_files)} зображень для обробки")
        self._process_images_with_flux(image_files, "flux_enhanced")
    
    def _process_original_images(self):
        """Обробка оригінальних зображень"""
        original_dirs = ["data/output/portrait_variations", "data/output/rotation_output"]
        image_files = []
        
        for dir_path in original_dirs:
            dir_obj = Path(dir_path)
            if dir_obj.exists():
                files = list(dir_obj.glob("*.jpg")) + list(dir_obj.glob("*.png"))
                original_files = [f for f in files if not f.name.startswith("enhanced_")]
                image_files.extend(original_files)
        
        if not image_files:
            print("❌ Не знайдено оригінальних зображень")
            return
        
        print(f"📁 Знайдено {len(image_files)} оригінальних зображень")
        self._process_images_with_flux(image_files, "original_enhanced")
    
    def _process_rotation_images(self):
        """Обробка зображень ротації"""
        input_dir = Path("data/output/rotation_output")
        image_files = list(input_dir.glob("*.jpg")) + list(input_dir.glob("*.png"))
        
        if not image_files:
            print("❌ Не знайдено зображень ротації")
            return
        
        print(f"📁 Знайдено {len(image_files)} зображень ротації")
        self._process_images_with_flux(image_files, "rotation_enhanced")
    
    def _process_six_images(self):
        """Обробка перших 6 зображень"""
        input_dir = Path("data/output/woman")
        image_files = list(input_dir.glob("*.jpg")) + list(input_dir.glob("*.png"))
        image_files = sorted(image_files)[:6]
        
        if not image_files:
            print("❌ Не знайдено зображень")
            return
        
        print(f"📁 Знайдено {len(image_files)} зображень")
        self._process_images_with_flux(image_files, "six_enhanced")
    
    def _process_images_with_flux(self, image_files: List[Path], output_subdir: str):
        """Обробка зображень з FLUX API"""
        output_dir = Path("data/output") / output_subdir
        output_dir.mkdir(parents=True, exist_ok=True)
        
        enhanced_prompts = [
            "beautiful face, detailed eyes, perfect skin, high quality, ultra realistic, sharp focus",
            "portrait with enhanced facial features, detailed eyes, flawless skin, professional photography",
            "high resolution face, detailed features, perfect skin texture, studio lighting",
            "close-up portrait, detailed eyes, smooth skin, high quality, professional"
        ]
        
        print(f"\n🚀 Початок обробки {len(image_files)} зображень...")
        processed_count = 0
        
        for i, image_path in enumerate(image_files, 1):
            print(f"\n📸 Обробка {i}/{len(image_files)}: {image_path.name}")
            
            try:
                prompt_index = (i - 1) % len(enhanced_prompts)
                enhanced_prompt = enhanced_prompts[prompt_index]
                
                output_path = self.flux_generator.generate_single_image(
                    prompt=enhanced_prompt,
                    seed=1000 + i,
                    aspect_ratio="2:3",
                    output_format="jpeg"
                )
                
                if output_path:
                    enhanced_filename = f"enhanced_{image_path.stem}_flux{image_path.suffix}"
                    enhanced_path = output_dir / enhanced_filename
                    
                    import shutil
                    shutil.copy2(output_path, enhanced_path)
                    
                    processed_count += 1
                    print(f"✅ Оброблено: {enhanced_filename}")
                else:
                    print(f"❌ Помилка обробки: {image_path.name}")
                
            except Exception as e:
                print(f"❌ Помилка обробки {image_path.name}: {e}")
        
        print(f"\n🎉 Обробка завершена!")
        print(f"✅ Успішно оброблено {processed_count}/{len(image_files)} зображень")
        print(f"📁 Збережено в: {output_dir}")
    
    def settings_menu(self):
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
                self.enhanced_generator.list_available_styles()
                style = input("Виберіть новий стиль: ").strip().lower()
                try:
                    self.enhanced_generator.set_style(style)
                    print(f"✅ Стиль змінено на: {style}")
                except ValueError as e:
                    print(f"❌ {e}")
            
            elif choice == "2":
                self.enhanced_generator.list_available_aspects()
                aspect = input("Виберіть новий аспект: ").strip().lower()
                try:
                    self.enhanced_generator.set_aspect_ratio(aspect)
                    print(f"✅ Аспект змінено на: {aspect}")
                except ValueError as e:
                    print(f"❌ {e}")
            
            elif choice == "3":
                self.enhanced_generator.list_available_qualities()
                quality = input("Виберіть нову якість: ").strip().lower()
                try:
                    self.enhanced_generator.set_quality(quality)
                    print(f"✅ Якість змінено на: {quality}")
                except ValueError as e:
                    print(f"❌ {e}")
            
            elif choice == "4":
                config = self.enhanced_generator.get_current_config()
                print(f"\n📋 Поточні налаштування:")
                print(f"🎨 Стиль: {config['style_name']}")
                print(f"📐 Аспект: {config['aspect_ratio']}")
                print(f"⭐ Якість: {self.enhanced_generator.current_quality}")
                print(f"📝 Промпт: {config['prompt'][:100]}...")
            
            elif choice == "5":
                break
            
            else:
                print("❌ Невірний вибір")
    
    def show_styles_info(self):
        """Показати інформацію про стилі"""
        print("\n📋 Інформація про стилі")
        self.enhanced_generator.list_available_styles()
        print("\n📐 Доступні аспекти:")
        self.enhanced_generator.list_available_aspects()
        print("\n⭐ Доступні якості:")
        self.enhanced_generator.list_available_qualities()
    
    def quick_generation(self):
        """Швидка генерація (всі функції)"""
        print("\n🚀 Швидка генерація (всі функції)")
        print("Це запустить послідовно всі основні функції:")
        print("1. Генерація портретів (всі стилі)")
        print("2. Генерація ротації персонажа")
        print("3. Обробка зображень")
        
        confirm = input("\nПродовжити? (y/N): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("❌ Скасовано")
            return
        
        print(f"\n🚀 Запуск швидкої генерації...")
        
        # 1. Генерація портретів
        print("\n📸 Крок 1: Генерація портретів...")
        try:
            summary = self.enhanced_generator.generate_all_variations_summary(
                count_per_variation=1,
                start_seed=1000,
                custom_prompt=None,
                include_aspects=["portrait"]
            )
            print(f"✅ Портрети згенеровано")
        except Exception as e:
            print(f"❌ Помилка генерації портретів: {e}")
        
        # 2. Генерація ротації
        print("\n🌀 Крок 2: Генерація ротації...")
        try:
            results = self.rotation_generator.generate_360_degree_sequence(
                steps=8,
                style="ultra_realistic",
                start_seed=1001
            )
            print(f"✅ Ротація згенерована")
        except Exception as e:
            print(f"❌ Помилка генерації ротації: {e}")
        
        # 3. Обробка зображень
        print("\n🔧 Крок 3: Обробка зображень...")
        try:
            input_dir = Path("data/output")
            image_files = list(input_dir.rglob("*.jpg")) + list(input_dir.rglob("*.png"))
            if image_files:
                self._process_images_with_flux(image_files[:10], "quick_enhanced")  # Обробити перші 10
                print(f"✅ Зображення оброблено")
            else:
                print("⚠️ Не знайдено зображень для обробки")
        except Exception as e:
            print(f"❌ Помилка обробки зображень: {e}")
        
        print(f"\n🎉 Швидка генерація завершена!")


def main():
    """Головна функція"""
    parser = argparse.ArgumentParser(description="🎨 SenteticData - Об'єднаний генератор зображень")
    parser.add_argument("--quick", action="store_true", help="Швидка генерація (всі функції)")
    parser.add_argument("--style", help="Стиль для генерації")
    parser.add_argument("--count", type=int, default=3, help="Кількість зображень")
    parser.add_argument("--rotation", action="store_true", help="Генерація ротації")
    parser.add_argument("--process", action="store_true", help="Обробка зображень")
    
    args = parser.parse_args()
    
    print("🚀 SenteticData - Об'єднаний генератор зображень")
    
    try:
        # Перевірка наявності вхідного зображення
        input_image = Path("data/input/character.jpg")
        if not input_image.exists():
            print("❌ Помилка: Файл data/input/character.jpg не знайдено")
            return 1
        
        # Створення генератора
        generator = SenteticDataGenerator()
        
        if not generator.initialize_generators():
            print("❌ Помилка ініціалізації генераторів")
            return 1
        
        # Тестування з'єднання
        if not generator.test_connection():
            print("❌ Помилка з'єднання з API")
            return 1
        
        print("✅ З'єднання з API успішне")
        
        # Якщо передано аргументи командного рядка
        if args.quick:
            generator.quick_generation()
            return 0
        
        if args.style:
            generator.enhanced_generator.set_style(args.style)
            generator.enhanced_generator.generate_images(args.count)
            return 0
        
        if args.rotation:
            generator.character_rotation_generation()
            return 0
        
        if args.process:
            generator.process_images_adetailer()
            return 0
        
        # Інтерактивне меню
        while True:
            generator.show_main_menu()
            choice = input("Виберіть опцію (0-9): ").strip()
            
            if choice == "1":
                generator.single_style_generation()
            elif choice == "2":
                generator.style_comparison()
            elif choice == "3":
                generator.custom_prompt_generation()
            elif choice == "4":
                generator.character_rotation_generation()
            elif choice == "5":
                generator.portrait_variations_generation()
            elif choice == "6":
                generator.process_images_adetailer()
            elif choice == "7":
                generator.settings_menu()
            elif choice == "8":
                generator.show_styles_info()
            elif choice == "9":
                generator.quick_generation()
            elif choice == "0":
                print("👋 До побачення!")
                break
            else:
                print("❌ Невірний вибір. Спробуйте ще раз.")
            
            input("\nНатисніть Enter для продовження...")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n👋 Програму перервано користувачем")
        return 0
    except Exception as e:
        print(f"❌ Неочікувана помилка: {e}")
        logger.error(f"Main error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 