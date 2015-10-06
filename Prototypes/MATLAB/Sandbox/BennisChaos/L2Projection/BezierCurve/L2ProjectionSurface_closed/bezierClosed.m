function [ C ] = bezierClosed( N,M,DIM )
%BEZIERCLOSED Summary of this function goes here
%   Detailed explanation goes here

C=zeros(DIM*(N+1)*(M+1),DIM);



[Bx0,By0]=generateBezierBasisFunction(0,N);
[BxN,ByN]=generateBezierBasisFunction(N,N);

fx0=@(t)arrayfun(@(t)Bx0(t)'*[1;0],t);
fy0=@(t)arrayfun(@(t)By0(t)'*[0;1],t);
fxN=@(t)arrayfun(@(t)-BxN(t)'*[1;0],t);
fyN=@(t)arrayfun(@(t)-ByN(t)'*[0;1],t);

C(1,1)=fx0(0);
C(N+1,1)=fxN(1);
C(N+2,2)=fy0(0);
C(2*N+2,2)=fyN(1);

end

