import csv

# Set input and output file names
input_file = '//vti.se/root/Mistrainfra/Data/Trafikdata/Trafikdata 2015/Export_RST_2015.csv'
output_file = '//vti.se/root/Mistrainfra/Data/Trafikdata/filter_traffic_data_pendeltag_Bal_Nyh_2015.csv'

# Define the list of valid platssignatur values
valid_platssignatur = ["Bål", "Bro", "Kän", "Khä", "Jkb", "Bkb", "Spå", "Sub", "Ke", "Cst", "Sst", "Åbe", "Äs", "Fas", \
                       "Tåd", "Skg", "Hnd", "Jbo", "Vhn", "Kda", "Ts", "Hfa", "Ssä", "Öso", "Ngd", "Gdv", "Nyh"]

# create the list of stretches
stretches = []
valid_platssignatur_lower = []
for i in range(len(valid_platssignatur)):
    stretches.append(valid_platssignatur[i] + "-" + valid_platssignatur[i])
    valid_platssignatur_lower.append(valid_platssignatur[i].lower())
    if(i<len(valid_platssignatur)-1):
        stretch = valid_platssignatur[i] + "-" + valid_platssignatur[i+1]
        stretches.append(stretch)
        stretch = valid_platssignatur[i+1] + "-" + valid_platssignatur[i]
        stretches.append(stretch)

# Open the input and output CSV files
with open(input_file, "r", encoding="utf-8") as csv_file, open(output_file, "w", newline="", encoding="utf-8") as output_csv_file:
    reader = csv.reader(csv_file)
    writer = csv.writer(output_csv_file)
    
    # Write the header row to the output CSV file
    header = next(reader)
    writer.writerow(header)
    
    # Loop through the rows in the input CSV file
    for row in reader:
        # check if it is a commuter train on the line Bålsta Nynäshamn (or first and last station in the line)
        if row[8].lower() in valid_platssignatur_lower and row[10].lower() in valid_platssignatur_lower:
            # check if arrival time exist
            if row[20] != 'Saknas     -    ':
                writer.writerow(row)