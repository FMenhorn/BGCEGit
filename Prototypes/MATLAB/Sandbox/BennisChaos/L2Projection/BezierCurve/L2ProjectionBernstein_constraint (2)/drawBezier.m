x=[0 1 0];
y=[0 1 2];

N=numel(x)-1;

bb=@(t)0;

for i = 0:N
    [Bx,By]=generateBezierBasisFunction(i,N);
    bb=@(t)bb(t)+Bx(t)*x(i+1);    
    bb=@(t)bb(t)+By(t)*y(i+1);
end

t=0:.01:1;

xy=bb(t);

figure(1)
hold on
    plot(xy(1,:),xy(2,:))
    plot(x,y,'*')
hold off