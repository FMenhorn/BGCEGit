syms xx yy 
A=sym('A',[3,1]);
B=sym('B',[3,1]);
C=sym('C',[3,1]);
D=sym('D',[3,1]);
P=sym('P',[3,1]);

assume(xx,'real')
assume(yy,'real')
assume(A,'real')
assume(B,'real')
assume(C,'real')
assume(D,'real')
assume(P,'real')

Q=A*(1-xx)*(1-yy)+B*xx*(1-yy)+C*xx*yy+D*(1-xx)*yy;

PQ=Q-P;

AB=B-A;
AC=C-A;
AD=D-A;

eqns=[PQ'*AB==0;
PQ'*AC==0;
PQ'*AD==0];

%algebraic problem
sol=solve(eqns,[xx,yy]);

%or as a minimization problem
f=(P-Q)'*(P-Q);
df=[diff(f,xx);diff(f,yy)];