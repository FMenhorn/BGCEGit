%L=3;
r=.3;
R=.7;
[X,Y,Z]=meshgrid(linspace(-1,1,2^L));
%[X,Y,Z]=meshgrid(linspace(-r-R-.1,r+R+.1,2^L));

f=@(x,y,z)x.^2+y.^2+z.^2-.5;
%f=@(x,y,z)(x.^2+y.^2+z.^2+R^2-r^2).^2-4*R^2*(x.^2+y.^2);

V=f(X,Y,Z)<0;