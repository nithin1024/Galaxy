import math
import hashlib
from typing import List, Dict, Any, Tuple
from src.contribution_analyzer import ContributionDay, ContributionData
from src.streak_analyzer import StreakMetrics, StreakPeriod
from src.achievements import Achievement
from src.level_system import LevelInfo

def get_hash_float(key: str) -> float:
    """Returns a deterministic float between 0.0 and 1.0 based on key string."""
    h = hashlib.md5(key.encode("utf-8")).hexdigest()
    return int(h[:8], 16) / 4294967295.0

class SVGComponents:
    """Generates SVG strings for styles, filters, background, galaxy layers, and UI panels."""

    def __init__(self, width: int = 850, height: int = 880, theme: Dict[str, str] = None, animation_enabled: bool = True):
        self.width = width
        self.height = height
        self.theme = theme or {}
        self.animation_enabled = animation_enabled

    def generate_styles_and_defs(self) -> str:
        bg_start = self.theme.get("bg_start", "#080a14")
        bg_end = self.theme.get("bg_end", "#030408")
        nebula_cyan = self.theme.get("nebula_cyan", "#00f0ff")
        nebula_purple = self.theme.get("nebula_purple", "#7000ff")
        nebula_pink = self.theme.get("nebula_pink", "#ff007b")
        accent_cyan = self.theme.get("accent_cyan", "#00f2fe")
        accent_violet = self.theme.get("accent_violet", "#4facfe")

        animations_css = ""
        if self.animation_enabled:
            animations_css = """
            @keyframes twinkle {
                0%, 100% { opacity: 0.3; transform: scale(0.8); }
                50% { opacity: 1.0; transform: scale(1.2); }
            }
            @keyframes pulse-glow {
                0%, 100% { opacity: 0.6; filter: drop-shadow(0 0 4px #00f0ff); }
                50% { opacity: 1.0; filter: drop-shadow(0 0 12px #ff007b); }
            }
            @keyframes rotate-nebula {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
            @keyframes orbit {
                from { transform: rotate(0deg) translateX(14px) rotate(0deg); }
                to { transform: rotate(360deg) translateX(14px) rotate(-360deg); }
            }
            .star-twinkle-1 { animation: twinkle 3s ease-in-out infinite; }
            .star-twinkle-2 { animation: twinkle 4.5s ease-in-out infinite 1.5s; }
            .star-twinkle-3 { animation: twinkle 6s ease-in-out infinite 3s; }
            .pulse-elem { animation: pulse-glow 4s ease-in-out infinite; }
            """

        return f"""
        <defs>
            <!-- Space Background Gradient -->
            <radialGradient id="bg-grad" cx="50%" cy="40%" r="75%" fx="50%" fy="30%">
                <stop offset="0%" stop-color="{bg_start}" />
                <stop offset="100%" stop-color="{bg_end}" />
            </radialGradient>

            <!-- Nebula Radial Gradients -->
            <radialGradient id="nebula-cyan" cx="45%" cy="45%" r="50%">
                <stop offset="0%" stop-color="{nebula_cyan}" stop-opacity="0.35" />
                <stop offset="60%" stop-color="{nebula_cyan}" stop-opacity="0.08" />
                <stop offset="100%" stop-color="{nebula_cyan}" stop-opacity="0" />
            </radialGradient>

            <radialGradient id="nebula-purple" cx="55%" cy="40%" r="55%">
                <stop offset="0%" stop-color="{nebula_purple}" stop-opacity="0.4" />
                <stop offset="70%" stop-color="{nebula_purple}" stop-opacity="0.1" />
                <stop offset="100%" stop-color="{nebula_purple}" stop-opacity="0" />
            </radialGradient>

            <radialGradient id="nebula-pink" cx="50%" cy="50%" r="45%">
                <stop offset="0%" stop-color="{nebula_pink}" stop-opacity="0.3" />
                <stop offset="80%" stop-color="{nebula_pink}" stop-opacity="0.05" />
                <stop offset="100%" stop-color="{nebula_pink}" stop-opacity="0" />
            </radialGradient>

            <!-- Accent & Constellation Gradients -->
            <linearGradient id="constellation-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="{accent_cyan}" stop-opacity="0.9" />
                <stop offset="100%" stop-color="{accent_violet}" stop-opacity="0.5" />
            </linearGradient>

            <linearGradient id="bar-grad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="{accent_cyan}" />
                <stop offset="50%" stop-color="{nebula_purple}" />
                <stop offset="100%" stop-color="{nebula_pink}" />
            </linearGradient>

            <!-- Glow Filters -->
            <filter id="glow-soft" x="-50%" y="-50%" width="200%" height="200%">
                <feGaussianBlur stdDeviation="2.5" result="blur" />
                <feMerge>
                    <feMergeNode in="blur" />
                    <feMergeNode in="SourceGraphic" />
                </feMerge>
            </filter>

            <filter id="glow-intense" x="-100%" y="-100%" width="300%" height="300%">
                <feGaussianBlur stdDeviation="6" result="blur1" />
                <feGaussianBlur stdDeviation="3" result="blur2" />
                <feMerge>
                    <feMergeNode in="blur1" />
                    <feMergeNode in="blur2" />
                    <feMergeNode in="SourceGraphic" />
                </feMerge>
            </filter>
        </defs>

        <style>
            .font-title {{ font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; font-weight: 800; letter-spacing: 2px; }}
            .font-body {{ font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; font-weight: 400; }}
            .font-mono {{ font-family: 'Cascadia Code', 'Fira Code', Consolas, monospace; font-weight: 600; }}
            {animations_css}
        </style>
        """

    def generate_background_and_nebula(self) -> str:
        cx, cy = self.width / 2, 370
        return f"""
        <!-- LAYER 1: Deep Space Background -->
        <rect width="{self.width}" height="{self.height}" fill="url(#bg-grad)" rx="16" />
        
        <!-- Subtle Space Grid -->
        <g opacity="0.04" stroke="#ffffff" stroke-width="0.5">
            <circle cx="{cx}" cy="{cy}" r="120" fill="none" stroke-dasharray="4,4" />
            <circle cx="{cx}" cy="{cy}" r="220" fill="none" stroke-dasharray="6,6" />
            <circle cx="{cx}" cy="{cy}" r="310" fill="none" stroke-dasharray="8,8" />
        </g>

        <!-- LAYER 2: Glowing Galaxy Nebulae -->
        <g transform="translate({cx}, {cy})">
            <ellipse cx="-60" cy="-40" rx="240" ry="170" fill="url(#nebula-cyan)" transform="rotate(-25)" />
            <ellipse cx="70" cy="50" rx="260" ry="180" fill="url(#nebula-purple)" transform="rotate(35)" />
            <ellipse cx="0" cy="0" rx="180" ry="140" fill="url(#nebula-pink)" transform="rotate(10)" />
            <circle cx="0" cy="0" r="45" fill="#ffffff" opacity="0.12" filter="url(#glow-intense)" />
        </g>
        """

    def generate_ambient_stars(self, count: int = 70) -> str:
        stars_svg = ['<!-- LAYER 3: Ambient Twinkling Stars -->\n<g id="ambient-stars">']
        for i in range(count):
            x = get_hash_float(f"star_x_{i}") * self.width
            y = get_hash_float(f"star_y_{i}") * 600  # Keep mostly in top galaxy region
            r = 0.5 + get_hash_float(f"star_r_{i}") * 1.5
            opacity = 0.2 + get_hash_float(f"star_op_{i}") * 0.7
            twinkle_cls = f"star-twinkle-{(i % 3) + 1}" if self.animation_enabled else ""
            stars_svg.append(f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="#ffffff" opacity="{opacity:.2f}" class="{twinkle_cls}" />')
        stars_svg.append('</g>')
        return "\n".join(stars_svg)

def calculate_galaxy_coordinates(days: List[ContributionDay], center_x: float = 425.0, center_y: float = 370.0) -> List[Tuple[float, float, ContributionDay]]:
    """
    Maps 365 contribution days onto a deterministic spiral galaxy layout.
    Uses double logarithmic-spiral arms with pseudo-random spatial jitter based on day date.
    """
    mapped: List[Tuple[float, float, ContributionDay]] = []
    total_days = len(days)

    for idx, c_day in enumerate(days):
        t = idx / max(total_days - 1, 1)  # 0.0 to 1.0
        
        # Spiral parameters
        arm = idx % 2  # 2 spiral arms
        base_angle = 2.4 * math.pi * (t ** 0.9) + (arm * math.pi)
        
        # Radius grows outward from center
        min_r = 35.0
        max_r = 290.0
        r = min_r + (max_r - min_r) * (t ** 0.82)

        # Deterministic spatial jitter
        jitter_r = (get_hash_float(f"jr_{c_day.date}") - 0.5) * 18.0
        jitter_a = (get_hash_float(f"ja_{c_day.date}") - 0.5) * 0.18

        final_r = r + jitter_r
        final_angle = base_angle + jitter_a

        x = center_x + final_r * math.cos(final_angle)
        y = center_y + final_r * math.sin(final_angle)

        mapped.append((x, y, c_day))

    return mapped

def render_star_shape(x: float, y: float, level: int, count: int, date_str: str) -> str:
    """Renders individual contribution star depending on intensity level."""
    if level == 0:
        return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.5" fill="#1b2234" opacity="0.5"><title>{date_str}: 0 contributions</title></circle>'
    elif level == 1:
        return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.4" fill="#00f2fe" opacity="0.85"><title>{date_str}: {count} contribution{"s" if count>1 else ""}</title></circle>'
    elif level == 2:
        return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.6" fill="#7000ff" filter="url(#glow-soft)"><title>{date_str}: {count} contributions</title></circle>'
    elif level == 3:
        # 4-point star flare
        s = 5.0
        path_d = f"M {x} {y-s} L {x+1.5} {y-1.5} L {x+s} {y} L {x+1.5} {y+1.5} L {x} {y+s} L {x-1.5} {y+1.5} L {x-s} {y} L {x-1.5} {y-1.5} Z"
        return f'<path d="{path_d}" fill="#00f0ff" filter="url(#glow-soft)"><title>{date_str}: {count} contributions</title></path>'
    elif level == 4:
        # 4-point bright gold/magenta flare
        s = 7.5
        path_d = f"M {x} {y-s} L {x+2} {y-2} L {x+s} {y} L {x+2} {y+2} L {x} {y+s} L {x-2} {y+2} L {x-s} {y} L {x-2} {y-2} Z"
        return f'<g><circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="#ff007b" opacity="0.25" /><path d="{path_d}" fill="#ff007b" filter="url(#glow-intense)"><title>{date_str}: {count} contributions</title></path></g>'
    else: # level == 5 (20+ contributions) -> Celestial Planet / Supernova
        return f"""
        <g class="pulse-elem">
            <circle cx="{x:.1f}" cy="{y:.1f}" r="12" fill="none" stroke="#00f0ff" stroke-width="1" opacity="0.6" stroke-dasharray="2,2" />
            <ellipse cx="{x:.1f}" cy="{y:.1f}" rx="10" ry="4" fill="none" stroke="#ff007b" stroke-width="1.2" transform="rotate(-20 {x} {y})" />
            <circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#ffffff" filter="url(#glow-intense)"><title>{date_str}: MAJOR MILESTONE - {count} contributions!</title></circle>
        </g>
        """

def render_constellations(coord_map: Dict[str, Tuple[float, float]], constellations: List[StreakPeriod]) -> str:
    """Renders SVG paths for active streak constellations with labels."""
    if not constellations:
        return '<!-- LAYER 5: Constellations (None) -->'

    out = ['<!-- LAYER 5: Streak Constellations -->\n<g id="constellations">']

    for streak in constellations:
        if len(streak.days) < 2:
            continue
            
        points = []
        for day in streak.days:
            if day.date in coord_map:
                points.append(coord_map[day.date])

        if len(points) >= 2:
            d_path = f"M {points[0][0]:.1f} {points[0][1]:.1f} " + " ".join([f"L {pt[0]:.1f} {pt[1]:.1f}" for pt in points[1:]])
            out.append(f'  <path d="{d_path}" fill="none" stroke="url(#constellation-grad)" stroke-width="2" stroke-dasharray="4,3" opacity="0.85" filter="url(#glow-soft)" />')
            
            # Add constellation badge label at mid-point
            mid_pt = points[len(points) // 2]
            out.append(f"""
            <g transform="translate({mid_pt[0]:.1f}, {mid_pt[1] - 12:.1f})">
                <rect x="-42" y="-10" width="84" height="18" rx="9" fill="#0d1326" stroke="#00f0ff" stroke-width="0.8" opacity="0.9" />
                <text x="0" y="2" fill="#00f0ff" font-size="9" text-anchor="middle" class="font-mono">{streak.length} DAY STREAK</text>
            </g>
            """)

    out.append('</g>')
    return "\n".join(out)

def render_statistics_panel(c_data: ContributionData, streaks: StreakMetrics, level_info: LevelInfo, achievements: List[Achievement], title: str = "GITHUB CONTRIBUTION GALAXY", width: int = 850, height: int = 880) -> str:
    """Renders statistics panel, level progress bar, and achievements badge row."""
    panel_y = 635
    card_w = 175
    card_h = 60

    stats = [
        ("CONTRIBUTIONS", f"{c_data.total_contributions:,}", "#00f0ff"),
        ("ACTIVE DAYS", f"{c_data.active_days} / {c_data.total_days}", "#7000ff"),
        ("CURRENT STREAK", f"{streaks.current_streak} DAYS", "#00f2fe"),
        ("LONGEST STREAK", f"{streaks.longest_streak} DAYS", "#ff007b")
    ]

    cards_svg = []
    start_x = (width - (4 * card_w + 3 * 16)) / 2  # Centered cards

    for idx, (label, val, col) in enumerate(stats):
        cx = start_x + idx * (card_w + 16)
        cards_svg.append(f"""
        <g transform="translate({cx:.1f}, {panel_y + 35})">
            <rect width="{card_w}" height="{card_h}" rx="10" fill="#0d1424" stroke="{col}" stroke-opacity="0.35" stroke-width="1" />
            <text x="14" y="22" fill="#7d8b9e" font-size="10" class="font-title">{label}</text>
            <text x="14" y="46" fill="#ffffff" font-size="17" class="font-mono">{val}</text>
        </g>
        """)

    # XP Progress Bar
    bar_x = start_x
    bar_w = 4 * card_w + 3 * 16
    bar_y = panel_y + 110
    fill_w = max(min((level_info.progress_percent / 100.0) * bar_w, bar_w), 4.0)

    # Render Achievements row
    unlocked = [a for a in achievements if a.unlocked]
    achieve_icons = []
    for i, a in enumerate(unlocked[:10]):  # top 10 badges
        ax = bar_x + i * 40
        achieve_icons.append(f"""
        <g transform="translate({ax}, {bar_y + 55})">
            <circle cx="16" cy="16" r="15" fill="#131b2e" stroke="#00f0ff" stroke-width="1" opacity="0.9" />
            <text x="16" y="21" font-size="14" text-anchor="middle">{a.icon}</text>
            <title>{a.title}: {a.description}</title>
        </g>
        """)

    return f"""
    <!-- LAYER 7: Dynamic Statistics Panel -->
    <g id="stats-panel">
        <!-- Panel Title & User Info -->
        <text x="{width/2}" y="{panel_y + 12}" fill="#ffffff" font-size="18" text-anchor="middle" class="font-title" letter-spacing="3">{title}</text>
        <text x="{width/2}" y="{panel_y + 28}" fill="#00f0ff" font-size="12" text-anchor="middle" class="font-mono">@{c_data.username.upper()}</text>

        <!-- Metric Cards -->
        {''.join(cards_svg)}

        <!-- Level & XP Bar Container -->
        <g transform="translate({bar_x}, {bar_y})">
            <text x="0" y="-8" fill="#ffffff" font-size="13" class="font-title">LEVEL {level_info.level} <tspan fill="#7d8b9e">• {level_info.title.upper()}</tspan></text>
            <text x="{bar_w}" y="-8" fill="#00f0ff" font-size="12" text-anchor="end" class="font-mono">{level_info.total_xp:,} XP ({level_info.progress_percent}% NEXT LEVEL)</text>
            
            <!-- Bar Track -->
            <rect width="{bar_w}" height="12" rx="6" fill="#0d1428" stroke="#1f2c47" stroke-width="1" />
            <!-- Bar Fill -->
            <rect width="{fill_w:.1f}" height="12" rx="6" fill="url(#bar-grad)" />
        </g>

        <!-- LAYER 8: Achievements Badge Row -->
        <g transform="translate(0, 0)">
            <text x="{bar_x}" y="{bar_y + 45}" fill="#7d8b9e" font-size="10" class="font-title">UNLOCKED ACHIEVEMENTS ({len(unlocked)}/{len(achievements)})</text>
            {''.join(achieve_icons)}
        </g>
    </g>
    """
