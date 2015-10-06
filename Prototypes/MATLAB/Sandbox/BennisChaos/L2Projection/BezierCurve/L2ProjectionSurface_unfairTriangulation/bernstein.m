function [ B ] = bernstein( i,n,t )
%BERNSTEIN calculates i-th bernstein polynomial of degree n at t.

B=bincoeff(n,i).*t.^i .* (1-t).^(n-i);

end

