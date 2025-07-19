#!/usr/bin/env python3
"""
Prompt Tester for FLUX API Image Generator
Автоматичне тестування різних промптів з обертанням персонажа
"""

import os
import time
import json
import requests
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from dotenv import load_dotenv
import base64
from datetime import datetime
from .prompts import PromptConfig

# Завантаження змінних середовища
load_dotenv()

class PromptTester:
    """Клас для автоматичного тестування промптів з обертанням"""
    
    def __init__(self):
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
        
        # Створення папки для датасетів
        self.datasets_dir = Path("data/output/datasets")
        self.datasets_dir.mkdir(parents=True, exist_ok=True)
        
        # 15 різних промптів для тестування
        self.test_prompts = [
            {
                "name": "ultra_realistic",
                "prompt": "ultra-realistic portrait of a woman, soft natural lighting, neutral background, high quality, detailed facial features, professional photography, 8k resolution",
                "description": "Ультрареалістичний портрет"
            },
            {
                "name": "cinematic_dramatic",
                "prompt": "cinematic portrait of a woman, dramatic lighting, shallow depth of field, film grain, professional cinematography, moody atmosphere, high contrast, golden hour",
                "description": "Кінематографічний драматичний"
            },
            {
                "name": "artistic_painterly",
                "prompt": "artistic portrait of a woman, painterly style, soft brushstrokes, artistic lighting, creative composition, masterpiece quality, fine art photography, oil painting effect",
                "description": "Художній живописний"
            },
            {
                "name": "fashion_editorial",
                "prompt": "fashion portrait of a woman, studio lighting, professional makeup, elegant pose, high fashion photography, magazine quality, sophisticated style, editorial look",
                "description": "Модний редакційний"
            },
            {
                "name": "vintage_retro",
                "prompt": "vintage portrait of a woman, retro style, film photography, warm tones, nostalgic atmosphere, classic beauty, timeless elegance, 1950s aesthetic",
                "description": "Вінтажний ретро"
            },
            {
                "name": "modern_minimalist",
                "prompt": "modern portrait of a woman, contemporary style, clean composition, minimalist background, sharp details, professional headshot quality, urban aesthetic",
                "description": "Сучасний мінімалістичний"
            },
            {
                "name": "dramatic_emotional",
                "prompt": "dramatic portrait of a woman, intense lighting, strong shadows, emotional expression, powerful composition, artistic photography, chiaroscuro lighting",
                "description": "Драматичний емоційний"
            },
            {
                "name": "soft_dreamy",
                "prompt": "soft dreamy portrait of a woman, gentle lighting, soft focus, ethereal atmosphere, romantic mood, delicate beauty, pastel tones, bokeh background",
                "description": "М'який мрійливий"
            },
            {
                "name": "professional_corporate",
                "prompt": "professional corporate portrait of a woman, business attire, clean background, confident expression, executive headshot, modern office setting, professional lighting",
                "description": "Професійний корпоративний"
            },
            {
                "name": "creative_artistic",
                "prompt": "creative artistic portrait of a woman, abstract background, artistic composition, creative lighting, modern art style, contemporary photography, experimental",
                "description": "Творчий художній"
            },
            {
                "name": "elegant_sophisticated",
                "prompt": "elegant sophisticated portrait of a woman, luxury setting, refined beauty, high-end fashion, premium quality, sophisticated lighting, exclusive atmosphere",
                "description": "Елегантний вишуканий"
            },
            {
                "name": "natural_outdoor",
                "prompt": "natural outdoor portrait of a woman, natural lighting, outdoor setting, environmental portrait, nature background, organic beauty, environmental photography",
                "description": "Природний зовнішній"
            },
            {
                "name": "studio_professional",
                "prompt": "studio professional portrait of a woman, controlled lighting, studio background, professional equipment, commercial photography, advertising quality",
                "description": "Студійний професійний"
            },
            {
                "name": "expressive_character",
                "prompt": "expressive character portrait of a woman, strong personality, character study, emotional depth, psychological portrait, human interest, documentary style",
                "description": "Експресивний характерний"
            },
            {
                "name": "contemporary_urban",
                "prompt": "contemporary urban portrait of a woman, city background, modern lifestyle, urban aesthetic, street photography style, contemporary culture, metropolitan",
                "description": "Сучасний міський"
            }
        ]
        
        # Кути обертання
        self.rotation_angles = [0, 10, 30, 45, 60, 90, 180]
        
    def encode_image(self, image_path: str) -> str:
        """Кодування зображення в base64"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def create_generation_request(self, prompt: str, seed: int, rotation: int = 0) -> Dict[str, Any]:
        """Створення запиту для генерації зображення з обертанням"""
        image_data = self.encode_image("data/input/character.jpg")
        
        # Додавання інформації про обертання до промпту
        rotation_prompt = ""
        if rotation > 0:
            rotation_prompt = f", rotated {rotation} degrees, different angle view"
        
        full_prompt = prompt + rotation_prompt
        
        return {
            "prompt": full_prompt,
            "input_image": image_data,
            "seed": seed,
            "aspect_ratio": "2:3",
            "output_format": "jpeg",
            "prompt_upsampling": True,
            "safety_tolerance": 2
        }
    
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
                time.sleep(60)
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
        max_attempts = 60
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
    
    def download_image(self, image_url: str, file_path: Path) -> bool:
        """Завантаження згенерованого зображення"""
        try:
            response = requests.get(image_url, timeout=30)
            
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print(f"✅ Збережено: {file_path.name}")
                return True
            else:
                print(f"❌ Помилка завантаження зображення: HTTP {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Помилка завантаження: {e}")
            return False
    
    def create_dataset_folder(self, prompt_name: str) -> Path:
        """Створення папки для датасету"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dataset_name = f"{prompt_name}_{timestamp}"
        dataset_path = self.datasets_dir / dataset_name
        dataset_path.mkdir(exist_ok=True)
        
        # Створення метаданих
        metadata = {
            "prompt_name": prompt_name,
            "created_at": datetime.now().isoformat(),
            "total_images": len(self.rotation_angles),
            "rotation_angles": self.rotation_angles,
            "prompt_text": next(p["prompt"] for p in self.test_prompts if p["name"] == prompt_name)
        }
        
        with open(dataset_path / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        return dataset_path
    
    def generate_single_image(self, prompt: Dict[str, str], rotation: int, seed: int, dataset_path: Path) -> bool:
        """Генерація одного зображення"""
        print(f"\n🎨 Генерація: {prompt['name']} (обертання: {rotation}°)")
        print(f"📝 Опис: {prompt['description']}")
        
        # Створення запиту
        request_data = self.create_generation_request(prompt["prompt"], seed, rotation)
        
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
            filename = f"{prompt['name']}_rotation{rotation:03d}_seed{seed}.jpg"
            file_path = dataset_path / filename
            return self.download_image(image_url, file_path)
        else:
            print(f"❌ URL зображення не знайдено в результаті")
            return False
    
    def test_prompt(self, prompt: Dict[str, str]) -> None:
        """Тестування одного промпту з усіма кутами обертання"""
        print(f"\n🚀 Тестування промпту: {prompt['name']}")
        print(f"📝 Опис: {prompt['description']}")
        print(f"🔄 Кути обертання: {self.rotation_angles}")
        
        # Створення папки для датасету
        dataset_path = self.create_dataset_folder(prompt["name"])
        print(f"📁 Датасет збережено в: {dataset_path}")
        
        successful_generations = 0
        base_seed = 5000 + hash(prompt["name"]) % 1000  # Унікальний seed для кожного промпту
        
        for i, rotation in enumerate(self.rotation_angles):
            seed = base_seed + i
            
            if self.generate_single_image(prompt, rotation, seed, dataset_path):
                successful_generations += 1
            
            # Пауза між запитами
            if i < len(self.rotation_angles) - 1:
                time.sleep(3)
        
        print(f"\n🎉 === Тестування завершено ===")
        print(f"✅ Успішно згенеровано: {successful_generations}/{len(self.rotation_angles)}")
        print(f"📁 Датасет: {dataset_path}")
    
    def test_all_prompts(self) -> None:
        """Тестування всіх промптів"""
        print(f"🧪 Початок тестування {len(self.test_prompts)} промптів")
        print(f"🔄 Кожен промпт буде протестований з {len(self.rotation_angles)} кутами обертання")
        print(f"📊 Всього зображень: {len(self.test_prompts) * len(self.rotation_angles)}")
        
        total_successful = 0
        total_attempted = 0
        
        for i, prompt in enumerate(self.test_prompts):
            print(f"\n{'='*60}")
            print(f"📋 Промпт {i+1}/{len(self.test_prompts)}: {prompt['name']}")
            print(f"{'='*60}")
            
            self.test_prompt(prompt)
            
            # Пауза між промптами
            if i < len(self.test_prompts) - 1:
                print(f"\n⏳ Пауза 10 секунд перед наступним промптом...")
                time.sleep(10)
        
        print(f"\n🎉 === ВСЕ ТЕСТУВАННЯ ЗАВЕРШЕНО ===")
        print(f"📊 Результати збережено в: {self.datasets_dir}")
    
    def list_prompts(self) -> None:
        """Виведення списку всіх промптів"""
        print("📝 Доступні промпти для тестування:")
        for i, prompt in enumerate(self.test_prompts, 1):
            print(f"{i:2d}. {prompt['name']}: {prompt['description']}")
    
    def list_rotations(self) -> None:
        """Виведення кутів обертання"""
        print("🔄 Кути обертання:")
        for angle in self.rotation_angles:
            print(f"  • {angle}°")

def main():
    """Головна функція для тестування"""
    try:
        # Перевірка наявності вхідного зображення
        if not Path("data/input/character.jpg").exists():
            print("❌ Помилка: Файл data/input/character.jpg не знайдено")
            return
        
        # Створення тестера
        tester = PromptTester()
        
        # Виведення інформації
        print("🧪 Prompt Tester for FLUX API Image Generator")
        print("=" * 60)
        tester.list_prompts()
        print()
        tester.list_rotations()
        print()
        
        # Підтвердження запуску
        print(f"⚠️  УВАГА: Буде згенеровано {len(tester.test_prompts) * len(tester.rotation_angles)} зображень!")
        print("Це може зайняти багато часу та використати багато API кредитів.")
        
        confirm = input("\nПродовжити? (y/N): ").strip().lower()
        if confirm != 'y':
            print("❌ Скасовано користувачем")
            return
        
        # Запуск тестування
        tester.test_all_prompts()
        
    except ValueError as e:
        print(f"❌ Помилка конфігурації: {e}")
    except Exception as e:
        print(f"❌ Неочікувана помилка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 