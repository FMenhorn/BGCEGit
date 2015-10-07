function [ B ] = bernstein_dderive( i,n,t )
%BERNSTEIN calculates i-th bernstein polynomial of degree n at t.

if(i==0)
    B=bincoeff(n,i).*((n-i)*(n-i-1)*(1-t).^(n-i-2));
elseif(i==n)
    B=bincoeff(n,i).*(i*(i-1)*t.^(i-2));
else
    B=bincoeff(n,i).*(i*t.^(i-1) .* (1-t).^(n-i)+t.^i .* (n-i)*(1-t).^(n-i-1)*-1);
end

end

