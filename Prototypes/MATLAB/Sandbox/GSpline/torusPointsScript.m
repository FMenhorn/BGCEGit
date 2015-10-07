
numPoints = 200;

polParams = rand(numPoints,1);
torParams = rand(numPoints,1);

minorRads = rand(numPoints,1) + 2;
majorRadi = 9;

torusPointY = @(majorRad,minorRad,torAngle,polAngle) sin(torAngle).*(majorRad.*(1+0.3.*sin(3.*torAngle)) + cos(polAngle).*minorRad.*(1+0.4.*cos(5.*torAngle)));
torusPointX = @(majorRad,minorRad,torAngle,polAngle) cos(torAngle).*(majorRad.*(1+0.3.*sin(3.*torAngle)) + cos(polAngle).*minorRad.*(1+0.4.*cos(5.*torAngle)));
torusPointZ = @(majorRad,minorRad,torAngle,polAngle) sin(polAngle).*minorRad.*(1+0.4.*cos(5.*torAngle));

pointsX = torusPointX(majorRadi, minorRads, torParams*2*pi, polParams*2*pi);
pointsY = torusPointY(majorRadi, minorRads, torParams*2*pi, polParams*2*pi);
pointsZ = torusPointZ(majorRadi, minorRads, torParams*2*pi, polParams*2*pi);

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
