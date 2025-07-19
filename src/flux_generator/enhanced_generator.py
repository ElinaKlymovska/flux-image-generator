#!/usr/bin/env python3
"""
Enhanced FLUX API Image Generator
Покращена версія генератора з підтримкою різних стилів та налаштувань
"""

import os
import time
import json
import requests
from pathlib import Path
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
import base64
from .prompts import PromptConfig

# Завантаження змінних середовища
load_dotenv()

class EnhancedFluxGenerator:
    """Покращений клас для роботи з FLUX API від BFL.ai"""
    
    def __init__(self, output_subdir: str = "enhanced"):
        self.api_key = os.getenv('BFL_API_KEY')
        if not self.api_key:
            raise ValueError("BFL_API_KEY не знайдено в змінних середовища")
        
        # Remove quotes if present
        self.api_key = self.api_key.strip('"\'')
        
        self.base_url = "https://api.bfl.ai/v1/flux-kontext-pro"
        self.headers = {
            "x-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        # Створення підпапки для покращених результатів
        self.output_dir = Path("data/output") / output_subdir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Поточні налаштування
        self.current_style = "realistic"
        self.current_aspect = "portrait"
        self.current_quality = "standard"
    
    def encode_image(self, image_path: str) -> str:
        """Кодування зображення в base64"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def set_style(self, style: str) -> None:
        """Встановлення стилю генерації"""
        if style not in PromptConfig.PROMPTS:
            available = list(PromptConfig.PROMPTS.keys())
            raise ValueError(f"Невідомий стиль: {style}. Доступні: {available}")
        self.current_style = style
    
    def set_aspect_ratio(self, aspect: str) -> None:
        """Встановлення співвідношення сторін"""
        if aspect not in PromptConfig.ASPECT_RATIOS:
            available = list(PromptConfig.ASPECT_RATIOS.keys())
            raise ValueError(f"Невідомий аспект: {aspect}. Доступні: {available}")
        self.current_aspect = aspect
    
    def set_quality(self, quality: str) -> None:
        """Встановлення якості генерації"""
        if quality not in PromptConfig.QUALITY_SETTINGS:
            available = list(PromptConfig.QUALITY_SETTINGS.keys())
            raise ValueError(f"Невідома якість: {quality}. Доступні: {available}")
        self.current_quality = quality
    
    def get_current_config(self) -> Dict[str, Any]:
        """Отримання поточної конфігурації"""
        return PromptConfig.get_prompt_config(
            self.current_style,
            self.current_aspect,
            self.current_quality
        )
    
    def create_generation_request(self, seed: int, custom_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Створення запиту для генерації зображення"""
        image_data = self.encode_image("data/input/character.jpg")
        config = self.get_current_config()
        
        # Використання кастомного промпту або стандартного
        prompt = custom_prompt if custom_prompt else config["prompt"]
        
        request_data = {
            "prompt": prompt,
            "input_image": image_data,
            "seed": seed,
            "aspect_ratio": config["aspect_ratio"],
            "output_format": "jpeg",
            **config["quality_settings"]
        }
        
        return request_data
    
    def submit_generation(self, request_data: Dict[str, Any]) -> Optional[str]:
        """Відправка запиту на генерацію"""
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=request_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('polling_url')
            elif response.status_code == 429:
                print(f"⚠️  Помилка 429: Перевищено ліміт запитів. Очікування...")
                time.sleep(60)  # Очікування 1 хвилини
                return None
            elif response.status_code == 500:
                print(f"❌ Помилка 500: Внутрішня помилка сервера")
                return None
            else:
                print(f"❌ Помилка HTTP {response.status_code}: {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            print("❌ Помилка: Таймаут запиту")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Помилка мережі: {e}")
            return None
    
    def poll_generation_status(self, polling_url: str) -> Optional[Dict[str, Any]]:
        """Очікування завершення генерації"""
        max_attempts = 60  # Максимум 5 хвилин (60 * 5 секунд)
        attempt = 0
        
        while attempt < max_attempts:
            try:
                response = requests.get(polling_url, timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    status = result.get('status')
                    
                    if status == 'completed' or status == 'Ready':
                        return result
                    elif status == 'failed':
                        print(f"❌ Генерація невдала: {result.get('error', 'Невідома помилка')}")
                        return None
                    elif status == 'processing' or status == 'Pending':
                        print(f"🔄 Обробка... (спроба {attempt + 1}/{max_attempts})")
                        time.sleep(5)
                    else:
                        print(f"ℹ️  Статус: {status}")
                        time.sleep(5)
                else:
                    print(f"❌ Помилка HTTP {response.status_code} при опитуванні статусу")
                    time.sleep(5)
                    
            except requests.exceptions.Timeout:
                print("⚠️  Таймаут при опитуванні статусу")
                time.sleep(5)
            except requests.exceptions.RequestException as e:
                print(f"❌ Помилка мережі при опитуванні: {e}")
                time.sleep(5)
            
            attempt += 1
        
        print("⏰ Перевищено час очікування генерації")
        return None
    
    def download_image(self, image_url: str, filename: str) -> bool:
        """Завантаження згенерованого зображення"""
        try:
            response = requests.get(image_url, timeout=30)
            
            if response.status_code == 200:
                file_path = self.output_dir / filename
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print(f"✅ Збережено: {filename}")
                return True
            else:
                print(f"❌ Помилка завантаження зображення: HTTP {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Помилка завантаження: {e}")
            return False
    
    def generate_single_image(self, seed: int, custom_prompt: Optional[str] = None) -> bool:
        """Генерація одного зображення"""
        config = self.get_current_config()
        
        print(f"\n🎨 Генерація зображення (seed: {seed})")
        print(f"📝 Стиль: {config['style_name']}")
        print(f"📐 Аспект: {config['aspect_ratio']}")
        print(f"⭐ Якість: {self.current_quality}")
        
        # Створення запиту
        request_data = self.create_generation_request(seed, custom_prompt)
        
        # Відправка запиту
        polling_url = self.submit_generation(request_data)
        if not polling_url:
            print(f"❌ Пропуск генерації через помилку")
            return False
        
        # Очікування завершення
        result = self.poll_generation_status(polling_url)
        if not result:
            print(f"❌ Пропуск генерації через помилку")
            return False
        
        # Завантаження зображення
        result_data = result.get('result', {})
        image_url = result_data.get('sample')
        if image_url:
            filename = f"{self.current_style}_{seed}.jpg"
            return self.download_image(image_url, filename)
        else:
            print(f"❌ URL зображення не знайдено в результаті")
            return False
    
    def generate_images(self, count: int = 5, custom_prompt: Optional[str] = None) -> None:
        """Генерація вказаної кількості зображень"""
        config = self.get_current_config()
        
        print(f"🚀 Початок генерації {count} зображень...")
        print(f"🎨 Стиль: {config['style_name']} - {config['description']}")
        print(f"📐 Аспект: {config['aspect_ratio']}")
        print(f"⭐ Якість: {self.current_quality}")
        print(f"📁 Збереження в: {self.output_dir.absolute()}")
        
        successful_generations = 0
        seeds_used = []
        
        for i in range(count):
            seed = 2000 + i  # Унікальні seed для покращених зображень
            seeds_used.append(seed)
            
            if self.generate_single_image(seed, custom_prompt):
                successful_generations += 1
            
            # Невелика пауза між запитами
            if i < count - 1:
                time.sleep(2)
        
        print(f"\n🎉 === Генерація завершена ===")
        print(f"✅ Успішно згенеровано: {successful_generations}/{count}")
        print(f"🎲 Використані seed: {seeds_used}")
        print(f"📁 Зображення збережено в папці: {self.output_dir.absolute()}")
    
    def generate_style_comparison(self, styles: List[str] = None, count_per_style: int = 2) -> None:
        """Генерація порівняння різних стилів"""
        if styles is None:
            styles = ["realistic", "cinematic", "artistic", "fashion"]
        
        print(f"🔄 Генерація порівняння стилів: {', '.join(styles)}")
        print(f"📊 {count_per_style} зображення на стиль")
        
        total_generated = 0
        
        for style in styles:
            print(f"\n🎨 === Стиль: {style.upper()} ===")
            self.set_style(style)
            
            for i in range(count_per_style):
                seed = 3000 + total_generated
                if self.generate_single_image(seed):
                    total_generated += 1
                
                if i < count_per_style - 1:
                    time.sleep(2)
        
        print(f"\n🎉 === Порівняння стилів завершено ===")
        print(f"✅ Всього згенеровано: {total_generated} зображень")
    
    def list_available_styles(self) -> None:
        """Виведення списку доступних стилів"""
        styles = PromptConfig.list_available_styles()
        print("🎨 Доступні стилі:")
        for style in styles:
            print(f"  • {style['key']}: {style['name']} - {style['description']}")
    
    def list_available_aspects(self) -> None:
        """Виведення списку доступних аспектів"""
        aspects = PromptConfig.list_available_aspects()
        print("📐 Доступні аспекти:")
        for key, value in aspects.items():
            print(f"  • {key}: {value}")
    
    def list_available_qualities(self) -> None:
        """Виведення списку доступних якостей"""
        qualities = PromptConfig.list_available_qualities()
        print("⭐ Доступні якості:")
        for quality in qualities:
            print(f"  • {quality}")

def main():
    """Головна функція для тестування"""
    try:
        # Перевірка наявності вхідного зображення
        if not Path("data/input/character.jpg").exists():
            print("❌ Помилка: Файл data/input/character.jpg не знайдено")
            return
        
        # Створення покращеного генератора
        generator = EnhancedFluxGenerator()
        
        # Виведення доступних опцій
        print("🔧 Налаштування генератора:")
        generator.list_available_styles()
        print()
        generator.list_available_aspects()
        print()
        generator.list_available_qualities()
        print()
        
        # Приклад генерації з різними стилями
        print("🎯 Приклад генерації:")
        
        # Реалістичний стиль
        generator.set_style("realistic")
        generator.set_aspect_ratio("portrait")
        generator.set_quality("high")
        generator.generate_images(2)
        
        # Кінематографічний стиль
        generator.set_style("cinematic")
        generator.set_quality("creative")
        generator.generate_images(2)
        
    except ValueError as e:
        print(f"❌ Помилка конфігурації: {e}")
    except Exception as e:
        print(f"❌ Неочікувана помилка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 