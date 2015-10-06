function bezierPoints = getBiquadraticPatch(controlPoints)

% given a 3x3 3-dim array of points, where the first dimension is (x,y,z)

bezierPoints = zeros(3,3,3);

for i = [1,3]
    bezierPoints(:,i,2) = (controlPoints(:,i,2) + controlPoints(:,2,2))/2;
    for j = [1,3]
    bezierPoints(:,i,j) = (controlPoints(:,i,j) + controlPoints(:,i,2) + controlPoints(:,2,j) + controlPoints(:,2,2))/4;
    end
end

bezierPoints(:,2,1) = (controlPoints(:,2,1) + controlPoints(:,2,2))/2;
bezierPoints(:,2,3) = (controlPoints(:,2,3) + controlPoints(:,2,2))/2;

bezierPoints(:,2,2) = controlPoints(:,2,2);



end