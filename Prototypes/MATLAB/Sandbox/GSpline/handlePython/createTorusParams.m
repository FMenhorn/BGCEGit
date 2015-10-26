%% create a set of ideal data complying to the stuff


numPoints1D = 31;

stepSize = 1/(numPoints1D);


% polParams = 0:stepSize:(1-stepSize);
% torParams = 0:stepSize:(1-stepSize);
[polParams,torParams] = meshgrid(0:stepSize:(1-stepSize));

minorRads = (1+0.0.*cos(2*pi*6.*torParams(:)));%.*(1 + 0.0*rand(numPoints1D,1));
majorRadis = 2.*(1+0.0.*sin(2*pi*3.*torParams(:)));

torusPointY = @(majorRad,minorRad,torAngle,polAngle) sin(torAngle).*(majorRad + cos(polAngle).*minorRad);
torusPointX = @(majorRad,minorRad,torAngle,polAngle) cos(torAngle).*(majorRad + cos(polAngle).*minorRad);
torusPointZ = @(majorRad,minorRad,torAngle,polAngle) sin(polAngle).*minorRad;

torPerturbations = 1 + 0.0.*sin(torParams(:)*2*pi);
polPerturbations = 1 + 0.0.*sin(polParams(:)*2*pi);

torParamsPerturbed = torParams(:) .* torPerturbations;
polParamsPerturbed = polParams(:) .* polPerturbations;

pointsX = torusPointX(majorRadis, minorRads, torParamsPerturbed*2*pi, polParamsPerturbed*2*pi);
pointsY = torusPointY(majorRadis, minorRads, torParamsPerturbed*2*pi, polParamsPerturbed*2*pi);
pointsZ = torusPointZ(majorRadis, minorRads, torParamsPerturbed*2*pi, polParamsPerturbed*2*pi);

patches1D = 3;

whichPatch = [floor(3.*torParams(:)),floor(3.*polParams(:))];
localCoords = [3.*torParams(:), 3.*polParams(:)] - whichPatch;
linearPatchNumber = whichPatch(:,1) + 3.*whichPatch(:,2);

createdParams = [linearPatchNumber,localCoords];
createdPoints = [pointsX,pointsY,pointsZ];

