function indexMask = get3x3ControlPointIndexMask(quad_list, quad_control_point_indices, quad_index, localIndexXY)

indexMask = zeros(3,3);

localX = localIndexXY(1);
localY = localIndexXY(2);

local_control_point_indices = [1,2,3,4;5,6,7,8;9,10,11,12;13,14,15,16]';
maskMinX = 1;
maskMaxX = 3;
maskMinY = 1;
maskMaxY = 3;
if(localX == 1)
    neighbourEdge = quad_list(quad_index,[1,4]);
    neighbourIndex = getNeighbourSharedEdge(quad_list,quad_index,neighbourEdge(1),neighbourEdge(2));
    indexMask(1,:) = getCellsAlongEdge(quad_list,quad_control_point_indices,neighbourIndex,neighbourEdge(1),neighbourEdge(2),...
        (localY-1):(localY+1));
    maskMinX = 2;
elseif(localX == 4)
    neighbourEdge = quad_list(quad_index,[2,3]);
    neighbourIndex = getNeighbourSharedEdge(quad_list,quad_index,neighbourEdge(1),neighbourEdge(2));
    indexMask(3,:) = getCellsAlongEdge(quad_list,quad_control_point_indices,neighbourIndex,neighbourEdge(1),neighbourEdge(2),...
        (localY-1):(localY+1));
    maskMaxX = 2;
elseif(localY == 1)
    neighbourEdge = quad_list(quad_index,[1,2]);   
    neighbourIndex = getNeighbourSharedEdge(quad_list,quad_index,neighbourEdge(1),neighbourEdge(2));
    indexMask(:,1) = getCellsAlongEdge(quad_list,quad_control_point_indices,neighbourIndex,neighbourEdge(1),neighbourEdge(2),...
        (localX-1):(localX+1));
    maskMinY = 2;
elseif(localY == 4)
    neighbourEdge = quad_list(quad_index,[4,3]);
    neighbourIndex = getNeighbourSharedEdge(quad_list,quad_index,neighbourEdge(1),neighbourEdge(2));
    indexMask(:,3) = getCellsAlongEdge(quad_list,quad_control_point_indices,neighbourIndex,neighbourEdge(1),neighbourEdge(2),...
        (localX-1):(localX+1));
    maskMaxY = 2;
end
minX = localX-2+maskMinX;
maxX = localX-2+maskMaxX;
minY = localY-2+maskMinY;
maxY = localY-2+maskMaxY;

for j = maskMinY:maskMaxY
    for i = maskMinX:maskMaxX
        % local_control_indices = local_control_point_indices((minX):(maxX),(minY):(maxY));
        indexMask(i,j) = ...
            quad_control_point_indices(quad_index,local_control_point_indices(localX-2+i,localY-2+j));
    end
end




end