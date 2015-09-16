function [ f ] = generateSpline( x,y )
%GENERATESPLINE Summary of this function goes here
%   Detailed explanation goes here

N=numel(x)-1;

fx=@(t)x(1)*(t==0);
fy=@(t)y(1)*(t==0);

for i = 1:numel(x)-1
    fx=@(t)fx(t)+(x(i).*(i-t*N)+x(i+1).*(t*N+1-i)).*(t>(i-1)/N).*(t<=i/N);   
    fy=@(t)fy(t)+(y(i).*(i-t*N)+y(i+1).*(t*N+1-i)).*(t>(i-1)/N).*(t<=i/N);   
end

f=@(t)[fx(t);fy(t)];


end

