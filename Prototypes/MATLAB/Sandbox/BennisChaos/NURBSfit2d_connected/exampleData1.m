%grid resolution
h = .5;

%grid dimensions for each patch
xmin = [-1 1];
xmax = [1 3];
ymin = [-1 -1];
ymax = [1 1];
zmin = [-1 -1];
zmax = [1 1];

n_patch = numel(xmin);

%Volume Data
ff=@(X,Y,Z)exp(Z)-Y.^2+X.^2-1.5;
f={@(X,Y,Z)ff(X,Y,Z),@(X,Y,Z)ff(X-2,Y,Z)};

XData = [];
TRI = [];
PATCH = [];
U = [];
V = [];

for i = 1:n_patch
    
    %grid
    [X,Y,Z]=meshgrid(xmin(i):h:xmax(i),ymin(i):h:ymax(i),zmin(i):h:zmax(i));
    
    %Marching Cubes
    fv=isosurface(X,Y,Z,f{i}(X,Y,Z),0);
    
    %connecticity info
    TRI=[TRI;fv.faces+size(XData,1)];
    
    %point data patch
    XData=[XData;fv.vertices];
    Px_tmp = fv.vertices(:,1);
    Py_tmp = fv.vertices(:,2);    
        
    %patch distribution
    PATCH=[PATCH;i*ones(size(fv.faces,1),1)];
    
    %corresponding parametrization for this patch
    U=[U;(Px_tmp-min(Px_tmp))/(max(Px_tmp)-min(Px_tmp))];
    V=[V;(Py_tmp-min(Py_tmp))/(max(Py_tmp)-min(Py_tmp))];
end

%put point data into different arrays
Px=XData(:,1);
Py=XData(:,2);
Pz=XData(:,3);

%visu
figure(1)
hold on
p=patch(struct('vertices',XData,'faces',TRI));
set(gca,'CLim',[min(PATCH)+.1 max(PATCH)-.1]);
cdata = PATCH;
set(p,'FaceColor','flat',...
'FaceVertexCData',cdata,...
'CDataMapping','scaled')
hold off


