function [ R ] = rationalBasis( i,w,t )
%RATIONALBASIS Summary of this function goes here
%   Detailed explanation goes here

n=numel(w)-1;
denominator = zeros(size(t));

for ii = 0:numel(w)-1
    denominator = denominator + w(ii+1) * bernstein(ii,n,t);
end

R = bernstein(i,n,t)./denominator;

end

