from dataclasses import dataclass, field
from typing import List, Dict, Any
from src.contribution_analyzer import ContributionDay, ContributionData

@dataclass
class StreakPeriod:
    start_date: str
    end_date: str
    length: int
    total_contributions: int
    days: List[ContributionDay] = field(default_factory=list)

@dataclass
class StreakMetrics:
    current_streak: int
    longest_streak: int
    longest_streak_period: StreakPeriod
    all_streaks: List[StreakPeriod]
    constellations: List[StreakPeriod]  # Streaks >= 5 days

class StreakAnalyzer:
    """Detects consecutive activity streaks and builds constellation periods."""

    def __init__(self, data: ContributionData):
        self.data = data

    def analyze(self) -> StreakMetrics:
        days = self.data.days
        if not days:
            empty_streak = StreakPeriod(start_date="N/A", end_date="N/A", length=0, total_contributions=0, days=[])
            return StreakMetrics(
                current_streak=0,
                longest_streak=0,
                longest_streak_period=empty_streak,
                all_streaks=[],
                constellations=[]
            )

        all_streaks: List[StreakPeriod] = []
        current_temp_days: List[ContributionDay] = []

        for day in days:
            if day.count > 0:
                current_temp_days.append(day)
            else:
                if current_temp_days:
                    start_date = current_temp_days[0].date
                    end_date = current_temp_days[-1].date
                    length = len(current_temp_days)
                    total_c = sum(d.count for d in current_temp_days)
                    all_streaks.append(StreakPeriod(
                        start_date=start_date,
                        end_date=end_date,
                        length=length,
                        total_contributions=total_c,
                        days=list(current_temp_days)
                    ))
                    current_temp_days = []

        # Catch tail streak
        if current_temp_days:
            start_date = current_temp_days[0].date
            end_date = current_temp_days[-1].date
            length = len(current_temp_days)
            total_c = sum(d.count for d in current_temp_days)
            all_streaks.append(StreakPeriod(
                start_date=start_date,
                end_date=end_date,
                length=length,
                total_contributions=total_c,
                days=list(current_temp_days)
            ))

        # Longest streak calculation
        longest_streak_period = max(all_streaks, key=lambda s: s.length) if all_streaks else StreakPeriod("N/A", "N/A", 0, 0, [])
        longest_streak = longest_streak_period.length

        # Current streak calculation: check if the latest day in dataset is in the active streak
        current_streak = 0
        if days and days[-1].count > 0:
            if all_streaks and all_streaks[-1].end_date == days[-1].date:
                current_streak = all_streaks[-1].length

        # Constellations: streaks of 5 or more days (or top streaks if none >= 5)
        constellations = [s for s in all_streaks if s.length >= 5]
        if not constellations and all_streaks:
            # Sort by length and take top 3 even if < 5
            constellations = sorted(all_streaks, key=lambda s: s.length, reverse=True)[:3]

        return StreakMetrics(
            current_streak=current_streak,
            longest_streak=longest_streak,
            longest_streak_period=longest_streak_period,
            all_streaks=all_streaks,
            constellations=constellations
        )
