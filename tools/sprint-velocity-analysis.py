"""Calculate sprint velocity from completed story-point values."""

from __future__ import annotations

import argparse
from typing import List


def calculate_velocity(story_points: List[float]) -> float:
    """Return the total completed story points for a sprint."""
    return sum(story_points)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calculate sprint velocity from story-point values."
    )
    parser.add_argument(
        "story_points",
        metavar="STORY_POINT",
        type=float,
        nargs="+",
        help="Completed story-point values for the sprint.",
    )
    args = parser.parse_args()

    if any(value < 0 for value in args.story_points):
        parser.error("story points must be non-negative")

    return args


def main() -> None:
    args = parse_args()
    velocity = calculate_velocity(args.story_points)
    print(f"Sprint velocity: {velocity:g} story points")


if __name__ == "__main__":
    main()