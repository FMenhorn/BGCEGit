function [ rotatedMatrix ] = rotateMatrixStructure( inputMatrix, clockwise90degturns)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

dimensions = size(inputMatrix,1);
lenI = size(inputMatrix,2);
lenJ = size(inputMatrix,3);

if (mod(clockwise90degturns,4) == 1)
    rotatedMatrix = zeros(dimensions,lenJ,lenI);
    for oldI = 1:lenI
        for oldJ = 1:lenJ
            rotatedMatrix(:,lenJ+1-oldJ,oldI) = inputMatrix(:,oldI,oldJ);
        end
    end
elseif (mod(clockwise90degturns,4) == 2)
    rotatedMatrix = zeros(dimensions,lenI,lenJ);
    for oldI = 1:lenI
        for oldJ = 1:lenJ
            rotatedMatrix(:,lenI+1-oldI,lenJ+1-oldJ) = inputMatrix(:,oldI,oldJ);
        end
    end
elseif (mod(clockwise90degturns,4) == 3)
    rotatedMatrix = zeros(dimensions,lenJ,lenI);
    for oldI = 1:lenI
        for oldJ = 1:lenJ
            rotatedMatrix(:,oldJ,lenI+1-oldI) = inputMatrix(:,oldI,oldJ);
        end
    end
else 
    rotatedMatrix = inputMatrix;
end



end

