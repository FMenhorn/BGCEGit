Y=sym('Y',[3,1],'real');
x=sym('x',[2,1],'real');
A=sym('A',[3,1],'real');
B=sym('B',[3,1],'real');
C=sym('C',[3,1],'real');
D=sym('D',[3,1],'real');
X(x)=(1-x(1))*(1-x(2))*A+x(1)*(1-x(2))*B+x(1)*x(2)*C+(1-x(1))*x(2)*D;

% X=subs(X,A,[0;0;0]);
% X=subs(X,B,[1;0;0]);
% X=subs(X,C,[1;1;1]);
% X=subs(X,D,[0;1;0]);

f(x)=simplify((X-Y)'*(X-Y));

% f=subs(f,Y,[.5;.5;1]);

Df(x)=gradient(f);
Hf(x)=hessian(f);

% m_f = matlabFunction(f,'vars',{x});
% m_Df = matlabFunction(Df,'vars',{x});
% m_Hf = matlabFunction(Hf,'vars',{x});

m_f=matlabFunction(f,'Vars',{x,A,B,C,D,Y});
m_Df=matlabFunction(Df,'Vars',{x,A,B,C,D,Y});
m_Hf=matlabFunction(Hf,'Vars',{x,A,B,C,D,Y});