function [ x ] = chordLength( P,t )
%CHORDLENGTH Summary of this function goes here
%   Detailed explanation goes here

tmax = max(t); %maximum value of knot vector

r=size(P,1);
x = zeros(r,1);
for s = 2:r
    x(s) = x(s-1) + norm(P(s,:)-P(s-1,:));
end

x=x/x(end)*tmax;


end

