%generate not plane quad
A=[0;0;0];
B=[0;1;0];
C=[1;1;1];
D=[1;0;0];

P=[A,B,C,D];

%check if quad is plane
C=zeros(3);
for i = 2:4
    C(:,i-1)=P(:,i)-P(:,1);
end

if(det(C)==0)
    disp('quad is plane!')
else
    disp('quad is not plane!')
end

%random point
Q=rand(3,1);

%project point onto quad
%bilinear interpolation of quad
X=@(t) (1-t(1)).*(1-t(2))*P(:,1)+t(1).*(1-t(2))*P(:,2)+t(1).*t(2)*P(:,3)+(1-t(1)).*t(2)*P(:,4);
%distance function
f=@(t)(X(t)-Q)'*(X(t)-Q);

%find minimizer -> THIS IS SLOW!
t0=fminsearch(f,[.5,.5]);

proj_Q=X(t0);

[U,V]=meshgrid(0:.05:1);
quad_X=zeros(size(U));
quad_Y=zeros(size(U));
quad_Z=zeros(size(U));
for i = 1:numel(U)
    XX=X([U(i),V(i)]);
    quad_X(i)=XX(1);
    quad_Y(i)=XX(2);
    quad_Z(i)=XX(3);
end

%plot result
figure(1)
hold on
surf(quad_X,quad_Y,quad_Z)
plot3(Q(1),Q(2),Q(3),'b.','MarkerSize',20)
plot3(proj_Q(1),proj_Q(2),proj_Q(3),'kx','MarkerSize',20)
view(3)
hold off
