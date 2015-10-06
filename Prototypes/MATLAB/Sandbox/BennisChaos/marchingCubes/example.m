[X,Y,Z]=meshgrid(-1:1:1);

V=@(X,Y,Z)exp(Z)-Y.^2+X.^2-1.5;
%V=@(x,y,z)x.^2+y.^2+z.^2-.75;

fv=isosurface(X,Y,Z,V(X,Y,Z),0);

figure(1)
%subplot(1,2,1)
hold on
patch(fv,'FaceColor','blue')
plotMeshgrid(X,Y,Z)
xlabel('X')
ylabel('Y')
zlabel('Z')
axis equal
hold off

h1=[];
h2=[];
h3=[];
h4=[];
h5=[];
for i = 1:size(fv.vertices,1)
    delete(h1)
    delete(h2)
    delete(h3)
    delete(h4)
    delete(h5)
    c = getConnectedNodes(fv.faces,fv.vertices,i);
    cv = fv.vertices(c,:);  
    figure(1)
    hold on
    h1 = plot3(fv.vertices(i,1),fv.vertices(i,2),fv.vertices(i,3),'ro','MarkerSize',20,'MarkerFaceColor','r');
    h2 = plot3(cv(:,1),cv(:,2),cv(:,3),'go','MarkerSize',10,'MarkerFaceColor','g');
    hold off
%     figure(2)
%     hold on
%     [vx,vy]=voronoi(fv.vertices([c;i],1),fv.vertices([c;i],2),'r');
%     h3=plot(vx,vy,'b');
%     h4=plot(fv.vertices(c,1),fv.vertices(c,2),'go','MarkerSize',10,'MarkerFaceColor','g');
%     h5=plot(fv.vertices(i,1),fv.vertices(i,2),'or','MarkerSize',20,'MarkerFaceColor','r');
%     axis equal
%     axis([-1 1 -1 1])
%     hold off
    figure(2)
    hold on
    P=fv.vertices(i,1:2)';
    Q=fv.vertices(c,1:2)';
    PQ=Q-P*ones(1,size(Q,2));
    newQ=zeros(size(Q));
    for j = 1:size(PQ,2)
        i_max=max(abs(PQ(:,j)))==abs(PQ(:,j));
        PQ(i_max,j);
        newQ(:,j)=P;
        newQ(i_max,j)=Q(i_max,j);
    end
    
    [vx,vy]=voronoi([newQ(1,:),P(1)],[newQ(2,:),P(2)],'r');
    h3=plot(vx,vy,'b');
    h4=plot([newQ(1,:)],[newQ(2,:)],'go','MarkerSize',10,'MarkerFaceColor','g');
    h5=plot(P(1),P(2),'or','MarkerSize',20,'MarkerFaceColor','r');
    axis equal
    axis([-1 1 -1 1])
    hold off
    pause()   
end


% subplot(1,2,2)
% hold on
% vert=fv.vertices;
% face=fv.faces;
% %triplot(face,vert(:,1),vert(:,2),'r')
% voronoi(vert(:,1),vert(:,2))
% axis equal
% hold off
