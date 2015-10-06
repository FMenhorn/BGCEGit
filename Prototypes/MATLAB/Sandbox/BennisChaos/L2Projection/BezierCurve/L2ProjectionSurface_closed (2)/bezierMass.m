function [ A ] = bezierMass( N,M,D )
%BEZIERMASS Summary of this function goes here
%   Detailed explanation goes here

A=zeros((N+1)*(M+1)*D);

for i = 0:N
    for j = 0:M
        zeta = i+j*(N+1);
        BzetaNM=@(u,v)bernstein(i,N,u).*bernstein(j,M,v);
        for ii = 0:N
            for jj = 0:M
                eta= ii+jj*(N+1);
                BetaNM=@(u,v)bernstein(ii,N,u).*bernstein(jj,M,v);
                integralValue=integral2(@(u,v)BzetaNM(u,v).*BetaNM(u,v),0,1,0,1);
                for d = 1:D
                    A(D*zeta+d,D*eta+d)=integralValue;
                end
            end
        end
    end
end

% %corner points lie on corner points of patch
% for i = [0,N]
%     for j = [0,M]
%         zeta = i+j*(N+1);
%         for d = 1:D
%             A(D*zeta+d,:)=0;
%             A(D*zeta+d,D*zeta+d)=1;
%         end
%     end
% end

end

