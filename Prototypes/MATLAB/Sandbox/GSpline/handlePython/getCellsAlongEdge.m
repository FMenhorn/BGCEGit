function cellIndices = getCellsAlongEdge(quad_list,control_point_indices,quad_index,ver1,ver2,cellNumbers)

% quad indices oriented:
% 4---3
% |   |
% 1---2

local_control_point_indices = [1,2,3,4;5,6,7,8;9,10,11,12;13,14,15,16]';

% dirOne = [-0.5, 0.5, 0.5,-0.5];
% dirTwo = [-0.5,-0.5, 0.5, 0.5];
dirOne = [ 1.0, 4.0, 4.0, 1.0];
dirTwo = [ 1.0, 1.0, 4.0, 4.0];

neighbourQuad = quad_list(quad_index,:);

cellIndices = zeros(size(cellNumbers));
verOneIndex = find(neighbourQuad == ver1);
verTwoIndex = find(neighbourQuad == ver2);

verOneLocal = [dirOne(verOneIndex), dirTwo(verOneIndex)];
verTwoLocal = [dirOne(verTwoIndex), dirTwo(verTwoIndex)];

directionToGo = (verTwoLocal - verOneLocal)/3.0;
for i = 1:length(cellIndices)
    cellsLocalIndex = verOneLocal + (cellNumbers(i)-1)*directionToGo;
    local_control_index = local_control_point_indices(cellsLocalIndex(1),cellsLocalIndex(2));
    cellIndices(i) = control_point_indices(quad_index,local_control_index);

end



end