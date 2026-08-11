import pytest
from src.github_client import generate_mock_contributions
from src.contribution_analyzer import ContributionAnalyzer
from src.streak_analyzer import StreakAnalyzer
from src.achievements import AchievementEngine

def test_achievement_engine_unlocks():
    raw_data = generate_mock_contributions(username="achievement_user", days=365)
    c_data = ContributionAnalyzer(raw_data).analyze()
    streaks = StreakAnalyzer(c_data).analyze()
    
    engine = AchievementEngine(c_data, streaks)
    achievements = engine.evaluate()

    assert len(achievements) > 0
    # First contribution & Galaxy Explorer should unlock for non-zero mock data
    first_contrib = next((a for a in achievements if a.id == "first_contribution"), None)
    assert first_contrib is not None
    assert first_contrib.unlocked is True

def test_achievement_engine_zero_data():
    raw_data = {"username": "zero_user", "totalContributions": 0, "weeks": []}
    c_data = ContributionAnalyzer(raw_data).analyze()
    streaks = StreakAnalyzer(c_data).analyze()
    
    engine = AchievementEngine(c_data, streaks)
    achievements = engine.evaluate()

    first_contrib = next((a for a in achievements if a.id == "first_contribution"), None)
    assert first_contrib.unlocked is False
