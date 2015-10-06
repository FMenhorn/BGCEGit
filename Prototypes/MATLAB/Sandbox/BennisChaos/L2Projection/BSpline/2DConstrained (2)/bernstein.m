function [ B ] = bernstein( i,n,t )
%BERNSTEIN calculates i-th bernstein polynomial of degree n at t.
if (i == -1 || i == n+1)
    B = zeros(size(t));
else
    B=bincoeff(n,i).*t.^i .* (1-t).^(n-i);
end

end

