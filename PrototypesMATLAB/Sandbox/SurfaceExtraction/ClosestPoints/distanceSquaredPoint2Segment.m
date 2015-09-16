function [ dsq,Q ] = distanceSquaredPoint2Segment( P,A,B )
%DISTANCEPOINT2SEGMENT Summary of this function goes here
%   Detailed explanation goes here

AB=B-A;
PA=A-P;

mu=-(AB'*PA)/(AB'*AB);

Q=A+mu*AB;

PQ=Q-P;

assert(abs(PQ'*AB)<10^-15);

if(mu>=0 && mu<=1)   
    dsq=PQ'*PQ;%distancePoint2Point(P,Q);
elseif(mu<0)
    AP=P-A;
    dsq=AP'*AP;%distancePoint2Point(A,P);
    Q=A;
elseif(mu>1)
    BP=P-B;
    dsq=BP'*BP;%distancePoint2Point(B,P);
    Q=B;
end

end

