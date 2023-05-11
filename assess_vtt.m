function delta_R = assess_vtt(measure, line, travel_time, alt_travel_time, waiting_time, avg_delay, delay_prob, OD_pax)
%ASSESS_VTT Summary of this function goes here
%   Detailed explanation goes here

% ASEK params (To IMPROVE!)
val_tt = (80+62)/2/60; % SEK per min
val_wt = [(93+70),(76+57),(37+28)]/2/60; % SEK per min
val_d = (2082+216)/2/60; % SEK per min
alpha = 1; % congestion param

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
        alt_w = 0;
        delta_w = w0_min - alt_w;
        % delay
        d0_min = avg_delay(from,to);
        p = delay_prob(from,to);
        % calculate the value in terms of accessibility
        if(strcmp(measure,"time-trip"))
            delta_R(from,to) = p*(alpha*t0_min +delta_t+delta_w+d0_min);
        elseif(strcmp(measure,"time-day"))
            delta_R(from,to) = OD_pax(from,to)*(alpha*t0_min +delta_t+delta_w+d0_min);
        else % otherwise convert to social costs
            delta_R(from,to) = p*val_tt*(alpha*t0_min+delta_t);
            if(delta_w<10)
                delta_R(from,to) = delta_R(from,to) + p*val_wt(1)*delta_w;
            elseif(delta_w>30)
                delta_R(from,to) = delta_R(from,to) + p*val_wt(3)*delta_w;
            else
                delta_R(from,to) = delta_R(from,to) + p*val_wt(2)*delta_w;
            end
            delta_R(from,to) = delta_R(from,to) + p*val_d*d0_min;
            if(strcmp(measure,"cost-day"))
                    delta_R(from,to) = OD_pax(from,to)*delta_R(from,to);
            end
        end
    end
end

end

