function [ B ] = bernstein_derive( i,n,t )
%BERNSTEIN calculates i-th bernstein polynomial of degree n at t.

if(i==0)
    B=bincoeff(n,i).*(t.^i .* (n-i).*(1-t).^(n-i-1)*-1);
elseif(i==n)
    B=bincoeff(n,i).*(i*t.^(i-1) .* (1-t).^(n-i));
else
    B=bincoeff(n,i).*(i*t.^(i-1) .* (1-t).^(n-i)+t.^i .* (n-i).*(1-t).^(n-i-1)*-1);
end

end

