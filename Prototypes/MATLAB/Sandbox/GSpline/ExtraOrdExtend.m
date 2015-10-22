 %% this is put on hold for feasible closed geometry with extraordinary faces
m=4;
As = zeros(3,m);
Cs = zeros(3,m);
CBots = zeros(3,m);
B1s = zeros(3,m);
B2s = zeros(3,m);

threeDPoint = @(rho,phi,z) [rho.*cos(phi), rho.*sin(phi), z];
rot = @(angle)[cos(angle),-sin(angle),0;sin(angle),cos(angle),0;0,0,1];


for i = 1:m
    Cs(:,i) = threeDPoint(sqrt(2)*0.5,(i-1)/m*2*pi+pi/4,1) + [3.5,3.5,0];
%     CBots(:,i) = threeDPoint(1,(i-1)/m*2*pi,-1);
    As(:,i) = threeDPoint(sqrt(2)*1.5,(i-1)/m*2*pi+pi/4,0) + [3.5,3.5,0];
    B1s(:,i) = rot(pi/2)^(i-1) * [1.5; 0.5;0] + [3.5;3.5;0];
    B2s(:,i) = rot(pi/2)^(i-1) * [0.5; 1.5;0] + [3.5;3.5;0];
end

Bs = cat(2,reshape(B1s,3,1,m),reshape(B2s,3,1,m));

figure;
%plot CTop patches
for i = 1:m
    CTopPatch = getBicubicPatchIndex(i,As,Bs,Cs);
%     patch(:,3,3) = rot(pi)*patch(:,3,3);
    [xx,yy,zz]=bezier(CTopPatch,0.05);
    surf(xx,yy,zz)
    hold on;
end
plotPoints(CTopPatch);
pause;

vertexMatrix = zeros(3,6,6);

for i_ind = 1:6
    for j_ind = 1:6
        vertexMatrix(:,i_ind,j_ind) = [i_ind,j_ind,0];
    end
end
for i = 1:4
    vertexMatrix(:,round(As(1,i)),round(As(2,i))) = As(:,i);
    vertexMatrix(:,round(Cs(1,i)),round(Cs(2,i))) = Cs(:,i);
%     vertexMatrix(:,8-3*(i<4) - 3*(i>1) ,5-3*(i>2)) = As(:,i);
%     vertexMatrix(:,5-(i<4) - (i>1),4-(i>2)) = Cs(:,i);
    vertexMatrix(:,round(B1s(1,i)),round(B1s(2,i))) = B1s(:,i);
    vertexMatrix(:,round(B2s(1,i)),round(B2s(2,i))) = B2s(:,i);
end



AControlPoints = zeros(3,3,3);

%plot A patches
for i_ind = 2:5
    for j_ind = 2:5
        if(((i_ind ~= 3) && (i_ind ~= 4)) || ((j_ind ~= 3) && (j_ind ~= 4)))
            controlPoints = vertexMatrix(:,(i_ind-1):(i_ind+1),(j_ind-1):(j_ind+1));
            APatch = getBiquadraticPatch(controlPoints);
            %     patch(:,3,3) = rot(pi)*patch(:,3,3);
            [xx,yy,zz]=bezier(APatch,0.05);
            surf(xx,yy,zz)
            pause;
            hold on;
        end
    end
end