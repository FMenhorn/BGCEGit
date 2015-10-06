clf

R=1;
h=.01;
xCirc=R*cos(0:h*pi:2*pi);
yCirc=R*sin(0:h*pi:2*pi);
N=7;

figure(1)
hold on
axis equal
plot(xCirc,yCirc)
hold off


R=1;
h=.2;
xSTL=R*cos(0:h*pi:2*pi);
ySTL=R*sin(0:h*pi:2*pi);
figure(2)
hold on
axis equal
plot(xSTL,ySTL)
plot(xSTL,ySTL,'.','MarkerSize',10)
plot(xCirc,yCirc,'--')
hold off

f=@(x,y)x.^2+y.^2-1;

[X,Y]=meshgrid(-1.2:.1:1.2);
figure(3)
C=double(f(X,Y)<0);
hold on
axis equal
surf(X,Y,C);
hold off

C(and((X<-.3),C))=.5;
figure(4)
hold on
axis equal
surf(X,Y,C);
quiver3(2,0,0,-1,0,0,'k','LineWidth',2);
hold off

C(and(and((abs(Y)>.1),(X>.1)),C~=.5))=0;
figure(5)
hold on
axis equal
surf(X,Y,C);
quiver3(2,0,0,-1,0,0,'k','LineWidth',2);
hold off

C(C>0)=1;
figure(6)
hold on
axis equal
surf(X,Y,C);
hold off

figure(7)
hold on
axis equal
contour(X,Y,C,1);
hold off
