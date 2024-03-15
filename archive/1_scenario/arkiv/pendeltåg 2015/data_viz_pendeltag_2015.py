import csv
import codecs # helps avoid getting "_csv.Error: line contains NUL"

import pandas as pd


from datetime import datetime, timedelta

# Set input and output file names
input_file = '//vti.se/root/Mistrainfra/Data/Trafikdata/filter_traffic_data_pendeltag_Bal_Nyh_2015.csv'
output_file = 'data_traffic_Bal_Nyh_2015.csv'



# List of valid platssignatur in the order of travel
valid_platssignatur = ["Bål", "Bro", "Kän", "Khä", "Jkb", "Bkb", "Spå", "Sub", "Ke", "Cst", "Sst", "Åbe", "Äs", "Fas", \
                       "Tåd", "Skg", "Hnd", "Jbo", "Vhn", "Kda", "Ts", "Hfa", "Ssä", "Öso", "Ngd", "Gdv", "Nyh"]

valid_platssignatur_lower = [x.lower() for x in valid_platssignatur]

# Open input file and output file
with open(input_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)

        # Write header row
        writer.writerow(["From station", "To station", "Average travel time"])

        # Initialize variables for tracking station and time
        prev_station = ""
        prev_time = None
        curr_station = ""
        curr_time = None
        travel_times = {}

        # Loop through each row in the input file
        for row in reader:
            # Check if current row is valid and extract relevant columns
            # from
            prev_station = row["Från platssignatur"]
            prev_time = datetime.strptime(row["Planerad avgångstid"], '%Y-%m-%d %H:%M')
            # to
            curr_time = datetime.strptime(row["Planerad ankomsttid"], '%Y-%m-%d %H:%M')
            curr_station = row["Till platssignatur"]
            # travel time
            travel_time = (curr_time - prev_time).total_seconds() / 60
            key = prev_station.upper() + "-" + curr_station.upper()
            if key not in travel_times:
                travel_times[key] = []
                travel_times[key].append(travel_time)
        
        # Calculate the average travel time for each station pair and write to output file
        for i in range(len(valid_platssignatur) - 1):
            key = valid_platssignatur[i].upper() + "-" + valid_platssignatur[i+1].upper()
            if key in travel_times:
                avg_travel_time = sum(travel_times[key]) / len(travel_times[key])
                writer.writerow([valid_platssignatur[i], valid_platssignatur[i+1], avg_travel_time])