import requests
from datetime import datetime, timedelta
import re

# Step A: Ask the user for observation ID
observation_id = input("Enter the observation ID: ")

# Step B: Ask for the local start time
local_start_time = input("Enter the local start time (format HH:MM:SS): ")

# Parse the local start time into a datetime object
local_start_datetime = datetime.strptime(local_start_time, "%H:%M:%S")

# Step C: Ask for the data in multiline input
print("Enter the data pairs (time, data, blank line). Type 'END' on a new line when finished:")

# Read multiline input until the user types 'END'
data_input = []
while True:
    time_line = input()
    if time_line.strip().upper() == "END":
        break
    data_line = input()
    blank_line = input()

    # Store each pair as a tuple if the data line length is >= 640
    if len(data_line) >= 640:
        data_input.append((time_line, data_line))

# Step C: Extract long data packets (214 hex doublets) and time
parsed_data = []
time_pattern = re.compile(r"\[(\d{2}:\d{2}:\d{2})R\]")

for time_line, data_line in data_input:
    time_match = time_pattern.search(time_line)
    if time_match:
        offset_time_str = time_match.group(1)  # Extract time offset (HH:MM:SS)
        parsed_data.append((offset_time_str, data_line))

# Verify if we have parsed data
if not parsed_data:
    print("No valid long data packets found in the provided data.")
    exit()

# Step D: Query the SatNOGS API for observation details
satnogs_api_url = f"https://network.satnogs.org/api/observations/{observation_id}/"
response = requests.get(satnogs_api_url)

if response.status_code == 200:
    observation_data = response.json()
    pass_start_time = observation_data.get("start")
    station_name = observation_data.get("ground_station")
    station_lat = observation_data.get("station_lat")
    station_lng = observation_data.get("station_lng")

    if not all([pass_start_time, station_name, station_lat, station_lng]):
        print("Failed to retrieve complete observation details.")
        exit()

    print(f"Observation Start Time: {pass_start_time}")
    print(f"Ground Station Name: {station_name}")
    print(f"Station Latitude: {station_lat}")
    print(f"Station Longitude: {station_lng}")
else:
    print(f"Failed to retrieve observation details. Status code: {response.status_code}")
    exit()

# Convert the pass start time into a datetime object, handling the 'Z' for UTC time
pass_start_datetime = datetime.strptime(pass_start_time, "%Y-%m-%dT%H:%M:%SZ")

# Step E: Generate URLs for each data packet
upload_base_url = "https://db.satnogs.org/api/telemetry/"
norad_id = 61502

print("\nGenerated URLs for uploading telemetry data:")
for offset_time_str, data_packet in parsed_data:
    # Parse the offset time into a datetime object
    offset_time = datetime.strptime(offset_time_str, "%H:%M:%S")

    # Calculate the time difference between local_start_datetime and offset_time
    time_difference = timedelta(
        hours=offset_time.hour - local_start_datetime.hour,
        minutes=offset_time.minute - local_start_datetime.minute,
        seconds=offset_time.second - local_start_datetime.second
    )

    # Add the time difference to the pass_start_datetime to get the final timestamp
    final_timestamp = pass_start_datetime + time_difference
    timestamp_str = final_timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Construct the URL
    upload_url = (
        f"{upload_base_url}?"
        f"satellite={norad_id}&"
        f"timestamp={timestamp_str}&"
        f"frame={data_packet}&"
        f"locator={station_lat},{station_lng}"
    )
    print(upload_url)
