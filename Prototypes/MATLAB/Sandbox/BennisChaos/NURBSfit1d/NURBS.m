function [x,y] = RationalBezier( C,t,p )
%PLOTRATIONALBEZIER Summary of this function goes here
%   Detailed explanation goes here
global knot_vector
n=size(C,1)-1;
%n = 4;
x=zeros(numel(t),1);
y=zeros(numel(t),1);
%p = 2;
for i = 1:numel(t)
    for j  = 0 : numel(knot_vector)- p -1
        x(i)=C(j+1,1)*bspline_basis(j,p,knot_vector, t(i))+x(i);
        y(i)=C(j+1,2)*bspline_basis(j,p,knot_vector, t(i))+y(i);
    end
end
end

