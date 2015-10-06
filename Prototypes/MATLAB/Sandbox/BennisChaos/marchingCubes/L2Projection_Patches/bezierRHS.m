function [ b ] = bezierRHS( N,M,DIM,P,TRI,U,V )
%BEZIERRHS Summary of this function goes here
%   Detailed explanation goes here

b=zeros(DIM*(N+1)*(M+1),1);

for i = 0:N
    for j = 0:M
        zeta = i+j*(N+1);
        BzetaNM=@(u,v)bernstein(i,N,u).*bernstein(j,M,v);
        for t = 1:size(TRI,1)
            
            idA=TRI(t,1);
            idB=TRI(t,2);
            idC=TRI(t,3);
            
            A=P(idA,:)';
            B=P(idB,:)';
            C=P(idC,:)';
            
            UVt=[U(idA),U(idB),U(idC);V(idA),V(idB),V(idC)];
            Pt=[A,B,C];
            
            b(DIM*zeta+(1:DIM))=b(DIM*zeta+(1:DIM))+quadrature_L2projection_tri(BzetaNM,ceil((N*M+2)/2),Pt,UVt);
            
        end
    end
end

% corner points lie on corner points of patch
for u = [0,1]
    for v = [0,1]
        i = u*N;
        j = v*M;
        zeta = i+j*(N+1);
        cornerPtid= find((U==u) .* (V==v));        
        b(DIM*zeta+(1:DIM))=P(cornerPtid,:);
    end
end

end

