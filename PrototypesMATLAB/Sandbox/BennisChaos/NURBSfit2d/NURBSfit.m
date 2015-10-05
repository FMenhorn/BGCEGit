exampleData;

% f=@(x)sin(x);
% g=@(y)cos(y);
% 
% yData=f(0:pi/20:pi)';
% xData=g(0:pi/20:pi)';
% X=[xData,yData];

%number of control points in u
N = 4;
%number of control points in v
M = 4;

%polynomial degree
p = 2;

global knot_vector_u;
global knot_vector_v;
%knot vector u
knot_vector_u = build_knot_vector(p,N);
%knot vector v
knot_vector_v = build_knot_vector(p,M);

tic
[Cx,Cy,Cz,res]=doRegression(p,Px,Py,Pz,U,V);
toc


[U,V]=meshgrid(0:.1:1);
[X,Y,Z]=NURBS(Cx,Cy,Cz,U,V,p);

figure(1)
hold on
surf(X,Y,Z)
plot3(Cx,Cy,Cz,'*')
hold off