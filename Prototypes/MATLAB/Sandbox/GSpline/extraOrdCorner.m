
m=5;
As = zeros(3,m);
Cs = zeros(3,m);
Bs = zeros(3,2,m);

for i = 1:m
    Cs(:,i) = threeDPoint(1,(i-1)/m*2*pi,1);
    As(:,i) = threeDPoint(3,(i-1)/m*2*pi,0);
    Bs(:,1,i) = threeDPoint(2,(2*(i-1))*pi/m,0.5);
    Bs(:,2,i) = threeDPoint(2,(2*(i-1) + 1)*pi/m,0.5);
end

figure;
hold on;

for i = 1:m
    patch = getBicubicPatchIndex(i,As,Bs,Cs);
    [xx,yy,zz]=bezier(patch,0.05);
    surf(xx,yy,zz)
end
    plotPoints(patch);
    