"""
Промпти та налаштування для FLUX API Image Generator
"""

from typing import Dict, Any, List

class PromptConfig:
    """Конфігурація промптів для різних стилів"""
    
    # Базові промпти для різних стилів
    PROMPTS = {
        "realistic": {
            "name": "Ultra Realistic",
            "prompt": "ultra-realistic portrait of a woman, soft natural lighting, neutral background, high quality, detailed facial features, professional photography, 8k resolution",
            "description": "Фотореалістичний портрет з природним освітленням"
        },
        "cinematic": {
            "name": "Cinematic",
            "prompt": "cinematic portrait of a woman, dramatic lighting, shallow depth of field, film grain, professional cinematography, moody atmosphere, high contrast",
            "description": "Кінематографічний стиль з драматичним освітленням"
        },
        "artistic": {
            "name": "Artistic",
            "prompt": "artistic portrait of a woman, painterly style, soft brushstrokes, artistic lighting, creative composition, masterpiece quality, fine art photography",
            "description": "Художній стиль з живописними ефектами"
        },
        "fashion": {
            "name": "Fashion",
            "prompt": "fashion portrait of a woman, studio lighting, professional makeup, elegant pose, high fashion photography, magazine quality, sophisticated style",
            "description": "Модний портрет в стилі fashion фотографії"
        },
        "vintage": {
            "name": "Vintage",
            "prompt": "vintage portrait of a woman, retro style, film photography, warm tones, nostalgic atmosphere, classic beauty, timeless elegance",
            "description": "Вінтажний стиль з ретро атмосферою"
        },
        "modern": {
            "name": "Modern",
            "prompt": "modern portrait of a woman, contemporary style, clean composition, minimalist background, sharp details, professional headshot quality",
            "description": "Сучасний мінімалістичний стиль"
        },
        "dramatic": {
            "name": "Dramatic",
            "prompt": "dramatic portrait of a woman, intense lighting, strong shadows, emotional expression, powerful composition, artistic photography",
            "description": "Драматичний стиль з сильними контрастами"
        },
        "soft": {
            "name": "Soft & Dreamy",
            "prompt": "soft dreamy portrait of a woman, gentle lighting, soft focus, ethereal atmosphere, romantic mood, delicate beauty, pastel tones",
            "description": "М'який мрійливий стиль з ефірною атмосферою"
        }
    }
    
    # Налаштування для різних аспектів
    ASPECT_RATIOS = {
        "portrait": "2:3",
        "square": "1:1", 
        "landscape": "3:2",
        "wide": "16:9"
    }
    
    # Налаштування якості
    QUALITY_SETTINGS = {
        "standard": {
            "prompt_upsampling": False,
            "safety_tolerance": 2
        },
        "high": {
            "prompt_upsampling": True,
            "safety_tolerance": 1
        },
        "creative": {
            "prompt_upsampling": True,
            "safety_tolerance": 3
        }
    }
    
    @classmethod
    def get_prompt_config(cls, style: str = "realistic", aspect_ratio: str = "portrait", quality: str = "standard") -> Dict[str, Any]:
        """Отримання конфігурації для генерації"""
        if style not in cls.PROMPTS:
            raise ValueError(f"Невідомий стиль: {style}. Доступні стилі: {list(cls.PROMPTS.keys())}")
        
        if aspect_ratio not in cls.ASPECT_RATIOS:
            raise ValueError(f"Невідомий аспект: {aspect_ratio}. Доступні аспекти: {list(cls.ASPECT_RATIOS.keys())}")
        
        if quality not in cls.QUALITY_SETTINGS:
            raise ValueError(f"Невідома якість: {quality}. Доступні якості: {list(cls.QUALITY_SETTINGS.keys())}")
        
        return {
            "prompt": cls.PROMPTS[style]["prompt"],
            "aspect_ratio": cls.ASPECT_RATIOS[aspect_ratio],
            "quality_settings": cls.QUALITY_SETTINGS[quality],
            "style_name": cls.PROMPTS[style]["name"],
            "description": cls.PROMPTS[style]["description"]
        }
    
    @classmethod
    def list_available_styles(cls) -> List[Dict[str, str]]:
        """Список доступних стилів"""
        return [
            {
                "key": key,
                "name": value["name"],
                "description": value["description"]
            }
            for key, value in cls.PROMPTS.items()
        ]
    
    @classmethod
    def list_available_aspects(cls) -> Dict[str, str]:
        """Список доступних аспектів"""
        return cls.ASPECT_RATIOS.copy()
    
    @classmethod
    def list_available_qualities(cls) -> List[str]:
        """Список доступних якостей"""
        return list(cls.QUALITY_SETTINGS.keys()) 