N=3;
M=3;

i=2;
j=2;

BzetaNM=@(u,v)bernstein(i,N,u).*bernstein(j,M,v);

P=rand(3);

patch(P(1,:),P(2,:),P(3,:),'b');

bq=zeros(3,1);
bi=zeros(3,1);

A=P(:,1);
B=P(:,2);
C=P(:,3);
AB=B-A;
AC=C-A;

umin = .5;
umax = 0;
vmin = 0;
vmax = .5;

N=6;

tridown = @(u,v,d)  A(d)+AB(d).*u+AC(d).*v;

disp('time with built in:')
tic
for d = 1:3
    fdown   = @(u,v) BzetaNM(u,v).*tridown(u,v,d);
    vmin_of_u=@(u)vmin*ones(size(u));
    vmax_of_u=@(u)u;
    figure(2)
    hold on
    Uparam=umin:.01*(umax-umin):umax;
    plot(Uparam,vmin_of_u(Uparam),'b')
    plot(Uparam,vmax_of_u(Uparam),'b')
    hold off
    bi(d)=integral2(fdown,umin,umax,vmin,vmax_of_u);
end
toc
   
disp('time with quad:')
UV=[umin umax umin;vmin vmin vmax];
tic
bq=quadrature_L2projection_tri(BzetaNM,N,[A,B,C],UV);
toc
norm(bi-bq)<10^-4