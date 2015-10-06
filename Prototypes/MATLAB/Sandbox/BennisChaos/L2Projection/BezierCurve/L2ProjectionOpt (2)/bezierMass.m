function [ M ] = bezierMass( N,D )
%BEZIERMASS Summary of this function goes here
%   Detailed explanation goes here

M=zeros((N+1)*D);

for i = 0:N
    BiN=@(t)bernstein(i,N,t);
    for j = 0:N
        BjN=@(t)bernstein(j,N,t);
        integralValue=integral(@(t)BiN(t).*BjN(t),0,1);
        for d = 1:D
            M(D*i+d,D*j+d)=integralValue;            
        end
    end
end


end

