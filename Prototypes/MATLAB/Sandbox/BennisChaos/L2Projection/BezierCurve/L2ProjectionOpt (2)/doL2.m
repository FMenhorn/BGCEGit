
x=[0 1 2];
y=[0 1 0];

x=cos((0:20)*pi/20);
y=sin((0:20)*pi/20);

N=5;

M=bezierMass(N,2);
rhs=bezierRHS(N,2,[x;y]);

w=M\rhs;

t=0:.002:1;

cxy=[w(1:2:end)';w(2:2:end)'];
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
handle(1)=plot(x,y,'b*');

handle(2)=plot(cx,cy,'r*');
handle(3)=plot(bx,by,'r');

legend(handle,'point data','control points','bezier curve')


hold off