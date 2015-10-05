function [y,x] = bspline_basis(j,n,t,x)
% B-spline basis function value B(j,n) at x.
%
% Input arguments:
% j:
%    interval index, 0 =< j < numel(t)-n
% n:
%    B-spline order (2 for linear, 3 for quadratic, etc.)
% t:
%    knot vector
% x (optional):
%    value where the basis function is to be evaluated
%
% Output arguments:
% y:
%    B-spline basis function value, nonzero for a knot span of n

% Copyright 2010 Levente Hunyadi

validateattributes(j, {'numeric'}, {'nonnegative','integer','scalar'});
validateattributes(n, {'numeric'}, {'positive','integer','scalar'});
validateattributes(t, {'numeric'}, {'real','vector'});
assert(all( t(2:end)-t(1:end-1) >= 0 ), ...
    'Knot vector values should be nondecreasing.');
if nargin < 4
    x = linspace(t(n), t(end-n+1), 100);  % allocate points uniformly
else
    validateattributes(x, {'numeric'}, {'real','vector'});
end
assert(0 <= j && j < numel(t)-n, ...
    'Invalid interval index j = %d, expected 0 =< j < %d (0 =< j < numel(t)-n).', j, numel(t)-n);

y = bspline_basis_recurrence(j,n,t,x);
