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

tridown = @(u,v,d)  A(d)+AB(d).*u+AC(d).*v;

disp('time with built in:')
tic
for d = 1:3
    fdown   = @(u,v) BzetaNM(u,v).*tridown(u,v,d);
    bi(d)=integral2(fdown,0,1,0,@(u)1-u);
end
toc
   
disp('time with quad:')
tic
for d = 1:3
    fdown   = @(u,v) BzetaNM(u,v).*tridown(u,v,d);
    bq(d)=int_f(fdown,6,0,1,0,0,0,1);
end
toc
norm(bi-bq)<10^-4