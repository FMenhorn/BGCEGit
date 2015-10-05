function [ A ] = derivedBezierMassU( Uval,N,M,D )
%BEZIERMASS Summary of this function goes here
%   Detailed explanation goes here

A=zeros((N+1)*(M+1)*D,(M+1)*D);

for i = 0:N
    for j = 0:M
        zeta = i+j*(N+1);
        BzetaNM=@(v)bernstein_derive(i,N,Uval).*bernstein(j,M,v);
        for ii = 0:N
            for jj = 0:M
                eta= jj;
                BetaNM=@(v)bernstein_derive(ii,N,Uval).*bernstein(jj,M,v);
                integralValue=integral(@(v)BzetaNM(v).*BetaNM(v),0,1);
                for d = 1:D
                    A(D*zeta+d,D*eta+d)=A(D*zeta+d,D*eta+d)+integralValue;
                end
            end
        end
    end
end

end

