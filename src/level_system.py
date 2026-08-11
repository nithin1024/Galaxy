import math
from dataclasses import dataclass
from typing import List
from src.contribution_analyzer import ContributionData
from src.streak_analyzer import StreakMetrics
from src.achievements import Achievement

LEVEL_TITLES = [
    (1, "Starlight Novice"),
    (3, "Asteroid Pioneer"),
    (5, "Constellation Architect"),
    (8, "Nebula Navigator"),
    (12, "Cosmic Voyager"),
    (18, "Galactic Commander"),
    (25, "Universal Overlord"),
    (35, "Celestial Legend"),
]

def get_level_title(level: int) -> str:
    current_title = "Starlight Novice"
    for lvl_req, title in LEVEL_TITLES:
        if level >= lvl_req:
            current_title = title
    return current_title

@dataclass
class LevelInfo:
    level: int
    title: str
    total_xp: int
    current_level_xp: int
    next_level_xp: int
    progress_percent: float

class LevelSystem:
    """Calculates XP and levels based on contributions, streaks, and achievements."""

    def __init__(self, c_data: ContributionData, streaks: StreakMetrics, achievements: List[Achievement], xp_multiplier: int = 10):
        self.c_data = c_data
        self.streaks = streaks
        self.achievements = achievements
        self.xp_multiplier = xp_multiplier

    def calculate(self) -> LevelInfo:
        unlocked_count = sum(1 for a in self.achievements if a.unlocked)
        
        # Calculate XP
        xp = (self.c_data.total_contributions * self.xp_multiplier) + \
             (self.streaks.longest_streak * 20) + \
             (unlocked_count * 50)

        # Level progression curve: Level L requires L^2 * 100 XP threshold
        # Level 1: 0, Level 2: 100, Level 3: 400, Level 4: 900, Level 5: 1600, etc.
        level = 1
        while True:
            next_req = (level ** 2) * 100
            if xp < next_req:
                break
            level += 1

        prev_req = ((level - 1) ** 2) * 100
        next_req = (level ** 2) * 100

        xp_in_level = xp - prev_req
        xp_needed = next_req - prev_req
        progress = round((xp_in_level / xp_needed) * 100, 1) if xp_needed > 0 else 100.0
        progress = min(max(progress, 0.0), 100.0)

        title = get_level_title(level)

        return LevelInfo(
            level=level,
            title=title,
            total_xp=xp,
            current_level_xp=prev_req,
            next_level_xp=next_req,
            progress_percent=progress
        )
