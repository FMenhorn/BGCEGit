
%% creation of raw data
%grid resolution
h = .25;

%grid dimensions
xmin = -1;
xmax = 1;
ymin = -1;
ymax = 1;
zmin = -1;
zmax = 1;

%Volume Data
f=@(X,Y,Z)Y.^2+Z.^2-1;
%f=@(X,Y,Z)X.^2+Y.^2+Z.^2-1;

%grid
[X,Y,Z]=meshgrid(xmin:h:xmax,ymin:h:ymax,zmin:h:zmax);

%Marching Cubes
fv=isosurface(X,Y,Z,f(X,Y,Z),0);

DATA = fv.vertices;
TRI = fv.faces;

%% division of surface into several patches

PATCHES = struct();

n_patches = 2;

for i = 1:n_patches
    name = ['patch',mat2str(i)];
    thisPatch = struct();
    
    thisPatch.id = i;    
    
    if(i==1)    
        vertex_ids = find(DATA(:,3)>=0);
    elseif(i==2)
        vertex_ids = find(DATA(:,3)<=0);
    end
    
    thisPatch.vertex_ids = vertex_ids
    
    TRI_ids_thisPatch = [];
    
    for t = 1:size(TRI,1)
        if(max(TRI(t,1)==vertex_ids) && max(TRI(t,2)==vertex_ids) && max(TRI(t,3)==vertex_ids))
            TRI_ids_thisPatch = [TRI_ids_thisPatch;t];
        end
    end
    
    thisPatch.tri_ids = TRI_ids_thisPatch;
    
    DATA_thisPatch = [DATA(thisPatch.vertex_ids,1),DATA(thisPatch.vertex_ids,2),DATA(thisPatch.vertex_ids,3)];
    
    xMin = min(DATA_thisPatch(:,1));
    xMax = max(DATA_thisPatch(:,1));
    yMin = min(DATA_thisPatch(:,2));
    yMax = max(DATA_thisPatch(:,2));
    thisPatch.vertex_u = (DATA_thisPatch(:,1)-xMin)/(xMax-xMin);
    thisPatch.vertex_v = (DATA_thisPatch(:,2)-yMin)/(yMax-yMin);
    
    PATCHES.(name)=thisPatch;
end

%% add connectivity of patches

for i = 1:n_patches
    name = ['patch',mat2str(i)];
    thisPatch = PATCHES.(name);
    vertex_ids = thisPatch.vertex_ids;
    connectedTo = zeros(size(vertex_ids));    
    PATCHES.(name).connectedTo=connectedTo;
end

for i = 1:n_patches
    name_i = ['patch',mat2str(i)];
    patch_i = PATCHES.(name_i);
    vertex_ids_i = patch_i.vertex_ids;  
    connectedTo_i = patch_i.connectedTo;
    for j = (i+1):n_patches
        name_j = ['patch',mat2str(j)];                
        patch_j = PATCHES.(name_j);
        vertex_ids_j = patch_j.vertex_ids;
        connectedTo_j = patch_j.connectedTo;        
        for v_i = 1:numel(vertex_ids_i)
            for v_j = 1:numel(vertex_ids_j)
                if(vertex_ids_i(v_i)==vertex_ids_j(v_j))
                    connectedTo_i(v_i)=j;
                    connectedTo_j(v_j)=i;
                end
            end
        end
        PATCHES.(name_j).connectedTo = connectedTo_j;
    end    
    PATCHES.(name_i).connectedTo = connectedTo_i;
end


%% visualisation

for i = 1:n_patches
    name = ['patch',mat2str(i)];
    thisPatch = PATCHES.(name);
    
    vertex_ids = thisPatch.vertex_ids;
    tri_ids = thisPatch.tri_ids;
    connected = thisPatch.connectedTo;
    
    DATA_thisPatch = [DATA(vertex_ids,1),DATA(vertex_ids,2),DATA(vertex_ids,3)];
    TRI_thisPatch = [TRI(tri_ids,1),TRI(tri_ids,2), TRI(tri_ids,3)];
    
    figure(1)
    hold on
    h_p=patch(struct('vertices',DATA,'faces',TRI_thisPatch));  
    if(i==1)
        col = 'k';
    else
        col = 'k';
    end
    h_v=plot3(DATA_thisPatch(:,1),DATA_thisPatch(:,2),DATA_thisPatch(:,3),'ko','MarkerFaceColor',col);
    h_b=plot3(DATA(vertex_ids(connected~=0),1),DATA(vertex_ids(connected~=0),2),DATA(vertex_ids(connected~=0),3),'ko','MarkerFaceColor','r');      
    set(gca,'CLim',[1 n_patches]);
    cdata = i * ones(size(TRI_thisPatch,1),1);
    set(h_p,'FaceColor','flat',...
        'FaceVertexCData',cdata,...        
        'CDataMapping','scaled') 
    view(3)
    hold off
end

%% fit NURBS to patches

for i = 1:n_patches
    
    name = ['patch',mat2str(i)];
    thisPatch = PATCHES.(name);
    
    N=5;
    M=5;
    h_p=3;
    
    [Cx,Cy,Cz,dataU,dataV,N,M,h_p,res]=NURBSfitOfPatch(N,M,h_p,DATA,thisPatch);
    %add boundary conditions!
    
    [U,V]=meshgrid(0:.1:1);
    [X,Y,Z]=NURBS(Cx,Cy,Cz,U,V,h_p);
    
    if(i==1)
        col = 'b';
    else
        col = 'y';
    end
    
    figure(1)
    hold on    
    surf(X,Y,Z,'FaceColor',col)
    plot3(Cx,Cy,Cz,'ko','MarkerFaceColor',col)
    axis([xmin,xmax,ymin,ymax,zmin,zmax])
    hold off   
    
    figure(2)
    subplot(2,1,i)
    hold on
    plot(U,V,'ko','MarkerFaceColor',col)
    hold off   
end


