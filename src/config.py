import json
import os
from typing import Dict, Any

DEFAULT_CONFIG: Dict[str, Any] = {
    "galaxy_title": "GITHUB CONTRIBUTION GALAXY",
    "svg_dimensions": {"width": 850, "height": 880},
    "days_analyzed": 365,
    "star_density": 1.0,
    "animation_enabled": True,
    "xp_multiplier": 10,
    "achievement_thresholds": {
        "streaks": [7, 30, 100],
        "contributions": [100, 500, 1000],
        "active_days": [100]
    },
    "theme": {
        "bg_start": "#080a14",
        "bg_end": "#030408",
        "nebula_cyan": "#00f0ff",
        "nebula_purple": "#7000ff",
        "nebula_pink": "#ff007b",
        "text_primary": "#ffffff",
        "text_secondary": "#8a99ad",
        "accent_cyan": "#00f2fe",
        "accent_violet": "#4facfe",
        "card_bg": "rgba(15, 20, 35, 0.75)",
        "card_border": "rgba(0, 240, 255, 0.25)"
    }
}

class Config:
    """Manages application configuration from config.json with fallback defaults."""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.data = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        config = DEFAULT_CONFIG.copy()
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    user_config = json.load(f)
                    config.update(user_config)
            except Exception as e:
                print(f"[Warning] Failed to load {self.config_path}, using defaults: {e}")
        return config

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    @property
    def title(self) -> str:
        return self.data.get("galaxy_title", "GITHUB CONTRIBUTION GALAXY")

    @property
    def dimensions(self) -> Dict[str, int]:
        return self.data.get("svg_dimensions", {"width": 850, "height": 880})

    @property
    def days_analyzed(self) -> int:
        return self.data.get("days_analyzed", 365)

    @property
    def animation_enabled(self) -> bool:
        return self.data.get("animation_enabled", True)

    @property
    def xp_multiplier(self) -> int:
        return self.data.get("xp_multiplier", 10)

    @property
    def theme(self) -> Dict[str, str]:
        return self.data.get("theme", DEFAULT_CONFIG["theme"])
