function [ localParams, nearWhich, whichPatch ] = createLocalParamsExtraordinary(global_quad_params)
%
nearWhich = -1; %default error!
whichPatch = floor(global_quad_params*4);
whichPatch(whichPatch > 3.5) = 3; % cap at 4 - can get 5 otherwise
shifted_scaled_coords = global_quad_params*4 - whichPatch;
shifted_scaled_coords(global_quad_params >= 1) = 1; %so param 1 doesn't give 0)

whichPatch = whichPatch + 1;
localParams = shifted_scaled_coords;
if(global_quad_params(1) <= 0.25)
    if(global_quad_params(2) <= 0.25)
        %bottom-left. Need to rotate by 180 degrees, but u stays u-dir and v
        %stays v-dir
        coordinatesReversed = 1 - shifted_scaled_coords;
        localParams = [coordinatesReversed(1), coordinatesReversed(2)];
        nearWhich = 1;
    elseif (global_quad_params(2) >= 0.75)
        %upper-left corner. Local u is global v, and local v is global 1-u.
        localParams = [shifted_scaled_coords(2), 1-shifted_scaled_coords(1)];
        nearWhich = 4;        
    end  
elseif(global_quad_params(1) >= 0.75)
    if(global_quad_params(2) <= 0.25)
        %bottom-right. Local u is global 1-v, local v is u.
        localParams = [1-shifted_scaled_coords(2), shifted_scaled_coords(1)];
        nearWhich = 2;
    elseif(global_quad_params(2) >= 0.75)
        %upper-right. NO SWITCHIES!!!!
        localParams = shifted_scaled_coords;
        nearWhich = 3;
    end
else
    while((whichPatch == 1) | (whichPatch == 4)) % both are 1/4! we're in a corner! error
        warning('thingy thought we were in a corner when we weren"t, so shifting. in createLocalParamsExtraordinary.m')
        %should be really close to next patch, so try
        moved_params = global_quad_params - 0.5;
        [~,closestCoordToMid] = min(abs(moved_params));
        %move the coordinate, and adjust param to edge
        whichPatch(closestCoordToMid) = whichPatch(closestCoordToMid) - sign(moved_params(closestCoordToMid));
        localParams(closestCoordToMid) = moved_params(closestCoordToMid) < 0;
    end    
end



