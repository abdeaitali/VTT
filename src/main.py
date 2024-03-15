from utils import aggregate_total_per_day, aggregate_avg_per_dep, get_delay_avg_std, get_delay_prob, merge_all_df, aggregate_gen_cost, calc_CBA, integrate_gen_cost,calc_gen_cost
from data_processing import read_traffic, read_tt_timetable, read_OD, read_distance, read_waiting
from plotting import plot_VT_trip, plot_VT_daily, plot_VT_avg_direction, plot_VT_avg, plot_gen_cost_all, plot_distance_contours, plot_OD_contours, plot_tt_timetable_contours, plot_delay_dist_at_station, plot_delay_mean_std, plot_nb_obs_all, plot_traffic_dist, plot_OD, plot_tt_timetable, plot_distance, plot_VT_before

import logging

# logging level set to INFO
logging.basicConfig(format='%(message)s',
                    level=logging.INFO)

LOG = logging.getLogger(__name__)

#######################
###     INITS
#######################

# inits for plotting and exporting
plot_ind = False
export_ind = False
head_ind = False

# path to the data files
path_name = 'C:/Users/AbdouAA/Work Folders/Documents/GitHub/VTT/data/'


#######################
##      TRAFFIC
#######################

# read traffic data
df_traffic = read_traffic()

#if plot_ind:
#    plot_nb_obs_all(df_traffic) # plot the number of departure per station & direction
#    plot_traffic_dist(df_traffic, 'Cst') # plot the distribution of traffic

#######################
##      DELAYS
#######################

df_delay = get_delay_prob(df_traffic)
df_delay_avg_std = get_delay_avg_std(df_delay)
if export_ind:
    df_delay.to_csv(path_name+'DF_delay.csv', index=False)
if plot_ind:
    plot_delay_dist_at_station(df_delay, ['Cst', 'Bkb', 'Skg'])
    plot_delay_mean_std(df_delay_avg_std) # average delays and std per stations and direction


#######################
##      OD
#######################
    
### Ridership data
# read ridership data
df_OD = read_OD(path_name+'data_commuter.xlsx')
if plot_ind:
    plot_OD(df_OD)
    plot_OD_contours(df_OD)
if export_ind:
    df_OD.to_csv(path_name+'DF_OD.csv', index=False)

#######################
##      TIMETABLE
#######################
    
### Travel time (timetable)
# read data about the travel times (in minutes) using timetable
df_tt = read_tt_timetable()
# waiting time (in minutes)
df_w = read_waiting()
if plot_ind:
    plot_tt_timetable(df_tt)
    plot_tt_timetable_contours(df_tt)
if export_ind:
    df_tt.to_csv(path_name+'DF_tt.csv', index=False)

#######################
##      DISTANCE
#######################
    
### Distances
# read data about the travel times using alternative mode
df_dist = read_distance()
if plot_ind:
    plot_distance(df_dist)
    plot_distance_contours(df_dist)
if export_ind:
    df_dist.to_csv(path_name+'DF_distance.csv', index=False)

LOG.info('--- Successfully READING, PLOTTING & EXPORTING INPUT DATA ---')

###############################################
###  Merging all the dataframes
###############################################

# Merge all the data
df_all = merge_all_df(df_delay, df_delay_avg_std, df_OD, df_w, df_tt, df_dist)

LOG.info('--- Successfully Merge all the data ---')

###############################################
###  Calculating the generalized costs
###############################################

# calculate the generalized cost
df_gen_cost = calc_gen_cost(df_all)
if plot_ind:
    plot_gen_cost_all(df_gen_cost)


LOG.info('--- Successfully calculate the generalized cost ---')

###############################################
###  Integration over delay distribution
###############################################

# integrated gen cost over all the delays
df_gen_cost_all = integrate_gen_cost(df_gen_cost)

LOG.info('--- Successfully integrated gen cost over all the delays ---')
# plot the results cost matrix
#if plot_ind:
#plot_gen_cost_before_after(df_gen_cost_all)
#plot_gen_cost_before(df_gen_cost_all)
#plot_VT_before(df_gen_cost_all)


###############################################
###  Aggregation using simple average
###############################################

df_VT_avg = aggregate_avg_per_dep(df_gen_cost_all)
if plot_ind:
    plot_VT_avg_direction(df_VT_avg)
    plot_VT_trip(df_VT_avg)
    plot_VT_avg(df_VT_avg)

###############################################
###  Aggregation using OD
###############################################

# consider the ridership data
df_VT_daily  = aggregate_total_per_day(df_gen_cost_all, df_OD)
if plot_ind:
    plot_VT_daily(df_VT_daily)
    plot_VT_avg_direction(df_VT_daily, OD=True)
    plot_VT_avg(df_VT_daily, OD=True)
    plot_VT_trip(df_VT_daily, OD=True)
LOG.info('--- Successfully consider the ridership data ---')


#######################
##    VTT (overview)
#######################
LOG.info('--- Calculating VTT ---')
aggregate_gen_cost(df_VT_avg)
aggregate_gen_cost(df_VT_avg, direction=True)

LOG.info('--- Calculating VTT using OD ---')
aggregate_gen_cost(df_VT_daily, OD=True)
aggregate_gen_cost(df_VT_daily, OD=True, direction=True)

###############################################
###  Comparing the gains with delay costs
###############################################

calc_CBA(df_all, df_VT_daily)
LOG.info('--- Successfully Comparing the gains with delay costs ---')