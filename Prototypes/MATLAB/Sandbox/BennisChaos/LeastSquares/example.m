N=10;
M=1;

%basis=@(i,x)x.^i;
basis=@(i,x)sin(mod(i,2)*(i+1)/2*x)+cos(mod(i+1,2)*i/2*x)-mod(2,i+1);

coeff=rand(N+1,1);

x=[-pi:.01*pi:pi]';

y=zeros(size(x));

for i = 0:N
    y=y+coeff(i+1)*basis(i,x);
end

%y=y+rand(size(y))/10;

y=heaviside(x);

A=zeros(numel(x),N+1);

%Least Squares Matrix
for i = 0:N
    A(:,i+1)=basis(i,x);
end

%Constraint: points (x_c,y_c) should be part of curve!
x_c = (rand(M,1)-.5)*2*pi;
y_c = (rand(M,1)-.5)*2*pi;

B=zeros(numel(x_c),N+1);
for i = 0:N
    B(:,i+1)=basis(i,x_c);
end

coeff_lsq=(A'*A)\(A'*y);

coeff_lsq_unconst = coeff_lsq;

G=[A'*A,B';B,zeros(numel(x_c))];
g=[A'*y;y_c];

coeff_lsq=G\g;

f_lsq=@(x)0*x;

for i = 0:N
    f_lsq=@(x)f_lsq(x)+coeff_lsq(i+1)*basis(i,x);
end

xx = linspace(-pi,pi,500);

figure(1)
hold on
plot(x,y,'*')
plot(x_c,y_c,'x')
plot(xx,f_lsq(xx))
hold off