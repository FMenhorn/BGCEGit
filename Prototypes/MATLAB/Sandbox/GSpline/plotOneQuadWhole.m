function plotHandle = plotOneQuadWhole(quad_list,AVertexList,B1VertexList,B2VertexList,CVertexList,quad_control_point_indices,control_points,quad_index,plotHandle)

whichCornerList = [1,4;2,3];

one4toone2 = @(i) (i-1)/3 + 1;

whichCornerFun = @(i,j) whichCornerList(one4toone2(i),one4toone2(j));

controlVertices = zeros(3,3,3);


figure(plotHandle);
% = figure('Name', 'Bezier surface plot');
hold on;
q = quad_index;
for j = 1:4
    for i = 1:4
        
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
            [xx,yy,zz]=bezier(patch,0.1);
            surf(xx,yy,zz)
            
            
        else
            neighbourMask = get3x3ControlPointIndexMask(quad_list,quad_control_point_indices,q,[i,j]);
            for bezierJ = 1:3
                for bezierI = 1:3
                    controlVertices(:,bezierI,bezierJ) = control_points(neighbourMask(bezierI,bezierJ),:);
                end
            end
            
            APatch = getBiquadraticPatch(controlVertices);
            %     patch(:,3,3) = rot(pi)*patch(:,3,3);
            [xx,yy,zz]=bezier(APatch,0.1);
            surf(xx,yy,zz)
            
            
            
        end
        
        
        
    end
end

end





