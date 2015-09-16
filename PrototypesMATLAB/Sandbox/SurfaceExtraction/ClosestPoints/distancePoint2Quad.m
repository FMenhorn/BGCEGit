function [ d,Q ] = distancePoint2Quad( P,A,B,C,D )
%DISTANCEPOINT2QUAD Summary of this function goes here
%   Detailed explanation goes here

fQ=@(x)A*(1-x(1))*(1-x(2))+B*x(1)*(1-x(2))+C*x(1)*x(2)+D*(1-x(1))*x(2);

f=@(x)(P-fQ(x))'*(P-fQ(x));
x=fminsearch(f,[.5,.5]);

Q=zeros(3,4);
d=zeros(1,4);

if(min(x>=0)&&min(x<=1))
    d=norm(fQ(x)-P);
    Q=fQ(x);
else
    CORNERS=[A,B,C,D,A];
    for i=1:4
        [dsq(i),Q(:,i)]=distanceSquaredPoint2Segment(P,CORNERS(:,i),CORNERS(:,i+1))
    end
    [dsq,i]=min(dsq);    
    Q=Q(:,i);  
    d=sqrt(dsq);
end

end

