
numPoints = 400;

polParams = rand(numPoints,1);
torParams = rand(numPoints,1);

minorRads =  (2   +rand(numPoints,1) ).*(1+0.1.*cos(2*pi*3.*torParams));
majorRadis = 9 .*(1+0.05.*sin(2*pi*3.*torParams));

torusPointY = @(majorRad,minorRad,torAngle,polAngle) sin(torAngle).*(majorRad + cos(polAngle).*minorRad);
torusPointX = @(majorRad,minorRad,torAngle,polAngle) cos(torAngle).*(majorRad + cos(polAngle).*minorRad);
torusPointZ = @(majorRad,minorRad,torAngle,polAngle) sin(polAngle).*minorRad;

torPerturbations = 1 + 0.1.*sin(torParams*2*pi);
polPerturbations = 1 + 0.1.*sin(polParams*2*pi);

torParamsPerturbed = torParams ;%.* torPerturbations;
polParamsPerturbed = polParams ;%.* polPerturbations;

pointsX = torusPointX(majorRadis, minorRads, torParamsPerturbed*2*pi, polParamsPerturbed*2*pi);
pointsY = torusPointY(majorRadis, minorRads, torParamsPerturbed*2*pi, polParamsPerturbed*2*pi);
pointsZ = torusPointZ(majorRadis, minorRads, torParamsPerturbed*2*pi, polParamsPerturbed*2*pi);

figure;
scatter3(pointsX,pointsY,pointsZ);

mod_index = @(i,modul) mod(i-1,modul) + 1;
m = 4;
%create coefs template once
[Acoefs, B1coefs, B2coefs, Ccoefs] = createBicubicCoefMatrices(m);
coefs_raw = cat(1, reshape(Acoefs,1,m,4,4),reshape(B1coefs,1,m,4,4),reshape(B2coefs,1,m,4,4),reshape(Ccoefs,1,m,4,4));


%create coefficients matrix
paramCoords = [torParams , polParams];
coefsThreeDMatrix = createExtraOrdCoefsMatrix(paramCoords,coefs_raw);

% make it in matrix-vector form
dataPoints = [pointsX, pointsY, pointsZ];
domainM = size(coefsThreeDMatrix,2)-2;
domainN = size(coefsThreeDMatrix,3)-2;

numCols = (domainM) * (domainN);
coefsTwoDMatrix = zeros (numPoints,numCols);

reducedMod = @ (i,size) mod(i-1,size)+1;

localIndex = @(i,j,iwidth,jwidth) (reducedMod(j-1,jwidth)-1) * iwidth + reducedMod(i-1,iwidth);


for j = 1:domainN+2
    for i = 1:domainM+2
        loc_ind = localIndex(i,j,domainM,domainN);
        for p = 1:numPoints
            coefsTwoDMatrix(p,loc_ind) = ...
                coefsTwoDMatrix(p,loc_ind) + coefsThreeDMatrix(p,i,j);
        end
    end
end

bezierControlPoints = coefsTwoDMatrix\dataPoints;

petersPoints = zeros(3,domainM+2,domainN+2);
for i = 1:domainM+2
    for j = 1:domainN+2
        petersPoints(:,i,j) = bezierControlPoints(localIndex(i,j,domainM,domainN),:);
    end
end
figure;
plotPoints(petersPoints);
hold on;
plot3(pointsX,pointsY,pointsZ,'ro');

biQuadPatch = zeros(3,3,3);
biCubePatch = zeros(3,4,4);
whichQuadrant = [[3;4] , [2;1]];
AInds = [[5;5],   [2;5],    [2;2],    [5;2]];
B1Inds = [[5;4],  [3;5],    [2;3],   [ 4;2]];
B2Inds = [[4;5],  [2;4],    [3;2],   [ 5;3]];
CInds = [[4;4],   [3;4],   [ 3;3],   [ 4;3]];

As = zeros(3,4);
Bs = zeros(3,2,4);
Cs = zeros(3,4);
shifted_indices = @(ind,modul) mod_index((0:(modul-1)) + ind,modul);

for j = 2:(domainN+1)
    for i = 2:(domainM+1)
        if(((i ~= 3) && (i~= 4)) || ((j ~= 3) && (j ~= 4)))
            neighbours = petersPoints(:,(i-1):(i+1),(j-1):(j+1));
            biQuadPatch = getBiquadraticPatch(neighbours);
            plotPoints(biQuadPatch);
            [x,y,z] = bezier(biQuadPatch,0.1);
            surf(x,y,z);
        else
            quadr = whichQuadrant(i-2,j-2);
            indShift = shifted_indices(quadr,4);
            As(:,1) = petersPoints(:,AInds(1,indShift(1)),AInds(2,indShift(1)));
            for k = 1:4
                Bs(:,1,k) = petersPoints(:,B1Inds(1,indShift(k)),B1Inds(2,indShift(k)));
                Bs(:,2,k) = petersPoints(:,B2Inds(1,indShift(k)),B2Inds(2,indShift(k)));
                Cs(:,k) = petersPoints(:,CInds(1,indShift(k)),CInds(2,indShift(k)));
            end
            biCubePatch = getBicubicPatchIndex(1,As,Bs,Cs);
            plotPoints(biCubePatch);
            [x,y,z] = bezier(biCubePatch,0.05);
            surf(x,y,z);
        end        
    end
end
