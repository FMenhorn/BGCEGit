function cellIndex = getCellAlongEdge(quadri,quadIndices,ver1,ver2,cellNumber)

% quad indices oriented:
% 4---3
% |   |
% 1---2

% dirOne = [-0.5, 0.5, 0.5,-0.5];
% dirTwo = [-0.5,-0.5, 0.5, 0.5];
dirOne = [ 0.0, 1.0, 1.0, 0.0];
dirTwo = [ 0.0, 0.0, 1.0, 1.0];


verOneIndex = find(quadri == ver1);
verTwoIndex = find(quadri == ver2);

verOneLocal = [dirOne(verOneIndex), dirTwo(verOneIndex)];
verTwoLocal = [dirOne(verTwoIndex), dirTwo(verTwoIndex)];

directionToGo = verTwoLocal - verOneLocal;

cellLocalIndex = verOneLocal + cellNumber*directionToGo;

cellIndex = quadIndices(cellLocalIndex(1),cellLocalIndex(2));





end