
[theta,phi]=meshgrid(0:pi/6:5*pi/6,0:pi/4:7/8*pi);
Px=cos(phi).*sin(theta);
Py=sin(phi).*sin(theta);
Pz=cos(theta);

% [Px,Py]=meshgrid(0:.1:1,0:.1:1);
% Pz=Px.^2+Py.^2;%.*sin(Py*pi/2);

N=4;
M=4;

A=bezierMass(N,M,3);
U0=bezierMassU(0,N,M,3);
U1=-bezierMassU(1,N,M,3);
%V0=bezierMassV(0,N,M,3);
%V1=-bezierMassV(1,N,M,3);
% dU0=derivedBezierMassU(0,N,M,3);
% dU1=derivedBezierMassU(1,N,M,3);
C=[U0+U1];%,V0+V1];%,dU0+dU1];
rhs=bezierRHS(N,M,3,Px,Py,Pz);

ww=[A,C;C',zeros(size(C,2))]\[rhs;zeros(size(C,2),1)];

w=ww(1:3*(N+1)*(M+1));
    
[U,V]=meshgrid(0:.01:1);

cx=zeros(N+1,M+1);
cy=zeros(N+1,M+1);
cz=zeros(N+1,M+1);

cxyz=[w(1:3:end)';w(2:3:end)';w(3:3:end)'];
cx(:)=cxyz(1,:);
cy(:)=cxyz(2,:);
cz(:)=cxyz(3,:);

bbx=@(u,v)0;
bby=@(u,v)0;
bbz=@(u,v)0;

for i = 0:N
    for j = 0:M
        BN=@(u)bernstein(i,N,u);
        BM=@(v)bernstein(j,M,v);
        bbx=@(u,v)bbx(u,v)+BN(u).*BM(v)*cx(i+1,j+1);
        bby=@(u,v)bby(u,v)+BN(u).*BM(v)*cy(i+1,j+1);
        bbz=@(u,v)bbz(u,v)+BN(u).*BM(v)*cz(i+1,j+1);
    end
end

[TX,TY,TZ]=Bilinear(Px,Py,Pz);

bx=bbx(U,V);
by=bby(U,V);
bz=bbz(U,V);

figure(1)
hold on
plot3(Px,Py,Pz,'b*')

%plot3(cx,cy,cz,'r*')
mesh(TX,TY,TZ,'FaceColor','none')
surf(bx,by,bz)

legend('point data','control points','bezier surface')


hold off