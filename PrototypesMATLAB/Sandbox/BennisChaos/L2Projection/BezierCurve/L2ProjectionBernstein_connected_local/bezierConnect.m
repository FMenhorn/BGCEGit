function [ C,rhsC ] = bezierConnect( N,CP )
%BEZIERCLOSED Summary of this function goes here
%   Detailed explanation goes here

C=zeros(2*(N+1),2);
rhsC=zeros(2,1);

[Bx0,By0]=generateBezierBasisFunction(0,N);

fx0=@(t)arrayfun(@(t)Bx0(t)'*[1;0],t);
fy0=@(t)arrayfun(@(t)By0(t)'*[0;1],t);

C(1,1)=fx0(0);
C(N+2,2)=fy0(0);

rhsC(1)=CP(1,N+1);
rhsC(2)=CP(2,N+1);

end

