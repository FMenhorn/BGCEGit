xData=[0:.1:1,1:-.1:0]';
yData=[sin((0:.1:1)*pi/2),1:-.1:0]';

yData=sin(0:pi/10:2*pi)';
xData=cos(0:pi/10:2*pi)';
X=[xData,yData];

n=6;

w=ones(n+1,1);

w=fminsearch(@(w)optWeights(X,n,w),w); % can be optimized further sinze we know an analytical expression for the gradient. -> see Paper Becker et al.
[C,res]=doRegression(X,n,w);

t=0:1/100:1;
[x,y]=RationalBezier(C,w,t);

figure(1)
hold on
plot(X(:,1),X(:,2),'r*')
plot(C(:,1),C(:,2),'*')
plot(x,y,'r-')
hold off