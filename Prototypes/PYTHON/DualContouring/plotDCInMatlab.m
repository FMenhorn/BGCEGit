edges = dlmread('edges.csv',';')+1;
verts = dlmread('verts.csv',';');
voxel = dlmread('voxels.csv',';');
X = dlmread('x_mat.csv',';');
Y = dlmread('y_mat.csv',';');

R=2;
C=[4,4];

fv=struct('faces',edges,'vertices',verts);

figure(1)
hold on
view(2)
for i = 1:numel(X)
    if(voxel(i)==1)
        plot(X(i),Y(i),'ro')
    else
        plot(X(i),Y(i),'rx')
    end
end
plot(verts(:,1),verts(:,2),'b*')
patch(fv,'FaceColor','blue','LineWidth',2);
plot(X,Y,'k:','LineWidth',.2)
plot(X',Y','k:','LineWidth',.2)
plot(cos(0:.1*pi:2*pi)*R+C(1),sin(0:.1*pi:2*pi)*R+C(2),'--')
hold off