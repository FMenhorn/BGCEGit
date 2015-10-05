sampleData

N=size(FV.vertices,1);
M=size(fv.vertices,1);

dataPoints = zeros(N,2);
parameters = zeros(N,1);
patchId = zeros(N,1);
parametrization=struct('dataPoints',dataPoints,'parameters',parameters,'patchId',patchId);

for i = 1:size(FV.vertices,1)
    P=FV.vertices(i,:)';
    [id,Q,t]=findClosestSegment(P,fv.faces,fv.vertices);
    figure(1)
    hold on
    plot([P(1),Q(1)],[P(2),Q(2)],'r');
    hold off
    if(~mod(i,100))
        str=sprintf('Point %i of %i',i,size(FV.vertices,1));
        disp(str)
    end        
    parametrization.dataPoints(i,:)=P';
    parametrization.parameters(i)=t;
    parametrization.patchId(i)=id;
end

patches=struct('patchId',zeros(M,1),'faces',zeros(M,2),'vertices',zeros(M,2));

patches.patchId(:) = 1:size(fv.faces,1);
patches.faces = FV.faces;
patches.vertices = FV.vertices;

figure(1)
hold on
patch(fv,'EdgeColor','black','FaceColor','blue');
patch(FV,'EdgeColor','none','FaceColor','green');
hold off