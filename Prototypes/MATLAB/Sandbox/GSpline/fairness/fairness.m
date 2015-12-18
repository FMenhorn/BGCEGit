%% Calculation of fairness functional coefficients

%the fairness functional for the surface s(u,v) parameterized over u,v in
%[0,1] should be

% e^2 = {integral: u and v from 0 to 1} [(d^2/du^2 s(u,v))^2 + (d^2/dudv
% s(u,v))^2 + (d^2/dv^2 s(u,v))^2 ]dudv

%this should be a least-squares thingy. Since 
% s = {sum over Bez pts} [bernstein_{n,i}(u)bernstein_{n,i}(v) *Bez pt.pos]

% the differentiation and integration over u and v should result in s being
% a sum over the bez points with the bernstein polynomial product being
% replaced by a constant coefficient.

% (This since the Bez pts are independent of u and v, so we can also just
% take them ot of the integrals)

%  we then have 3
% independent linear equations on the Bez points:

%E1 = sum [Bez pts * coefsFrom[d^2/du^2] ]
%E2 = sum [Bez pts * coefsFrom[d^2/dudv] ]
%E3 = sum [Bez pts * coefsFrom[d^2/dv^2] ]

%=> can formulate these being set to zero as a LSq minimization problem:

% find min || EX - 0 ||^2 

% which is equivalent to minimizing their squared sum=fairness functional.

% this means we can put it in the minimization matrix as three new rows,
% where the datapoint is 0 and the coeficcients are from the
% diff.+integration.

%% 1. Calculation of linear coefficients (can be done on beforehand)
% create symbolic variables


matrixAbiq = [232 -134 -38 -134 -32 46 -38 46 52;-134 328 -134 -32 -56 -32 46 -32 46;-38 -134 232 46 -32 -134 52 46 -38;-134 -32 46 328 -56 -32 -134 -32 46;-32 -56 -32 -56 352 -56 -32 -56 -32;46 -32 -134 -32 -56 328 46 -32 -134;-38 46 52 -134 -32 46 232 -134 -38;46 -32 46 -32 -56 -32 -134 328 -134;52 46 -38 46 -32 -134 -38 -134 232]/45;
[biqEigVecs,biqEigVals] = eig(matrixAbiq);
linConstraints = find(abs(diag(biqEigVals)) > 10^-6);
leastSqConstraints = biqEigVecs(:,linConstraints)*sqrt(biqEigVals(linConstraints,linConstraints));

oneone = [1734 -867 -316.5 -24;-867 -166.5 99 147;-316.5 99 126 93;-24 147 93 46.5];
onetwo = [-867 1836 -126 -318;-166.5 -198 -522 99;99 -72 -153 126;147 9 13.5 93];
twotwo = [-166.5 -198 -522 99;-198 1584 261 -72;-522 261 -373.5 -153;99 -72 -153 126];







