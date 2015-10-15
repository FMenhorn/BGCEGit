%%Example code for mesh refinement using Doo Sabin algorithm
clear all
close all
a=5;
c=10;
% [u,v]=meshgrid(0:10:370);
% % %torus equations
% size_v = size(v);
% x=(c+a*cosd(v)).*cosd(u);
% y=(c+a*cosd(v)).*sind(u);
% z=a*sind(v);
% S = surfl(x,y,z);
% hold off
% %convert our surface to patch
% [faces, verts, facevertexdata] = surf2patch(S);
% % [X, Y, Z] = sphere
% s = surf(X, Y, Z);
% [faces, verts, facevertexdata] = surf2patch(s);
 faces = dlmread('quads_Torus.csv',';')+1;
 verts = dlmread('vers_Torus.csv',';');
% 
 patch('Faces', faces, 'Vertices', verts)
 fv=struct('faces',faces,'vertices',verts);


%set up an averaging parameter alpha
alpha = 0.5;
[verts_new, faces_new, colours] = DooSabin(verts, faces, alpha);
%[verts_new2, faces_new2, colours_new] = DooSabin(verts_new, faces_new, alpha);
%patch('Faces', faces_new([433   865   869],:), 'Vertices', verts_new);
%colours
[patch3 patch4 patch5 patch6] = visualisation(faces_new, verts_new);
%plot refined torus
figure
patch('Faces', patch3, 'Vertices', verts_new, 'FaceVertexCData', ones(size(patch3,1), 1), 'FaceColor','flat');
patch('Faces', patch4, 'Vertices', verts_new, 'FaceVertexCData', 3.*ones(size(patch4,1), 1), 'FaceColor','flat');
patch('Faces', patch5, 'Vertices', verts_new, 'FaceVertexCData', 2.*ones(size(patch5,1), 1), 'FaceColor','flat');
patch('Faces', patch6, 'Vertices', verts_new, 'FaceVertexCData', 4.*ones(size(patch6,1), 1), 'FaceColor','flat');

% [patch31 patch41 patch51 patch61] = visualisation(faces_new2, verts_new2);
% figure
% patch('Faces', patch31, 'Vertices', verts_new2, 'FaceVertexCData', ones(size(patch31,1), 1), 'FaceColor','flat');
% patch('Faces', patch41, 'Vertices', verts_new2, 'FaceVertexCData', ones(size(patch41,1), 1), 'FaceColor','flat');
% patch('Faces', patch51, 'Vertices', verts_new2, 'FaceVertexCData', ones(size(patch51,1), 1), 'FaceColor','flat');
% patch('Faces', patch61, 'Vertices', verts_new2, 'FaceVertexCData', ones(size(patch61,1), 1), 'FaceColor','flat');