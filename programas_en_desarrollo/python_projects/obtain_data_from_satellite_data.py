import re
from datetime import datetime

# Read the contents of the file
input_filename = "Track.txt"
with open(input_filename, "r") as file:
    file_content = file.read()

# Replace "a. m." with "AM" and "p. m." with "PM"
file_content = re.sub(r"[a]\. [m]\.", "AM", file_content)
file_content = re.sub(r"[p]\. [m]\.", "PM", file_content)

# Search for date, time, latitude and longitude strings using regular expressions
date_time_pattern = r"(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2} [AP][M])"
coordinate_pattern = r"N(\d+\.\d+) W(\d+\.\d+)"
date_time_matches = re.findall(date_time_pattern, file_content)
coordinate_matches = re.findall(coordinate_pattern, file_content)

print("\nDate, time, latitude and longitude strings found!")

# Write the results to a new file
output_filename = "clean_satellite_data.txt"
with open(output_filename, "w") as file:
    for i in range(len(date_time_matches)):
        date_time = date_time_matches[i]
        coordinate = coordinate_matches[i]
        latitude = coordinate[0]
        longitude = coordinate[1]
        # Convert 12-hour clock to 24-hour clock
        date_time_24h = datetime.strptime(date_time, "%d/%m/%Y %I:%M:%S %p").strftime("%d/%m/%Y %H:%M:%S")
        file.write(f"{date_time_24h}, {latitude}, {longitude}\n")