function coefsMatrix = createFairnessControlMeshCoefs(quad_list,AVertexList,B1VertexList,B2VertexList,CVertexList,quad_control_point_indices)

% takes the list of N quads, the corner points and the connectivity
% information and spits out the fairness coefficients as an
% (N*16*3)x(N*16) matrix.

N = size(quad_control_point_indices,1)*size(quad_control_point_indices,2)*3;
M = size(quad_control_point_indices,1)*size(quad_control_point_indices,2);
coefsMatrix = zeros(N,M);

%precalculate the coefficients between all the vertex control points and
%the bezier control points for 7 different number of intersecting
%edges as a start

%(number of incoming edges(between 3 an 7 hardcoded), [A,B1,B2,C], [in which quad 1-7], bezier point
%first coord, bezier point second coord)
extraOrdinaryCoefsRaw = zeros(7,4,7,4,4);
ordinaryCoefsRaw = zeros(3,3,3,3);
ACoefsRaw = zeros(7,7,4,4);
B1CoefsRaw = zeros(7,7,4,4);
B2CoefsRaw = zeros(7,7,4,4);
CCoefsRaw  = zeros(7,7,4,4);
for i = 3:7
    [ACoefsRaw(i,1:i,:,:),...
        B1CoefsRaw(i,1:i,:,:),...
        B2CoefsRaw(i,1:i,:,:),...
        CCoefsRaw(i,1:i,:,:)] = ...
        createBicubicCoefMatrices(i);
end

%also for ordinary patches
for bezierI = 1:3
    for bezierJ = 1:3
        ordinaryCoefsRaw(:,:,bezierI,bezierJ) = getBiquadraticPatchCoefs(bezierI,bezierJ);
    end 
end



mod_index = @(i,modul) mod(i-1,modul) + 1;
shifted_indices = @(ind,modul) mod_index((0:(modul-1)) + ind,modul);
reverse_shifted_indices = @(ind,modul) mod_index(((modul):-1:1) + ind,modul);


coefsRawTemp = zeros(4,7,4,4);

%The precalculated fairness coefficients on the bezier points
uu2mat = [2 2 2;-4 -4 -4;2 2 2]/3;
vv2mat = uu2mat';
uv2mat = [1 0 -1;0 0 0;-1 0 1];

uu3mat = [3 3 3 3;-3 -3 -3 -3;-3 -3 -3 -3;3 3 3 3]/4;
vv3mat = uu3mat';
uv3mat = [1 0 0 -1;0 0 0 0;0 0 0 0;-1 0 0 1];

biqBezCoefs = cat(3,uu2mat,2*uv2mat,vv2mat);
bicBezCoefs = cat(3,uu3mat,2*uv3mat,vv3mat);


whichCornerList = [1,4;2,3];

one4toone2 = @(i) (i-1)/3 + 1;

whichCornerFun = @(i,j) whichCornerList(one4toone2(i),one4toone2(j));
% controlVertices = zeros(3,3,3);
p = 1;
for q = 1:size(quad_list,1)
    for j = 1:4
        for i = 1:4
    
            if ([i,j]==1 | [i,j] == 4)
                whichCorner = whichCornerFun(i,j);
                indexMask = getExtraOrdCornerIndexMask(quad_list,AVertexList,B1VertexList,B2VertexList,CVertexList,quad_control_point_indices,q,whichCorner);
                numberOfEdges = size(indexMask,2);
%                 As =  quad_control_point_indices(indexMask(1,:),:)';
%                 B1s =  quad_control_point_indices(indexMask(2,:),:)';
%                 B2s =  quad_control_point_indices(indexMask(3,:),:)';
%                 Cs =  quad_control_point_indices(indexMask(4,:),:)';
%                 Bs = cat(2,reshape(B1s,3,1,numberOfEdges),reshape(B2s,3,1,numberOfEdges));
                
                coefsRawTemp(1,1:numberOfEdges,:,:) = ACoefsRaw(numberOfEdges,1:numberOfEdges,:,:);
                coefsRawTemp(2,1:numberOfEdges,:,:) = B1CoefsRaw(numberOfEdges,1:numberOfEdges,:,:);
                coefsRawTemp(3,1:numberOfEdges,:,:) = B2CoefsRaw(numberOfEdges,1:numberOfEdges,:,:);
                coefsRawTemp(4,1:numberOfEdges,:,:) = CCoefsRaw(numberOfEdges,1:numberOfEdges,:,:);
                
                
                for matType = 1:3
                    bezier_points = squeeze(bicBezCoefs(:,:,matType));
                    patchCoefsMatrix = getPetersControlPointCoefs(bezier_points,coefsRawTemp(:,1:numberOfEdges,:,:));
                    %         coefsMatrix(p,AIndices) = patchCoefsMatrix(1,:);
                    %         coefsMatrix(p,B1Indices) = patchCoefsMatrix(2,:);
                    %         coefsMatrix(p,B2Indices) = patchCoefsMatrix(3,:);
                    %         coefsMatrix(p,CIndices) = patchCoefsMatrix(4,:);
                    coefsMatrix(p,indexMask(:)) = patchCoefsMatrix(:);
                    p = p+1;
                end

%                 patch = getBicubicPatchIndex(1,As,Bs,Cs);
%                     patch(:,3,3) = rot(pi)*patch(:,3,3);
%                 [xx,yy,zz]=bezier(patch,0.1);
%                 surf(xx,yy,zz)
                
                
            else
                neighbourMask = get3x3ControlPointIndexMask(quad_list,quad_control_point_indices,q,[i,j]);
                
                %                 for bezierJ = 1:3
                %                     for bezierI = 1:3
                %                         controlVertices(:,bezierI,bezierJ) = control_points(neighbourMask(bezierI,bezierJ),:);
                %                     end
                %                 end
                %
                for matType = 1:3
                    bezier_points = squeeze(biqBezCoefs(:,:,matType));
                    ordinaryPatchCoefsMatrix = getPetersControlPointCoefs(bezier_points,ordinaryCoefsRaw);
                    
                    
                    coefsMatrix(p,neighbourMask(:)) = ordinaryPatchCoefsMatrix(:);
                    p = p+1;
                end
%                 
%                 
%                 APatch = getBiquadraticPatch(controlVertices);
%                     patch(:,3,3) = rot(pi)*patch(:,3,3);
%                 [xx,yy,zz]=bezier(APatch,0.1);
%                 surf(xx,yy,zz)
                
                
                
            end
            
            
            
        end
    end
    
end


end