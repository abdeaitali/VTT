function [line, travel_time, alt_travel_time, waiting_time, avg_delay, OD_pax] = read_input_df()
%READ_INPUT reading input data for testing the model
%   function that reads data defining the case study (travel time, lines, delays, etc)


%% read page with line, and waiting time
filename = './1_scenario/data_commuter.xlsx';
T_line = readtable(filename, 'Sheet','Nynäshamn-Bålsta_2015','Range', 'A1:F28','VariableNamingRule', 'preserve');
% set the waiting time at the station (improve to be OD!)
waiting_time = table2array(T_line(1:end,4))/2; % in minutes, div 2 (random)

% set the line (Station | 3-letter code)
line = T_line(1:end,1:2);

%% read OD with travel time
filename_OD = './1_scenario/arkiv/pendeltåg 2015/DF_OD.csv';
OD_pax = readtable(filename_OD);

filename_tt = './1_scenario/arkiv/pendeltåg 2015/DF_tt.csv';
travel_time = readtable(filename_tt);

%% read OD with alternative travel times (NOW with distance and avg_speed = 50km/h)
T_alt_travel_time = readtable(filename, 'Sheet','OD_distances','Range', 'A1:AZ52','VariableNamingRule', 'preserve');

alt_travel_time = zeros(size(line,1));
for from=1:size(line,1)
    for to=1:size(line,1)
        if(from==to)
           continue; 
        end
        station_from = line{from,1};
        station_to = line{to,1};
        from_idx = find(ismember(T_alt_travel_time{:,1},station_from));
        % Extract the distance and calculate the alternative travel time
        % (2nd best), assuming 50 km/h for replacement buses
        speed = 50;
        alt_travel_time(from,to) = T_alt_travel_time{from_idx,station_to}/1000/speed*60; % in minutes
        % in case of alternative is faster, assume it is 25% longer than
        % best route
        if(alt_travel_time(from,to)<=travel_time(from,to))
            alt_travel_time(from,to) = 1.25*travel_time(from,to);
        end
    end
    
end

%% read the average delay and disruption probabiliy data (FROM LUPP 2015)
% average delays in minutes
filename_delay = './1_scenario/arkiv/pendeltåg 2015/DF_delay.csv';
avg_delay = readtable(filename_delay);

end

