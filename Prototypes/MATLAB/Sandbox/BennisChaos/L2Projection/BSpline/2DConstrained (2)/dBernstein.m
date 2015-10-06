function [ dB ] = dBernstein( i,n,t )
%DBERNSTEIN calculates the derivative of the i-th bernstein polynomial of degree n at t.

dB=n*(bernstein(i-1,n-1,t)-bernstein(i,n-1,t));

end

