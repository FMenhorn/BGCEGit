function coefsMatrix = createCoefsMatrix(parameterCoordinates)

domainM = 14;
domainN = 8;

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
    coefsMatrix(p,i:(i+2),j:(j+2)) = getBezierPointCoefs(localCoords);
end