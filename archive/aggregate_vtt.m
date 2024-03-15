function [R_agg] = aggregate_vtt(type, delta_R, OD_pax)
%AGGREGATE_VTT Summary of this function goes here
%   Detailed explanation goes here
nb_st = size(delta_R,1);
if(strcmp(type,'avg'))
    nb_combin = nb_st^2-nb_st; % minus diagonals
    R_agg = sum(delta_R,'all')/nb_combin;
elseif(strcmp(type,'pax_weight'))
    R_agg = sum(delta_R.*OD_pax,'all')/sum(OD_pax,'all');
end

end

