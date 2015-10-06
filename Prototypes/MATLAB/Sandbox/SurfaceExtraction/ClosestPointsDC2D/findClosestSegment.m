function [id,Q,t]=findClosestSegment(P,faces,vertices)
%FINDCLOSESTSEGMENT Summary of this function goes here
%   Detailed explanation goes here

d=inf;
Q=zeros(2,1);
id=0;
for i = 1:size(faces,1)      
    A=vertices(faces(i,1),:)';            
    B=vertices(faces(i,2),:)';        
    [dnew,Qnew,tnew]=distanceSquaredPoint2Segment(P,A,B);
    if(dnew<d)        
        d=dnew;
        Q=Qnew;
        t=tnew;
        id=i;        
    end
end




end

