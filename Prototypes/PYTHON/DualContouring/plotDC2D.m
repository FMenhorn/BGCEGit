edges_fine = dlmread('edges_fine.csv',';')+1;
verts_fine = dlmread('verts_fine.csv',';');
edges_coarse = dlmread('edges_coarse.csv',';')+1;
verts_coarse = dlmread('verts_coarse.csv',';');
voxel = dlmread('voxels_fine.csv',';');
X = dlmread('x_mat_fine.csv',';');
Y = dlmread('y_mat_fine.csv',';');

R=2;
C=[4,4];

fv_fine=struct('faces',edges_fine,'vertices',verts_fine);
fv_coarse=struct('faces',edges_coarse,'vertices',verts_coarse);

figure(1)
hold on
view(2)
% for i = 1:numel(X)
%     if(voxel(i)==1)
%         plot(X(i),Y(i),'ro')
%     else
%         plot(X(i),Y(i),'rx')
%     end
% end
plot(verts_fine(:,1),verts_fine(:,2),'b*')
patch(fv_fine,'FaceColor','blue','EdgeColor','blue','LineWidth',2);
plot(verts_coarse(:,1),verts_coarse(:,2),'r*')
patch(fv_coarse,'FaceColor','red','EdgeColor','red','LineWidth',2);

plot(X,Y,'k-','LineWidth',.2)
plot(X',Y','k-','LineWidth',.2)
plot(cos(0:.1*pi:2*pi)*R+C(1),sin(0:.1*pi:2*pi)*R+C(2),'g--','LineWidth',2)
hold off