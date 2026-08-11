import os
import random
import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any, Optional
import requests

logger = logging.getLogger(__name__)

GRAPHQL_URL = "https://api.github.com/graphql"

GRAPHQL_QUERY = """
query($username: String!) {
  user(login: $username) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
            contributionLevel
          }
        }
      }
    }
  }
}
"""

class GitHubClientError(Exception):
    """Custom exception for GitHub API errors."""
    pass

class GitHubClient:
    """Client for fetching GitHub contribution calendar data using GraphQL API."""

    def __init__(self, token: Optional[str] = None, username: Optional[str] = None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.username = username or os.getenv("GITHUB_USERNAME")

    def fetch_contributions(self, mock_if_missing: bool = True) -> Dict[str, Any]:
        """
        Fetches contribution calendar data.
        If credentials are missing or API fails, falls back to mock data if allowed.
        """
        if not self.username:
            if mock_if_missing:
                logger.warning("GITHUB_USERNAME not provided. Using mock data mode.")
                return generate_mock_contributions(username="explorer-user")
            raise GitHubClientError("Missing required environment variable: GITHUB_USERNAME")

        if not self.token:
            if mock_if_missing:
                logger.warning("GITHUB_TOKEN not provided. Using mock data mode.")
                return generate_mock_contributions(username=self.username)
            raise GitHubClientError("Missing required environment variable: GITHUB_TOKEN")

        headers = {
            "Authorization": f"bearer {self.token}",
            "User-Agent": "GitHub-Contribution-Galaxy"
        }

        try:
            logger.info(f"Fetching contribution data for user '{self.username}' via GitHub GraphQL API...")
            response = requests.post(
                GRAPHQL_URL,
                json={"query": GRAPHQL_QUERY, "variables": {"username": self.username}},
                headers=headers,
                timeout=15
            )

            if response.status_code == 401:
                raise GitHubClientError("Authentication failed: Invalid GITHUB_TOKEN")
            elif response.status_code == 403:
                raise GitHubClientError("GitHub API rate limit exceeded or access forbidden")
            elif response.status_code != 200:
                raise GitHubClientError(f"GitHub API returned HTTP status {response.status_code}")

            data = response.json()
            if "errors" in data and data["errors"]:
                error_msg = data["errors"][0].get("message", "Unknown GraphQL error")
                raise GitHubClientError(f"GitHub GraphQL error: {error_msg}")

            user_data = data.get("data", {}).get("user")
            if not user_data:
                raise GitHubClientError(f"User '{self.username}' not found on GitHub")

            calendar = user_data.get("contributionsCollection", {}).get("contributionCalendar")
            if not calendar:
                raise GitHubClientError("Contribution calendar data not found in response")

            logger.info(f"Successfully retrieved {calendar.get('totalContributions', 0)} total contributions for '{self.username}'")
            return {
                "username": self.username,
                "totalContributions": calendar.get("totalContributions", 0),
                "weeks": calendar.get("weeks", []),
                "is_mock": False
            }

        except requests.RequestException as req_err:
            logger.error(f"Network error while fetching GitHub data: {req_err}")
            if mock_if_missing:
                logger.info("Falling back to mock contribution data.")
                return generate_mock_contributions(username=self.username)
            raise GitHubClientError(f"Network error connecting to GitHub: {req_err}")
        except GitHubClientError as client_err:
            logger.error(f"GitHub client error: {client_err}")
            if mock_if_missing and "Invalid" not in str(client_err):
                logger.info("Falling back to mock contribution data.")
                return generate_mock_contributions(username=self.username)
            raise

def generate_mock_contributions(username: str = "galaxy-dev", days: int = 365) -> Dict[str, Any]:
    """Generates realistic mock contribution history for local testing and offline execution."""
    random.seed(42)  # Deterministic seed for reproducible testing
    end_date = datetime.now(timezone.utc).date()
    start_date = end_date - timedelta(days=days)

    weeks = []
    current_date = start_date
    
    # Align to previous Sunday for proper week grid
    days_since_sunday = (current_date.weekday() + 1) % 7
    current_date -= timedelta(days=days_since_sunday)

    total_contributions = 0

    while current_date <= end_date:
        week_days = []
        for _ in range(7):
            if current_date <= end_date:
                # Generate realistic activity patterns (streaks, active days, peak days)
                is_active = random.random() < 0.65
                if is_active:
                    # 70% normal, 20% high, 10% peak day
                    roll = random.random()
                    if roll < 0.7:
                        count = random.randint(1, 4)
                    elif roll < 0.9:
                        count = random.randint(5, 12)
                    else:
                        count = random.randint(13, 25)
                else:
                    count = 0

                # Assign intensity level
                if count == 0:
                    level = "NONE"
                elif count <= 2:
                    level = "FIRST_QUARTILE"
                elif count <= 5:
                    level = "SECOND_QUARTILE"
                elif count <= 10:
                    level = "THIRD_QUARTILE"
                else:
                    level = "FOURTH_QUARTILE"

                total_contributions += count
                week_days.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "contributionCount": count,
                    "contributionLevel": level
                })
            current_date += timedelta(days=1)
        
        if week_days:
            weeks.append({"contributionDays": week_days})

    return {
        "username": username,
        "totalContributions": total_contributions,
        "weeks": weeks,
        "is_mock": True
    }
