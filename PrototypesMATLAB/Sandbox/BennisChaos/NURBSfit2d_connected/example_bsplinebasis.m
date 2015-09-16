function example_bsplinebasis
% Illustrates B-spline basis functions.

% Copyright 2010 Levente Hunyadi

n = 3;
t = build_knot_vector(n,10)
%t = [0 0 0 0.5 1 1 1];  % knot vector
%n = 3;  % quadratic spline
figure( ...
    'Name', sprintf('NURBS basis functions of order %d', n));
hold all;
for j = 0 : numel(t)-n-1
    [y,x] = bspline_basis(j,n,t);
    plot(x, y);
end
hold off;
