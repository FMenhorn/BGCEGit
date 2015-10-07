

function tempMatrix = plotPoints(points)



m = size(points,2);
n = size(points,3);

% create temporary matrix

tempMatrix = zeros(3,n*m);

tempMatrixIndex = @(i,j, width) (i-1)*width + j;

for j = 1:n
    for i  = 1:m
        tempMatrix(:,tempMatrixIndex(i,j,m)) = points(:,i,j);
    end
end


scatter3(tempMatrix(1,:),tempMatrix(2,:),tempMatrix(3,:));

end
