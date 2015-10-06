function [ S ] = bezierSmooth( N )
%BEZIERCLOSED Summary of this function goes here
%   Detailed explanation goes here

S=zeros(2*(N+1),2);

for i = 0:N
    S(i+1,1)=bernstein_derive(i,N,0)-bernstein_derive(i,N,1);
    S(N+2+i,2)=bernstein_derive(i,N,0)-bernstein_derive(i,N,1);
end

end

