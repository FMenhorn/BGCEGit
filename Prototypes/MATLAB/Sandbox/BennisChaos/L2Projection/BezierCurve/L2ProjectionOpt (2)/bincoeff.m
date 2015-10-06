function [ b ] = bincoeff( n,k )
%BINCOEFF calculates binomial coefficient: n! / k! / (n-k)!

if(n<k)
    error('n has to be greater or equal to k!');
elseif(n<0 || k<0)
    error('n and k both have to be positive!');
end

b=zeros(numel(n),numel(k));

for i = 1:numel(n)
    for j = 1:numel(k)
        b(i,j) = factorial(n(i))/factorial(k(j))/factorial(n(i)-k(j));
    end
end

end

