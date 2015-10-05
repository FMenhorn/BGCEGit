%% Example file
% This example plots all bspline basis functions on a given interval with
% the given knot vector and degree.

n=4; %bspline order (n=3 quadratic)
t=[zeros(1,n-1),0:.2:1,ones(1,n-1)]; %knot vector
j=0:numel(t)-n-1; %interval index 0<= j < numel(t)-n
x=0:.01:1; %evaluation points

figure(1)
hold on
for jj = 1:numel(j)
    [yy,xx]=bspline_basis(j(jj),n,t,x);
    plot(xx,yy)
end
hold off