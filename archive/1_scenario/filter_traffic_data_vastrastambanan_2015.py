import csv

# Set input and output file names
input_file = '//vti.se/root/Mistrainfra/Data/Trafikdata/Trafikdata 2015/Export_RST_2015.csv'
output_file = '//vti.se/root/Mistrainfra/Data/Trafikdata/filter_traffic_data_vastrastambanan_2015.csv'

# Define the list of valid platssignatur values
valid_platssignatur = ["Cst", "Flb", "Söö", "K", "Hpbg", "Sk", "F", "Hr", "A", "G"]
valid_platssignatur_lower = [x.lower() for x in valid_platssignatur]

# initializing the titles and rows list and line counter
# col 1 - tåguppdrag
# col 2 - tågnr
# col 3  {"Tågordning uppdrag", Int64.Type}
# col 4 - {"Datum (PAU)", type date}
# col 5 - {"Tågslag", type text}
# col 6 - {"UppehållstypAvgång", type text}
# col 7 - {"UppehållstypAnkomst", type text}
# col 8 - {"Delsträckanummer", Int64.Type}
# col 9 - {"Första platssignatur", type text}
# col 10 - {"Första platssignatur för uppdrag", type text}
# col 11 - {"Sista platssignatur", type text}
# col 12 - {"Sista platssignatur för uppdrag", type text}

# col 13 - {"Avgångsplats", type text}
# col 14 - {"Från platssignatur", type text}

# col 15 - {"Ankomstplats", type text}
# col 16 - {"Till platssignatur", type text}
# col 17 - {"Sträcka med riktning", type text}
# col 18 - {"Inställelseorsakskod", type text}
# col 19 - {"Inställelseorsak", type text}, 
# 20 {"Ankomsttid", type text}, 
# 21 {"Avgångstid", type text}
# 22 {"Planerad ankomsttid", type datetime}, 
# 23 {"Planerad avgångstid", type datetime}, 
# 24 {"Dragfordonsid", type text}, 
# 25 {"Framförda tågkm", type text}, 
# 26 {"Rapporterad tågvikt", type text}, 
# 27 {"Rapporterad tåglängd", type text}, 
# 28 {"Antal rapporterade vagnar", Int64.Type}, 
# 29 {"Antal rapporterade hjulaxlar", Int64.Type}, 
# 30 {"Inställtflagga", type text},
# 31 {"Planeringsstatus", type text}})


# Open the input and output CSV files
with open(input_file, "r", encoding="utf-8") as csv_file, open(output_file, "w", newline="", encoding="utf-8") as output_csv_file:
    reader = csv.reader(csv_file)
    writer = csv.writer(output_csv_file)
    
    # Write the header row to the output CSV file
    header = next(reader)
    writer.writerow(header)
    

# col 9 - {"Första platssignatur", type text}
# col 10 - {"Första platssignatur för uppdrag", type text}
# col 11 - {"Sista platssignatur", type text}
# col 12 - {"Sista platssignatur för uppdrag", type text}

    # Loop through the rows in the input CSV file
    for row in reader:
        # check if it is a commuter train on the line Bålsta Nynäshamn (or first and last station in the line)
        if (row[8].lower() == 'g' and row[10].lower() == 'cst') or (row[10].lower() == 'g' and row[8].lower() == 'cst'):
            # consider only stops
            if(row[13].lower() in  valid_platssignatur_lower or row[15].lower() in  valid_platssignatur_lower):
                # check if arrival time exist
 #               if row[20] != 'Saknas     -    ':
                writer.writerow(row)