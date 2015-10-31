%% create a set of ideal data complying to the stuff

%num datapoints in toroidal and poloidal directions
numPoints1D = 31;

stepSize = 1/(numPoints1D);


% polParams = 0:stepSize:(1-stepSize);
% torParams = 0:stepSize:(1-stepSize);
[polParams,torParams] = meshgrid(0:stepSize:(1-stepSize));

%generate datapoints on a torus
minorRad = 1;
majorRad = 2;

%minor and major radius vectors
minorRads = minorRad*(1+0.0.*cos(2*pi*6.*torParams(:)));%.*(1 + 0.0*rand(numPoints1D,1));
majorRadis = majorRad.*(1+0.0.*sin(2*pi*3.*torParams(:)));

%x y z vectors on torus: functions 
torusPointY = @(majorRadius,minorRadius,torAngle,polAngle) sin(torAngle).*(majorRadius + cos(polAngle).*minorRadius);
torusPointX = @(majorRadius,minorRadius,torAngle,polAngle) cos(torAngle).*(majorRadius + cos(polAngle).*minorRadius);
torusPointZ = @(majorRadius,minorRadius,torAngle,polAngle) sin(polAngle).*minorRadius;

torPerturbations = 1 + 0.0.*sin(torParams(:)*2*pi);
polPerturbations = 1 + 0.0.*sin(polParams(:)*2*pi);

torParamsPerturbed = torParams(:) .* torPerturbations;
polParamsPerturbed = polParams(:) .* polPerturbations;

%x y z vectors on torus: data
pointsX = torusPointX(majorRadis, minorRads, torParamsPerturbed*2*pi, polParamsPerturbed*2*pi);
pointsY = torusPointY(majorRadis, minorRads, torParamsPerturbed*2*pi, polParamsPerturbed*2*pi);
pointsZ = torusPointZ(majorRadis, minorRads, torParamsPerturbed*2*pi, polParamsPerturbed*2*pi);

%num of patches per dimension (need to number the vertices of the quads
%manually though if you change!)
patches1D = 3;

whichPatch = [floor(patches1D.*torParams(:)),floor(patches1D.*polParams(:))];
localCoords = [patches1D.*torParams(:), patches1D.*polParams(:)] - whichPatch;
linearPatchNumber = whichPatch(:,1) + patches1D.*whichPatch(:,2);

createdParams = [linearPatchNumber,localCoords];
createdPoints = [pointsX,pointsY,pointsZ];
createdQuads = ...
   [0 1 4 3;...
    1 2 5 4;...
    2 0 3 5;...
    3 4 7 6;...
    4 5 8 7;...
    5 3 6 8;...
    6 7 1 0;...
    7 8 2 1;...
    8 6 0 2];

whichQuadY = @(i) floor(i/patches1D);
whichQuadX = @(i) i-patches1D*whichQuadY(i);
createdQuadVerts = zeros(patches1D,3);
for torI = 0:patches1D-1
    for polI = 0:patches1D-1
        createdQuadVerts(patches1D*polI + torI + 1,:) = [torusPointX(majorRad,minorRad,torI*2*pi/patches1D,polI*2*pi/patches1D),...
            torusPointY(majorRad,minorRad,torI*2*pi/patches1D,polI*2*pi/patches1D),...
            torusPointZ(majorRad,minorRad,torI*2*pi/patches1D,polI*2*pi/patches1D)];
    end
end

% lin_interp = @(u,vec1,vec2)  vec1 * (2*u-1) + (1-u) * vec2;






