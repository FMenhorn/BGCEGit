function pointLocation = getVertexOnQuad(quad_list,quad_vertex_points,quad_control_points,control_point_index)




[quad_index,control_point_local_index] = find(quad_control_points == control_point_index);

thisQuadVertices = quad_vertex_points(quad_list(quad_index,:),:);
xVector = thisQuadVertices(2,:) - thisQuadVertices(1,:);
yVector = thisQuadVertices(4,:) - thisQuadVertices(1,:);

x = mod(control_point_local_index-1,4);
y = (control_point_local_index-x)/4;

pointLocation = thisQuadVertices(1,:) + (x + 0.5) * xVector/4 + (y + 0.5) * yVector/4;




end