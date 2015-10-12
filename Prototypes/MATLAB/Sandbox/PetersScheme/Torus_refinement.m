%%Example code for mesh refinement using Doo Sabin algorithm
clear all
close all
a=5;
c=10;
[u,v]=meshgrid(0:10:370);
% %torus equations
% size_v = size(v);
% x=(c+a*cosd(v)).*cosd(u);
% y=(c+a*cosd(v)).*sind(u);
% z=a*sind(v);
% S = surfl(x,y,z);
% hold off
% %convert our surface to patch
% [faces, verts, facevertexdata] = surf2patch(S);
[X, Y, Z] = sphere
s = surf(X, Y, Z);
[faces, verts, facevertexdata] = surf2patch(s);

%set up an averaging parameter alpha
alpha = 0.5;
[verts_new, faces_new, colours] = DooSabin(verts, faces, alpha);
%[verts_new2, faces_new2, colours_new] = DooSabin(verts_new, faces_new, alpha);
%colours

%plot refined torus
figure
patch('Faces', faces_new, 'Vertices', verts_new, 'FaceVertexCData', colours', 'FaceColor','flat');