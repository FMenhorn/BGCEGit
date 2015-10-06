function [ dR ] = dRationalBasis( i,w,t )
%RATIONALBASIS Summary of this function goes here
%   Detailed explanation goes here

n=numel(w)-1;
denominator = zeros(size(t));
dDenominator = zeros(size(t));

for ii = 0:numel(w)-1
    denominator = denominator + w(ii+1) * bernstein(ii,n,t);
    dDenominator = dDenominator + w(ii+1) * dBernstein(ii,n,t);
end

dR = (denominator.*dBernstein(i,n,t)-bernstein(i,n,t).*dDenominator)./(denominator).^2;

end

