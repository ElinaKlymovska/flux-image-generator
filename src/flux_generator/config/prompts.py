"""
Промпти та налаштування для FLUX API Image Generator
Вдосконалена система з прецизійними технічними параметрами та контекстуальними анотаціями
"""

from typing import Dict, Any, List, Optional

class PromptConfig:
    """Конфігурація промптів для різних стилів з прецизійними параметрами"""
    
    # Базові промпти для різних стилів з уніфікованими технічними параметрами
    PROMPTS = {
        "ultra_realistic": {
            "name": "Ultra Realistic",
            "prompt": "Ultra-realistic portrait of a woman, soft natural lighting, neutral seamless background, hyper-detailed facial features, professional photography setup, 8K resolution, high dynamic range, RAW image quality, perfect skin texture, natural makeup, professional headshot composition",
            "description": "Фотореалістичний портрет з природним освітленням",
            "use_case": "Professional headshots, corporate profiles, high-end fashion catalogs, medical aesthetics documentation",
            "technical_specs": {
                "resolution": "8K",
                "lighting": "soft natural",
                "background": "neutral seamless",
                "focus": "hyper-detailed facial features",
                "quality": "RAW image quality"
            }
        },
        "cinematic": {
            "name": "Cinematic",
            "prompt": "Cinematic portrait of a woman, dramatic lighting, shallow depth of field, film grain effect, professional cinematographic approach, moody atmosphere, high contrast, 8K resolution, cinematic color grading, storytelling composition, emotional depth",
            "description": "Кінематографічний стиль з драматичним освітленням",
            "use_case": "Movie posters, film promotional materials, dramatic storytelling visuals, entertainment industry portfolios",
            "technical_specs": {
                "resolution": "8K",
                "lighting": "dramatic",
                "background": "cinematic depth",
                "focus": "emotional expression",
                "quality": "film grain effect"
            }
        },
        "artistic": {
            "name": "Artistic",
            "prompt": "Artistic portrait of a woman, painterly style, soft brushstrokes, artistic lighting, creative composition, masterpiece quality, fine art photography, 8K resolution, artistic interpretation, gallery-worthy presentation, sophisticated color palette",
            "description": "Художній стиль з живописними ефектами",
            "use_case": "Art galleries, creative portfolios, luxury brand campaigns, cultural exhibitions, fine art publications",
            "technical_specs": {
                "resolution": "8K",
                "lighting": "artistic",
                "background": "creative composition",
                "focus": "painterly style",
                "quality": "masterpiece quality"
            }
        },
        "fashion": {
            "name": "Fashion",
            "prompt": "Fashion portrait of a woman, studio lighting, professional makeup, elegant pose, high fashion photography, magazine quality, sophisticated style, 8K resolution, runway-ready presentation, luxury brand aesthetic, editorial composition",
            "description": "Модний портрет в стилі fashion фотографії",
            "use_case": "Fashion magazines, luxury brand campaigns, runway presentations, beauty product launches, high-end retail catalogs",
            "technical_specs": {
                "resolution": "8K",
                "lighting": "studio",
                "background": "editorial",
                "focus": "fashion presentation",
                "quality": "magazine quality"
            }
        },
        "vintage": {
            "name": "Vintage",
            "prompt": "Vintage portrait of a woman, retro film photography style, warm tones, nostalgic ambiance, classic beauty, timeless elegance, 8K resolution, film grain texture, period-accurate styling, heritage quality preservation",
            "description": "Вінтажний стиль з ретро атмосферою",
            "use_case": "Vintage fashion advertising, themed editorial spreads, heritage brand campaigns, retro product launches, nostalgic marketing materials",
            "technical_specs": {
                "resolution": "8K",
                "lighting": "retro film",
                "background": "nostalgic",
                "focus": "classic beauty",
                "quality": "heritage quality"
            }
        },
        "modern": {
            "name": "Modern",
            "prompt": "Modern portrait of a woman, contemporary style, clean composition, minimalist background, sharp details, professional quality, 8K resolution, contemporary aesthetics, clean lines, sophisticated simplicity",
            "description": "Сучасний мінімалістичний стиль",
            "use_case": "Tech company profiles, modern brand identities, contemporary art exhibitions, minimalist design campaigns, professional networking platforms",
            "technical_specs": {
                "resolution": "8K",
                "lighting": "contemporary",
                "background": "minimalist",
                "focus": "clean composition",
                "quality": "professional quality"
            }
        },
        "dramatic": {
            "name": "Dramatic",
            "prompt": "Dramatic portrait of a woman, intense lighting, strong shadows, emotional expression, powerful composition, artistic photography, 8K resolution, high contrast dynamics, theatrical presentation, impactful visual storytelling",
            "description": "Драматичний стиль з сильними контрастами",
            "use_case": "Theater productions, dramatic advertising campaigns, artistic exhibitions, emotional storytelling, impactful brand messaging",
            "technical_specs": {
                "resolution": "8K",
                "lighting": "intense",
                "background": "dramatic",
                "focus": "emotional expression",
                "quality": "theatrical quality"
            }
        },
        "soft_dreamy": {
            "name": "Soft & Dreamy",
            "prompt": "Soft dreamy portrait of a woman, gentle lighting, soft focus, ethereal atmosphere, romantic mood, delicate beauty, pastel tones, 8K resolution, dreamlike quality, ethereal presentation, romantic storytelling",
            "description": "М'який мрійливий стиль з ефірною атмосферою",
            "use_case": "Romance novels, wedding photography, beauty product campaigns, dreamy advertising, ethereal brand identities",
            "technical_specs": {
                "resolution": "8K",
                "lighting": "gentle",
                "background": "ethereal",
                "focus": "delicate beauty",
                "quality": "dreamlike quality"
            }
        },
        "fantasy": {
            "name": "Fantasy",
            "prompt": "Fantasy portrait of a woman, magical atmosphere, ethereal lighting, fantasy elements, mystical background, dreamlike quality, 8K resolution, otherworldly beauty, enchanted presentation, mystical storytelling",
            "description": "Фентезі стиль з магічною атмосферою",
            "use_case": "Fantasy book covers, gaming character designs, mystical product campaigns, enchanted brand identities, magical storytelling",
            "technical_specs": {
                "resolution": "8K",
                "lighting": "ethereal",
                "background": "mystical",
                "focus": "otherworldly beauty",
                "quality": "enchanted quality"
            }
        },
        "sci_fi": {
            "name": "Sci-Fi",
            "prompt": "Sci-fi portrait of a woman, futuristic lighting, technological elements, neon colors, cyberpunk atmosphere, high tech background, 8K resolution, futuristic aesthetics, technological beauty, advanced presentation",
            "description": "Науково-фантастичний стиль з футуристичними елементами",
            "use_case": "Sci-fi entertainment, tech company branding, futuristic product launches, cyberpunk aesthetics, advanced technology marketing",
            "technical_specs": {
                "resolution": "8K",
                "lighting": "futuristic",
                "background": "high tech",
                "focus": "technological beauty",
                "quality": "advanced quality"
            }
        },
        "noir": {
            "name": "Film Noir",
            "prompt": "Film noir portrait of a woman, black and white, dramatic shadows, film noir lighting, mysterious atmosphere, classic cinema style, 8K resolution, monochromatic beauty, mysterious presentation, classic storytelling",
            "description": "Фільм-нуар стиль з драматичними тінями",
            "use_case": "Classic cinema promotions, mystery genre marketing, vintage detective stories, dramatic advertising, classic film aesthetics",
            "technical_specs": {
                "resolution": "8K",
                "lighting": "film noir",
                "background": "mysterious",
                "focus": "monochromatic beauty",
                "quality": "classic quality"
            }
        },
        "impressionist": {
            "name": "Impressionist",
            "prompt": "Impressionist portrait of a woman, impressionist painting style, soft brushstrokes, natural light, outdoor atmosphere, artistic interpretation, 8K resolution, painterly beauty, artistic presentation, natural storytelling",
            "description": "Імпресіоністичний стиль живопису",
            "use_case": "Art exhibitions, cultural campaigns, artistic brand identities, natural product marketing, outdoor lifestyle promotions",
            "technical_specs": {
                "resolution": "8K",
                "lighting": "natural",
                "background": "outdoor",
                "focus": "painterly beauty",
                "quality": "artistic quality"
            }
        }
    }
    
    # Налаштування для різних аспектів
    ASPECT_RATIOS = {
        "portrait": "2:3",
        "square": "1:1", 
        "landscape": "3:2",
        "wide": "16:9",
        "ultra_wide": "21:9"
    }
    
    # Налаштування якості з прецизійними параметрами
    QUALITY_SETTINGS = {
        "standard": {
            "prompt_upsampling": False,
            "safety_tolerance": 2,
            "description": "Standard quality for general use"
        },
        "high": {
            "prompt_upsampling": True,
            "safety_tolerance": 1,
            "description": "High quality for professional use"
        },
        "creative": {
            "prompt_upsampling": True,
            "safety_tolerance": 3,
            "description": "Creative quality for artistic projects"
        },
        "ultra": {
            "prompt_upsampling": True,
            "safety_tolerance": 0,
            "description": "Ultra quality for premium applications"
        }
    }
    
    @classmethod
    def get_prompt_config(cls, style: str = "ultra_realistic", aspect_ratio: str = "portrait", quality: str = "high") -> Dict[str, Any]:
        """Отримання конфігурації для генерації з прецизійними параметрами"""
        if style not in cls.PROMPTS:
            raise ValueError(f"Невідомий стиль: {style}. Доступні стилі: {list(cls.PROMPTS.keys())}")
        
        if aspect_ratio not in cls.ASPECT_RATIOS:
            raise ValueError(f"Невідомий аспект: {aspect_ratio}. Доступні аспекти: {list(cls.ASPECT_RATIOS.keys())}")
        
        if quality not in cls.QUALITY_SETTINGS:
            raise ValueError(f"Невідома якість: {quality}. Доступні якості: {list(cls.QUALITY_SETTINGS.keys())}")
        
        prompt_data = cls.PROMPTS[style]
        
        return {
            "prompt": prompt_data["prompt"],
            "aspect_ratio": cls.ASPECT_RATIOS[aspect_ratio],
            "quality_settings": cls.QUALITY_SETTINGS[quality],
            "style_name": prompt_data["name"],
            "description": prompt_data["description"],
            "use_case": prompt_data["use_case"],
            "technical_specs": prompt_data["technical_specs"]
        }
    
    @classmethod
    def get_prompt_by_use_case(cls, use_case: str) -> List[Dict[str, Any]]:
        """Отримання промптів за use case"""
        matching_prompts = []
        for style, data in cls.PROMPTS.items():
            if use_case.lower() in data["use_case"].lower():
                matching_prompts.append({
                    "style": style,
                    "name": data["name"],
                    "prompt": data["prompt"],
                    "use_case": data["use_case"],
                    "description": data["description"]
                })
        return matching_prompts
    
    @classmethod
    def get_prompt_by_technical_spec(cls, spec_type: str, spec_value: str) -> List[Dict[str, Any]]:
        """Отримання промптів за технічними специфікаціями"""
        matching_prompts = []
        for style, data in cls.PROMPTS.items():
            if spec_type in data["technical_specs"]:
                if spec_value.lower() in data["technical_specs"][spec_type].lower():
                    matching_prompts.append({
                        "style": style,
                        "name": data["name"],
                        "prompt": data["prompt"],
                        "technical_specs": data["technical_specs"],
                        "description": data["description"]
                    })
        return matching_prompts
    
    @classmethod
    def list_available_styles(cls) -> List[Dict[str, str]]:
        """Список доступних стилів з use cases"""
        return [
            {
                "key": key,
                "name": value["name"],
                "description": value["description"],
                "use_case": value["use_case"]
            }
            for key, value in cls.PROMPTS.items()
        ]
    
    @classmethod
    def list_available_aspects(cls) -> Dict[str, str]:
        """Список доступних аспектів"""
        return cls.ASPECT_RATIOS.copy()
    
    @classmethod
    def list_available_qualities(cls) -> List[Dict[str, str]]:
        """Список доступних якостей з описами"""
        return [
            {
                "key": key,
                "description": value["description"]
            }
            for key, value in cls.QUALITY_SETTINGS.items()
        ]
    
    @classmethod
    def get_style_info(cls, style: str) -> Dict[str, Any]:
        """Отримання детальної інформації про стиль"""
        if style not in cls.PROMPTS:
            raise ValueError(f"Невідомий стиль: {style}")
        
        return cls.PROMPTS[style].copy() 