f=@(x)x;
g=@(y)sin(3*y);

xData=f(0:pi/20:2*pi)';
yData=g(0:pi/20:2*pi)';
X=[xData,yData];

n = 7;

p = 3;
global knot_vector;
knot_vector = build_knot_vector(p,n);
tic
[C,res]=doRegression(X,p);
toc

C=[ 0,0;...
   .1,1;...
    2,2;...
    2,3;...
    1,3;...
   -1,1;...
   -2,1;...
    -2,2];

t=0:1/100:1;
[x,y]=NURBS(C,t,p);

figure(1)
hold on
%plot(X(:,1),X(:,2),'r*')
plot(C(:,1),C(:,2),'b*')
plot(x,y,'b-')
legend('control pt.','BSpline')
hold off