function [ id,Q ] = findClosestFace( P,faces,vertices )
%FINDCLOSESTFACE Summary of this function goes here
%   Detailed explanation goes here

d=inf;
Q=zeros(3,1);
id=0;
for i = 1:size(faces,1)      
    A=vertices(faces(i,2),:)';
    B=vertices(faces(i,3),:)';
    C=vertices(faces(i,1),:)';            
    [dnew,Qnew]=distancePoint2Tri(P,A,B,C);    
    if(dnew<d)        
        d=dnew;
        Q=Qnew;
        id=i;
        TRI=[A,B,C];
    end
end

end

