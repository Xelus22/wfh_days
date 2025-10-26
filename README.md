# Calculate the estimated WFH days

All dates in the files are inclusive

Example is NSW Australia public holidays for the 2024-2025 financial year.
Note: If there are extra days outside of the financial year they are not counted.

`public_holidays_2024_2025.txt`

```
2024-06-10
2024-10-07
2024-12-25
2024-12-26
2025-01-01
2025-01-27
2025-04-18
2025-04-19
2025-04-20
2025-04-21
2025-04-25
2025-06-09
2025-08-04
2025-10-06
```

leave_dates_2024_2025.txt
```
2024-12-20, 2025-01-03
2025-04-14, 2025-04-25
```

Example Usage:
`Usage: python wfh_hours.py <financial_year_start> <financial_year_end> <avg_days_wfh_per_week> <public_holidays_file> <leave_dates_file>`

`python3 wfh_hours.py 2024-07-01 2025-06-30 2 public_holidays_2024_2025.txt leave_dates_2024_2025.txt`

