import requests

departure_date = 9
train_number = 27

# she needs to arrive by 16:00

url = f"/api/v1/trains/{departure_date}/{train_number}"

url = f"https://rata.digitraffic.fi/api/v1/trains/2020-01-01/27"
x = requests.get(url).json()
# print(x.json())

for row in x[0].get("timeTableRows"):
    # print(row)
    # for y in row
    if row.get("stationShortCode") == 'TPE':
        print(row)
