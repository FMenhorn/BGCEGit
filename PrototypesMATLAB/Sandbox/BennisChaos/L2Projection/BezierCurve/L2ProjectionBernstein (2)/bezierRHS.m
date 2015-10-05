function [ b ] = bezierRHS( N,s )
%BEZIERRHS Summary of this function goes here
%   Detailed explanation goes here

b=zeros(2*(N+1),1);
for i = 0:N    
    [Bx,By]=generateBezierBasisFunction(i,N);
    f1=@(t)arrayfun(@(t)s(t)'*Bx(t),t);
    f2=@(t)arrayfun(@(t)s(t)'*By(t),t);
    b(i+1)=integral(f1,0,1);
    b(i+2+N)=integral(f2,0,1);
end

end

