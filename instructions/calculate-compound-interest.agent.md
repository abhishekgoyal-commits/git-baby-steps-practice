# Calculate Compound Interest

## Purpose
Use this instruction when a user needs to calculate compound interest from the command line with the repository's `tools/compound_interest.py` utility.

## Usage
- Invoke the script with four positional arguments in this order: `principal`, `annual_rate`, `compounds_per_year`, and `years`.
- Provide `annual_rate` as a percentage, such as `5` for 5%.
- Use a non-negative principal, annual rate, and number of years; `compounds_per_year` must be a positive integer.
- Run the utility from the repository root:

  ```text
  py tools/compound_interest.py <principal> <annual_rate> <compounds_per_year> <years>
  ```

- Example:

  ```text
  py tools/compound_interest.py 1000 5 12 2
  ```

## Result Format
- Report the `Final amount` and `Interest earned` lines from the tool output.
- Preserve the currency formatting and two decimal places.
- Explain that interest earned is the final amount minus the original principal when additional context is useful.
- Surface argument-validation errors clearly and request corrected non-negative values or a positive compounding frequency.

## Validation Checklist
- Confirm the command includes all four positional arguments in the documented order.
- Confirm the annual rate is interpreted as a percentage rather than a decimal fraction.
- Confirm the output includes both final amount and interest earned.
- Check the known example output: final amount `$1,104.94` and interest earned `$104.94`.
