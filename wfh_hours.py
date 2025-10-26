# Calculate the total hours worked from the start and end times
# Get user input
# - financial year start date
# - financial year end date
# - average number of days wfh per week
# - file for public holidays
# - file for range of dates for leave (including annaul leave, sick leave, etc.)

import sys
import datetime

# convert string date to datetime object


def str_to_date(date_str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

# convert the public holidays file into a list of dates


def load_public_holidays(file_path):
    with open(file_path, 'r') as file:
        holidays = [line.strip() for line in file.readlines()]
        # convert to date objects if necessary
        holidays = [str_to_date(date) for date in holidays]
    return holidays

# convert the leave dates file into a list of date ranges


def load_leave_dates(file_path):
    leave_ranges = []
    with open(file_path, 'r') as file:
        for line in file.readlines():
            start_str, end_str = line.strip().split(',')
            start_date = str_to_date(start_str.strip())
            end_date = str_to_date(end_str.strip())
            leave_ranges.append((start_date, end_date))
    return leave_ranges


# check the arguments
if len(sys.argv) != 6:
    print("Usage: python wfh_hours.py <financial_year_start> <financial_year_end> <avg_days_wfh_per_week> <public_holidays_file> <leave_dates_file>")
    sys.exit(1)

financial_year_start = str_to_date(sys.argv[1])
financial_year_end = str_to_date(sys.argv[2])
avg_days_wfh_per_week = int(sys.argv[3])
public_holidays_file = sys.argv[4]
leave_dates_file = sys.argv[5]

public_holiday_dates = load_public_holidays(public_holidays_file)
# print("Public Holidays:", public_holiday_dates)

# number of weekdays in the financial year
total_weeks = (financial_year_end - financial_year_start).days // 7
weekdays = total_weeks * 5
remaining_days = (financial_year_end - financial_year_start).days % 7
for i in range(remaining_days):
    if (financial_year_start + datetime.timedelta(days=total_weeks * 7 + i)).weekday() < 5:
        weekdays += 1
# this is usually 260, but can vary with leap years and start/end days
# print("Total Weekdays in Financial Year:", weekdays)

days_public_holidays = 0
for holiday in public_holiday_dates:
    # check if the holiday is a weekday
    if holiday.weekday() < 5:  # 0-4 are Mon-Fri
        if financial_year_start <= holiday <= financial_year_end:
            days_public_holidays += 1
    else:
        # print(f"Skipping weekend holiday: {holiday}")
        pass

# print("Total Public Holidays (weekdays only):", days_public_holidays)

# load leave dates
leave_dates = load_leave_dates(leave_dates_file)
days_leave = 0
for start_date, end_date in leave_dates:
    current_date = start_date
    while current_date <= end_date:
        # check if its a public holiday
        if current_date in public_holiday_dates:
            # print(f"Skipping public holiday during leave: {current_date}")
            current_date += datetime.timedelta(days=1)
            continue
        if current_date.weekday() < 5:  # only count weekdays
            if financial_year_start <= current_date <= financial_year_end:
                # print(f"Counting leave day: {current_date}")
                days_leave += 1
        current_date += datetime.timedelta(days=1)

# print("Total Leave Days (weekdays only):", days_leave)

# calculate total wfh days
total_wfh_days = (weekdays - days_public_holidays - days_leave) * (avg_days_wfh_per_week / 5)
print(f"Total WFH Days in Financial Year: {total_wfh_days:.2f}")