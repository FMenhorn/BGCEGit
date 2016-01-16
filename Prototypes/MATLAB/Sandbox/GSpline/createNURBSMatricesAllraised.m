function [NURBSMatrix,NURBSIndices] = createNURBSMatricesAllraised(quad_list,AVertexList,B1VertexList,B2VertexList,CVertexList,quad_control_point_indices,control_points)

whichCornerList = [1,4;2,3];

one4toone2 = @(i) (i-1)/3 + 1;

whichCornerFun = @(i,j) whichCornerList(one4toone2(i),one4toone2(j));

% 
% controlVertices = zeros(3,3,3);

number_of_quads = size(quad_list,1);
% counterBic = 1;
% counterBiq = 1;
% biquadtraticMatrix = zeros(12*9*number_of_quads,3);
% biquadraticIndices = zeros(12*number_of_quads,9);
% bicubicMatrix = zeros(4*16*number_of_quads,3);
% bicubicIndices = zeros(4*number_of_quads,16);
tempBiquadBezierMatrix = zeros(3,3,3);

NURBSMatrix = zeros(13*13*number_of_quads,3);
NURBSIndices = zeros(number_of_quads,13*13);



getLinearIndexing = @(i,j,width) i + (j-1)*width;
% hold on;
for q = 1:number_of_quads
    for j = 1:4
        for i = 1:4
            addToIndexI = i*3-3;
            addToIndexJ = j*3-3;
    
            if ([i,j]==1 | [i,j] == 4)
                whichCorner = whichCornerFun(i,j);
                indexMask = getExtraOrdCornerIndexMask(quad_list,AVertexList,B1VertexList,B2VertexList,CVertexList,quad_control_point_indices,q,whichCorner);
                numberOfEdges = size(indexMask,2);
                As =  control_points(indexMask(1,:),:)';
                B1s =  control_points(indexMask(2,:),:)';
                B2s =  control_points(indexMask(3,:),:)';
                Cs =  control_points(indexMask(4,:),:)';
                Bs = cat(2,reshape(B1s,3,1,numberOfEdges),reshape(B2s,3,1,numberOfEdges));
                patch = getBicubicPatchIndex(1,As,Bs,Cs);
                %     patch(:,3,3) = rot(pi)*patch(:,3,3);
                
                %shift the points to lie in the same order as the nurbs
                %patch: corner 3 is in the correct orientation, the next
                %(corner 4) needs to be rotated one 90deg rotation
                %clockwise, the next another one clockwise etc... 
                patch = rotateMatrixStructure(patch,whichCorner-3);
                
                for jPatch = 1:4
                    for iPatch = 1:4
%                         currentIndex = (counterBic -1)*16 + getLinearIndexing(iPatch,jPatch,4);%
%                         %
%                         bicubicMatrix(currentIndex,:) = patch(:,iPatch,jPatch);%
%                         bicubicIndices(counterBic,getLinearIndexing(iPatch,jPatch,4)) = currentIndex;%
                        
                        NURBScurrentIndex = (q-1)*13*13 + getLinearIndexing(iPatch+addToIndexI,jPatch+addToIndexJ,13);
                        NURBSMatrix(NURBScurrentIndex,:) = patch(:,iPatch,jPatch);
                        NURBSIndices(q,getLinearIndexing(iPatch+addToIndexI,jPatch+addToIndexJ,13)) = NURBScurrentIndex;
                        
                    end
                end
%                 counterBic = counterBic + 1;%
            else
                neighbourMask = get3x3ControlPointIndexMask(quad_list,quad_control_point_indices,q,[i,j]);
                
                for jPatch = 1:3
                    for iPatch = 1:3
                        
                        tempBiquadBezierMatrix(:,iPatch,jPatch) = control_points(neighbourMask(iPatch,jPatch),:);
                    end
                end
                
                tempBiquadBezierMatrix = getBiquadraticPatch(tempBiquadBezierMatrix);
                raisedBiquadMatrix = raiseDeg2D(tempBiquadBezierMatrix);
                
                for iPatch = 1:4
                    for jPatch = 1:4
                        NURBScurrentIndex = (q-1)*13*13 + getLinearIndexing(iPatch+addToIndexI,jPatch+addToIndexJ,13);
                        NURBSMatrix(NURBScurrentIndex,:) = raisedBiquadMatrix(:,iPatch,jPatch);
                        NURBSIndices(q,getLinearIndexing(iPatch+addToIndexI,jPatch+addToIndexJ,13)) = NURBScurrentIndex;
                    end
                    
                end
                
                
                
            end
            
            
            
        end
    end
    
end





end
