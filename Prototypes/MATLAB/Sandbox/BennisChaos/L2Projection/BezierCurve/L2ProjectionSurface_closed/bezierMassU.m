function [ A ] = bezierMassU( Uval,N,M,D )
%BEZIERMASS Summary of this function goes here
%   Detailed explanation goes here

A=zeros((N+1)*(M+1)*D,(M+1)*D);

for i = 0:N
    for j = 0:M
        zeta = i+j*(N+1);
        BzetaNM=@(u,v)bernstein(i,N,u).*bernstein(j,M,v);
        for jj = 0:M
            eta= jj;
            BetaNM=@(u,v)bernstein(jj,M,v);
            integralValue=integral(@(v)BzetaNM(Uval,v).*BetaNM(Uval,v),0,1);
            for d = 1:D
                A(D*zeta+d,D*eta+d)=integralValue;
            end
        end
    end
end

end

