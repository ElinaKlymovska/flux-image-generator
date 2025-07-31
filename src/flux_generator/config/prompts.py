"""
Промпти та налаштування для FLUX API Image Generator
"""

from typing import Dict, Any, List, Optional

class PromptConfig:
    
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
        "safe_realistic": {
            "name": "Safe Realistic",
            "prompt": "Professional portrait of a woman, natural lighting, clean background, clear facial details, studio photography, high resolution, professional quality, business headshot composition",
            "description": "Безпечний реалістичний портрет без проблемних фраз",
            "use_case": "Business profiles, professional headshots, corporate photography, safe content generation",
            "technical_specs": {
                "resolution": "high",
                "lighting": "natural",
                "background": "clean",
                "focus": "clear details",
                "quality": "professional"
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
        "safe": {
            "prompt_upsampling": False,
            "safety_tolerance": 6,
            "description": "Safe quality to avoid content moderation"
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
    
    @classmethod
    def get_preset_config(cls, preset: str, aspect_ratio: str = "portrait", quality: str = "high") -> Dict[str, Any]:
        # Пресети для різних типів генерації
        PRESETS = {
            "rotation_front": {
                "name": "Rotation - Front View",
                "prompt": "Front-facing portrait of a woman, direct eye contact, symmetrical composition, professional headshot angle, neutral expression, 8K resolution, perfect lighting from front, maintain exact facial features and identity",
                "description": "Прямий фронтальний ракурс з збереженням ідентичності",
                "use_case": "Character rotation sequences, professional headshots, identity preservation",
                "technical_specs": {
                    "resolution": "8K",
                    "lighting": "front lighting",
                    "background": "neutral",
                    "focus": "facial features preservation",
                    "quality": "identity consistency"
                }
            },
            "rotation_left": {
                "name": "Rotation - Left View",
                "prompt": "Left-facing portrait of a woman, head turned 45 degrees left, elegant pose, side lighting, 8K resolution, dynamic composition, maintain exact facial features, hairstyle, and distinctive characteristics",
                "description": "Поворот на 45° вліво з збереженням ідентичності",
                "use_case": "Character rotation sequences, dynamic portraits",
                "technical_specs": {
                    "resolution": "8K",
                    "lighting": "side lighting",
                    "background": "dynamic",
                    "focus": "identity preservation",
                    "quality": "character consistency"
                }
            },
            "rotation_right": {
                "name": "Rotation - Right View",
                "prompt": "Right-facing portrait of a woman, head turned 45 degrees right, elegant pose, side lighting, 8K resolution, dynamic composition, maintain exact facial features, hairstyle, and distinctive characteristics",
                "description": "Поворот на 45° вправо з збереженням ідентичності",
                "use_case": "Character rotation sequences, dynamic portraits",
                "technical_specs": {
                    "resolution": "8K",
                    "lighting": "side lighting",
                    "background": "dynamic",
                    "focus": "identity preservation",
                    "quality": "character consistency"
                }
            },
            "rotation_back": {
                "name": "Rotation - Back View",
                "prompt": "Back view of a woman, elegant neck and shoulder line, sophisticated back lighting, 8K resolution, artistic rear composition, maintain exact hairstyle and distinctive features from behind",
                "description": "Вид ззаду з збереженням характерних рис",
                "use_case": "Character rotation sequences, artistic portraits",
                "technical_specs": {
                    "resolution": "8K",
                    "lighting": "back lighting",
                    "background": "artistic",
                    "focus": "hairstyle preservation",
                    "quality": "character consistency"
                }
            },
            "rotation_profile_left": {
                "name": "Rotation - Left Profile",
                "prompt": "Left profile portrait of a woman, pure side view, elegant profile line, dramatic side lighting, 8K resolution, classic profile composition, maintain exact facial profile and distinctive features",
                "description": "Профіль вліво з збереженням профілю обличчя",
                "use_case": "Character rotation sequences, profile portraits",
                "technical_specs": {
                    "resolution": "8K",
                    "lighting": "dramatic side",
                    "background": "classic",
                    "focus": "profile preservation",
                    "quality": "character consistency"
                }
            },
            "rotation_profile_right": {
                "name": "Rotation - Right Profile",
                "prompt": "Right profile portrait of a woman, pure side view, elegant profile line, dramatic side lighting, 8K resolution, classic profile composition, maintain exact facial profile and distinctive features",
                "description": "Профіль вправо з збереженням профілю обличчя",
                "use_case": "Character rotation sequences, profile portraits",
                "technical_specs": {
                    "resolution": "8K",
                    "lighting": "dramatic side",
                    "background": "classic",
                    "focus": "profile preservation",
                    "quality": "character consistency"
                }
            },
            "rotation_three_quarter_left": {
                "name": "Rotation - Three Quarter Left",
                "prompt": "Three-quarter left view of a woman, head turned 30 degrees left, classic portrait angle, professional lighting, 8K resolution, timeless composition, maintain exact facial features, eye color, and distinctive characteristics",
                "description": "Три чверті вліво з збереженням ідентичності",
                "use_case": "Character rotation sequences, classic portraits",
                "technical_specs": {
                    "resolution": "8K",
                    "lighting": "professional",
                    "background": "timeless",
                    "focus": "identity preservation",
                    "quality": "character consistency"
                }
            },
            "rotation_three_quarter_right": {
                "name": "Rotation - Three Quarter Right",
                "prompt": "Three-quarter right view of a woman, head turned 30 degrees right, classic portrait angle, professional lighting, 8K resolution, timeless composition, maintain exact facial features, eye color, and distinctive characteristics",
                "description": "Три чверті вправо з збереженням ідентичності",
                "use_case": "Character rotation sequences, classic portraits",
                "technical_specs": {
                    "resolution": "8K",
                    "lighting": "professional",
                    "background": "timeless",
                    "focus": "identity preservation",
                    "quality": "character consistency"
                }
            }
        }
        
        if preset not in PRESETS:
            raise ValueError(f"Невідомий пресет: {preset}. Доступні пресети: {list(PRESETS.keys())}")
        
        if aspect_ratio not in cls.ASPECT_RATIOS:
            raise ValueError(f"Невідомий аспект: {aspect_ratio}. Доступні аспекти: {list(cls.ASPECT_RATIOS.keys())}")
        
        if quality not in cls.QUALITY_SETTINGS:
            raise ValueError(f"Невідома якість: {quality}. Доступні якості: {list(cls.QUALITY_SETTINGS.keys())}")
        
        preset_data = PRESETS[preset]
        
        return {
            "prompt": preset_data["prompt"],
            "aspect_ratio": cls.ASPECT_RATIOS[aspect_ratio],
            "quality_settings": cls.QUALITY_SETTINGS[quality],
            "preset_name": preset_data["name"],
            "description": preset_data["description"],
            "use_case": preset_data["use_case"],
            "technical_specs": preset_data["technical_specs"]
        }
    
    @classmethod
    def list_available_presets(cls) -> List[Dict[str, str]]:
        """Список доступних пресетів"""
        PRESETS = {
            "rotation_front": "Rotation - Front View",
            "rotation_left": "Rotation - Left View", 
            "rotation_right": "Rotation - Right View",
            "rotation_back": "Rotation - Back View",
            "rotation_profile_left": "Rotation - Left Profile",
            "rotation_profile_right": "Rotation - Right Profile",
            "rotation_three_quarter_left": "Rotation - Three Quarter Left",
            "rotation_three_quarter_right": "Rotation - Three Quarter Right"
        }
        
        return [
            {
                "key": key,
                "name": value
            }
            for key, value in PRESETS.items()
        ] 