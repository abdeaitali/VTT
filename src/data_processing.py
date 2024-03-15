
import pandas as pd


def read_OD(file_path):
    # Ridership data
    sheet_name = 'OD_pax'
    df_OD = pd.read_excel(file_path, sheet_name=sheet_name, index_col=0)
    # Reset the index to make 'From' a column
    df_OD.reset_index(inplace=True)
    df_OD.rename(columns={'index': 'From'}, inplace=True)
    tidy_df = pd.melt(df_OD, id_vars=['From'], var_name='To', value_name='Passenger_Count')
    return tidy_df

def read_tt_timetable():

    # Load travel time data
    file_path = 'C:/Users/AbdouAA/Work Folders/Documents/GitHub/VTT/data/data_commuter.xlsx'
    sheet_name = 'OD_travel_time'
    df_tt = pd.read_excel(file_path, sheet_name=sheet_name, index_col=0)

    # Reset the index to make 'From' a column
    df_tt.reset_index(inplace=True)
    df_tt.rename(columns={'index': 'From'}, inplace=True)
    tidy_df = pd.melt(df_tt, id_vars=['From'], var_name='To', value_name='Travel_Time')

    # Load station name mapping DataFrame
    stations_mapping_data = {
        'Station': ['Bålsta', 'Bro', 'Kungsängen', 'Kallhäll', 'Jakobsberg', 'Barkarby', 'Spånga', 'Sundbyberg',
                    'Karlberg', 'Stockholms central', 'Stockholms södra', 'Årstaberg', 'Älvsjö', 'Farsta strand',
                    'Trångsund', 'Skogås', 'Handen', 'Jordbro', 'Västerhaninge', 'Krigslida', 'Tungelsta', 'Hemfosa',
                    'Segersäng', 'Ösmo', 'Nynäsgård', 'Gröndalsviken', 'Nynäshamn'],
        'Plts': ['Bål', 'Bro', 'Kän', 'Khä', 'Jkb', 'Bkb', 'Spå', 'Sub', 'Ke', 'Cst', 'Sst', 'Åbe', 'Äs', 'Fas', 'Tåd',
                'Skg', 'Hnd', 'Jbo', 'Vhe', 'Kda', 'Ts', 'Hfa', 'Ssä', 'Öso', 'Ngd', 'Gdv', 'Nyh']
    }

    # Create a DataFrame from the mapping
    stations_mapping = pd.DataFrame(stations_mapping_data)

    # Replace 'From' and 'To' columns in tidy_df with shorter names
    tidy_df['From'] = tidy_df['From'].map(stations_mapping.set_index('Station')['Plts'])
    tidy_df['To'] = tidy_df['To'].map(stations_mapping.set_index('Station')['Plts'])
    tidy_df = tidy_df.dropna(subset=['From', 'To'])
    # convert to minutes (from seconds)
    tidy_df['Travel_Time'] = tidy_df['Travel_Time'] / 60
    return tidy_df    

def read_distance():

    # Load travel time data
    file_path = 'C:/Users/AbdouAA/Work Folders/Documents/GitHub/VTT/data/data_commuter.xlsx'
    sheet_name = 'OD_distances'
    df_dist = pd.read_excel(file_path, sheet_name=sheet_name, index_col=0)

    # Reset the index to make 'From' a column
    df_dist.reset_index(inplace=True)
    df_dist.rename(columns={'index': 'From'}, inplace=True)
    tidy_df = pd.melt(df_dist, id_vars=['From'], var_name='To', value_name='Distance')

    # Load station name mapping DataFrame
    stations_mapping_data = {
        'Station': ['Bålsta', 'Bro', 'Kungsängen', 'Kallhäll', 'Jakobsberg', 'Barkarby', 'Spånga', 'Sundbyberg',
                    'Karlberg', 'Stockholms central', 'Stockholms södra', 'Årstaberg', 'Älvsjö', 'Farsta strand',
                    'Trångsund', 'Skogås', 'Handen', 'Jordbro', 'Västerhaninge', 'Krigslida', 'Tungelsta', 'Hemfosa',
                    'Segersäng', 'Ösmo', 'Nynäsgård', 'Gröndalsviken', 'Nynäshamn'],
        'Plts': ['Bål', 'Bro', 'Kän', 'Khä', 'Jkb', 'Bkb', 'Spå', 'Sub', 'Ke', 'Cst', 'Sst', 'Åbe', 'Äs', 'Fas', 'Tåd',
                'Skg', 'Hnd', 'Jbo', 'Vhe', 'Kda', 'Ts', 'Hfa', 'Ssä', 'Öso', 'Ngd', 'Gdv', 'Nyh']
    }

    # Create a DataFrame from the mapping
    stations_mapping = pd.DataFrame(stations_mapping_data)

    # Replace 'From' and 'To' columns in tidy_df with shorter names
    tidy_df['From'] = tidy_df['From'].map(stations_mapping.set_index('Station')['Plts'])
    tidy_df['To'] = tidy_df['To'].map(stations_mapping.set_index('Station')['Plts'])
    tidy_df = tidy_df.dropna(subset=['From', 'To'])
    # convert to kilometers (from meters)
    tidy_df['Distance'] = tidy_df['Distance'] / 1000
    return tidy_df  

def read_traffic(remove_weekends=True):
    input_file = 'C:/Users/AbdouAA/Work Folders/Documents/GitHub/VTT/data/filter_traffic_data_pendeltag_Bal_Nyh_2015.csv'
    df = pd.read_csv(input_file, delimiter=',')

    # drop observation of departures which are not in the studied stations
    # Your list of valid values
    valid_values = ['Bål', 'Bro', 'Kän', 'Khä', 'Jkb', 'Bkb', 'Spå', 'Sub', 'Ke', 'Cst', 'Sst', 'Åbe', 'Äs', 'Fas', 'Tåd',
                    'Skg', 'Hnd', 'Jbo', 'Vhe', 'Kda', 'Ts', 'Hfa', 'Ssä', 'Öso', 'Ngd', 'Gdv', 'Nyh']

    # Filter rows based on the 'Från platssignatur' column
    df_filtered = df[df['Från platssignatur'].isin(valid_values)]

    # Create a dictionary mapping each station to its index in the north-to-south order
    station_index_mapping = {station: index for index, station in enumerate(valid_values)}

    # Create 'Direction' column based on the mapping for both 'Från platssignatur' and 'Till platssignatur'
    df_filtered['Direction_From'] = df_filtered['Första platssignatur'].str.capitalize().map(station_index_mapping)
    df_filtered['Direction_To'] = df_filtered['Sista platssignatur'].str.capitalize().map(station_index_mapping)

    # Assign direction based on the comparison of indices
    df_filtered['Direction'] = (df_filtered['Direction_To'] < df_filtered['Direction_From']).astype(int)

    if(remove_weekends): # keep only working days (i.e., remove weekend data)
        # Assuming df_traffic is your DataFrame
        df_filtered['Avgångstid'] = pd.to_datetime(df_filtered['Avgångstid'])

        # Extract the day of the week information
        df_filtered['DayOfWeek'] = df_filtered['Avgångstid'].dt.dayofweek

        # Filter out weekends (Saturday and Sunday)
        df_filtered = df_filtered[(df_filtered['DayOfWeek'] >= 0) & (df_filtered['DayOfWeek'] < 5)]
        
    return df_filtered

def read_waiting():
    # Station names and corresponding wait times during peak hours
    data = {
        'From': ["Bål", "Bro", "Kän", "Khä", "Jkb", "Bkb", "Spå", "Sub", "Ke", "Cst", "Sst", "Åbe", "Äs", "Fas", "Tåd", "Skg", "Hnd", "Jbo", "Vhe", "Kda", "Ts", "Hfa", "Ssä", "Öso", "Ngd", "Gdv", "Nyh"],
        'Waiting_Time': [22.5, 22.5, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 22.5, 22.5, 22.5, 22.5, 22.5, 22.5, 22.5, 22.5]
    }

    # avg_waiting = avg_headway / 2
    data['Waiting_Time'] = [value / 2 for value in data['Waiting_Time']]

    # Create the DataFrame
    df = pd.DataFrame(data) 

    return df
