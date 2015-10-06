function [X,Y,Z] = NURBS( Cx,Cy,Cz,U,V,p )
%PLOTRATIONALBEZIER Summary of this function goes here
%   Detailed explanation goes here
global knot_vector_u
global knot_vector_v

N_control_points_u=numel(knot_vector_u)-p;
N_control_points_v=numel(knot_vector_v)-p;

X=zeros(size(U));
Y=zeros(size(U));
Z=zeros(size(U));

for i = 1:numel(U)
    for j_u = 1 : N_control_points_u
        for j_v = 1: N_control_points_v            
            j = (j_v-1)*N_control_points_u+j_u;
            X(i)=Cx(j)*bspline_basis(j_u-1,p,knot_vector_u, U(i))*bspline_basis(j_v-1,p,knot_vector_v, V(i))+X(i);
            Y(i)=Cy(j)*bspline_basis(j_u-1,p,knot_vector_u, U(i))*bspline_basis(j_v-1,p,knot_vector_v, V(i))+Y(i);
            Z(i)=Cz(j)*bspline_basis(j_u-1,p,knot_vector_u, U(i))*bspline_basis(j_v-1,p,knot_vector_v, V(i))+Z(i);
        end
    end
end

end

