
% x=rand(5,1);
% y=[0 0 1 1 0];
% x(5)=x(1);

% x=cos((0:10)*pi/5);
% y=sin((0:10)*pi/5);

x=0:.5:20;
y=cos(x);

segments=2;

s1=generateSpline(x(1:ceil(end/2)),y(1:ceil(end/2)));
s2=generateSpline(x(ceil(end/2):end),y(ceil(end/2):end));

N=6;

M=bezierMass(N);

rhs1=bezierRHS(N,s1);
rhs2=bezierRHS(N,s2);

[C,rhsC]=bezierConnect_glob(N);
[S,rhsS]=bezierConnectSmooth_glob(N);

M_glob=[M,zeros(size(M));zeros(size(M)),M];
rhs_glob=[rhs1;rhs2];
G=[M_glob,C,S;[C,S]',zeros(size(C,2)+size(S,2))];
w_glob=G\[rhs_glob;rhsC;rhsS];

t=[0:.002:1];

sxy=[s1(t),s2(t)];
sx=sxy(1,:);
sy=sxy(2,:);

w_glob=w_glob(1:end-size(C,2)-size(S,2));

w1 = w_glob(1:end/2);
w2 = w_glob(end/2+1:end);

c1xy=[w1(1:N+1)';w1(N+2:end)'];
c1x=c1xy(1,:);
c1y=c1xy(2,:);

c2xy=[w2(1:N+1)';w2(N+2:end)'];
c2x=c2xy(1,:);
c2y=c2xy(2,:);

bb1=@(t)0;
bb2=@(t)0;

for i = 0:N
    [Bx,By]=generateBezierBasisFunction(i,N);
    bb1=@(t)bb1(t)+Bx(t)*c1x(i+1);    
    bb1=@(t)bb1(t)+By(t)*c1y(i+1);
    bb2=@(t)bb2(t)+Bx(t)*c2x(i+1);    
    bb2=@(t)bb2(t)+By(t)*c2y(i+1);
end

bxy=[bb1(t),bb2(t)];
bx=bxy(1,:);
by=bxy(2,:);

figure(1)
hold on
axis equal
%plot(x,y,'b*')
%plot(sx,sy,'b')

plot(c1x,c1y,'r*')
plot(bx,by,'r')

legend('point data','linear spline','control points','bezier curve')
plot(c2x,c2y,'r*')


hold off