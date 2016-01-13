function [ new_bezier_points ] = raiseDeg1D( old_bezier_points )
%raiseDeg1D Raise the order of the bezier curve by 1.
%   Provided a dxN - matrix of d-dimensional bezier points, the algorithm outputs a
%   dx(N+1) matrix of bezier points drawing te exact same curve but with a
%   degree 1 higher. Tested and works.


dimensions = size(old_bezier_points,1);
new_degree = size(old_bezier_points,2);

new_bezier_points = zeros([dimensions,new_degree+1]);

inv_degree = 1/(new_degree);

new_bezier_points(:,1) = old_bezier_points(:,1);
new_bezier_points(:,end) = old_bezier_points(:,end);

for i = 2:new_degree
    new_bezier_points(:,i) = ...
            (i-1)*inv_degree      * old_bezier_points(:,i-1)...
        +   (1-(i-1)*inv_degree)  * old_bezier_points(:,i);
end

