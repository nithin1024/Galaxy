from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any, Optional

@dataclass
class ContributionDay:
    date: str
    count: int
    level: int  # 0: 0, 1: 1-2, 2: 3-5, 3: 6-10, 4: 11-20, 5: 20+
    day_of_week: int  # 0: Mon, 6: Sun
    week_index: int
    month: str  # YYYY-MM

@dataclass
class ContributionData:
    username: str
    total_contributions: int
    active_days: int
    total_days: int
    avg_per_active_day: float
    most_active_day: Dict[str, Any]
    most_active_month: Dict[str, Any]
    monthly_totals: Dict[str, int]
    weekly_totals: Dict[int, int]
    intensity_distribution: Dict[int, int]
    days: List[ContributionDay] = field(default_factory=list)
    is_mock: bool = False

def get_intensity_level(count: int) -> int:
    """Maps contribution count to intensity level 0 to 5."""
    if count == 0:
        return 0
    elif count <= 2:
        return 1
    elif count <= 5:
        return 2
    elif count <= 10:
        return 3
    elif count <= 20:
        return 4
    else:
        return 5

class ContributionAnalyzer:
    """Analyzes raw GitHub calendar data into structured metrics."""

    def __init__(self, raw_data: Dict[str, Any]):
        self.raw_data = raw_data
        self.username = raw_data.get("username", "developer")
        self.is_mock = raw_data.get("is_mock", False)

    def analyze(self) -> ContributionData:
        days: List[ContributionDay] = []
        weeks = self.raw_data.get("weeks", [])

        total_contributions = 0
        active_days = 0
        monthly_totals: Dict[str, int] = {}
        weekly_totals: Dict[int, int] = {}
        intensity_dist: Dict[int, int] = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

        most_active_day = {"date": "N/A", "count": 0}

        for week_idx, week in enumerate(weeks):
            week_count = 0
            for day_info in week.get("contributionDays", []):
                date_str = day_info.get("date", "")
                count = day_info.get("contributionCount", 0)
                level = get_intensity_level(count)

                dt = datetime.strptime(date_str, "%Y-%m-%d") if date_str else datetime.now()
                month_str = dt.strftime("%Y-%m")
                day_of_week = dt.weekday()

                c_day = ContributionDay(
                    date=date_str,
                    count=count,
                    level=level,
                    day_of_week=day_of_week,
                    week_index=week_idx,
                    month=month_str
                )
                days.append(c_day)

                total_contributions += count
                week_count += count
                if count > 0:
                    active_days += 1

                monthly_totals[month_str] = monthly_totals.get(month_str, 0) + count
                intensity_dist[level] = intensity_dist.get(level, 0) + 1

                if count > most_active_day["count"]:
                    most_active_day = {"date": date_str, "count": count}

            weekly_totals[week_idx] = week_count

        total_days = len(days)
        avg_per_active_day = round(total_contributions / active_days, 1) if active_days > 0 else 0.0

        # Calculate most active month
        most_active_month = {"month": "N/A", "count": 0}
        for month_key, month_count in monthly_totals.items():
            if month_count > most_active_month["count"]:
                most_active_month = {"month": month_key, "count": month_count}

        return ContributionData(
            username=self.username,
            total_contributions=total_contributions,
            active_days=active_days,
            total_days=total_days,
            avg_per_active_day=avg_per_active_day,
            most_active_day=most_active_day,
            most_active_month=most_active_month,
            monthly_totals=monthly_totals,
            weekly_totals=weekly_totals,
            intensity_distribution=intensity_dist,
            days=days,
            is_mock=self.is_mock
        )
