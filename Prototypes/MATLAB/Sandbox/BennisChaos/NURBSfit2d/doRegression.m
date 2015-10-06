function [Cx,Cy,Cz,res] = doRegression(p,Px,Py,Pz,U,V)

% put point data into vector
XData = [Px;Py;Pz];

% construct least squares matrix
A=discreteProblem(p,U,V);

% least squares with mldivide
C=A\XData;

% compute points of fit
X=A*C;

% residual
res = sum(sum((X-XData).^2));

Cx = C(1:end/3);
Cy = C(end/3+1:end*2/3);
Cz = C(end*2/3+1:end);

end