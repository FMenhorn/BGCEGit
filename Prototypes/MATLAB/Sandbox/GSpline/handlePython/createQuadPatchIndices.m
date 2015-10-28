function quadIndices = createQuadPatchIndices(quadIndex)

quadIndices = zeros(4,4);

counter = quadIndex;

for j = 1:4
    for i = 1:4
        counter = counter + 1;
        quadIndices(i,j) = counter;
    end 
end


end