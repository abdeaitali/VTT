function [] = plot_figure(type,line, delta_R)
%PLOT_FIGURE Summary of this function goes here
%   Detailed explanation goes here
Plts = table2cell(line(:,"Plts"));
heatmap(Plts,Plts,delta_R)
colorbar
if(strcmp(type,"time-trip"))
    title('VTT (in minutes per trip)')
elseif(strcmp(type,"cost-trip"))
    title('VTT (in SEK per trip)')
elseif(strcmp(type,"cost-day"))
    title('VTT (in SEK per day)')
elseif(strcmp(type,"time-day"))
    title('VTT (in minutes per day)')    
end

end

