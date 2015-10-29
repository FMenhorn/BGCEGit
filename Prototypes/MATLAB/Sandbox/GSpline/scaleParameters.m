function scaledParams = scaleParameters(unscaledParameters)


quad_ids = unique(unscaledParameters(:,1));

scaledParams = zeros(size(unscaledParameters));

scaledParams (:,1) = unscaledParameters(:,1);

for i = 1:length(quad_ids)
    umax = max(unscaledParameters(unscaledParameters(:,1) == quad_ids(i),2));
    umin = min(unscaledParameters(unscaledParameters(:,1) == quad_ids(i),2));
    vmax = max(unscaledParameters(unscaledParameters(:,1) == quad_ids(i),3));
    vmin = min(unscaledParameters(unscaledParameters(:,1) == quad_ids(i),3));
    
    uscale = umax - umin;
    vscale = vmax - vmin;
    
    scaledParams(unscaledParameters(:,1) == quad_ids(i),2) = (unscaledParameters(unscaledParameters(:,1) == quad_ids(i),2) - umin)/uscale;
    scaledParams(unscaledParameters(:,1) == quad_ids(i),3) = (unscaledParameters(unscaledParameters(:,1) == quad_ids(i),3) - vmin)/vscale;
    
    
    
end




end
