import pytest
from src.github_client import generate_mock_contributions
from src.contribution_analyzer import ContributionAnalyzer, get_intensity_level

def test_get_intensity_level():
    assert get_intensity_level(0) == 0
    assert get_intensity_level(1) == 1
    assert get_intensity_level(2) == 1
    assert get_intensity_level(3) == 2
    assert get_intensity_level(5) == 2
    assert get_intensity_level(6) == 3
    assert get_intensity_level(10) == 3
    assert get_intensity_level(15) == 4
    assert get_intensity_level(20) == 4
    assert get_intensity_level(25) == 5

def test_contribution_analyzer_mock_data():
    raw_data = generate_mock_contributions(username="test_user", days=100)
    analyzer = ContributionAnalyzer(raw_data)
    c_data = analyzer.analyze()

    assert c_data.username == "test_user"
    assert c_data.total_contributions > 0
    assert c_data.active_days > 0
    assert len(c_data.days) > 0
    assert c_data.most_active_day["count"] > 0
    assert c_data.avg_per_active_day > 0

def test_contribution_analyzer_empty_data():
    raw_data = {
        "username": "empty_user",
        "totalContributions": 0,
        "weeks": []
    }
    analyzer = ContributionAnalyzer(raw_data)
    c_data = analyzer.analyze()

    assert c_data.username == "empty_user"
    assert c_data.total_contributions == 0
    assert c_data.active_days == 0
    assert c_data.avg_per_active_day == 0.0
    assert c_data.most_active_day["count"] == 0
