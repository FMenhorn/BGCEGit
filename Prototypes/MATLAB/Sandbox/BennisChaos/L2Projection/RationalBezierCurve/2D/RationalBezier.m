function [x,y] = RationalBezier( C,w,t )
%PLOTRATIONALBEZIER Summary of this function goes here
%   Detailed explanation goes here

n=size(C,1)-1;

x=zeros(numel(t),1);
y=zeros(numel(t),1);

for i = 1:numel(t)
    for j = 0:n
        x(i)=C(j+1,1)*rationalBasis(j,w,t(i))+x(i);
        y(i)=C(j+1,2)*rationalBasis(j,w,t(i))+y(i);
    end
end
end

