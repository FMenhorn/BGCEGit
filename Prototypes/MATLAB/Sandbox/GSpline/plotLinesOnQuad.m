function figure_handle = plotLinesOnQuad(quad_list, quad_vertices, quad_index, figure_handle)
% 
% datapointsOnQuad = data_points(data_parameters(:,1) == quad_index,:);
% parametersOnQuad = data_parameters(data_parameters(:,1) == quad_index,:);
% 
% numPointsOnQuad = size(datapointsOnQuad,1);

thisQuadVertices = quad_list(quad_index,:);

% getQuadVector = @(corn1,corn2) quad_vertices(thisQuadVertices(corn2)) - quad_vertices(thisQuadVertices(corn1));

% botVec = getQuadVector(1,2);
% topVec = getQuadVector(4,3);
% leftVec = getQuadVector(1,4);
% rightVec = getQuadVector(2,3);
% quadOrigin = quad_vertices(thisQuadVertices(1));

lin_interp = @(u,vec1,vec2)  vec1 * (1-u) + (u) * vec2;
getPointOnQuad = @(u,v,p1,p2,p3,p4) lin_interp(v,lin_interp(u,p1,p2),lin_interp(u,p4,p3));
getPointOnThisQuad = @(u,v) getPointOnQuad(u,v,quad_vertices(thisQuadVertices(1),:),...
    quad_vertices(thisQuadVertices(2),:),...
    quad_vertices(thisQuadVertices(3),:),...
    quad_vertices(thisQuadVertices(4),:));

figure(figure_handle);
hold on;

% plots the face
%patch('Faces',thisQuadVertices,'Vertices',quad_vertices,'FaceColor', 'cyan', 'FaceAlpha', 0.5)%, 'BackFaceLighting', 'reverselit')
fill3(quad_vertices(thisQuadVertices(1,:),1), quad_vertices(thisQuadVertices(1,:),2), quad_vertices(thisQuadVertices(1,:),3), 'cyan', 'FaceAlpha', 0.3)

% 
% %plots the points and hairs
% for p = 1:numPointsOnQuad
%     pointOnQuad = getPointOnThisQuad(parametersOnQuad(p,2),parametersOnQuad(p,3));
% %     datapointsOnQuad(p,:)
%     plot3(datapointsOnQuad(p,1),datapointsOnQuad(p,2),datapointsOnQuad(p,3),'r.');
%     plot3(pointOnQuad(1),pointOnQuad(2),pointOnQuad(3),'b.');
%     plot3([datapointsOnQuad(p,1),pointOnQuad(1)],[datapointsOnQuad(p,2),pointOnQuad(2)],[datapointsOnQuad(p,3),pointOnQuad(3)],'k');
%     
%     
% end

%plot the lines

plotLine = @(point1,point2) plot3([point1(1),point2(1)],...
    [point1(2),point2(2)],...
    [point1(3),point2(3)],'k--');

for i = 1:3
    botPoint = getPointOnThisQuad(i*0.25,0);
    topPoint = getPointOnThisQuad(i*0.25,1);
    leftPoint = getPointOnThisQuad(0,i*0.25);
    rightPoint = getPointOnThisQuad(1,i*0.25);
    
    plotLine(botPoint,topPoint);
    plotLine(leftPoint,rightPoint);
    
end

hold off











end