import sqlite3
import requests
from datetime import datetime, date, timedelta


def fetchAPI(num_days):
    today_date = datetime.now().date()

    # Calculate one year before the given date
    one_year_before = today_date - timedelta(days=num_days)

    # Create a list to store the dates
    all_dates = []

    # Generate all dates within the specified range
    current_date = one_year_before
    while current_date <= today_date:
        all_dates.append(current_date)
        current_date += timedelta(days=1)
    train_data = []

    # I wish there was an easier way to fetch a range of dates directly from the API
    for day in all_dates:
        url = f"https://rata.digitraffic.fi/api/v1/trains/{day}/27"
        x = requests.get(url).json()
        train_data.extend(x)

    data_to_insert = []

    for day in train_data:
        for row in day.get("timeTableRows"):
            if row.get("stationShortCode") == 'TPE' and row.get("type") == "ARRIVAL":
                data_to_insert.append(
                    (
                        row.get("scheduledTime"),
                        row.get("stationShortCode"),
                        row.get("cancelled"),
                        row.get("actualTime"),
                        row.get("differenceInMinutes")
                    )
                )
    return data_to_insert


conn = sqlite3.connect('./data/train.db')

# Create a cursor object
cursor = conn.cursor()
# I'll overwrite the file each time to get fresh calculations
# I'll just add one day each time after the initial run
# if length is 365 then just add one row
# fetch latest date as well and if last row already has that date then don't add anything

# cursor.execute("DROP TABLE TrainArrivals")
# Define the schema of the table
create_table_query = """
CREATE TABLE IF NOT EXISTS TrainArrivals (
    scheduledTime DATETIME PRIMARY KEY UNIQUE,
    stationShortCode TEXT,
    cancelled INTEGER,
    actualTime DATETIME,
    differenceInMinutes INTEGER
);
"""

cursor.execute(create_table_query)

res = cursor.execute("SELECT count(*) FROM TrainArrivals")
table_length = int(res.fetchone()[0])

# Only update the current date if a full year has already been loaded
if table_length >= 364:
    num_days = 0
else:
    num_days = 365

# Upsert only
insert_query = """
INSERT OR REPLACE INTO TrainArrivals (
    scheduledTime,
    stationShortCode,
    cancelled,
    actualTime,
    differenceInMinutes
) VALUES (?, ?, ?, ?, ?);
"""

data_to_insert = fetchAPI(num_days)
cursor.executemany(insert_query, data_to_insert)

res = cursor.execute("SELECT count(*) FROM TrainArrivals")
print("Table length:", res.fetchone()[0])

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data loaded into the local database.")
