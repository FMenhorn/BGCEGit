%Grid
h = .5;
[X,Y,Z]=meshgrid(-1:h:1,-1:h:1,-1:h:1);

%Volume Data
V=@(X,Y,Z)exp(Z)-Y.^2+X.^2-1.5;

%Marching Cubes
fv=isosurface(X,Y,Z,V(X,Y,Z),0);

isosurface(X,Y,Z,V(X,Y,Z),0)

%V=@(x,y,z)x.^2+y.^2+z.^2-.75;
%fv=isosurface(X,Y,Z,VV,.9);

%point data
P=fv.vertices;
Px=P(:,1);
Py=P(:,2);
Pz=P(:,3);

%connectivity information
TRI=fv.faces;

%corresponding parametrization
U=(Px-min(Px))/(max(Px)-min(Px));
V=(Py-min(Px))/(max(Py)-min(Px));


