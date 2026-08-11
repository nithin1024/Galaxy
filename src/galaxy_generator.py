import json
import os
import logging
from dataclasses import asdict
from typing import Dict, Any, Optional

from src.config import Config
from src.github_client import GitHubClient, generate_mock_contributions
from src.contribution_analyzer import ContributionAnalyzer, ContributionData
from src.streak_analyzer import StreakAnalyzer, StreakMetrics
from src.achievements import AchievementEngine, Achievement
from src.level_system import LevelSystem, LevelInfo
from src.svg_components import (
    SVGComponents,
    calculate_galaxy_coordinates,
    render_star_shape,
    render_constellations,
    render_statistics_panel
)

logger = logging.getLogger(__name__)

class GalaxyGenerator:
    """Master generator producing SVG visual galaxy and stats.json export."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()

    def generate(self, raw_data: Optional[Dict[str, Any]] = None, output_dir: str = "output") -> Dict[str, str]:
        os.makedirs(output_dir, exist_ok=True)

        # Step 1: Fetch raw data if not provided
        if not raw_data:
            client = GitHubClient()
            raw_data = client.fetch_contributions(mock_if_missing=True)

        # Step 2: Analyze contribution data
        c_analyzer = ContributionAnalyzer(raw_data)
        c_data: ContributionData = c_analyzer.analyze()

        # Step 3: Analyze streaks
        s_analyzer = StreakAnalyzer(c_data)
        streaks: StreakMetrics = s_analyzer.analyze()

        # Step 4: Evaluate achievements
        a_engine = AchievementEngine(c_data, streaks)
        achievements = a_engine.evaluate()

        # Step 5: Calculate XP and Level
        l_system = LevelSystem(c_data, streaks, achievements, xp_multiplier=self.config.xp_multiplier)
        level_info: LevelInfo = l_system.calculate()

        # Step 6: Generate SVG layers
        dims = self.config.dimensions
        w, h = dims.get("width", 850), dims.get("height", 880)

        svg_comp = SVGComponents(
            width=w,
            height=h,
            theme=self.config.theme,
            animation_enabled=self.config.animation_enabled
        )

        svg_parts = []
        svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="auto">')
        svg_parts.append(svg_comp.generate_styles_and_defs())
        svg_parts.append(svg_comp.generate_background_and_nebula())
        svg_parts.append(svg_comp.generate_ambient_stars(count=80))

        # Map 365 contribution days to coordinates
        coord_tuples = calculate_galaxy_coordinates(c_data.days, center_x=w/2.0, center_y=370.0)
        coord_map: Dict[str, tuple] = {}

        # LAYER 4: Contribution Stars
        star_svgs = ['<!-- LAYER 4: Contribution Stars -->\n<g id="contribution-stars">']
        for x, y, c_day in coord_tuples:
            coord_map[c_day.date] = (x, y)
            star_svgs.append(render_star_shape(x, y, c_day.level, c_day.count, c_day.date))
        star_svgs.append('</g>')

        svg_parts.append("\n".join(star_svgs))
        svg_parts.append(render_constellations(coord_map, streaks.constellations))
        svg_parts.append(render_statistics_panel(
            c_data=c_data,
            streaks=streaks,
            level_info=level_info,
            achievements=achievements,
            title=self.config.title,
            width=w,
            height=h
        ))

        svg_parts.append('</svg>')
        full_svg = "\n".join(svg_parts)

        # Write galaxy.svg
        svg_path = os.path.join(output_dir, "galaxy.svg")
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(full_svg)
        logger.info(f"Generated SVG saved to {svg_path}")

        # Step 7: Export stats.json for Web Preview
        stats_payload = {
            "username": c_data.username,
            "is_mock": c_data.is_mock,
            "total_contributions": c_data.total_contributions,
            "active_days": c_data.active_days,
            "total_days": c_data.total_days,
            "avg_per_active_day": c_data.avg_per_active_day,
            "most_active_day": c_data.most_active_day,
            "most_active_month": c_data.most_active_month,
            "current_streak": streaks.current_streak,
            "longest_streak": streaks.longest_streak,
            "level": asdict(level_info),
            "achievements": [asdict(a) for a in achievements],
            "intensity_distribution": c_data.intensity_distribution,
            "monthly_totals": c_data.monthly_totals
        }

        json_path = os.path.join(output_dir, "stats.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(stats_payload, f, indent=2)
        logger.info(f"Exported statistics JSON saved to {json_path}")

        return {
            "svg_path": svg_path,
            "json_path": json_path
        }
