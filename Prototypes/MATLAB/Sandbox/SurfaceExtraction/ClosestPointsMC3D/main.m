L=5;

sampleData

%plot3(X(V),Y(V),Z(V),'*');
v=V;
x=X;
y=Y;
z=Z;
for i=1:3
    [v,x,y,z]=coarsen(v,x,y,z);
end
v
%plot3(x(v),y(v),z(v),'x');
FV=isosurface(X,Y,Z,V,.5);
fv=isosurface(x,y,z,v,.5);
size(fv.faces,1)

for i = 1:size(FV.vertices,1)
    P=FV.vertices(i,:)';
    [id,Q]=findClosestFace(P,fv.faces,fv.vertices);
    figure(1)
    hold on
    plot3([P(1),Q(1)],[P(2),Q(2)],[P(3),Q(3)],'r');
    % for i = 1:size(fv.faces,1)
    %     h=patch('Faces',fv.faces(i,:),'Vertices',fv.vertices,'EdgeColor','black','FaceColor','green');
    %     %pause()
    %     delete(h)
    % end
    hold off
    if(~mod(i,100))
        str=sprintf('Point %i of %i',i,size(FV.vertices,1));
        disp(str)
    end    
end

figure(1)
hold on
patch(fv,'EdgeColor','black','FaceColor','blue');
patch(FV,'EdgeColor','none','FaceColor','green','FaceAlpha',.5);
hold off