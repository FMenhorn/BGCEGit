function [ Bx,By,Bz ] = generateBezierBasisFunction( i,N )
%SPLINEBASISFUNCTION Summary of this function goes here
%   Detailed explanation goes here

basis=@(t)bernstein(i,N,t);
zero=@(t)0.*t;

Bx=@(t)[basis(t);zero(t);zero(t)];
By=@(t)[zero(t);basis(t);zero(t)];
Bz=@(t)[zero(t);zero(t);basis(t)];

end

