function delta_R = assess_vtt(measure, line, travel_time, alt_travel_time, waiting_time, avg_delay, delay_prob)
%ASSESS_VTT Summary of this function goes here
%   Detailed explanation goes here

% ASEK params (To IMPROVE!)
val_tt = (80+62)/2/60; % SEK per min
val_wt = [(93+70),(76+57),(37+28)]/2/60; % SEK per min
val_d = (2082+216)/2/60; % SEK per min
alpha = 0.5; % congestion param
% uncertain travel time
beta = 0.9; % 90 percent of travel time
% initializations
delta_R = zeros(size(line,1));
for from=1:size(line,1)
    for to=1:size(line,1)
        if(from==to)
           continue; 
        end
        % travel time
        t0_min = travel_time(from,to);
        alt_t = alt_travel_time(from,to);
        delta_t =  t0_min - alt_t;
        % waiting time
        w0_min = waiting_time(from);
        % delay
        d0_min = avg_delay(from,to);
        p = delay_prob(from,to);
        % calculate the value in terms of accessibility
        if(strcmp(measure,"time"))
            delta_R(from,to) = p*((alpha+beta)*t0_min +delta_t+w0_min+d0_min);
        else % otherwise convert to social costs
            delta_R(from,to) = p*val_tt*((alpha+beta)*t0_min+delta_t);
            if(w0_min<10)
                delta_R(from,to) = delta_R(from,to) + p*val_wt(1)*w0_min;
            elseif(w0_min>30)
                delta_R(from,to) = delta_R(from,to) + p*val_wt(3)*w0_min;
            else
                delta_R(from,to) = delta_R(from,to) + p*val_wt(2)*w0_min;
            end
            delta_R(from,to) = delta_R(from,to) + p*val_d*d0_min;
        end
    end
end

end

