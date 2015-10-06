function [ B ] = bernstein_stable( i,n,t )
%BERNSTEIN_STABLE Summary of this function goes here
%   Detailed explanation goes here

if(n==0)
    B=1*ones(size(t));
else
db    B=benstein_stable(i,n-1,t).*(1-t)+benstein_stable(i+1,n-1,t).*t;
end

end

