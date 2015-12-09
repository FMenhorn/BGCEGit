function [newB1,newB2] = sortB1B2Indices(oldB1,oldB2)


mod_index = @(i,modul) mod(i-1,modul) + 1;
shifted_indices = @(ind,modul) mod_index((0:(modul-1)) + ind,modul);
newB1 = zeros(size(oldB1));
newB2 = zeros(size(oldB2));

for i = 1:size(oldB2,1)
    m = getNumOfEdgesMeetingMatlab(oldB2,i);
    indicesLocB1 = zeros(1,m);
    indicesLocB2 = zeros(1,m);
    
    [~,B1Indices,B2Indices] = intersect(reshape(oldB1(i,1:m,3:4),m,2),reshape(oldB2(i,1:m,3:4),m,2),'rows');
    nextIndex = 1;
    for local_quad_index = 1:m
        current_quad = B2Indices(nextIndex);
        neighbour = B1Indices(nextIndex);
        neighbourQuad = oldB1(i,neighbour,2);
        neighbourB2Index = find(oldB2(i,1:m,2) == neighbourQuad);
        nextIndex = find(B2Indices == neighbourB2Index);
        indicesLocB1(mod_index(local_quad_index+1,m)) = neighbour;
        indicesLocB2(local_quad_index) = current_quad;
    end
    newB1(i,1:m,:) = oldB1(i,indicesLocB1,:);
    newB2(i,1:m,:) = oldB2(i,indicesLocB2,:);
end