function [ v,x,y,z ] = coarsen( V,X,Y,Z )
%COARSEN Summary of this function goes here
%   Detailed explanation goes here

v=logical(zeros(size(V)/2));
x=zeros(size(V)/2);
y=x;
z=x;

for i = 1:size(v,1)
    I=2*i-1;
    for j = 1:size(v,2)
        J=2*j-1;
        for k = 1:size(v,3)            
            K=2*k-1;
            v(i,j,k)=double(sum(sum(sum(double(V(I:I+1,J:J+1,K:K+1))))))/8>.5;
            x(i,j,k)=sum(sum(sum(X(I:I+1,J:J+1,K:K+1))))/8;
            y(i,j,k)=sum(sum(sum(Y(I:I+1,J:J+1,K:K+1))))/8;
            z(i,j,k)=sum(sum(sum(Z(I:I+1,J:J+1,K:K+1))))/8;
        end
    end
end  

end

