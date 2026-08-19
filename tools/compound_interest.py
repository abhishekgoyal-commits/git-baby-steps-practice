"""Calculate compound interest from command-line inputs."""

from __future__ import annotations

import argparse


def calculate_amount(principal: float, annual_rate: float, compounds_per_year: int, years: float) -> float:
    """Return the final amount after compound interest."""
    rate = annual_rate / 100
    return principal * (1 + rate / compounds_per_year) ** (compounds_per_year * years)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Calculate compound interest.")
    parser.add_argument("principal", type=float, help="Initial principal amount")
    parser.add_argument("annual_rate", type=float, help="Annual interest rate as a percentage")
    parser.add_argument("compounds_per_year", type=int, help="Number of times interest compounds per year")
    parser.add_argument("years", type=float, help="Total investment time in years")
    args = parser.parse_args()

    if args.principal < 0:
        parser.error("principal must be non-negative")
    if args.annual_rate < 0:
        parser.error("annual_rate must be non-negative")
    if args.compounds_per_year <= 0:
        parser.error("compounds_per_year must be positive")
    if args.years < 0:
        parser.error("years must be non-negative")

    return args


def main() -> None:
    args = parse_args()
    final_amount = calculate_amount(
        args.principal,
        args.annual_rate,
        args.compounds_per_year,
        args.years,
    )
    interest_earned = final_amount - args.principal

    print(f"Final amount: ${final_amount:,.2f}")
    print(f"Interest earned: ${interest_earned:,.2f}")


if __name__ == "__main__":
    main()
