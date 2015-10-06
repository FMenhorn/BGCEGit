[X,Y,Z]=meshgrid(-.9:.1:.9,-.9:.1:.9,-1:.2:1);

ZZ=peaks(size(X,1));
ZZ=ZZ/max(max(ZZ));

VV=zeros(size(X));
for i = 1:size(ZZ,1)
    for j = 1:size(ZZ,1)
        VV(i,j,:)=Z(i,j,:)<ZZ(i,j);
    end
end

isosurface(X,Y,Z,VV,.5);

%V=@(X,Y,Z)exp(Z)-Y.^2+X.^2-1.5;
%fv=isosurface(X,Y,Z,V(X,Y,Z),0);
%V=@(x,y,z)x.^2+y.^2+z.^2-.75;

fv=isosurface(X,Y,Z,VV,.9);

N=3;
M=3;

P=fv.vertices;
Px=P(:,1);
Py=P(:,2);
Pz=P(:,3);

TRI=fv.faces;
U=(Px-min(Px))/(max(Px)-min(Px));
V=(Py-min(Px))/(max(Py)-min(Px));

disp('calculating A');
A=bezierMass(N,M,3);
disp('calculating rhs');
rhs=bezierRHS(N,M,3,P,TRI,U,V);


w=A\rhs;

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

[Uplot,Vplot]=meshgrid(0:.1:1);

bx=bbx(Uplot,Vplot);
by=bby(Uplot,Vplot);
bz=bbz(Uplot,Vplot);

figure(1)
hold on
%plot3(Px,Py,Pz,'b*')
%patch(fv,'FaceColor','blue')
%plot3(cx,cy,cz,'r*')
surf(bx,by,bz)
mesh(X(:,:,1),Y(:,:,1),ZZ,'FaceColor','none')

legend('point data','initial tri','control points','bezier surface')


hold off