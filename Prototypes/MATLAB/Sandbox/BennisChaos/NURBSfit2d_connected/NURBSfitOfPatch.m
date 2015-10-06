function [Cx,Cy,Cz,U,V,N,M,p,res] = NURBSfitOfPatch(N,M,p,DATA,PATCH)

global knot_vector_u;
global knot_vector_v;
%knot vector u
knot_vector_u = build_knot_vector(p,N);
%knot vector v
knot_vector_v = build_knot_vector(p,M);

Px=DATA(PATCH.vertex_ids,1);
Py=DATA(PATCH.vertex_ids,2);
Pz=DATA(PATCH.vertex_ids,3);

U=PATCH.vertex_u;
V=PATCH.vertex_v;

tic
[Cx,Cy,Cz,res]=doRegression(p,Px,Py,Pz,U,V);
toc

end