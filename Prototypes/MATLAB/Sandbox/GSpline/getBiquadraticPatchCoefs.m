function points = getBiquadraticPatchCoefs(i,j)
% returns a matrix with the biquadractic point coefficients of its
% neighbour vertices for the control point (i,j) on the biquadratic patch,
% in the form of a 3x3 matrix of neighbouring vertex point coefs
points = zeros(3);

if (i==2)
    if (j ==2 ) 
        points(i,j) = 1;
    else 
        points(i,j) = 0.5;
        points(2,2) = 0.5;
    end
else
    if (j == 2)
        points(i,j) = 0.5;
        points(2,2) = 0.5;
    else
        points(i,j) = 0.25;
        points(i,2) = 0.25;
        points(2,j) = 0.25;
        points(2,2) = 0.25;
    end
end
end
 