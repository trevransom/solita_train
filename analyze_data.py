import matplotlib
from flask import Flask, render_template
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd
import sqlite3
import datetime
import pytz

# Connect to the SQLite database
conn = sqlite3.connect('./data/train.db')  # Replace with the path to your SQLite database file

# Create a Pandas DataFrame from a SQL query
query = "SELECT * FROM TrainArrivals"  # Replace with your table name
df = pd.read_sql_query(query, conn)

conn.close()

# Now, the data from the database is in the Pandas DataFrame 'df'
df = df[df['differenceInMinutes'].notna()]
# Convert the 'UTC_Time' column to a datetime object
df['actualTime'] = pd.to_datetime(df['actualTime'])
df['scheduledTime'] = pd.to_datetime(df['scheduledTime'])
# Define the Finland time zone (Eastern European Time, EET)
finland_timezone = pytz.timezone('Europe/Helsinki')

# Apply the time zone conversion using built-in support
df['scheduledTime'] = df['scheduledTime'].dt.tz_convert(finland_timezone)
df['actualTime'] = df['actualTime'].dt.tz_convert(finland_timezone)

# Convert the data into a Pandas Series
arrival_series = pd.Series(df["actualTime"])

# Filter the dataframe to only work on Thursday's
df = df[df['actualTime'].dt.dayofweek == 3]
average_delay = df["differenceInMinutes"].mean()

# Calculate the average time between arrivals
average_time_between_trains = arrival_series.diff().mean()

# Calculate the forecast for the next train arrival
# last_arrival = arrival_series.iloc[-1]
last_scheduled_arrival = df["scheduledTime"].iloc[-1]
# next_arrival_forecast = last_scheduled_arrival + average_time_between_trains

time_prediction = last_scheduled_arrival + datetime.timedelta(minutes=average_delay)
time_prediction = time_prediction.time()

matplotlib.use('Agg')  # Set the Agg backend
data = {
    'Date': df["scheduledTime"].dt.strftime('%m/%d/%Y'),
    'DelayMinutes': df["differenceInMinutes"].values
}
df2 = pd.DataFrame(data)

app = Flask(__name__)


@app.route('/')
def visualize_data():
    # Create an improved line chart to map train delays over the year
    plt.figure(figsize=(14, 10))
    plt.plot(df2['Date'], df2['DelayMinutes'], marker='o', linestyle='-', color='b', markersize=6)
    plt.xlabel('Date')
    plt.ylabel('Delay (minutes)')
    plt.title('Train Delay Mapping Over a Year')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(rotation=45)

    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    chart_url = base64.b64encode(image_stream.read()).decode()
    image_stream.close()
    plt.close()

    # Render the chart on the Flask template
    return render_template('./visuals.html', chart_url=chart_url, arrival_time=time_prediction)


if __name__ == '__main__':
    app.run(debug=True)
