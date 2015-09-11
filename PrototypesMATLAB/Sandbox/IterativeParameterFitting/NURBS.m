function [X,Y,Z] = NURBS( B,x,t,n )
%NURBS Summary of this function goes here
%   Detailed explanation goes here

%x is the parameter vector
%t is the knot vector
%n the degree of the spline (n=2 linear...)
%m is the number of intervals

X=zeros(numel(x),1);
Y=zeros(numel(x),1);
Z=zeros(numel(x),1);
%p = 2;
for i = 1:numel(x)
    for j  = 0 : (numel(t)-n-1)
        b=bspline_basis(j,n,t, x(i));
        X(i)=B(j+1,1)*b+X(i);
        Y(i)=B(j+1,2)*b+Y(i);
        Z(i)=B(j+1,3)*b+Z(i);
    end
end
end

