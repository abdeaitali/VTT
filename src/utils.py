import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


#######################
##      TRAFFIC
#######################


#######################
##      DELAY
#######################

def get_delay_prob(df, max_delay=30):

    # Convert date columns to datetime format
    df['Planerad avgångstid'] = pd.to_datetime(df['Planerad avgångstid'])
    df['Avgångstid'] = pd.to_datetime(df['Avgångstid'])

    # Calculate departure delays
    df['Departure Delay'] = (df['Avgångstid'] - df['Planerad avgångstid']).dt.total_seconds() / 60. # in minutes
    df['Departure Delay'] = np.maximum(0, df['Departure Delay'])
    df['Departure Delay'] = np.minimum(max_delay, df['Departure Delay'])

    # Filter out only the relevant columns
    delay_data = df[['Från platssignatur', 'Direction', 'Departure Delay']]

    # Group by departure station and delay, then count occurrences
    grouped_data = delay_data.groupby(['Från platssignatur', 'Direction','Departure Delay']).size().reset_index(name='Count')

    # Calculate total number of departures for each station
    total_departures_per_direction = delay_data.groupby(['Från platssignatur', 'Direction']).size().reset_index(name='TotalDepartures')

    # Calculate the standard deviation of delays per departure station
    std_delay_per_station = delay_data.groupby(['Från platssignatur', 'Direction'])['Departure Delay'].std().reset_index(name='Std_Delay')

    # Merge the two DataFrames on 'Från platssignatur'
    merged_data = pd.merge(grouped_data, total_departures_per_direction, on=['Från platssignatur', 'Direction'])
    merged_data = pd.merge(merged_data, std_delay_per_station, on=['Från platssignatur', 'Direction'])

    # Calculate probability as Count / TotalDepartures
    merged_data['Probability'] = merged_data['Count'] / merged_data['TotalDepartures']

    # rename column to "From" instead of "Från platssignatur"
    merged_data.rename(columns={'Från platssignatur': 'From'}, inplace=True)

    # Display the resulting DataFrame
    #print(merged_data.head(40))

    return merged_data


def get_delay_avg_std(df_delay):

    # Group data by 'From' and 'Direction' columns
    grouped_data = df_delay.groupby(['From', 'Direction'])

    # Calculate the weighted average and standard deviation of 'Departure Delay' for each group
    average_delay_per_station = grouped_data.apply(lambda group: (group['Departure Delay'] * group['Count'] / group['TotalDepartures']).sum())
    std_delay_per_station = grouped_data.apply(lambda group: ((group['Departure Delay'] - average_delay_per_station[group.name]) ** 2 * group['Count'] / group['TotalDepartures']).sum())

    # Combine average and standard deviation into a single DataFrame
    delay_stats_per_station = pd.DataFrame({
        'Mean Delay': average_delay_per_station,
        'Std Delay': std_delay_per_station
    })

    # Order the stations
    stations_order = ["Bål", "Bro", "Kän", "Khä", "Jkb", "Bkb", "Spå", "Sub", "Ke", "Cst", "Sst", "Åbe", "Äs", "Fas", "Tåd", "Skg", "Hnd", "Jbo", "Vhe", "Kda", "Ts", "Hfa", "Ssä", "Öso", "Ngd", "Gdv", "Nyh"]
    stations_order = stations_order[::-1]

    # Add the terminal stations with an average of 0
    delay_stats_per_station.loc[('Bål', 1), 'Mean Delay'] = 0
    delay_stats_per_station.loc[('Nyh', 0), 'Mean Delay'] = 0
    delay_stats_per_station.loc[('Bål', 1), 'Std Delay'] = 0
    delay_stats_per_station.loc[('Nyh', 0), 'Std Delay'] = 0

    # Sort the data based on the custom order
    delay_stats_sorted = delay_stats_per_station.loc[stations_order]

    return delay_stats_sorted



#######################
##      OTHERS
#######################

def merge_all_df(df_delay, df_delay_avg_std, df_OD, df_w, df_tt, df_dist):
    # replace std in df_delay with Std Delay from df_delay_avg_std
    # Assuming 'From' and 'Direction' are the key columns for merging
    merged_df = pd.merge(df_delay, df_delay_avg_std, how='left', left_on=['From', 'Direction'], right_index=True)
    # Merge dataframes based on 'From', this valid for mergine waiting time (per departure station) and delay
    merged_df = pd.merge(merged_df, df_w, on=['From'], how='left')

    ### Merge DataFrames based on 'From' and 'To'
    # this valid for OD, distances, travel times
    df_combined = pd.merge(df_OD, df_tt, on=['From', 'To'], how='inner')
    df_combined = pd.merge(df_combined, df_dist, on=['From', 'To'], how='inner')

    ### include a column for mapping from to and direction
    # list of station in order from north to south
    valid_values = ['Bål', 'Bro', 'Kän', 'Khä', 'Jkb', 'Bkb', 'Spå', 'Sub', 'Ke', 'Cst', 'Sst', 'Åbe', 'Äs', 'Fas', 'Tåd',
                    'Skg', 'Hnd', 'Jbo', 'Vhe', 'Kda', 'Ts', 'Hfa', 'Ssä', 'Öso', 'Ngd', 'Gdv', 'Nyh']

    # Create a dictionary mapping each station to its index in the north-to-south order
    station_index_mapping = {station: index for index, station in enumerate(valid_values)}

    # Create 'Direction' column based on the mapping for both 'Från platssignatur' and 'Till platssignatur'
    df_combined['Direction_From'] = df_combined['From'].map(station_index_mapping)
    df_combined['Direction_To'] = df_combined['To'].map(station_index_mapping)

    # Assign direction based on the comparison of indices
    df_combined['Direction'] = (df_combined['Direction_To'] < df_combined['Direction_From']).astype(int)

    # final merge
    df_combined = pd.merge(merged_df, df_combined, on=['From', 'Direction'], how='outer')

    # remove rows with no passengers
    df_result = df_combined[df_combined['Passenger_Count']!=0]

    # return relevant columns/results
    df_result = df_result[['From', 'To', 'Direction', 'Passenger_Count', 'Departure Delay', 'Mean Delay','Std Delay','Count', 'TotalDepartures', 'Probability', 'Travel_Time', 'Waiting_Time', 'Distance']]
    return df_result

#######################
##    GEN. COSTS
#######################

def calc_gen_cost(df_combined):
    # Define cost parameters 
    waiting_cost_short = 81.5/60  # Example waiting time cost per minute
    waiting_cost_long = 66.5/60
    waiting_cost_active = 178.5/60 # Waiting time cost for active waiting (at station)
    travel_time_cost = 71 / 60  # Example travel time cost per minute
    gamma = 0.9  # uncertainty of travel time
    avg_speed = 50 / 60  # speed in km per minute

    # Calculate generalized cost for each case
    df_combined['Generalized_Cost_Never'] = (
        np.where(df_combined['Waiting_Time'] > 10,
                waiting_cost_long * (df_combined['Waiting_Time']-10) + 10*waiting_cost_short, 
                df_combined['Waiting_Time']*waiting_cost_short) +
        waiting_cost_active * df_combined['Departure Delay'] +
        travel_time_cost * np.where(df_combined['Departure Delay'] == 30,
                                                df_combined['Distance'] * avg_speed, df_combined['Travel_Time']) +
                                                travel_time_cost*gamma*df_combined['Std Delay']
    )

    df_combined['Generalized_Cost_After'] = (
        np.where(df_combined['Waiting_Time'] > 10,
                waiting_cost_long * (df_combined['Waiting_Time']-10) + 10*waiting_cost_short, df_combined['Waiting_Time']*waiting_cost_short) +
        waiting_cost_active * df_combined['Departure Delay'] +
        travel_time_cost * np.where(df_combined['Departure Delay'] == 30,
                                    df_combined['Distance'] * avg_speed, df_combined['Travel_Time'])
    )

    df_combined['Generalized_Cost_Before'] = (
         np.where(df_combined['Waiting_Time'] + df_combined['Departure Delay'] > 10,
                waiting_cost_long * (df_combined['Waiting_Time'] + df_combined['Departure Delay']-10)+10*waiting_cost_short, 
                waiting_cost_short*(df_combined['Waiting_Time'] + df_combined['Departure Delay']))  +
        travel_time_cost * np.where(df_combined['Departure Delay'] == 30,
                                    df_combined['Distance'] * avg_speed, 
                                    df_combined['Travel_Time'])
    )

    # Display the DataFrame with generalized costs
    return df_combined[['From', 'To', 'Direction', 'Passenger_Count', 'Probability', 'Generalized_Cost_Never', 'Generalized_Cost_After', 'Generalized_Cost_Before']]

def integrate_gen_cost(df_combined):

    # Group by 'From' and 'To' columns
    grouped_df = df_combined.groupby(['From', 'To', 'Direction'])

    # Calculate the total generalized cost for each case
    total_costs_after = grouped_df.apply(
        lambda group: ((group['Generalized_Cost_Never']-group['Generalized_Cost_After'] )* group['Probability']).sum()
    ).reset_index()

    total_costs_before = grouped_df.apply(
        lambda group: ((group['Generalized_Cost_Never']-group['Generalized_Cost_Before'] )* group['Probability']).sum()
    ).reset_index()

    # Merge the two DataFrames on 'From' and 'To'
    result_df = pd.merge(total_costs_after, total_costs_before, on=['From', 'To', 'Direction'])

    # Rename the columns for clarity
    result_df.columns = ['From', 'To', 'Direction', 'Total_Cost_After', 'Total_Cost_Before']

    return result_df


#######################
##    Aggregation (average)
#######################

def aggregate_avg_per_dep(df):
    # Calculate the average per departure station and direction
    df_mean = df.groupby(['From', 'Direction']).mean().reset_index()
    
    # rename to average
    df_mean = df_mean.rename(columns={'Total_Cost_Before': 'Avg_Cost_Before', 'Total_Cost_After': 'Avg_Cost_After'})

    # Add the zero costs for the terminal stations with an average of 0
    new_row = {'From': 'Bål', 'Direction': 1, 'Avg_Cost_After': 0, 'Avg_Cost_Before': 0}
    df_mean = df_mean.append(new_row, ignore_index=True)
    new_row = {'From': 'Nyh', 'Direction': 0, 'Avg_Cost_After': 0, 'Avg_Cost_Before': 0}
    df_mean = df_mean.append(new_row, ignore_index=True)
 
    # Select only the relevant columns
    result_df = df_mean[['From', 'Direction', 'Avg_Cost_Before', 'Avg_Cost_After']]
    
    return result_df


#######################
##    Aggregation (OD)
#######################

def aggregate_total_per_day(df_costs, df_OD):

    # Merge DataFrames based on 'From' and 'To'
    df_combined = pd.merge(df_OD, df_costs, on=['From', 'To'], how='inner')

    # Calculate the total cost for each pair by multiplying the cost by the passenger count
    df_combined['Daily_Cost_After'] = df_combined['Total_Cost_After'] * df_combined['Passenger_Count']
    df_combined['Daily_Cost_Before'] = df_combined['Total_Cost_Before'] * df_combined['Passenger_Count']

    # Group by "From" and "Direction" and sum the daily costs
    grouped_df = df_combined.groupby(['From', 'Direction'])[['Daily_Cost_After', 'Daily_Cost_Before', 'Passenger_Count']].sum().reset_index()

    return grouped_df[['From', 'Direction', 'Passenger_Count', 'Daily_Cost_After', 'Daily_Cost_Before']]

#######################
##    VTT (overview)
#######################

def aggregate_gen_cost(df_costs, OD=False, direction=False):

    # Calculate the total cost for each pair by multiplying the cost by the passenger count
    if(OD):
        print('------ Aggregated Cost (OD-weighted average)')
        if(direction):
            print('## Southbound')
            print(f"> After: {df_costs[df_costs['Direction']==0]['Daily_Cost_After'].sum()/df_costs[df_costs['Direction']==0]['Passenger_Count'].sum()}")
            print(f"> Before: {df_costs[df_costs['Direction']==0]['Daily_Cost_Before'].sum()/df_costs[df_costs['Direction']==0]['Passenger_Count'].sum()}")    
            print('## Northbound')
            print(f"> After: {df_costs[df_costs['Direction']==1]['Daily_Cost_After'].sum()/df_costs[df_costs['Direction']==1]['Passenger_Count'].sum()}")
            print(f"> Before: {df_costs[df_costs['Direction']==1]['Daily_Cost_Before'].sum()/df_costs[df_costs['Direction']==1]['Passenger_Count'].sum()}")              
        else:
            print(f"> After: {df_costs['Daily_Cost_After'].sum()/df_costs['Passenger_Count'].sum()}")
            print(f"> Before: {df_costs['Daily_Cost_Before'].sum()/df_costs['Passenger_Count'].sum()}")
    else:
        print('------ Aggregated Cost (simple average)')
        if(direction):
            print('## Southbound')
            print(f"> After: {df_costs[df_costs['Direction']==0]['Avg_Cost_After'].mean()}")
            print(f"> Before: {df_costs[df_costs['Direction']==0]['Avg_Cost_Before'].mean()}")    
            print('## Northbound')
            print(f"> After: {df_costs[df_costs['Direction']==1]['Avg_Cost_After'].mean()}")
            print(f"> Before: {df_costs[df_costs['Direction']==1]['Avg_Cost_Before'].mean()}")            
        else:
            print(f"> After : {df_costs['Avg_Cost_After'].mean()}")
            print(f"> Before: {df_costs['Avg_Cost_Before'].mean()}")

#######################
##    CBA delay
#######################

def calc_CBA(df_all, df_VT_daily):

    # Calculate the total generalized cost for each case
    total_benefits_after = df_VT_daily['Daily_Cost_After'].sum()/10**6
    total_benefits_before = df_VT_daily['Daily_Cost_Before'].sum()/10**6

#[['From', 'To', 'Direction', 'Passenger_Count', 'Departure Delay', 'Mean Delay','Std Delay',
# 'Count', 'TotalDepartures', 'Probability', 'Travel_Time', 'Waiting_Time', 'Distance']]

    df_all_filter  = df_all[['From', 'To', 'Direction', 'Passenger_Count', 'Departure Delay','Count', 'TotalDepartures']]
    df_no_duplicates = df_all_filter.drop_duplicates() 

    # calculate the delay costs
    grouped_df = df_no_duplicates.groupby(['From'])

    # Calculate the total generalized cost for each case
    delay_cost = 71*3 / 60  # Example delay cost per minute
    #  group['Passenger_Count']/group['TotalDepartures']

    yearly_costs_delay_from = grouped_df.apply(
        lambda group: (delay_cost*135*
                       group['Departure Delay']*group['Count']).sum()
    ).reset_index()

    yearly_costs_delay_from.columns = ['From', 'Total_Delay_Cost']
    
    n_weekdays = 255
    total_costs_delay = yearly_costs_delay_from['Total_Delay_Cost'].sum()/10**6/n_weekdays

    print(f"Total delay cost: {total_costs_delay} million SEK per day")

    # Print benefits
    print(f"Daily benefits After: {total_benefits_after} million SEK per day ({total_benefits_after/total_costs_delay*100} % of total delay cost)")
    print(f"Daily benefits Before: {total_benefits_before} million SEK per day ({total_benefits_before/total_costs_delay*100} % of total delay cost)")
