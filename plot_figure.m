function [] = plot_figure(type,line, delta_R)
%PLOT_FIGURE Summary of this function goes here
%   Detailed explanation goes here
Plts = table2cell(line(:,"Plts"));
heatmap(Plts,Plts,delta_R_time)
colorbar
if()
title('VTT (in minutes per trip)')
title('VTT (SEK per trip)')
title('VTT (SEK per day)')
end

