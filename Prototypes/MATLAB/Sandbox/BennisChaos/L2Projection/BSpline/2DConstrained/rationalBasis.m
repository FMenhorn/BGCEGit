function [ R ] = rationalBasis( i,n,w,t )
%RATIONALBASIS Summary of this function goes here
%   Detailed explanation goes here

k = [zeros(1,n-1) 0:1/(n-1):1 ones(1,n-1)];

R = bspline_basis(i,n,k,t);

end

