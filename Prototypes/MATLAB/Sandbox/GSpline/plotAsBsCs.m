

mod_index = @(i,modul) mod(i-1,modul) + 1;

quad_list = quads_Torus;
quad_control_points = regularPoints;
quad_vertex_points = torus_verts_coarse;
dataPoints = newPoints;
parameterPoints = newParams;
APoints = newA;
B1Points = newB1;
B2Points = newB2;
CPoints = newC;

numQuads = size(quad_list,1);

scatter3(quad_vertex_points(:,1),quad_vertex_points(:,2),quad_vertex_points(:,3),...
        'MarkerEdgeColor','k');
hold on;

for q = 1:numQuads
    thisQuadVertices = quad_vertex_points(quad_list(q,:),:);
    thisQuadsVertexIndices = quad_list(q,:);
    thisQuadsDataPoints = dataPoints(parameterPoints(:,1) == q,:);
    hold on;
    scatter3(thisQuadVertices(:,1),thisQuadVertices(:,2),thisQuadVertices(:,3),...
        'MarkerEdgeColor','r');
    for i = 1:4
        
        thisVertexIndex = thisQuadsVertexIndices(i);
        scatter3(quad_vertex_points(thisVertexIndex,1),quad_vertex_points(thisVertexIndex,2),quad_vertex_points(thisVertexIndex,3),...
        'MarkerEdgeColor','r',...
        'MarkerFaceColor','r');
        thisQuadLocalIndex = find(APoints(thisVertexIndex,:,2) == q);
        scatter3(thisQuadVertices(i,1),thisQuadVertices(i,2),thisQuadVertices(i,3));
        m = getNumOfEdgesMeetingMatlab(APoints,thisVertexIndex);
        for k = 1:m
            
            
            currentAPoint = getVertexOnQuad(...
                quad_list,quad_vertex_points,quad_control_points,APoints(thisVertexIndex,mod_index(thisQuadLocalIndex-1+k,m),1));
            currentB1Point = getVertexOnQuad(...
                quad_list,quad_vertex_points,quad_control_points,B1Points(thisVertexIndex,mod_index(thisQuadLocalIndex-1+k,m),1));
            currentB2Point = getVertexOnQuad(...
                quad_list,quad_vertex_points,quad_control_points,B2Points(thisVertexIndex,mod_index(thisQuadLocalIndex-1+k,m),1));
            currentCPoint = getVertexOnQuad(...
                quad_list,quad_vertex_points,quad_control_points,CPoints(thisVertexIndex,mod_index(thisQuadLocalIndex-1+k,m),1));
            scatter3(currentAPoint(:,1),currentAPoint(:,2),currentAPoint(:,3),'MarkerEdgeColor','g');
            scatter3(currentB1Point(:,1),currentB1Point(:,2),currentB1Point(:,3),'MarkerEdgeColor',[1,0,1]);
            scatter3(currentB2Point(:,1),currentB2Point(:,2),currentB2Point(:,3),'MarkerEdgeColor','y');
            scatter3(currentCPoint(:,1),currentCPoint(:,2),currentCPoint(:,3),'MarkerEdgeColor',[0,.75,.75]);
            pause;
            scatter3(currentAPoint(:,1),currentAPoint(:,2),currentAPoint(:,3),'MarkerEdgeColor','b');
            scatter3(currentB1Point(:,1),currentB1Point(:,2),currentB1Point(:,3),'MarkerEdgeColor','b');
            scatter3(currentB2Point(:,1),currentB2Point(:,2),currentB2Point(:,3),'MarkerEdgeColor','b');
            scatter3(currentCPoint(:,1),currentCPoint(:,2),currentCPoint(:,3),'MarkerEdgeColor','b');
            
        end
        scatter3(quad_vertex_points(thisVertexIndex,1),quad_vertex_points(thisVertexIndex,2),quad_vertex_points(thisVertexIndex,3),...
        'MarkerEdgeColor','b',...
        'MarkerFaceColor','b');
        
        
    end
    scatter3(thisQuadVertices(:,1),thisQuadVertices(:,2),thisQuadVertices(:,3),...
        'MarkerEdgeColor','b');
%     scatter3(thisQuadsDataPoints(:,1),thisQuadsDataPoints(:,2),thisQuadsDataPoints(:,3),...
%         'MarkerEdgeColor','r');
%     pause;
%     scatter3(thisQuadVertices(:,1),thisQuadVertices(:,2),thisQuadVertices(:,3),...
%         'MarkerEdgeColor','b',...
%         'MarkerFaceColor','b');
%     scatter3(thisQuadsDataPoints(:,1),thisQuadsDataPoints(:,2),thisQuadsDataPoints(:,3),...
%         'MarkerEdgeColor','b');
end