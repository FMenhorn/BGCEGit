%% multiply datapoints on same quads

N = size(quads_Torus,1);
counter = 0;

newPoints = zeros(size(torus_verts_fine));
newParams = zeros(size(parameters));

for p = 1:N
    pointsOnQuad = find(parameters(:,1) == p);
    numPoints = length(pointsOnQuad);
    for newPointIndex = 1:(numPoints-1)
        counter = counter + 1;
        newPoints(counter,:) = (torus_verts_fine(pointsOnQuad(newPointIndex),:) + torus_verts_fine(pointsOnQuad(newPointIndex+1),:))/2; 
        newParams(counter,2:3) = (parameters(pointsOnQuad(newPointIndex),2:3) + parameters(pointsOnQuad(newPointIndex+1),2:3))/2; 
        newParams(counter,1) = parameters(pointsOnQuad(newPointIndex),1);
    end
end

newPoints = cat(1,torus_verts_fine,newPoints(1:counter,:));
newParams = cat(1,parameters,newParams(1:counter,:));