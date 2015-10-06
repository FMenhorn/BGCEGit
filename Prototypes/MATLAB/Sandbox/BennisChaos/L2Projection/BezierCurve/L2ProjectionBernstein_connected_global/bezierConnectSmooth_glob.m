function [ S,rhsS ] = bezierConnectSmooth_glob( N )
%BEZIERCLOSED Summary of this function goes here
%   Detailed explanation goes here

segments = 2;
S=zeros(segments * 2*(N+1),2);
rhsS=zeros(2,1);

dB0=bernstein_derive(0,N,0);
dB1=bernstein_derive(1,N,0);

dBN=bernstein_derive(N,N,1);
dBNm1=bernstein_derive(N-1,N,1);

S(N,1)=dBNm1;
S(N+1,1)=dBN;
S(2*N+3,1)=-dB0;
S(2*N+4,1)=-dB1;
S(N+1+N,2)=dBNm1;
S(N+1+N+1,2)=dBN;
S(N+1+2*N+3,2)=-dB0;
S(N+1+2*N+4,2)=-dB1;

rhsS(1)=0;
rhsS(2)=0;

end

