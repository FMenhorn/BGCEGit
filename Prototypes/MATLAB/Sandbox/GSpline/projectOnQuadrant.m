function localCoords = projectOnQuadrant(localCoords_in, quadrant)
% QUADRANTS:
% 2 | 1
% --+--
% 3 | 4

rot  =@(angle)...
    [   cos(angle), -sin(angle); ...
        sin(angle),  cos(angle)];
angle = -(quadrant-3) * pi/2;

aroundOrigin = localCoords_in - 0.5;

rotatedAroundOrigin = rot(angle) * [aroundOrigin(1); aroundOrigin(2)];

localCoords = rotatedAroundOrigin + 0.5;