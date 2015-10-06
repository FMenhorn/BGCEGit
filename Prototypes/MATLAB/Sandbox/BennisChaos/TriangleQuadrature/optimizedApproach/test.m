A=[2,3,0]';
B=[3,3,0]';
C=[3,5,0]';
P=[A,B,C];

UV=[1,.5,1;1,0,0];

area_quad=quadrature_L2projection_tri(@(x,y)1+0.*x+0.*y,6,P,UV);
area_buildin=integral2(
AB=B-A;
AC=C-A;

area = abs(.5*cross(AB,AC));