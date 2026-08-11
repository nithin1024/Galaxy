from dataclasses import dataclass, asdict
from typing import List, Dict, Any
from src.contribution_analyzer import ContributionData
from src.streak_analyzer import StreakMetrics

@dataclass
class Achievement:
    id: str
    title: str
    description: str
    icon: str
    category: str  # streak, total, milestone, consistency
    unlocked: bool
    progress_text: str

class AchievementEngine:
    """Evaluates user contribution metrics against achievements."""

    def __init__(self, c_data: ContributionData, streaks: StreakMetrics):
        self.c_data = c_data
        self.streaks = streaks

    def evaluate(self) -> List[Achievement]:
        total_c = self.c_data.total_contributions
        active_days = self.c_data.active_days
        total_days = max(self.c_data.total_days, 1)
        longest_streak = self.streaks.longest_streak
        max_single_day = self.c_data.most_active_day.get("count", 0)
        active_ratio = active_days / total_days

        achievements_def = [
            Achievement(
                id="first_contribution",
                title="First Contribution",
                description="Made your first contribution to GitHub.",
                icon="🌱",
                category="milestone",
                unlocked=total_c >= 1,
                progress_text=f"{min(total_c, 1)}/1"
            ),
            Achievement(
                id="streak_7",
                title="7 Day Streak",
                description="Maintained a contribution streak for 7 consecutive days.",
                icon="🔥",
                category="streak",
                unlocked=longest_streak >= 7,
                progress_text=f"{min(longest_streak, 7)}/7 days"
            ),
            Achievement(
                id="streak_30",
                title="30 Day Streak",
                description="Maintained a contribution streak for 30 consecutive days.",
                icon="⚡",
                category="streak",
                unlocked=longest_streak >= 30,
                progress_text=f"{min(longest_streak, 30)}/30 days"
            ),
            Achievement(
                id="streak_100",
                title="100 Day Streak",
                description="Maintained an epic 100-day contribution streak.",
                icon="☄️",
                category="streak",
                unlocked=longest_streak >= 100,
                progress_text=f"{min(longest_streak, 100)}/100 days"
            ),
            Achievement(
                id="contributions_100",
                title="100 Contributions",
                description="Reached 100 total contributions in a year.",
                icon="⭐",
                category="total",
                unlocked=total_c >= 100,
                progress_text=f"{min(total_c, 100)}/100"
            ),
            Achievement(
                id="contributions_500",
                title="500 Contributions",
                description="Reached 500 total contributions in a year.",
                icon="🌟",
                category="total",
                unlocked=total_c >= 500,
                progress_text=f"{min(total_c, 500)}/500"
            ),
            Achievement(
                id="contributions_1000",
                title="1000 Contributions",
                description="Reached 1,000 total contributions in a year.",
                icon="✨",
                category="total",
                unlocked=total_c >= 1000,
                progress_text=f"{min(total_c, 1000)}/1000"
            ),
            Achievement(
                id="active_days_100",
                title="100 Active Days",
                description="Active on GitHub for at least 100 distinct days.",
                icon="🗓️",
                category="milestone",
                unlocked=active_days >= 100,
                progress_text=f"{min(active_days, 100)}/100 days"
            ),
            Achievement(
                id="night_coder",
                title="Night Coder",
                description="Pushed 15+ contributions in a single day.",
                icon="🌌",
                category="milestone",
                unlocked=max_single_day >= 15,
                progress_text=f"{min(max_single_day, 15)}/15 in 1 day"
            ),
            Achievement(
                id="consistent_coder",
                title="Consistent Coder",
                description="Active on more than 50% of the days in a year.",
                icon="🎯",
                category="consistency",
                unlocked=active_ratio >= 0.5,
                progress_text=f"{int(active_ratio * 100)}%/50%"
            ),
            Achievement(
                id="galaxy_explorer",
                title="Galaxy Explorer",
                description="Mapped your contribution history into the galaxy.",
                icon="🚀",
                category="milestone",
                unlocked=total_c >= 1,
                progress_text="Unlocked"
            )
        ]

        return achievements_def
