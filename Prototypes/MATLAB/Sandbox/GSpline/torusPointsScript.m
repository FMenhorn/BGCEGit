
numPoints = 200;

polParams = rand(numPoints,1);
torParams = rand(numPoints,1);

minorRads = (rand(numPoints,1) + 2) .*(1+0.4.*cos(5.*torParams));
majorRadis = 9.*(1+0.3.*sin(3.*torParams));

torusPointY = @(majorRad,minorRad,torAngle,polAngle) sin(torAngle).*(majorRad + cos(polAngle).*minorRad);
torusPointX = @(majorRad,minorRad,torAngle,polAngle) cos(torAngle).*(majorRad + cos(polAngle).*minorRad);
torusPointZ = @(majorRad,minorRad,torAngle,polAngle) sin(polAngle).*minorRad;

torPerturbations = 1 + 0.1.*sin(torParams*2*pi);
polPerturbations = 1 + 0.1.*sin(polParams*2*pi);

torParamsPerturbed = torParams .* torPerturbations;
polParamsPerturbed = polParams .* polPerturbations;

pointsX = torusPointX(majorRadis, minorRads, torParamsPerturbed*2*pi, polParamsPerturbed*2*pi);
pointsY = torusPointY(majorRadis, minorRads, torParamsPerturbed*2*pi, polParamsPerturbed*2*pi);
pointsZ = torusPointZ(majorRadis, minorRads, torParamsPerturbed*2*pi, polParamsPerturbed*2*pi);

figure;
scatter3(pointsX,pointsY,pointsZ);

%create coefficients matrix
paramCoords = [torParams , polParams];
coefsThreeDMatrix = createCoefsMatrix(paramCoords);

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

petersPlot(petersPoints,0.05);
