function newB2 = rotateB2fromB1(B1,oldB2)


mod_index = @(i,modul) mod(i-1,modul) + 1;
shifted_indices = @(ind,modul) mod_index((0:(modul-1)) + ind,modul);

newB2 = zeros(size(oldB2));

for i = 1:size(oldB2,1)
    m = getNumOfEdgesMeetingMatlab(oldB2,i);
    indices = zeros(1,m);
    for local_quad_index = 1:m
        indices(local_quad_index) = find(oldB2(i,:,2) == B1(i,local_quad_index,2));
    end
    newB2(i,1:m,:) = oldB2(i,indices,:);
end