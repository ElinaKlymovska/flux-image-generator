#!/usr/bin/env python3
"""
FLUX API Image Generator
Генерація реалістичних зображень жінки за допомогою BFL.ai FLUX API
"""

import os
import time
import json
import requests
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import base64

# Завантаження змінних середовища
load_dotenv()

class FluxImageGenerator:
    """Клас для роботи з FLUX API від BFL.ai"""
    
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
        self.output_dir = Path("data/output")
        self.output_dir.mkdir(exist_ok=True)
    
    def encode_image(self, image_path: str) -> str:
        """Кодування зображення в base64"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def create_generation_request(self, seed: int) -> Dict[str, Any]:
        """Створення запиту для генерації зображення"""
        image_data = self.encode_image("data/input/character.jpg")
        
        return {
            "prompt": "ultra-realistic portrait of a woman, soft natural lighting, neutral background, high quality, detailed facial features",
            "input_image": image_data,
            "seed": seed,
            "aspect_ratio": "2:3",
            "output_format": "jpeg",
            "prompt_upsampling": False,
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
                print(f"Помилка 429: Перевищено ліміт запитів. Очікування...")
                time.sleep(60)  # Очікування 1 хвилини
                return None
            elif response.status_code == 500:
                print(f"Помилка 500: Внутрішня помилка сервера")
                return None
            else:
                print(f"Помилка HTTP {response.status_code}: {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            print("Помилка: Таймаут запиту")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Помилка мережі: {e}")
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
                        print(f"Генерація невдала: {result.get('error', 'Невідома помилка')}")
                        return None
                    elif status == 'processing' or status == 'Pending':
                        print(f"Обробка... (спроба {attempt + 1}/{max_attempts})")
                        time.sleep(5)
                    else:
                        print(f"Статус: {status}")
                        time.sleep(5)
                else:
                    print(f"Помилка HTTP {response.status_code} при опитуванні статусу")
                    time.sleep(5)
                    
            except requests.exceptions.Timeout:
                print("Таймаут при опитуванні статусу")
                time.sleep(5)
            except requests.exceptions.RequestException as e:
                print(f"Помилка мережі при опитуванні: {e}")
                time.sleep(5)
            
            attempt += 1
        
        print("Перевищено час очікування генерації")
        return None
    
    def download_image(self, image_url: str, filename: str) -> bool:
        """Завантаження згенерованого зображення"""
        try:
            response = requests.get(image_url, timeout=30)
            
            if response.status_code == 200:
                file_path = self.output_dir / filename
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print(f"Збережено: {filename}")
                return True
            else:
                print(f"Помилка завантаження зображення: HTTP {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"Помилка завантаження: {e}")
            return False
    
    def generate_images(self, count: int = 15) -> None:
        """Генерація вказаної кількості зображень"""
        print(f"Початок генерації {count} зображень...")
        
        successful_generations = 0
        seeds_used = []
        
        for i in range(count):
            seed = 1000 + i  # Унікальні seed для кожного зображення
            seeds_used.append(seed)
            
            print(f"\n--- Генерація {i + 1}/{count} (seed: {seed}) ---")
            
            # Створення запиту
            request_data = self.create_generation_request(seed)
            
            # Відправка запиту
            polling_url = self.submit_generation(request_data)
            if not polling_url:
                print(f"Пропуск генерації {i + 1} через помилку")
                continue
            
            # Очікування завершення
            result = self.poll_generation_status(polling_url)
            if not result:
                print(f"Пропуск генерації {i + 1} через помилку")
                continue
            
            # Завантаження зображення
            result_data = result.get('result', {})
            image_url = result_data.get('sample')
            if image_url:
                filename = f"woman_{i:02d}_seed{seed}.jpg"
                if self.download_image(image_url, filename):
                    successful_generations += 1
                else:
                    print(f"Помилка завантаження зображення {i + 1}")
            else:
                print(f"URL зображення не знайдено в результаті")
                print(f"Доступні ключі в результаті: {list(result.keys())}")
                print(f"Доступні ключі в result: {list(result_data.keys())}")
            
            # Невелика пауза між запитами
            if i < count - 1:
                time.sleep(2)
        
        print(f"\n=== Генерація завершена ===")
        print(f"Успішно згенеровано: {successful_generations}/{count}")
        print(f"Використані seed: {seeds_used}")
        print(f"Зображення збережено в папці: {self.output_dir.absolute()}")

def main():
    """Головна функція"""
    try:
        # Перевірка наявності вхідного зображення
        if not Path("character.jpg").exists():
            print("Помилка: Файл character.jpg не знайдено")
            return
        
        # Створення генератора
        generator = FluxImageGenerator()
        
        # Генерація 15 зображень
        generator.generate_images(15)
        
    except ValueError as e:
        print(f"Помилка конфігурації: {e}")
    except Exception as e:
        print(f"Неочікувана помилка: {e}")

if __name__ == "__main__":
    main() 