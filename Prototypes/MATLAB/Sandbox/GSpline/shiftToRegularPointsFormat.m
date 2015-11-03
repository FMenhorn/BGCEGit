function verticesInRegularPointsFormat = shiftToRegularPointsFormat(regularPoints,verticesInIndexFormat)

verticesInRegularPointsFormat = zeros(size(regularPoints,1)*size(regularPoints,2),3);

for quad_index = 1:size(regularPoints,1)
    for i = 1:16
        reg_index = regularPoints(quad_index,i);
        verticesInRegularPointsFormat(reg_index,:) = verticesInIndexFormat(:,quad_index,i);
        
        
    end 
end




end