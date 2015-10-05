function [ M ] = bezierMass( N )
%BEZIERMASS Summary of this function goes here
%   Detailed explanation goes here

M=zeros((N+1)*2);

for i = 0:N    
    for j = 0:N
        [Bxi,Byi]=generateBezierBasisFunction(i,N);
        [Bxj,Byj]=generateBezierBasisFunction(j,N);
        
        f11=@(t)arrayfun(@(t)Bxi(t)'*Bxj(t),t);
        f22=@(t)arrayfun(@(t)Byi(t)'*Byj(t),t);
        
        M(i+1,j+1)=integral(f11,0,1);
        M(N+2+i,N+2+j)=integral(f22,0,1);
    end
end


end

