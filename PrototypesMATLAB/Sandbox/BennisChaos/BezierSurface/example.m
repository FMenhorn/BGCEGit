nx=5;
ny=5;

P=zeros(3,nx,ny);
[P(1,:,:),P(2,:,:)]=meshgrid(0:1/(nx-1):1,0:1/(ny-1):1);
P(3,2:3,2:3)=0;
P(3,2,2)=2;
P(3,3,3)=3;

for ix = 1:nx
    P(3,ix,1)=((ix-1)/(nx-1))^(1/5)*3;
    P(3,ix,end)=((ix-1)/(nx-1))^5*3;
end

for iy = 1:ny
    P(3,1,iy)=((iy-1)/(ny-1))^(1/5)*3;
    P(3,end,iy)=((iy-1)/(ny-1))^5*3;
end

[x,y,z]=bezier(P,.05);
Px=zeros(nx,ny);
Py=zeros(nx,ny);
Pz=zeros(nx,ny);

Px(:,:)=P(1,:,:);
Py(:,:)=P(2,:,:);
Pz(:,:)=P(3,:,:);

hold on
surf(x,y,z)
mesh(Px,Py,Pz,'FaceColor','none','EdgeColor','k')
lighting gouraud
axis([0 1 0 1 -3 3])
hold off