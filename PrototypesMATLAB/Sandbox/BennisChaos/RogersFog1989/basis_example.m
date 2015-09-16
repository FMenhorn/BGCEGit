n = 5;
m = 10;
x = 0:.001:1;
t = [zeros(1,n-1),linspace(0,1,m),ones(1,n-1)];

for i = 0:m
figure(1)
subplot(2,1,1)
hold on
h1=plot(x,bspline_basis(i,n,t,x));
hold off
subplot(2,1,2)
hold on
h2=plot(x,d_bspline_basis(i,n,t,x));
hold off
pause()
delete([h1,h2]);
end