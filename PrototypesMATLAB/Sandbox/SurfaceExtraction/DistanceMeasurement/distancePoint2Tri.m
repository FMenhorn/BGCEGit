function [ d,Q ] = distancePoint2Tri( P,A,B,C )
%DISTANCEPOINT2TRI Summary of this function goes here
%   Detailed explanation goes here

AB=B-A;
AC=C-A;
n=cross(AB,AC);
AP=P-A;
QP=AP'*n/(n'*n)*n;
PQ=-QP;
Q=P+PQ;

% a=AB'*AB;
% b=AB'*AC;
% c=AC'*AC;
% alpha = P'*AB;
% beta = P'*AC;
% 
% mu = (beta*b-alpha*c)/(b^2-a*c);
% nu = (alpha*b-beta*a)/(b^2-a*c);
% 
% Q=A+mu*AB+nu*AC;
% PQ=Q-P

d=norm(PQ);
assert(abs(PQ'*AB)<10^-13);
assert(abs(PQ'*AC)<10^-13);
AQ=Q-A;
xx=[AB,AC,n]\AQ;
mu=xx(1);
nu=xx(2);
if((mu+nu)>1 || mu < 0 || nu < 0)
    CORNERS=[A,B,C,A];
    for i=1:3
        [dsq(i),Q(:,i)]=distanceSquaredPoint2Segment(P,CORNERS(:,i),CORNERS(:,i+1));
    end
    [dsq,i]=min(dsq);  
    Q=Q(:,i); 
    d=sqrt(dsq);
end


end

