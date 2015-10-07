function [C,res] = doRegression(XData,n,w)

Rji=discreteProblem(n,XData,w);

% define constraint A*C=b
% closed curve:
m=numel(w)-1;
A=zeros(1,m+1);
for i = 0:n  
    A(1,i+1)=rationalBasis(i,n,w,0)-rationalBasis(i,n,w,1);    
%    A(2,i+1)=dRationalBasis(i,w,0)-dRationalBasis(i,w,1);    
end
A=[A,zeros(size(A));...
   zeros(size(A)),A];
b=[0;0];%;0;0];

% constrained least squares
options = optimoptions('lsqlin','Algorithm','active-set');
RjiOLD=Rji;
Rji=[Rji,zeros(size(Rji));zeros(size(Rji)),Rji];
XDataOLD=XData;
XData=[XData(:,1);XData(:,2)];
C=Rji\XData;
C=lsqlin(Rji,XData,[],[],A,b,[],[],C,options);
C=[C(1:end/2),C(end/2+1:end)];
Rji=RjiOLD;
XData=XDataOLD;

% least squares with mldivide
% C=Rji\XData;

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