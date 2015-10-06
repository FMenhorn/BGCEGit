function [ C,rhsC ] = bezierConnect_glob( N )
%BEZIERCLOSED Summary of this function goes here
%   Detailed explanation goes here

segments = 2;
C=zeros(segments * 2*(N+1),2);
rhsC=zeros(2,1);

dB0=bernstein(0,N,0);
dBN=bernstein(N,N,1);

C(N+1,1)=-dBN;
C(2*N+2+1,1)=dB0;
C(N+1+N+1,2)=-dBN;
C(N+1+2*N+3,2)=dB0;

rhsC(1)=0;
rhsC(2)=0;
end

