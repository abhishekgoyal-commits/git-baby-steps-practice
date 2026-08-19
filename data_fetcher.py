"""Helpers for fetching Jira sprint data."""

from __future__ import annotations

import os
from typing import Any, Dict, List

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None


def get_jira_config() -> Dict[str, str]:
    """Read Jira connection settings from environment variables."""
    return {
        "base_url": os.getenv("JIRA_BASE_URL", "https://your-company.atlassian.net"),
        "email": os.getenv("JIRA_EMAIL", ""),
        "token": os.getenv("JIRA_API_TOKEN", ""),
    }


def fetch_jira_issues(jql: str, max_results: int = 50) -> List[Dict[str, Any]]:
    """Fetch Jira issues matching the provided JQL.

    This is a lightweight starter implementation for the sprint dashboard project.
    It validates configuration, then returns a list of issue summaries.
    """
    if requests is None:
        raise RuntimeError("requests is required. Install it with: pip install requests")

    config = get_jira_config()
    if not config["email"] or not config["token"]:
        raise ValueError("Set JIRA_EMAIL and JIRA_API_TOKEN before fetching Jira data.")

    auth = (config["email"], config["token"])
    url = f"{config['base_url'].rstrip('/')}/rest/api/3/search"
    params = {"jql": jql, "maxResults": max_results, "fields": "summary,status,assignee,storyPoints,duedate"}

    response = requests.get(url, auth=auth, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()
    return payload.get("issues", [])
