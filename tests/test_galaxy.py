import os
import json
import pytest
from src.config import Config
from src.github_client import generate_mock_contributions
from src.galaxy_generator import GalaxyGenerator

def test_galaxy_generator_file_creation(tmp_path):
    output_dir = str(tmp_path / "output")
    config = Config()
    raw_data = generate_mock_contributions(username="galaxy_test", days=100)

    generator = GalaxyGenerator(config)
    result = generator.generate(raw_data=raw_data, output_dir=output_dir)

    assert os.path.exists(result["svg_path"])
    assert os.path.exists(result["json_path"])

    # Verify SVG Content
    with open(result["svg_path"], "r", encoding="utf-8") as f:
        svg_content = f.read()
        assert "<svg" in svg_content
        assert "</svg>" in svg_content
        assert "viewBox" in svg_content
        assert "GITHUB CONTRIBUTION GALAXY" in svg_content

    # Verify Stats JSON Content
    with open(result["json_path"], "r", encoding="utf-8") as f:
        stats_data = json.load(f)
        assert stats_data["username"] == "galaxy_test"
        assert "total_contributions" in stats_data
        assert "level" in stats_data
        assert "achievements" in stats_data
