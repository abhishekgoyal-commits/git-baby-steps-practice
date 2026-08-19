"""Formatting logic for converting Jira sprint data into reports."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List


def calculate_sprint_metrics(issues: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate key metrics from Jira issues.
    
    Args:
        issues: List of issue dictionaries from Jira API
        
    Returns:
        Dictionary containing sprint metrics
    """
    total_story_points = 0
    completed_story_points = 0
    total_issues = len(issues)
    completed_issues = 0
    blocked_issues = 0
    overdue_issues = 0
    
    for issue in issues:
        fields = issue.get("fields", {})
        story_points = fields.get("storyPoints", 0) or 0
        status = fields.get("status", {}).get("name", "").lower()
        due_date = fields.get("duedate")
        
        total_story_points += story_points
        
        if status in ["done", "closed", "resolved"]:
            completed_issues += 1
            completed_story_points += story_points
        
        # Check for blocked status
        if "blocked" in status or fields.get("labels"):
            labels = fields.get("labels", [])
            if any("blocked" in str(label).lower() for label in labels):
                blocked_issues += 1
        
        # Check for overdue
        if due_date:
            try:
                due = datetime.strptime(due_date, "%Y-%m-%d")
                if due < datetime.now():
                    overdue_issues += 1
            except (ValueError, TypeError):
                pass
    
    remaining_story_points = total_story_points - completed_story_points
    remaining_issues = total_issues - completed_issues
    completion_percentage = (
        (completed_story_points / total_story_points * 100)
        if total_story_points > 0
        else 0
    )
    
    return {
        "total_story_points": total_story_points,
        "completed_story_points": completed_story_points,
        "remaining_story_points": remaining_story_points,
        "total_issues": total_issues,
        "completed_issues": completed_issues,
        "remaining_issues": remaining_issues,
        "blocked_issues": blocked_issues,
        "overdue_issues": overdue_issues,
        "completion_percentage": round(completion_percentage, 1),
    }


def group_issues_by_assignee(issues: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Group Jira issues by assignee.
    
    Args:
        issues: List of issue dictionaries from Jira API
        
    Returns:
        Dictionary mapping assignee names to their issues
    """
    grouped = {}
    for issue in issues:
        assignee = issue.get("fields", {}).get("assignee")
        assignee_name = assignee.get("displayName", "Unassigned") if assignee else "Unassigned"
        
        if assignee_name not in grouped:
            grouped[assignee_name] = []
        grouped[assignee_name].append(issue)
    
    return grouped


def format_report_section(title: str, content: List[str]) -> str:
    """Format a report section with title and content.
    
    Args:
        title: Section title
        content: List of content lines
        
    Returns:
        Formatted section as string
    """
    section = f"\n## {title}\n"
    section += "\n".join(f"- {line}" for line in content if line)
    return section


def generate_report_from_issues(
    issues: List[Dict[str, Any]], 
    project_name: str = "Sprint", 
    reporting_period: str = None
) -> str:
    """Generate a formatted report from Jira issues.
    
    Args:
        issues: List of issue dictionaries from Jira API
        project_name: Name of project/team for the report
        reporting_period: Optional reporting period description
        
    Returns:
        Formatted report as markdown string
    """
    if reporting_period is None:
        reporting_period = datetime.now().strftime("%B %d, %Y")
    
    metrics = calculate_sprint_metrics(issues)
    grouped_by_assignee = group_issues_by_assignee(issues)
    
    # Determine overall status based on metrics
    if metrics["completion_percentage"] >= 80 and metrics["blocked_issues"] == 0:
        status = "Green"
    elif metrics["completion_percentage"] >= 50:
        status = "Yellow"
    else:
        status = "Red"
    
    report = f"# Status Report\n"
    report += f"\n## Summary\n"
    report += f"- Project/Team: {project_name}\n"
    report += f"- Reporting period: {reporting_period}\n"
    report += f"- Overall status: {status}\n"
    report += f"- Executive summary: Sprint completion at {metrics['completion_percentage']}%. "
    report += f"{metrics['blocked_issues']} blocked items and {metrics['overdue_issues']} overdue items."
    
    # Key Updates
    completed = [f"{metrics['completed_story_points']} story points completed"]
    in_progress = [f"{metrics['remaining_story_points']} story points remaining"]
    risks = []
    if metrics["blocked_issues"] > 0:
        risks.append(f"{metrics['blocked_issues']} blocked items")
    if metrics["overdue_issues"] > 0:
        risks.append(f"{metrics['overdue_issues']} overdue items")
    
    report += format_report_section("Key Updates", [
        f"Completed this period: {', '.join(completed)}",
        f"In progress: {', '.join(in_progress)}",
        f"Risks/blockers: {', '.join(risks) if risks else 'None identified'}",
    ])
    
    # Metrics
    metrics_content = [
        f"Sprint progress: {metrics['completion_percentage']}% complete",
        f"Delivery: {metrics['completed_issues']}/{metrics['total_issues']} issues done",
        f"Team capacity: {len(grouped_by_assignee)} team members involved",
        f"Quality: {metrics['blocked_issues']} blocked items, {metrics['overdue_issues']} overdue",
    ]
    report += format_report_section("Metrics", metrics_content)
    
    # Next Steps
    next_steps = ["Continue tracking blocked items", "Address overdue tasks"]
    report += format_report_section("Next Steps", next_steps)
    
    # Team View
    team_content = []
    for assignee, assignee_issues in sorted(grouped_by_assignee.items()):
        assignee_metrics = calculate_sprint_metrics(assignee_issues)
        team_content.append(
            f"{assignee}: {assignee_metrics['completed_story_points']}/"
            f"{assignee_metrics['total_story_points']} story points "
            f"({assignee_metrics['remaining_issues']} issues remaining)"
        )
    report += format_report_section("Team View", team_content)
    
    return report
