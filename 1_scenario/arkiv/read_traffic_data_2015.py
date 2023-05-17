import csv
import codecs # helps avoid getting "_csv.Error: line contains NUL"
import datetime

import pandas as pd

# csv file name
input_filename = 'c:/Users/AbdouAA/Downloads/VTI_20150101_20151231_TrafikJVG.csv'
output_filename = '//vti.se/root/Mistrainfra/Data/Trafikdata/Trafikdata 2015/Export_RST_2015.csv'

# small sample (for testing)
#
  
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

# Open/create sample file
with open(output_filename, 'w', encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    
    # Extracting field names through first row
    with open(input_filename, 'r', encoding="utf-8") as csvfile:
        csv_reader = csv.reader(csvfile)
        fields = next(csv_reader)
        writer.writerow(fields)

        # Extracting each data row one by one
        for row in csv_reader:
                row = list(row[0].split(';'))
                if(len(row)<31): # skip if incomplete row
                    continue
                if('J' == row[29]): # skip if train is cancelled
                    continue
                if(row[20]=="Saknas     -    "): # skip if no depature time
                    continue
                if(row[4]=='RST'):
                    # otherwise write the row
                    writer.writerow(row)