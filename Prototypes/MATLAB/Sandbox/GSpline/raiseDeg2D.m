function [ new_bezier_points ] = raiseDeg2D( old_bezier_points )
%raiseDeg1D Raise the order of the bezier curve by 1.
%   Provided a dxN - matrix of d-dimensional bezier points, the algorithm outputs a
%   dx(N+1) matrix of bezier points drawing te exact same curve but with a
%   degree 1 higher. Tested and works.


dimensions = size(old_bezier_points,1);
new_degreeU = size(old_bezier_points,2);
new_degreeV = size(old_bezier_points,3);

half_raised = zeros([dimensions,new_degreeU+1,new_degreeV]);
new_bezier_points = zeros([dimensions,new_degreeU+1,new_degreeV+1]);

for j = 1:new_degreeV
    half_raised(:,:,j) = raiseDeg1D(squeeze(old_bezier_points(:,:,j)));
end
for i = 1:(new_degreeU+1)
    new_bezier_points(:,i,:) = raiseDeg1D(squeeze(half_raised(:,i,:)));
end

