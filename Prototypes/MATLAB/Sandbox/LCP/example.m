% minimized function:
% f(x)=x'*S*x-c'*x+K
% Distance of point x to P
% f(x)=x'*Id*x-2*P'*x+P'*P

d=2;

P=[1;3];

S=eye(d);
c=-2*P;
K=P'*P;

% constraining function:
% g(x)=[A*x-b;-x] <= 0
% x has to be on the line defined by:
% m*x+t

m = 2;
t = 1;

% m*x-y+t = 0
% reformulation
% m*x-y+t <= 0 AND -m*x+y-t <= 0
A=[m,-1;-m,+1];
b=[-t;t];

M=[2*S,A';-A,zeros(size(A,1))];
q=[-c;b];

[w,z,retcode]=LCPSolve(M,q);

x=z;

XX=x(1:2);

xx = linspace(0,10);

yy = m*xx+t;

figure(1)
hold on
plot(xx,yy)
plot(XX(1),XX(2),'r*')
plot(P(1),P(2),'bx')
hold off
