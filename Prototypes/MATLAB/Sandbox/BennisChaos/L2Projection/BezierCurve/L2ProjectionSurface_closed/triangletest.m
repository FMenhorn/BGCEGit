[X,Y]=meshgrid(0:1,0:.5:1);
Z=sin(X*pi).*sin(Y*pi);

[TX,TY,TZ]=Bilinear(X,Y,Z);

figure(1)
hold on
surf(TX,TY,TZ)
plot3(X,Y,Z,'*')
hold off
