% 
% x=rand(5,1);
% y=[0 0 1 1 0];
% x(5)=x(1);

x=cos((0:10)*pi/5);
y=sin((0:10)*pi/5);

s=generateSpline(x,y);

N=4;

M=bezierMass(N);
C=bezierClosed(N);
S=bezierSmooth(N);
CC=bezierCurvature(N);

rhs=bezierRHS(N,s);

%constrained
lala=4;
w=[M,C,S;[C,S]',zeros(lala,lala)]\[rhs;zeros(lala,1)];
%unconstrained
% lala=0;
% w=M\rhs;

t=[0:.002:1];

sxy=s(t);
sx=sxy(1,:);
sy=sxy(2,:);

cxy=[w(1:N+1)';w(N+2:end-lala)'];
cx=cxy(1,:);
cy=cxy(2,:);

bb=@(t)0;

for i = 0:N
    [Bx,By]=generateBezierBasisFunction(i,N);
    bb=@(t)bb(t)+Bx(t)*cx(i+1);    
    bb=@(t)bb(t)+By(t)*cy(i+1);
end

bxy=bb(t);
bx=bxy(1,:);
by=bxy(2,:);

figure(1)
hold on
axis equal
plot(x,y,'b*')
plot(sx,sy,'b')

plot(cx,cy,'r*')
plot(bx,by,'r')

legend('point data','linear spline','control points','bezier curve')


hold off