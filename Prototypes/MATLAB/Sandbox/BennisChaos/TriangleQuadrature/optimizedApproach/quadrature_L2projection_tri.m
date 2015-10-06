function rhs = quadrature_L2projection_tri(f,N,P,UV)
%   This function evaluates \iint_K f(x,y) dxdy using
%   the Gaussian quadrature of order N where K is a
%   triangle with vertices (x1,y1), (x2,y2) and (x3,y3).

xw = TriGaussPoints(N);  % get quadrature points and weights

% get corners of the triangle geometry patch
A = P(:,1);
B = P(:,2);
C = P(:,3);
AB=B-A;
BC=C-B;

% get corners of the triangle in parameter space
u1 = UV(1,1);
v1 = UV(2,1);
u2 = UV(1,2);
v2 = UV(2,2);
u3 = UV(1,3);
v3 = UV(2,3);

% calculate the area of the triangle in parameter space
Area=abs(u1*(v2-v3)+u2*(v3-v1)+u3*(v1-v2))/2.0;

% find number of Gauss points
NP=length(xw(:,1));

rhs=zeros(3,1);

figure(1)
subplot(1,2,1)
hold on
patch(P(1,:),P(2,:),P(3,:),'b')
xlabel('x')
ylabel('y')
zlabel('z')
hold off
subplot(1,2,2)
hold on
patch(UV(1,:),UV(2,:),'b')
xlabel('u')
ylabel('v')
hold off

PLocal =@(u,v) A.*(1-u-v)+B.*u+C.*v;

for j = 1:NP
    
    % calculate global parameters in the global parameter space belonging
    % to the currently evaluated quadrature point
    uGlobal = u1*(1-xw(j,1)-xw(j,2))+u2*xw(j,1)+u3*xw(j,2);
    vGlobal = v1*(1-xw(j,1)-xw(j,2))+v2*xw(j,1)+v3*xw(j,2);
    
    % evaluate triangle geometry at Gauss points of parameter space    
    % map to local coordinates on triangle 
    % (uLocal,vLocal)=(0,0) -> A
    % (uLocal,vLocal)=(1,0) -> B
    % (uLocal,vLocal)=(0,1) -> C
    uLocal = xw(j,1);
    vLocal = xw(j,2);
    Ptri = PLocal(uLocal,vLocal);
    rhs = rhs + Ptri*f(uGlobal,vGlobal)*xw(j,3);
    subplot(1,2,1)
    hold on
    plot3(Ptri(1),Ptri(2),Ptri(3),'.','MarkerSize',10)
    hold off
    subplot(1,2,2)
    hold on
    plot(uGlobal,vGlobal,'.','MarkerSize',10)
    coord_string = sprintf('(u=%1.3f,v=%1.3f)',uLocal,vLocal);
    text(uGlobal,vGlobal,coord_string)
    hold off
end
rhs = Area*rhs;
return
end