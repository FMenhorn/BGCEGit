
h_coarse=.25;
x=cos(0:h_coarse*pi:2*pi);
y=sin(0:h_coarse*pi:2*pi);

fv=struct('faces',[[1:numel(x)]',[2:numel(x),1]'],'vertices',[x',y']);

h_fine=.01;
X=cos(0:h_fine*pi:2*pi);
Y=sin(0:h_fine*pi:2*pi);

FV=struct('faces',[[1:numel(X)]',[2:numel(Y),1]'],'vertices',[X',Y']);