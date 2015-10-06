f=@(x)sin(6*x);
app=@(x)0*x;
n=100;
for i = 0:n
app=@(x)app(x)+f(i/n).*bernstein_stable(i,n,x);
end
x=[0:.001:1];
plot(x,f(x),'b',x,app(x),'r')