function [scaledParams,throwndata] = scaleAwayParameters(unscaledParams,datapoints)


quad_ids = unique(unscaledParams(:,1));
% 
% scaledParams = zeros(size(unscaledParameters));

scaledParams = unscaledParams(unscaledParams(:,3) >=0 & unscaledParams(:,2) >=0 & unscaledParams(:,2) <= 1 & unscaledParams(:,3) <= 1,:);
throwndata = datapoints(unscaledParams(:,3) >=0 & unscaledParams(:,2) >=0 & unscaledParams(:,2) <= 1 & unscaledParams(:,3) <= 1,:);



for i = 1:length(quad_ids)
    umax = max(scaledParams(scaledParams(:,1) == quad_ids(i),2));
    umin = min(scaledParams(scaledParams(:,1) == quad_ids(i),2));
    vmax = max(scaledParams(scaledParams(:,1) == quad_ids(i),3));
    vmin = min(scaledParams(scaledParams(:,1) == quad_ids(i),3));
    
    uscale = umax - umin;
    vscale = vmax - vmin;
    if(uscale)
        scaledParams(scaledParams(:,1) == quad_ids(i),2) = (scaledParams(scaledParams(:,1) == quad_ids(i),2) - umin)/uscale;
    end
    if(vscale)
        scaledParams(scaledParams(:,1) == quad_ids(i),3) = (scaledParams(scaledParams(:,1) == quad_ids(i),3) - vmin)/vscale;
    end
    
    
end




end
