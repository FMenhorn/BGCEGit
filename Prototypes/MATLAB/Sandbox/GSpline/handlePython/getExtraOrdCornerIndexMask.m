function indexMask = getExtraOrdCornerIndexMask(quad_list,AVertexList,B1VertexList,B2VertexList,CVertexList,quad_control_point_indices,quad_index,whichCorner)

mod_index = @(i,modul) mod(i-1,modul) + 1;
shifted_indices = @(ind,modul) mod_index((0:(modul-1)) + ind,modul);
reverse_shifted_indices = @(ind,modul) mod_index(((modul):-1:1) + ind,modul);

cornerVertexIndex = quad_list(quad_index,whichCorner);
numberOfEdges = getNumOfEdgesMeetingMatlab(AVertexList,cornerVertexIndex);
quadLocalIndex = find(AVertexList(cornerVertexIndex,:,2) == quad_index);
if(checkB1B2Reversal_opt(B1VertexList,quad_list,quad_index,cornerVertexIndex,quad_control_point_indices))
    %if mirrored in comparison with list, reverse B1 and B2
    if(checkB1B2OrientationReversal(B2VertexList,B1VertexList,quad_list,quad_index,cornerVertexIndex))
        aroundcorner_indices = reverse_shifted_indices(quadLocalIndex,numberOfEdges);
    else
        aroundcorner_indices = shifted_indices(quadLocalIndex,numberOfEdges);
    end
    B1Indices = B2VertexList(cornerVertexIndex,aroundcorner_indices,1);
    B2Indices = B1VertexList(cornerVertexIndex,aroundcorner_indices,1);
    
else
    if(checkB1B2OrientationReversal(B1VertexList,B2VertexList,quad_list,quad_index,cornerVertexIndex))
        aroundcorner_indices = reverse_shifted_indices(quadLocalIndex,numberOfEdges);
    else
        aroundcorner_indices = shifted_indices(quadLocalIndex,numberOfEdges);
    end
    B1Indices = B1VertexList(cornerVertexIndex,aroundcorner_indices,1);
    B2Indices = B2VertexList(cornerVertexIndex,aroundcorner_indices,1);
end
AIndices = AVertexList(cornerVertexIndex,aroundcorner_indices,1);
CIndices = CVertexList(cornerVertexIndex,aroundcorner_indices,1);
indexMask = [AIndices(:)';B1Indices(:)';B2Indices(:)';CIndices(:)'];
end
%         coefsRawTemp(1,1:numberOfEdges,:,:) = ACoefsRaw(numberOfEdges,1:numberOfEdges,:,:);
%         coefsRawTemp(2,1:numberOfEdges,:,:) = B1CoefsRaw(numberOfEdges,1:numberOfEdges,:,:);
%         coefsRawTemp(3,1:numberOfEdges,:,:) = B2CoefsRaw(numberOfEdges,1:numberOfEdges,:,:);
%         coefsRawTemp(4,1:numberOfEdges,:,:) = CCoefsRaw(numberOfEdges,1:numberOfEdges,:,:);
%
%         patchCoefsMatrix = getBicubicBezierPointCoefs(localCoords,coefsRawTemp(:,1:numberOfEdges,:,:));
%         coefsMatrix(p,AIndices) = patchCoefsMatrix(1,:);
%         coefsMatrix(p,B1Indices) = patchCoefsMatrix(2,:);
%         coefsMatrix(p,B2Indices) = patchCoefsMatrix(3,:);
%         coefsMatrix(p,CIndices) = patchCoefsMatrix(4,:);