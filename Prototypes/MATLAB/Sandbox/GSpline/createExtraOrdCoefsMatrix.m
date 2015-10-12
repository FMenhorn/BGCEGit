function coefsMatrix = createExtraOrdCoefsMatrix(parameterCoordinates,coefs_raw)


domainM = 4;
domainN = 4;

mod_index = @(i,modul) mod(i-1,modul) + 1;
% rot = @(angle)[cos(angle),-sin(angle),0;sin(angle),cos(angle),0;0,0,1];

shifted_indices = @(ind,modul) mod_index((0:(modul-1)) + ind,modul);
AInds = [[5;5],   [2;5],    [2;2],    [5;2]];
B1Inds = [[5;4],   [3;5],   [ 2;3],   [ 4;2]];
B2Inds = [[4;5],   [2;4],   [ 3;2],   [ 5;3]];
CInds = [[4;4],   [3;4],   [ 3;3],   [ 4;3]];



whichQuadrant = [[3;4] , [2;1]];


% takes parameterCoordinates[Nx2](on a patch that spans over [0,1] with 4x4
% local bezier patches) and computes the coefficient matrix for each of
% these as a Nx6x6 matrix (where the first and last columns/rows are the
% neighbouring points)
N = size(parameterCoordinates,1);
coefsMatrix = zeros(N,domainM+2,domainN+2);

for p = 1:N
    scaledCoords = [(domainM*parameterCoordinates(p,1)), (domainN*parameterCoordinates(p,2))];
    whichPatch = floor(scaledCoords);
    localCoords = scaledCoords - ...
        whichPatch;
    i = whichPatch(1) + 1;
    j = whichPatch(2) + 1;
    if(((i ~= 2) && (i~= 3)) || ((j ~= 2) && (j ~= 3)))
        coefsMatrix(p,i:(i+2),j:(j+2)) = getBezierPointCoefs(localCoords);
    else
        quadr = whichQuadrant(i-1,j-1);
        localCoordsRot = projectOnQuadrant(localCoords,quadr);
        coefsTemp = getBicubicBezierPointCoefs(localCoordsRot,coefs_raw);
        indShift = shifted_indices(quadr,4);
        for anotherIndex = 1:length(indShift)
            coefsMatrix(p,AInds(1,indShift(anotherIndex)),AInds(2,indShift(anotherIndex))) = coefsTemp(1,anotherIndex);
            coefsMatrix(p,B1Inds(1,indShift(anotherIndex)),B1Inds(2,indShift(anotherIndex))) = coefsTemp(2,anotherIndex);
            coefsMatrix(p,B2Inds(1,indShift(anotherIndex)),B2Inds(2,indShift(anotherIndex))) = coefsTemp(3,anotherIndex);
            coefsMatrix(p,CInds(1,indShift(anotherIndex)), CInds(2,indShift(anotherIndex))) = coefsTemp(4,anotherIndex);
        end
    end
    
    
end