import pytest
from src.github_client import generate_mock_contributions
from src.contribution_analyzer import ContributionAnalyzer
from src.streak_analyzer import StreakAnalyzer
from src.achievements import AchievementEngine
from src.level_system import LevelSystem, get_level_title

def test_get_level_title():
    assert get_level_title(1) == "Starlight Novice"
    assert get_level_title(3) == "Asteroid Pioneer"
    assert get_level_title(5) == "Constellation Architect"
    assert get_level_title(12) == "Cosmic Voyager"
    assert get_level_title(40) == "Celestial Legend"

def test_level_system_progression():
    raw_data = generate_mock_contributions(username="level_tester", days=100)
    c_data = ContributionAnalyzer(raw_data).analyze()
    streaks = StreakAnalyzer(c_data).analyze()
    achievements = AchievementEngine(c_data, streaks).evaluate()

    l_system = LevelSystem(c_data, streaks, achievements, xp_multiplier=10)
    info = l_system.calculate()

    assert info.level >= 1
    assert info.total_xp > 0
    assert 0.0 <= info.progress_percent <= 100.0
    assert isinstance(info.title, str)
