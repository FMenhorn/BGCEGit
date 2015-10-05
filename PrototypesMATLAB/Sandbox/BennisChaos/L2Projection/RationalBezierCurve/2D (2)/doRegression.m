function [C,res] = doRegression(XData,n,w)

Rji=discreteProblem(n,XData,w);

% least squares with mldivide
C=Rji\XData;

% least squares with svd
% [U,S,V]=svd(Rji);
% 
% Dinv=zeros(size(S'));
% Dinv(S'~=0)=1./S(S~=0);
% 
% Rinv =V*Dinv*U';
% C=Rinv*XData;

X=Rji*C;

res = sum(sum((X-XData).^2));

end