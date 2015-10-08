
m=5;
As = zeros(3,m);
Cs = zeros(3,m);
Bs = zeros(3,2,m);

threeDPoint = @(rho,phi,z) [rho.*cos(phi), rho.*sin(phi), z];

for i = 1:m
    Cs(:,i) = threeDPoint(1,(i-1)/m*2*pi,1);
    As(:,i) = threeDPoint(3,(i-1)/m*2*pi,0);
    Bs(:,1,i) = threeDPoint(2,(2*(i-1.25))*pi/m,0.5);
    Bs(:,2,i) = threeDPoint(2,(2*(i-1.25) + 1)*pi/m,0.5);
end

figure;

for i = 1:m
    patch = getBicubicPatchIndex(i,As,Bs,Cs);
%     patch(:,3,3) = rot(pi)*patch(:,3,3);
    [xx,yy,zz]=bezier(patch,0.05);
    surf(xx,yy,zz)
    hold on;
end
plotPoints(patch);
    