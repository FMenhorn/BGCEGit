
quad_list = quads_Torus;
quad_control_points = regularPoints;
quad_vertex_points = torus_verts_coarse;
dataPoints = newPoints;
parameterPoints = newParams;
APoints = A;
B1Points = B1;
B2Points = B2;
CPoints = C;
coef_matrix = coefs;
numParameters = size(dataPoints,1);
color_inactive_control_point = [0.8,.8,.8];
color_inactive_vertex_point = [0.4,.4,.4];
hold on;

for index = 1:length(quad_control_points(:));
    thisPoint = getVertexOnQuad(quad_list,quad_vertex_points,quad_control_points,quad_control_points(index));
    scatter3(thisPoint(1),thisPoint(2),thisPoint(3),'MarkerEdgeColor',color_inactive_control_point);
    
end
for index = 1:size(quad_vertex_points,1);
    thisPoint = quad_vertex_points(index,:);
    scatter3(thisPoint(1),thisPoint(2),thisPoint(3),'MarkerEdgeColor',color_inactive_vertex_point);
    
end
pause

for p = 1:numParameters
    quad_index = parameterPoints(p,1);
    thisQuadVertices = quad_vertex_points(quad_list(quad_index,:),:);
    theDataPoint = dataPoints(p,:);
    scatter3(theDataPoint(:,1),theDataPoint(:,2),theDataPoint(:,3),...
        'MarkerEdgeColor','r');
    
    scatter3(thisQuadVertices(:,1),thisQuadVertices(:,2),thisQuadVertices(:,3),...
        'MarkerEdgeColor',[0.0 .5 .0]);

    theVertexPoints = find(coef_matrix(p,:));
    
    for i = 1:length(theVertexPoints)
        pointColor = 1-coef_matrix(p,theVertexPoints(i));
        theVertexPoint = getVertexOnQuad(quad_list,quad_vertex_points,quad_control_points,theVertexPoints(i));
        scatter3(theVertexPoint(:,1),theVertexPoint(:,2),theVertexPoint(:,3),...
        'MarkerEdgeColor',[pointColor/2 pointColor/2 1],...
        'MarkerFaceColor',[pointColor/2 pointColor/2 1]);
    end
    pause
    
    scatter3(theDataPoint(:,1),theDataPoint(:,2),theDataPoint(:,3),...
        'MarkerEdgeColor',[1 1 1]);
    for i = 1:length(theVertexPoints)
        theVertexPoint = getVertexOnQuad(quad_list,quad_vertex_points,quad_control_points,theVertexPoints(i));
        scatter3(theVertexPoint(:,1),theVertexPoint(:,2),theVertexPoint(:,3),...
        'MarkerEdgeColor',color_inactive_control_point,...
        'MarkerFaceColor',[1 1 1]);
    end
     scatter3(thisQuadVertices(:,1),thisQuadVertices(:,2),thisQuadVertices(:,3),...
        'MarkerEdgeColor',color_inactive_vertex_point);
%     pause;
%     scatter3(thisQuadVertices(:,1),thisQuadVertices(:,2),thisQuadVertices(:,3),...
%         'MarkerEdgeColor','b',...
%         'MarkerFaceColor','b');
%     scatter3(thisQuadsDataPoint(:,1),thisQuadsDataPoint(:,2),thisQuadsDataPoint(:,3),...
%         'MarkerEdgeColor','b');
end