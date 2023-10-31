import requests
from datetime import datetime, date, timedelta

today_date = datetime.now().date()

# Calculate one year before the given date
one_year_before = today_date - timedelta(days=365)  # Assuming a year has 365 days


# Create a list to store the dates
all_dates = []

# Generate all dates within the specified range
current_date = one_year_before
while current_date <= today_date:
    all_dates.append(current_date)
    current_date += timedelta(days=1)

url = f"https://rata.digitraffic.fi/api/v1/trains/2022-01-01/27"
x = requests.get(url).json()
# print(x.json())

train_data = []

for day in all_dates[:10]:
    url = f"https://rata.digitraffic.fi/api/v1/trains/{day}/27"
    x = requests.get(url).json()
    train_data.extend(x)


for day in train_data:
    for row in day.get("timeTableRows"):
        if row.get("stationShortCode") == 'TPE' and row.get("type") == "ARRIVAL":
            print(row)
