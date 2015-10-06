function [ A ] = discreteProblem( p,U,V)
%DISCRETEPROBLEM Summary of this function goes here
%   Detailed explanation goes here

global knot_vector_u;
global knot_vector_v;

N_data=numel(U);
N_control_points_u=numel(knot_vector_u)-p;
N_control_points_v=numel(knot_vector_v)-p;
N_control_points_total=N_control_points_u*N_control_points_v;


A=zeros(N_data,N_control_points_total);
for i_u = 1 : N_control_points_u
    for i_v = 1: N_control_points_v
        for j = 1: N_data
            i = (i_v-1)*N_control_points_u+i_u;
            A(j,i) = bspline_basis(i_u-1,p,knot_vector_u, U(j))*bspline_basis(i_v-1,p,knot_vector_v, V(j));
        end
    end
end

%put three blocks A on the diagonal of a matrix.
A=kron(eye(3),A);

end

