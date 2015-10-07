A=[1 1];
b=3;
c=[2;1];
q=[-c;b];
S=zeros(2);
M=[S,A';A,zeros(size(A,1))];

[w,z,retcode]=LCPSolve(M,q);

% x should be [3;0;2]; w = M*x+q = [0;1;0], w'*z != 0