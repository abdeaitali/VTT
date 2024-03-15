function [line, travel_time, alt_travel_time, waiting_time, avg_delay, delay_prob, OD_pax] = read_input(filename, type, d_param, d_pr_param)
%READ_INPUT reading input data for testing the model
%   function that reads data defining the case study (travel time, lines, delays, etc)


%% read page with line, and waiting time
if(strcmp(type, 'commuter'))
    T_line = readtable(filename, 'Sheet','Nynäshamn-Bålsta_2015','Range', 'A1:F28','VariableNamingRule', 'preserve');
    % set the waiting time at the station (improve to be OD!)
    waiting_time = table2array(T_line(1:end,4))/2; % in minutes, div 2 (random)
else
    T_line = readtable(filename, 'Sheet','Västra_Stambanan_stationer_2015','Range', 'A1:C11','VariableNamingRule', 'preserve');
    waiting_time = zeros(size(T_line,1),1);
end

% set the line (Station | 3-letter code)
line = T_line(1:end,1:2);


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
        if(strcmp(type, 'commuter'))
            if(from<to) % dir Bålsta -> Nyh
                travel_time(from,to) = sum(T_line{from:to-1,3});
            else % % dir Bålsta <- Nyh
                travel_time(from,to) = sum(T_line{to+1:from,5});
            end
            % add dwell time (at centralen and/or Vhn)
            travel_time(from,to) = travel_time(from,to) + sum(T_line{from+1:to-1,6});
        else
            % get travel time (in minutes) using time from G
            travel_time(from,to) = abs(T_line{from,3} - T_line{to,3});
        end
    end
end


%% read OD with alternative travel times (NOW with distance and avg_speed = 50km/h)
if(strcmp(type, 'commuter'))
    T_alt_travel_time = readtable(filename, 'Sheet','OD_distances','Range', 'A1:AZ52','VariableNamingRule', 'preserve');
else % no OD, only alternative travel time using distance and avg_speed = 100 km/h)
    % read distance from Göteborg
    T_alt_travel_time = readtable(filename, 'Sheet','OD_distances','Range', 'A1:B11','VariableNamingRule', 'preserve');
end
alt_travel_time = zeros(size(line,1));
for from=1:size(line,1)
    for to=1:size(line,1)
        if(from==to)
           continue; 
        end
        station_from = line{from,1};
        station_to = line{to,1};
        from_idx = find(ismember(T_alt_travel_time{:,1},station_from));
        if(strcmp(type, 'commuter'))
            % Extract the distance and calculate the alternative travel time
            % (2nd best), assuming 50 km/h for replacement buses
            speed = 50;
            alt_travel_time(from,to) = T_alt_travel_time{from_idx,station_to}/1000/speed*60; % in minutes
        else
            % Extract the distance (in km)
            to_idx = find(ismember(T_alt_travel_time{:,1},station_to));
            distance_alt_travel_time = abs(T_alt_travel_time{from_idx,2}-T_alt_travel_time{to_idx,2});
            % calculate the alternative travel time (2nd best), assuming 100 km/h for replacement buses
            speed_intercity = 100;
            alt_travel_time(from,to) = distance_alt_travel_time/1000/speed_intercity*60; % in minutes
        end
        % in case of alternative is faster, assume it is 25% longer than
        % best route
        if(alt_travel_time(from,to)<=travel_time(from,to))
            alt_travel_time(from,to) = 1.25*travel_time(from,to);
        end
    end
    
end

%% read the average delay and disruption probabiliy data (FROM LUPP 2015)
% average delays in minutes
if(strcmp(type, 'commuter'))
   T_delay = readtable(filename, 'Sheet','Delay','Range', 'A1:C28','VariableNamingRule', 'preserve');
else
   T_delay = readtable(filename, 'Sheet','Delay','Range', 'A1:C11','VariableNamingRule', 'preserve'); 
end
% for sensitivity analysis
if(d_param>0)
    T_delay{:,2} = T_delay{:,2}*d_param;
end
if(d_pr_param>0)
    T_delay{:,3} = T_delay{:,3}*d_pr_param;
end
% init
avg_delay = zeros(size(line,1)); % in minutes
delay_prob = zeros(size(line,1));
for from=1:size(line,1)
    for to=1:size(line,1)
        if(from==to)
            continue;
        end
        delay_prob(from,to) = T_delay{from,3};
        if(from<to) % dir Bålsta -> Nyh
            avg_delay(from,to) = sum(T_delay{from:to-1,2}'*T_delay{from:to-1,3});
        else % % dir Bålsta <- Nyh
            avg_delay(from,to) = sum(T_delay{to+1:from,2}'*T_delay{to+1:from,3});
        end
    end
end

%% read OD passenger data
if(strcmp(type, 'commuter'))
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
else
    OD_pax = 0;
end

end

