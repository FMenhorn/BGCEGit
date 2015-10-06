
[theta,phi]=meshgrid(pi/8:pi/8:3*pi/8,0:pi/4:1/2*pi);
Px=cos(phi).*sin(theta);
Py=sin(phi).*sin(theta);
Pz=cos(theta);

% [Px,Py]=meshgrid(0:.1:1,0:.1:1);
% Pz=Px.^2+Py.^2;%.*sin(Py*pi/2);

N=3;
M=3;

% A=bezierMass(N,M,3);

disp('quad:');
tic
rhs=bezierRHS(N,M,3,Px,Py,Pz);
toc

disp('no quad:')
tic
rhs_noquad=bezierRHS_noquad(N,M,3,Px,Py,Pz);
toc

rhs-rhs_noquad

% w=A\rhs;
%     
% [U,V]=meshgrid(0:.1:1);
% 
% cx=zeros(N+1,M+1);
% cy=zeros(N+1,M+1);
% cz=zeros(N+1,M+1);
% 
% cxyz=[w(1:3:end)';w(2:3:end)';w(3:3:end)'];
% cx(:)=cxyz(1,:);
% cy(:)=cxyz(2,:);
% cz(:)=cxyz(3,:);
% 
% bbx=@(u,v)0;
% bby=@(u,v)0;
% bbz=@(u,v)0;
% 
% for i = 0:N
%     for j = 0:M
%         BN=@(u)bernstein(i,N,u);
%         BM=@(v)bernstein(j,M,v);
%         bbx=@(u,v)bbx(u,v)+BN(u).*BM(v)*cx(i+1,j+1);
%         bby=@(u,v)bby(u,v)+BN(u).*BM(v)*cy(i+1,j+1);
%         bbz=@(u,v)bbz(u,v)+BN(u).*BM(v)*cz(i+1,j+1);
%     end
% end
% 
% [TX,TY,TZ]=Bilinear(Px,Py,Pz);
% 
% bx=bbx(U,V);
% by=bby(U,V);
% bz=bbz(U,V);
% 
% figure(1)
% hold on
% plot3(Px,Py,Pz,'b*')
% 
% %plot3(cx,cy,cz,'r*')
% mesh(TX,TY,TZ,'FaceColor','none')
% surf(bx,by,bz)
% 
% legend('point data','control points','bezier surface')
% 
% 
% hold off