function [ CC ] = bezierCurvature( N )
%BEZIERCLOSED Summary of this function goes here
%   Detailed explanation goes here

CC=zeros(2*(N+1),2);

CC(1,1)=bernstein_dderive(0,N,0);
CC(N+1,1)=bernstein_dderive(N,N,1);
CC(N+2,2)=bernstein_dderive(0,N,0);
CC(2*N+2,2)=bernstein_dderive(N,N,1);

end

