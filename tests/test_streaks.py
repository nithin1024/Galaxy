import pytest
from src.contribution_analyzer import ContributionAnalyzer, ContributionDay
from src.streak_analyzer import StreakAnalyzer

def create_mock_cdata(counts):
    days = []
    total_c = sum(counts)
    active_d = sum(1 for c in counts if c > 0)

    for idx, c in enumerate(counts):
        date_str = f"2026-01-{(idx+1):02d}"
        days.append(ContributionDay(
            date=date_str,
            count=c,
            level=1 if c > 0 else 0,
            day_of_week=0,
            week_index=idx // 7,
            month="2026-01"
        ))

    raw_data = {
        "username": "streak_tester",
        "totalContributions": total_c,
        "weeks": []
    }
    analyzer = ContributionAnalyzer(raw_data)
    c_data = analyzer.analyze()
    c_data.days = days
    c_data.total_contributions = total_c
    c_data.active_days = active_d
    c_data.total_days = len(counts)
    return c_data

def test_streak_calculation_continuous():
    counts = [1, 2, 3, 4, 5, 6, 7]  # 7-day streak
    c_data = create_mock_cdata(counts)
    analyzer = StreakAnalyzer(c_data)
    metrics = analyzer.analyze()

    assert metrics.longest_streak == 7
    assert metrics.current_streak == 7
    assert len(metrics.constellations) == 1

def test_streak_calculation_broken():
    counts = [1, 2, 3, 0, 0, 5, 5, 5, 5, 5, 0]  # 3 days, 2 zeroes, 5 days, 1 zero
    c_data = create_mock_cdata(counts)
    analyzer = StreakAnalyzer(c_data)
    metrics = analyzer.analyze()

    assert metrics.longest_streak == 5
    assert metrics.current_streak == 0

def test_streak_zero_contributions():
    counts = [0, 0, 0, 0]
    c_data = create_mock_cdata(counts)
    analyzer = StreakAnalyzer(c_data)
    metrics = analyzer.analyze()

    assert metrics.longest_streak == 0
    assert metrics.current_streak == 0
    assert len(metrics.constellations) == 0
