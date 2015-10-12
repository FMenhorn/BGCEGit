quads_fine = dlmread('quads_fine.csv',';')+1;
verts_fine = dlmread('verts_fine.csv',';');
quads_coarse = dlmread('quads_coarse.csv',';')+1;
verts_coarse = dlmread('verts_coarse.csv',';');
% voxel = dlmread('voxels_fine.csv',';');
% X = dlmread('x_mat_fine.csv',';');
% Y = dlmread('y_mat_fine.csv',';');
% Z = dlmread('z_mat_fine.csv',';');

R=2;
C=[4,4];

fv_fine=struct('faces',quads_fine,'vertices',verts_fine);
fv_coarse=struct('faces',quads_coarse,'vertices',verts_coarse);

figure(1)
hold on
view(3)
% for i = 1:numel(X)
%     if(voxel(i)==1)
%         plot(X(i),Y(i),'ro')
%     else
%         plot(X(i),Y(i),'rx')
%     end
% end
% plot(verts_fine(:,1),verts_fine(:,2),verts_fine(:,3),'b*')
patch(fv_fine,'FaceColor','blue','EdgeColor','black','LineWidth',2,'FaceAlpha',.5);
% plot(verts_coarse(:,1),verts_coarse(:,2),verts_coarse(:,3),'r*')
patch(fv_coarse,'FaceColor','red','EdgeColor','black','LineWidth',2,'FaceAlpha',.5);

% plot(X,Y,Z,'k-','LineWidth',.2)
% plot(X',Y',Z','k-','LineWidth',.2)
%plot(cos(0:.1*pi:2*pi)*R+C(1),sin(0:.1*pi:2*pi)*R+C(2),'g--','LineWidth',2)
axis equal
hold off