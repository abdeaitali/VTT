from ..src.data_processing import read_traffic
#from ..src.plotting import plot_mean_std, plot_dist_centralen, plot_OD, plot_tt_timetable, plot_distance, plot_VT_before

import logging

# logging level set to INFO
logging.basicConfig(format='%(message)s',
                    level=logging.INFO)

LOG = logging.getLogger(__name__)

###############################################
###  Tests with traffic data
###############################################


# Traffic data: Set the path to your CSV file and Read the CSV file into a DataFrame

path_name = 'C:/Users/AbdouAA/Work Folders/Documents/GitHub/VTT/data/'

df_traffic = read_traffic()

print(df_traffic.head(7))

#plot_mean_std(df_traffic)
#plot_dist_centralen(df_traffic)
