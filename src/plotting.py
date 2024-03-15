
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


#######################
##      TRAFFIC
#######################

def plot_traffic_dist(df_traffic, station):
    # Filter data for the provided station
    df_traffic_station = df_traffic[df_traffic['Från platssignatur'] == station]

    # Convert to date
    df_traffic_station['Avgångstid'] = pd.to_datetime(df_traffic_station['Avgångstid'])
    # Extract the hour information
    df_traffic_station['Hour'] = df_traffic_station['Avgångstid'].dt.hour

    # Create separate DataFrames for each direction
    df_traffic_north = df_traffic_station[df_traffic_station['Direction'] == 1]
    df_traffic_south = df_traffic_station[df_traffic_station['Direction'] == 0]

    # Plot the histograms with different colors
    plt.figure(figsize=(10, 6))
    plt.hist([df_traffic_north['Hour'], df_traffic_south['Hour']], bins=24, edgecolor='black', alpha=0.7, color=['blue', 'orange'], label=['Northbound', 'Southbound'], stacked=True)

    plt.xlabel('Hour of the Day')
    plt.ylabel('Number of Departures')
    plt.title(f'Number of Departures for Different Hours of the Day at Station {station}')
    plt.xticks(range(24))
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

def plot_nb_obs_all(df):
    # Stations order
    stations_order = ["Bål", "Bro", "Kän", "Khä", "Jkb", "Bkb", "Spå", "Sub", "Ke", "Cst", "Sst", "Åbe", "Äs", "Fas",
                    "Tåd", "Skg", "Hnd", "Jbo", "Vhe", "Kda", "Ts", "Hfa", "Ssä", "Öso", "Ngd", "Gdv", "Nyh"]

    # Count the number of observations per departure station and direction, and order them
    observations_per_direction = df.groupby(['Från platssignatur', 'Direction']).size().unstack().loc[stations_order]

    # Plotting the number of observations per departure station and direction
    plt.figure(figsize=(12, 6))

    fnt_size = 14

    # First plot: Observations for Southwards
    x_south = range(len(stations_order))
    width = 0.4

    plt.bar(x_south, observations_per_direction[0], width=width, color='blue', label='Southwards')
    
    # Second plot: Observations for Northwards
    x_north = [pos + width for pos in x_south]
    plt.bar(x_north, observations_per_direction[1], width=width, color='orange', label='Northwards')

    plt.title('Number of Observations per Departure Station and Direction')
    plt.xlabel('Departure Station')
    plt.ylabel('Number of Observations')
    plt.xticks([pos + width / 2 for pos in x_south], stations_order, rotation='vertical', fontsize=fnt_size)
    plt.legend()
    plt.tight_layout()
    plt.show()

#######################
##      DELAY
#######################

def plot_delay_mean_std(df_delay_avg_std):
    # Order the stations
    stations_order = ["Bål", "Bro", "Kän", "Khä", "Jkb", "Bkb", "Spå", "Sub", "Ke", "Cst", "Sst", "Åbe", "Äs", "Fas", "Tåd", "Skg", "Hnd", "Jbo", "Vhe", "Kda", "Ts", "Hfa", "Ssä", "Öso", "Ngd", "Gdv", "Nyh"]
    stations_order = stations_order[::-1]

    # Sort the data based on the custom order
    df_delay_avg_std_sorted = df_delay_avg_std.loc[stations_order]

    # Create subplots
    fig, axes = plt.subplots(1, 2, figsize=(18, 8))

    # First subplot: Mean Delay
    y_south = range(len(stations_order))
    height = 0.4
    fnt_size = 16

    axes[0].barh(y_south, df_delay_avg_std_sorted['Mean Delay'].loc[:, 0], height=height, color='black', label='Southbound')
    y_north = [pos + height for pos in y_south]
    axes[0].barh(y_north, df_delay_avg_std_sorted['Mean Delay'].loc[:, 1], height=height, color='gray', label='Northbound')

    axes[0].set_title('Average departure delay per station and direction', fontsize=fnt_size)
    axes[0].set_ylabel('Departure stations (ordered from south to north)', fontsize=fnt_size)
    axes[0].set_xlabel('Average delay (in minutes)', fontsize=fnt_size)
    axes[0].tick_params(axis='x', labelsize=fnt_size)  # Set font size for x-axis ticks
    axes[0].set_yticks([pos + height / 2 for pos in y_south], stations_order, fontsize=fnt_size)
    axes[0].grid(axis='y', linestyle='--', alpha=0.7)
    # Move the legend outside
    axes[0].legend(fontsize=fnt_size, bbox_to_anchor=(1.05, 1), loc='upper left')

    # Second subplot: Standard Deviation
    axes[1].barh(y_south, df_delay_avg_std_sorted['Std Delay'].loc[:, 0], height=height, color='black', label='Southbound')
    axes[1].barh(y_north, df_delay_avg_std_sorted['Std Delay'].loc[:, 1], height=height, color='gray', label='Northbound')

    axes[1].set_title('Standard deviation of departure delays per station and direction', fontsize=fnt_size)
    axes[1].set_ylabel('Departure stations', fontsize=fnt_size)
    axes[1].set_xlabel('Standard deviation of delay (in minutes)', fontsize=fnt_size)
    axes[1].set_yticks([pos + height / 2 for pos in y_south], stations_order, fontsize=fnt_size)
    # Move the legend outside
    axes[1].grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()


def plot_delay_dist_at_station(df, stations):
    fnt_size = 20
    plt.figure(figsize=(12, 8))

    for station in stations:
        df_station = df[df['From'] == station][['Direction', 'Departure Delay', 'Probability']]

        df_station_prob_south = df_station[df_station['Direction'] == 0][['Departure Delay', 'Probability']]
        df_station_prob_north = df_station[df_station['Direction'] == 1][['Departure Delay', 'Probability']]

        # Calculate cumulative probabilities
        df_station_prob_south['Cumulative Probability'] = df_station_prob_south['Probability'].cumsum()
        df_station_prob_north['Cumulative Probability'] = df_station_prob_north['Probability'].cumsum()

        # Plot the cumulative distribution functions for southbound and northbound delays at the station
        plt.plot(df_station_prob_south['Departure Delay'], df_station_prob_south['Cumulative Probability'], label=f'{station} - Southbound', alpha=0.7)
        plt.plot(df_station_prob_north['Departure Delay'], df_station_prob_north['Cumulative Probability'], label=f'{station} - Northbound', alpha=0.7)

    plt.title('Delay distribution function per direction at certain stations', fontsize=fnt_size)
    plt.xlabel('Departure delay (in minutes)', fontsize=fnt_size)
    plt.ylabel('Cumulative distribution', fontsize=fnt_size)
    plt.xticks(fontsize=fnt_size)
    plt.yticks(fontsize=fnt_size)
    plt.legend(fontsize=fnt_size)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

## not yet tested
def plot_nb_dep_pairs(df):
    # Stations order
    stations_order = ["Bål", "Bro", "Kän", "Khä", "Jkb", "Bkb", "Spå", "Sub", "Ke", "Cst", "Sst", "Åbe", "Äs", "Fas",
                    "Tåd", "Skg", "Hnd", "Jbo", "Vhe", "Kda", "Ts", "Hfa", "Ssä", "Öso", "Ngd", "Gdv", "Nyh"]

    # Create consecutive station pairs
    station_pairs = list(zip(stations_order, stations_order[1:]))

    # Convert 'Från platssignatur' and 'Till platssignatur' to Categorical to ensure correct ordering
    df['Från platssignatur'] = pd.Categorical(df['Från platssignatur'], categories=stations_order, ordered=True)
    df['Till platssignatur'] = pd.Categorical(df['Till platssignatur'], categories=stations_order, ordered=True)

    # Count the number of departures between consecutive pairs of stations
    departures_per_pair = df.groupby(['Från platssignatur', 'Till platssignatur']).size().loc[station_pairs]

    # Plotting the number of departures between consecutive pairs of stations
    plt.figure(figsize=(12, 6))
    departures_per_pair.plot(kind='bar', color='green')
    plt.title('Number of Departures between Consecutive Station Pairs')
    plt.xlabel('Station Pair')
    plt.ylabel('Number of Departures')
    plt.xticks(rotation='vertical')
    plt.show()

## not yet tested
def plot_nb_dep_pairs_all(df):

    # Count the number of departures for each pair of stations
    departure_counts = df.groupby(['Från platssignatur', 'Till platssignatur']).size().reset_index(name='Departure Count')

    # Sort the data by departure count in descending order
    sorted_departure_counts = departure_counts.sort_values(by='Departure Count', ascending=False)

    # Select the top 30 pairs for plotting
    top_pairs = sorted_departure_counts.head(30)

    # Plot the most frequent departures
    plt.figure(figsize=(12, 6))
    plt.bar(range(len(top_pairs)), top_pairs['Departure Count'], color='blue', edgecolor='black')
    plt.xticks(range(len(top_pairs)), [f"{pair[0]} to {pair[1]}" for pair in zip(top_pairs['Från platssignatur'], top_pairs['Till platssignatur'])], rotation='vertical')
    plt.title('Most Frequent Departures Between Pairs of Stations')
    plt.xlabel('Station Pair')
    plt.ylabel('Departure Count')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

#######################
##      OD
#######################
    
def plot_OD(tidy_df):
    stations_order = ["Bål", "Bro", "Kän", "Khä", "Jkb", "Bkb", "Spå", "Sub", "Ke", "Cst", "Sst", "Åbe", "Äs", "Fas", "Tåd", "Skg", "Hnd", "Jbo", "Vhe", "Kda", "Ts", "Hfa", "Ssä", "Öso", "Ngd", "Gdv", "Nyh"]

    # Pivot the DataFrame to create a matrix suitable for heatmap
    heatmap_data = tidy_df.pivot(index='From', columns='To', values='Passenger_Count')

    # Reorder the rows and columns based on stations_order
    heatmap_data = heatmap_data.loc[stations_order, stations_order]

    # Create an inverted grayscale colormap
    colormap = sns.color_palette("gray_r", as_cmap=True)

    # Create a 2D heatmap with only the upper triangle
    plt.figure(figsize=(10, 8))
    sns.heatmap(heatmap_data, cmap=colormap, annot=False, cbar_kws={'label': 'Number of daily passengers'})#, mask=mask)

    # Set axis labels and title
    plt.xlabel('Arrival stations')
    plt.ylabel('Departure stations')
    plt.title('Daily ridership from departure to arrival stations')

    # Show the plot
    plt.show()


def plot_OD_contours(tidy_df, num_contours=3):
    stations_order = ["Bål", "Bro", "Kän", "Khä", "Jkb", "Bkb", "Spå", "Sub", "Ke", "Cst", "Sst", "Åbe", "Äs", "Fas", "Tåd", "Skg", "Hnd", "Jbo", "Vhe", "Kda", "Ts", "Hfa", "Ssä", "Öso", "Ngd", "Gdv", "Nyh"]

    # Pivot the DataFrame to create a matrix suitable for heatmap
    heatmap_data = tidy_df.pivot(index='From', columns='To', values='Passenger_Count')

    # Reorder the rows and columns based on stations_order
    heatmap_data = heatmap_data.loc[stations_order, stations_order]

    # Create an inverted grayscale colormap
    colormap = sns.color_palette("gray_r", as_cmap=True)

    # Create a 2D heatmap with only the upper triangle
    plt.figure(figsize=(10, 8))
    sns.heatmap(heatmap_data, cmap=colormap, annot=False, cbar_kws={'label': 'Number of daily passengers'})

    # Add contour lines for better visualization of value contours
    contour_lines = plt.contour(heatmap_data, colors='black', linewidths=2, levels=num_contours)

    # Label the contour lines with the contour values
    plt.clabel(contour_lines, inline=True, fontsize=10, fmt='%1.0f')

    # Set axis labels and title
    plt.xlabel('Arrival stations')
    plt.ylabel('Departure stations')
    plt.title('Daily ridership from departure to arrival stations')

    # Add a colorbar for reference
    cbar = plt.colorbar()
    cbar.set_label('Number of daily passengers (contours)')

    # Show the plot
    plt.show()

#######################
##      TIMETABLE
#######################
    
def plot_tt_timetable(tidy_df):
    stations_order = ["Bål", "Bro", "Kän", "Khä", "Jkb", "Bkb", "Spå", "Sub", "Ke", "Cst", "Sst", "Åbe", "Äs", "Fas", "Tåd", "Skg", "Hnd", "Jbo", "Vhe", "Kda", "Ts", "Hfa", "Ssä", "Öso", "Ngd", "Gdv", "Nyh"]

    # Pivot the DataFrame to create a matrix suitable for heatmap
    heatmap_data = tidy_df.pivot(index='From', columns='To', values='Travel_Time')

    # Reorder the rows and columns based on stations_order
    heatmap_data = heatmap_data.loc[stations_order, stations_order]

    # Create an inverted grayscale colormap
    colormap = sns.color_palette("gray_r", as_cmap=True)

    # Create a 2D heatmap with only the upper triangle
    plt.figure(figsize=(10, 8))
    sns.heatmap(heatmap_data, cmap=colormap, annot=False, cbar_kws={'label': 'Travel time in minutes'})

    # Set axis labels and title
    plt.xlabel('Arrival stations')
    plt.ylabel('Departure stations')
    plt.title('Travel time from departure to arrival station according to the timetable')

    # Show the plot
    plt.show()


def plot_tt_timetable_contours(tidy_df, num_contours=5):
    stations_order = ["Bål", "Bro", "Kän", "Khä", "Jkb", "Bkb", "Spå", "Sub", "Ke", "Cst", "Sst", "Åbe", "Äs", "Fas", "Tåd", "Skg", "Hnd", "Jbo", "Vhe", "Kda", "Ts", "Hfa", "Ssä", "Öso", "Ngd", "Gdv", "Nyh"]

    # Pivot the DataFrame to create a matrix suitable for heatmap
    heatmap_data = tidy_df.pivot(index='From', columns='To', values='Travel_Time')

    # Reorder the rows and columns based on stations_order
    heatmap_data = heatmap_data.loc[stations_order, stations_order]

    # Create an inverted grayscale colormap
    colormap = sns.color_palette("gray_r", as_cmap=True)

    # Create a 2D heatmap with only the upper triangle
    plt.figure(figsize=(10, 8))
    sns.heatmap(heatmap_data, cmap=colormap, annot=False, cbar_kws={'label': 'Travel time in minutes'})

    # Add contour lines for better visualization of value contours
    contour_lines = plt.contour(heatmap_data, colors='black', linewidths=2, levels=num_contours)

    # Label the contour lines with the contour values
    plt.clabel(contour_lines, inline=True, fontsize=10, fmt='%1.0f')

    # Set axis labels and title
    plt.xlabel('Arrival stations')
    plt.ylabel('Departure stations')
    plt.title('Travel time from departure to arrival station according to the timetable')

    # Show the plot
    plt.show()


#######################
##      DISTANCE
#######################
    
def plot_distance(tidy_df):
    stations_order = ["Bål", "Bro", "Kän", "Khä", "Jkb", "Bkb", "Spå", "Sub", "Ke", "Cst", "Sst", "Åbe", "Äs", "Fas", "Tåd", "Skg", "Hnd", "Jbo", "Vhe", "Kda", "Ts", "Hfa", "Ssä", "Öso", "Ngd", "Gdv", "Nyh"]

    # Pivot the DataFrame to create a matrix suitable for heatmap
    heatmap_data = tidy_df.pivot(index='From', columns='To', values='Distance')

    # Reorder the rows and columns based on stations_order
    heatmap_data = heatmap_data.loc[stations_order, stations_order]

    # Create an inverted grayscale colormap
    colormap = sns.color_palette("gray_r", as_cmap=True)

    # Create a 2D heatmap with only the upper triangle
    plt.figure(figsize=(10, 8))
    sns.heatmap(heatmap_data, cmap=colormap, annot=False, cbar_kws={'label': 'Distance in km'})

    # Set axis labels and title
    plt.xlabel('Arrival stations')
    plt.ylabel('Departure stations')
    plt.title('Distance from departure to arrival station')

    # Show the plot
    plt.show()

def plot_distance_contours(tidy_df, num_contours=5):
    stations_order = ["Bål", "Bro", "Kän", "Khä", "Jkb", "Bkb", "Spå", "Sub", "Ke", "Cst", "Sst", "Åbe", "Äs", "Fas", "Tåd", "Skg", "Hnd", "Jbo", "Vhe", "Kda", "Ts", "Hfa", "Ssä", "Öso", "Ngd", "Gdv", "Nyh"]

    # Pivot the DataFrame to create a matrix suitable for heatmap
    heatmap_data = tidy_df.pivot(index='From', columns='To', values='Distance')

    # Reorder the rows and columns based on stations_order
    heatmap_data = heatmap_data.loc[stations_order, stations_order]

    # Create an inverted grayscale colormap
    colormap = sns.color_palette("gray_r", as_cmap=True)

    # Create a 2D heatmap with only the upper triangle
    plt.figure(figsize=(10, 8))
    sns.heatmap(heatmap_data, cmap=colormap, annot=False, cbar_kws={'label': 'Distance in km'})

    # Add contour lines for better visualization of value contours
    contour_lines = plt.contour(heatmap_data, colors='black', linewidths=2, levels=num_contours)

    # Label the contour lines with the contour values
    plt.clabel(contour_lines, inline=True, fontsize=10, fmt='%1.0f')

    # Set axis labels and title
    plt.xlabel('Arrival stations')
    plt.ylabel('Departure stations')
    plt.title('Distance from departure to arrival station')

    # Show the plot
    plt.show()


#######################
##      COSTS
#######################
    
def plot_gen_cost_all(df_combined):

    # Group by 'From' and 'To' columns
    grouped_df = df_combined.groupby(['From', 'To'])

    # Calculate the total generalized cost for each case
    total_costs_never = grouped_df.apply(
        lambda group: (group['Generalized_Cost_Never']* group['Probability']).sum()
    ).reset_index()

    total_costs_after = grouped_df.apply(
        lambda group: (group['Generalized_Cost_After']* group['Probability']).sum()
    ).reset_index()

    total_costs_before = grouped_df.apply(
        lambda group: (group['Generalized_Cost_Before']* group['Probability']).sum()
    ).reset_index()

    # Merge the two DataFrames on 'From' and 'To'
    result_df = pd.merge(total_costs_after, total_costs_before, on=['From', 'To'])
    result_df = pd.merge(result_df, total_costs_never, on=['From', 'To']) 

    # Rename the columns for clarity
    result_df.columns = ['From', 'To', 'Total_Cost_Never', 'Total_Cost_After', 'Total_Cost_Before']

    # Order according to total cost before
    result_df = result_df.sort_values(by='Total_Cost_Before', ascending=False)

    positions = range(len(result_df))

    # Plot the line chart for both 'Total_Cost_Before' and 'Total_Cost_After'
    plt.figure(figsize=(14, 8))

    # Plot lines for 'Total_Cost_Before'
    plt.plot(positions, result_df['Total_Cost_Before'] , linestyle='-', color='black', label='Pre-trip')

    # Plot lines for 'Total_Cost_After'
    plt.plot(positions, result_df['Total_Cost_After'], linestyle='-', color='gray', label='On-trip')

    # Plot lines for 'Total_Cost_Never'
    plt.plot(positions, result_df['Total_Cost_Never'], linestyle='-', color='blue', label='Never')

    # Set labels and title
    plt.xlabel('Station pairs (Departure - Arrival) ordered from highest value')
    plt.ylabel('Value in SEK/trip')
    plt.title("Value of travellers' information availability before and after trip start")

    # Rotate x-axis labels for better visibility
    plt.xticks(rotation=45, ha="right")

    # Show legend
    plt.legend()

    # Show the plot
    plt.tight_layout()
    plt.show()

def plot_gen_cost_before(result_df):

    # Select relevant columns from the result_df
    total_costs = result_df[['From', 'To', 'Total_Cost_Before']]

    # order according to total cost before
    total_costs = total_costs.sort_values(by='Total_Cost_Before', ascending=False)

    positions = range(len(result_df))

    # Assuming total_costs is already sorted based on 'Total_Cost_Before'
    # If not, you can use total_costs.sort_values(by='Total_Cost_Before', ascending=False, inplace=True)

    # Plot the bar chart for both 'Total_Cost_Before' and 'Total_Cost_After'
    plt.figure(figsize=(14, 8))


    # Plot lines for 'Total_Cost_Before'
    plt.plot(positions, total_costs['Total_Cost_Before'] , linestyle='-', color='black')

    # Set labels and title
    plt.xlabel('Station pairs - ordered from highest value')
    plt.ylabel('Value in SEK/trip')
    plt.title('Value of pre-trip travel information')

    # Show the plot
    plt.tight_layout()
    plt.show()

def plot_gen_cost_before_after(result_df):

    # Select relevant columns from the result_df
    total_costs = result_df[['From', 'To', 'Total_Cost_Before', 'Total_Cost_After']]

    # order according to total cost before
    total_costs = total_costs.sort_values(by='Total_Cost_Before', ascending=False)

    total_costs = total_costs.head(30)

    # Assuming total_costs is already sorted based on 'Total_Cost_Before'
    # If not, you can use total_costs.sort_values(by='Total_Cost_Before', ascending=False, inplace=True)

    # Plot the bar chart for both 'Total_Cost_Before' and 'Total_Cost_After'
    plt.figure(figsize=(14, 8))

    # Bar width (adjust as needed)
    bar_width = 0.35

    # Position of bars for 'Total_Cost_Before'
    positions_before = range(len(total_costs))
    plt.bar(positions_before, total_costs['Total_Cost_Before'], width=bar_width, color='black', label='Before trip start')

    # Position of bars for 'Total_Cost_After' (shifted by bar_width)
    positions_after = [pos + bar_width for pos in positions_before]
    plt.bar(positions_after, total_costs['Total_Cost_After'], width=bar_width, color='gray', label='After trip start')

    # Set labels and title
    plt.xlabel('Station pairs (Departure - Arrival) ordered from highest value')
    plt.ylabel('Value in SEK/trip')
    plt.title('Value of travellers\' information availability before and after trip start')

    # Set x-axis ticks at the center of each pair
    plt.xticks([pos + bar_width / 2 for pos in positions_before], total_costs['From'] + ' - ' + total_costs['To'], rotation=45, ha="right")

    # Show legend
    plt.legend()

    # Show the plot
    plt.tight_layout()
    plt.show()

#######################
##    VT (average)
#######################
    
def plot_VT_before(result_df):

    stations_order = ["Bål", "Bro", "Kän", "Khä", "Jkb", "Bkb", "Spå", "Sub", "Ke", "Cst", "Sst", "Åbe", "Äs", "Fas", "Tåd", "Skg", "Hnd", "Jbo", "Vhe", "Kda", "Ts", "Hfa", "Ssä", "Öso", "Ngd", "Gdv", "Nyh"]

    # Select relevant columns from the result_df
    total_costs = result_df[['From', 'To', 'Total_Cost_Before']]

    # Pivot the DataFrame to create a matrix suitable for heatmap
    heatmap_data = total_costs.pivot(index='From', columns='To', values='Total_Cost_Before')


    # Reorder the rows and columns based on stations_order
    heatmap_data = heatmap_data.loc[stations_order, stations_order]

    # Create an inverted grayscale colormap
    colormap = sns.color_palette("gray_r", as_cmap=True)

    # Create a 2D heatmap with only the upper triangle
    plt.figure(figsize=(10, 8))
    sns.heatmap(heatmap_data, cmap=colormap, annot=False, cbar_kws={'label': 'Value in SEK/passenger'})

    # Set axis labels and title
    plt.xlabel('Arrival stations')
    plt.ylabel('Departure stations')
    plt.title('Value of pre-trip travel information')

    # Show the plot
    plt.show()


def plot_VT_avg(result_df, OD=False):
    # Order the stations
    stations_order = ["Bål", "Bro", "Kän", "Khä", "Jkb", "Bkb", "Spå", "Sub", "Ke", "Cst", "Sst", "Åbe", "Äs", "Fas", "Tåd", "Skg", "Hnd", "Jbo", "Vhe", "Kda", "Ts", "Hfa", "Ssä", "Öso", "Ngd", "Gdv", "Nyh"]
    stations_order = stations_order[::-1]

    # Plot the average total cost per station for both directions as adjacent bars
    plt.figure(figsize=(12, 8))

    # Group by 'From' and sum the costs for each direction
    if(OD):
        result_df['Avg_Cost_After'] = result_df['Daily_Cost_After']
        result_df['Avg_Cost_Before'] = result_df['Daily_Cost_Before']
        grouped_df = result_df.groupby('From')[['Avg_Cost_After', 'Avg_Cost_Before', 'Passenger_Count']].sum()
        grouped_df['Avg_Cost_After'] = grouped_df['Avg_Cost_After']/grouped_df['Passenger_Count']
        grouped_df['Avg_Cost_Before'] = grouped_df['Avg_Cost_Before']/grouped_df['Passenger_Count']
    else:
        grouped_df = result_df.groupby('From')[['Avg_Cost_After', 'Avg_Cost_Before']].sum()

    # Sort the data based on the custom order   
    grouped_df_sorted = grouped_df.sort_values(by=['From'], key=lambda x: x.map({station: i for i, station in enumerate(stations_order)}))

    # Plot bars for Total Cost After and Total Cost Before (horizontal)
    y = np.arange(len(stations_order))
    width = 0.4

    plt.barh(y - width/2, grouped_df_sorted['Avg_Cost_After'], height=width, color='black', label='On-trip information')
    plt.barh(y + width/2, grouped_df_sorted['Avg_Cost_Before'], height=width, color='gray', label='Pre-trip information')

    plt.title('Average savings per station for different types of travel information')
    plt.ylabel('Departure station')
    plt.xlabel('Average savings compared to no travel information (SEK/trip)')
    plt.yticks(y, stations_order, fontsize=12)
    plt.legend()
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


def plot_VT_avg_direction(result_df, OD=False):
    # Order the stations
    stations_order = ["Bål", "Bro", "Kän", "Khä", "Jkb", "Bkb", "Spå", "Sub", "Ke", "Cst", "Sst", "Åbe", "Äs", "Fas", "Tåd", "Skg", "Hnd", "Jbo", "Vhe", "Kda", "Ts", "Hfa", "Ssä", "Öso", "Ngd", "Gdv", "Nyh"]
    stations_order = stations_order[::-1]

    if(OD):
        result_df['Avg_Cost_After'] = result_df['Daily_Cost_After']/result_df['Passenger_Count']
        result_df['Avg_Cost_Before'] = result_df['Daily_Cost_Before']/result_df['Passenger_Count']
        # Add the zero costs for the terminal stations with an average of 0
        new_row = {'From': 'Bål', 'Direction': 1, 'Avg_Cost_After': 0, 'Avg_Cost_Before': 0}
        result_df = result_df.append(new_row, ignore_index=True)
        new_row = {'From': 'Nyh', 'Direction': 0, 'Avg_Cost_After': 0, 'Avg_Cost_Before': 0}
        result_df = result_df.append(new_row, ignore_index=True)

    # Sort the data based on the custom order
    result_df_sorted = result_df.sort_values(by=['From'], key=lambda x: x.map({station: i for i, station in enumerate(stations_order)}))

    # Initialize a DataFrame for both "Before" and "After" data
    grouped_df = pd.DataFrame(index=stations_order)

    # Get the average cost before and after for northbound direction (0) and southbound direction (1)
    grouped_df['Before_South'] = result_df_sorted[result_df_sorted['Direction'] == 0]['Avg_Cost_Before'].values
    grouped_df['Before_North'] = result_df_sorted[result_df_sorted['Direction'] == 1]['Avg_Cost_Before'].values
    grouped_df['After_South'] = result_df_sorted[result_df_sorted['Direction'] == 0]['Avg_Cost_After'].values
    grouped_df['After_North'] = result_df_sorted[result_df_sorted['Direction'] == 1]['Avg_Cost_After'].values

    # Define the width of each bar
    bar_width = 0.3

    # Plot stacked bars for Total Cost Before and Total Cost After (horizontal)
    ax = grouped_df[['Before_South', 'Before_North']].plot(kind='barh', stacked=True, figsize=(12, 8), colormap='viridis', width=bar_width)

    # Plot bars for Total Cost After with adjusted position
    grouped_df[['After_South', 'After_North']].plot(kind='barh', stacked=True, ax=ax, colormap='turbo', alpha=1, width=bar_width, position=bar_width+1.2)

    # Set labels and title
    ax.set_ylabel('Departure station')
    ax.set_xlabel('Average savings compared to no travel information (SEK/trip)')
    ax.set_title('Average savings per station and direction for different types of travel information')

    plt.legend(['Pre-trip - southbound', 'Pre-trip - northbound', 'On-trip - southbound', 'Pre-trip - northbound'], loc='lower right')
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


def plot_VT_trip(result_df, OD=False):  

    # Group by 'From' and 'To' columns
    if(OD):
        result_df['Avg_Cost_After'] = result_df['Daily_Cost_After']
        result_df['Avg_Cost_Before'] = result_df['Daily_Cost_Before']
        grouped_df = result_df.groupby('From')[['Avg_Cost_After', 'Avg_Cost_Before', 'Passenger_Count']].sum().reset_index()  
        grouped_df['Avg_Cost_After'] = grouped_df['Avg_Cost_After']/grouped_df['Passenger_Count']
        grouped_df['Avg_Cost_Before'] = grouped_df['Avg_Cost_Before']/grouped_df['Passenger_Count']
    else:
        grouped_df = result_df.groupby(['From'])[['Avg_Cost_After', 'Avg_Cost_Before']].sum().reset_index()  

    # order according to total cost before
    total_costs_OD = grouped_df.sort_values(by='Avg_Cost_Before', ascending=False)

    #total_costs_OD = total_costs_OD.head(30)

    # Assuming total_costs is already sorted based on 'Total_Cost_Before'
    # If not, you can use total_costs.sort_values(by='Total_Cost_Before', ascending=False, inplace=True)

    plt.rcParams.update({'font.size': 22})

    # Plot the bar chart for both 'Total_Cost_Before' and 'Total_Cost_After'
    plt.figure(figsize=(14, 8))

    # Bar width (adjust as needed)
    bar_width = 0.35

    # Position of bars for 'Total_Cost_Before'
    positions_before = range(len(total_costs_OD))
    plt.bar(positions_before, total_costs_OD['Avg_Cost_Before'], width=bar_width, color='black', label='Pre-trip')

    # Position of bars for 'Total_Cost_After' (shifted by bar_width)
    positions_after = [pos + bar_width for pos in positions_before]
    plt.bar(positions_after, total_costs_OD['Avg_Cost_After'], width=bar_width, color='gray', label='On-trip')

    # Set labels and title
    plt.xlabel('Departure stations (in descending order of benefits)')
    plt.ylabel('Average benefits (in SEK/trip)')
    plt.title('Average benefits of pre-trip and on-trip travel information')

    # Set x-axis ticks at the center of each pair
    plt.xticks([pos + bar_width / 2 for pos in positions_before], total_costs_OD['From'], rotation=45, ha="right")

    # Show legend
    plt.legend()

    # Show the plot
    plt.tight_layout()
    plt.show()

#######################
##    VT (with OD)
#######################

def plot_VT_daily(result_df):
    
    # Group by 'From' and 'To' columns
    grouped_df = result_df.groupby(['From'])[['Daily_Cost_After', 'Daily_Cost_Before']].sum().reset_index()  

    # order according to total cost before
    total_costs_OD = grouped_df.sort_values(by='Daily_Cost_Before', ascending=False)

    #total_costs_OD = total_costs_OD.head(30)

    # Assuming total_costs is already sorted based on 'Total_Cost_Before'
    # If not, you can use total_costs.sort_values(by='Total_Cost_Before', ascending=False, inplace=True)

    plt.rcParams.update({'font.size': 22})

    # Plot the bar chart for both 'Total_Cost_Before' and 'Total_Cost_After'
    plt.figure(figsize=(14, 8))

    # Bar width (adjust as needed)
    bar_width = 0.35

    # Position of bars for 'Total_Cost_Before'
    positions_before = range(len(total_costs_OD))
    plt.bar(positions_before, total_costs_OD['Daily_Cost_Before']/10**6, width=bar_width, color='black', label='Pre-trip')

    # Position of bars for 'Total_Cost_After' (shifted by bar_width)
    positions_after = [pos + bar_width for pos in positions_before]
    plt.bar(positions_after, total_costs_OD['Daily_Cost_After']/10**6, width=bar_width, color='gray', label='On-trip')

    # Set labels and title
    plt.xlabel('Departure stations (in descending order of benefits)')
    plt.ylabel('Total daily benefits (in million  SEK/weekday)')
    plt.title('Daily benefits of pre-trip and on-trip travel information')

    # Set x-axis ticks at the center of each pair
    plt.xticks([pos + bar_width / 2 for pos in positions_before], total_costs_OD['From'], rotation=45, ha="right")

    # Show legend
    plt.legend()

    # Show the plot
    plt.tight_layout()
    plt.show()
