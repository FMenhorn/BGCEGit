function coefsMatrix = createGlobalControlMeshCoefs(parameterCoordinates,quad_list,AVertexList,B1VertexList,B2VertexList,CVertexList,quad_control_point_indices)

% takes, for N datapoints, an array parameterCoordinates[Nx3](for every 
% datapoint: first entry the quad index, second and third parameterson a patch that spans over [0,1]x[0,1]
% for the quad. The function computes the coefficient matrix for between
% each datapoint and the array of M/16 quads x [4x4] vertex control points,
% outputting the coefficients as an N x M matrix.

N = size(parameterCoordinates,1);
M = size(quad_control_point_indices,1)*size(quad_control_point_indices,2);
coefsMatrix = zeros(N,M);

%precalculate the coefficients between all the vertex control points and
%the bezier control points for 7 different number of intersecting
%edges as a start

%(number of incoming edges(between 3 an 7 hardcoded), [A,B1,B2,C], [in which quad 1-7], bezier point
%first coord, bezier point second coord)
extraOrdinaryCoefsRaw = zeros(7,4,7,4,4);
ACoefsRaw = zeros(7,7,4,4);
B1CoefsRaw = zeros(7,7,4,4);
B2CoefsRaw = zeros(7,7,4,4);
CCoefsRaw  = zeros(7,7,4,4);
for i = 3:7
    [ACoefsRaw(i,1:i,:,:),...
        B1CoefsRaw(i,1:i,:,:),...
        B2CoefsRaw(i,1:i,:,:),...
        CCoefsRaw(i,1:i,:,:)] = ...
        createBicubicCoefMatrices(i);
end


mod_index = @(i,modul) mod(i-1,modul) + 1;
shifted_indices = @(ind,modul) mod_index((0:(modul-1)) + ind,modul);
reverse_shifted_indices = @(ind,modul) mod_index(((modul):-1:1) + ind,modul);

% aroundcorner_indices = zeros(1,7);
AIndices = zeros(1,7);
B1Indices = zeros(1,7);
B2Indices = zeros(1,7);
CIndices = zeros(1,7);

coefsRawTemp = zeros(4,7,4,4);



for p = 1:N
    % check if on a corner patch : if both coords are outside [0.25,0.75]
    quadParameters = parameterCoordinates(p,2:3);
    quad_index = parameterCoordinates(p,1);
    %TODO: look up patch index already here to have definite decision
    [localCoords,whichCorner,whichPatch] = createLocalParamsExtraordinary(quadParameters);
    
    % if there is a specified corner set
    if(whichCorner ~= -1)
        
        
        
        cornerVertexIndex = quad_list(quad_index,whichCorner);
        numberOfEdges = getNumOfEdgesMeetingMatlab(AVertexList,cornerVertexIndex);
%         quadLocalIndex = find(AVertexList(cornerVertexIndex,:,2) == quad_index);
        indexMask = getExtraOrdCornerIndexMask(quad_list,AVertexList,B1VertexList,B2VertexList,CVertexList,quad_control_point_indices,quad_index,whichCorner);
        
        coefsRawTemp(1,1:numberOfEdges,:,:) = ACoefsRaw(numberOfEdges,1:numberOfEdges,:,:);
        coefsRawTemp(2,1:numberOfEdges,:,:) = B1CoefsRaw(numberOfEdges,1:numberOfEdges,:,:);
        coefsRawTemp(3,1:numberOfEdges,:,:) = B2CoefsRaw(numberOfEdges,1:numberOfEdges,:,:);
        coefsRawTemp(4,1:numberOfEdges,:,:) = CCoefsRaw(numberOfEdges,1:numberOfEdges,:,:);
        
        patchCoefsMatrix = getBicubicBezierPointCoefs(localCoords,coefsRawTemp(:,1:numberOfEdges,:,:));
%         coefsMatrix(p,AIndices) = patchCoefsMatrix(1,:);
%         coefsMatrix(p,B1Indices) = patchCoefsMatrix(2,:);
%         coefsMatrix(p,B2Indices) = patchCoefsMatrix(3,:);
%         coefsMatrix(p,CIndices) = patchCoefsMatrix(4,:);
        coefsMatrix(p,indexMask(:)) = patchCoefsMatrix(:);
        
        
    else
        %     scaledCoords = [(domainM*parameterCoordinates(p,1)), (domainN*parameterCoordinates(p,2))];
        %     whichPatch = floor(scaledCoords);
        %     localCoords = scaledCoords - ...
        %         whichPatch;
        %     i = whichPatch(1) + 1;
        %     j = whichPatch(2) + 1;
        
        %TODO: get a neighbour mask
        neighbourMask = get3x3ControlPointIndexMask(quad_list,quad_control_point_indices,quad_index,whichPatch);
        neighbourCoefs = getBezierPointCoefs(localCoords);
        %
        for j = 1:3
            for i = 1:3
                coefsMatrix(p,neighbourMask(i,j)) = neighbourCoefs(i,j);
            end
        end
    end
    
end
end