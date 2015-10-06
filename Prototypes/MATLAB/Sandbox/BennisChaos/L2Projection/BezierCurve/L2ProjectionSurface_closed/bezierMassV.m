function [ A ] = bezierMassV( Vval,N,M,D )
%BEZIERMASS Summary of this function goes here
%   Detailed explanation goes here

A=zeros((N+1)*(M+1)*D,(N+1)*D);

for i = 0:N
    for j = 0:M
        zeta = i+j*(N+1);
        BzetaNM=@(u,v)bernstein(i,N,u).*bernstein(j,M,v);
        for ii = 0:N
            eta= ii;
            BetaNM=@(u,v)bernstein(ii,N,u);
            integralValue=integral(@(u)BzetaNM(u,Vval).*BetaNM(u,Vval),0,1);
            for d = 1:D
                A(D*zeta+d,D*eta+d)=integralValue;
            end
        end
    end
end

end

