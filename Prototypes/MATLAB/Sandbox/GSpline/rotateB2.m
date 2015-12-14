function newB2 = rotateB2(oldB2)


mod_index = @(i,modul) mod(i-1,modul) + 1;
shifted_indices = @(ind,modul) mod_index((0:(modul-1)) + ind,modul);

newB2 = -1*ones(size(oldB2));

for i = 1:size(oldB2,1)
    m = getNumOfEdgesMeeting(oldB2,i);
    indices = shifted_indices(2,m);
    newB2(i,1:m,:) = oldB2(i,indices,:);
end