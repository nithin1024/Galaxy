#!/usr/bin/env python3
"""
GitHub Contribution Galaxy Generator CLI
Usage: python generate.py [--mock] [--username USERNAME] [--output-dir DIR] [--config CONFIG]
"""

import argparse
import logging
import sys
import os

# Add root directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config import Config
from src.github_client import GitHubClient, generate_mock_contributions
from src.galaxy_generator import GalaxyGenerator

def setup_logging():
    # Force UTF-8 output on Windows consoles
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%H:%M:%S"
    )

def main():
    setup_logging()
    
    # Load .env file manually if it exists
    if os.path.exists(".env"):
        try:
            with open(".env", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        os.environ[k.strip()] = v.strip()
        except Exception as e:
            logging.warning(f"Failed to read .env file: {e}")

    parser = argparse.ArgumentParser(description="Generate an animated SVG GitHub Contribution Galaxy.")
    parser.add_argument("--mock", action="store_true", help="Force mock data generation for local testing.")
    parser.add_argument("--username", type=str, help="GitHub username override.")
    parser.add_argument("--output-dir", type=str, default="output", help="Directory to save generated files.")
    parser.add_argument("--config", type=str, default="config.json", help="Path to config.json file.")

    args = parser.parse_args()

    config = Config(args.config)
    print("==================================================")
    print("      🌌 GITHUB CONTRIBUTION GALAXY GENERATOR     ")
    print("==================================================")

    # Determine data source
    if args.mock:
        username = args.username or "demo-explorer"
        logging.info(f"Running in explicit MOCK DATA mode for '{username}'")
        raw_data = generate_mock_contributions(username=username)
    else:
        client = GitHubClient(username=args.username)
        try:
            raw_data = client.fetch_contributions(mock_if_missing=True)
        except Exception as e:
            logging.error(f"Error fetching GitHub data: {e}")
            sys.exit(1)

    # Run generator
    generator = GalaxyGenerator(config)
    result = generator.generate(raw_data=raw_data, output_dir=args.output_dir)

    print("\n✅ Generation Complete!")
    print(f"  • SVG Galaxy Saved: {result['svg_path']}")
    print(f"  • Stats JSON Saved: {result['json_path']}")
    print("==================================================\n")

if __name__ == "__main__":
    main()
