function quadIndex = getNeighbourSharedEdge(quads,selfIndex,ver1,ver2)

% dirOne = [-0.5, 0.5, 0.5,-0.5];
% dirTwo = [-0.5,-0.5, 0.5, 0.5];

[hasVer1,~] = find(quads == ver1);
[hasVer2,~] = find(quads(hasVer1,:) == ver2);

hasBoth = hasVer1(hasVer2);

quadIndex = hasBoth(hasBoth ~= selfIndex);
% 
% verOneIndex = find(quadri == ver1);
% verTwoIndex = find(quadri == ver2);
% 
% verOneLocal = [dirOne(verOneIndex), dirTwo(verOneIndex)];
% verTwoLocal = [dirOne(verTwoIndex), dirTwo(verTwoIndex)];
% 
% directionToGo = verTwoLocal - verOneLocal;
% 
% cellLocalIndex = verOneLocal + cellNumber*directionToGo;
% 
% cellIndex = quadIndices(cellLocalIndex(1),cellLocalIndex(2));
% 
% 



end