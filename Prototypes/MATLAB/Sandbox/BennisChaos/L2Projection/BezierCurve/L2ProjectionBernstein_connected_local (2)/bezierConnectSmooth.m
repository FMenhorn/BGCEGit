function [ S,rhsS ] = bezierConnectSmooth( N,CP )
%BEZIERCLOSED Summary of this function goes here
%   Detailed explanation goes here

S=zeros(2*(N+1),2);
rhsS=zeros(2,1);

dB0=bernstein_derive(0,N,0);
dB1=bernstein_derive(1,N,0);

S(1,1)=dB0;
S(2,1)=dB1;
S(N+2,2)=dB0;
S(N+3,2)=dB1;

rhsS(1)=-(CP(1,N+1)*dB0+CP(1,N)*dB1);
rhsS(2)=-(CP(2,N+1)*dB0+CP(2,N)*dB1);

end

