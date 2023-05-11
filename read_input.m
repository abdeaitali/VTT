function [line, travel_time, alt_travel_time, waiting_time, avg_delay, delay_prob, OD_pax] = read_input(filename)
%READ_INPUT Summary of this function goes here
%   Detailed explanation goes here


%% read page with line, and waiting time
T_line = readtable(filename, 'Sheet','Nynäshamn-Bålsta_2015','Range', 'A1:F28','VariableNamingRule', 'preserve');

% set the line (Station | 3-letter code)
line = T_line(1:end,1:2);

% set the waiting time at the station (improve to be OD!)
waiting_time = table2array(T_line(1:end,4))/2; % in minutes, div 2 (random)


%% read OD with travel time
% set the travel time to the next station
%T_travel_time = readtable(filename, 'Sheet','OD_travel_time','Range', 'A1:AZ52','VariableNamingRule', 'preserve');
travel_time = zeros(size(line,1));
for from=1:size(line,1)
    for to=1:size(line,1)
        if(from==to)
           continue; 
        end
%        station_from = line{from,1};
%        station_to = line{to,1};
        % Extract the value from the table
        %row_idx = find(ismember(T_travel_time{:,1},station_from));
%        travel_time(from,to) = T_travel_time{row_idx,station_to}/60; % in minutes
        % alternative
        if(from<to) % dir Bålsta -> Nyh
            travel_time(from,to) = sum(T_line{from:to-1,3});
        else % % dir Bålsta <- Nyh
            travel_time(from,to) = sum(T_line{to+1:from,5});
        end
        % add dwell time (at centralen and/or Vhn)
        travel_time(from,to) = travel_time(from,to) + sum(T_line{from+1:to-1,6});
    end
end


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
        row_idx = find(ismember(T_alt_travel_time{:,1},station_from));
        % Extract the distance and calculate the alternative travel time
        % (2nd best), assuming 50 km/h for replacement buses
        alt_travel_time(from,to) = T_alt_travel_time{row_idx,station_to}/1000/50*60; % in minutes
        % in case of alternative is faster, assume it is 25% longer than
        % best route
        if(alt_travel_time(from,to)<=travel_time(from,to))
            alt_travel_time(from,to) = 1.25*travel_time(from,to);
        end
    end
end

%% read the average delay and disruption probabiliy data
% temporarily set as 30 seconds delay in average
avg_delay = 30*ones(size(line,1))/60; % in minutes
% temporarily set to .5
delay_prob = .5*ones(size(line,1));

%% read OD passenger data
T_pax = readtable(filename, 'Sheet','OD_pax','Range', 'A1:AZ52','VariableNamingRule', 'preserve');
OD_pax = zeros(size(line,1));
for from=1:size(line,1)
    for to=1:size(line,1)
        if(from==to)
           continue; 
        end
        station_from = line{from,2};
        station_to = line{to,2};
        row_idx = find(ismember(T_pax{:,1},station_from));
        % Extract the OD passengers (daily)
        OD_pax(from,to) = T_pax{row_idx,station_to};
    end
end


end

