function [vertices_refined, faces_refined, colours] = DooSabin(vertices, faces, alpha)
%%function performs 1 refinement using Doo-Sabin algorithm

%determine the number of vertices of our faces
n = size(faces,2);

%Determine the number of points
N = size(vertices, 1);

%Create the arrays for the refined grid
vertices_refined = [];
faces_refined = [];

edges = [];
counter = 0;
colours = [];
%create an array  of edges
for i = 1:size(faces,1)
    if (size(edges,1) == 0)
        for j=0:3
            new_edge = [faces(i, j+1) faces(i, mod(j+1,4)+1)];
            counter = counter + 1;
            edges(counter,:) = new_edge;
        end
    else
        for j=0:3
            new_edge = [faces(i, j+1) faces(i, mod(j+1,4)+1)];
            ind1 = find(edges(:,1) == new_edge(1));
            ind2 = find(edges(:,2) == new_edge(1));
            if ((size(find(edges(ind1, 2) == new_edge(2)),1) == 0) || (size(find(edges(ind1, 2) == new_edge(2)),2) == 0)) && ((size(find(edges(ind2, 1) == new_edge(2)),1) == 0) || (size(find(edges(ind2, 1) == new_edge(2)),2) == 0))
                counter = counter+1;
                edges(counter,:) = new_edge;
            end     
        end
    end
end

edges(1,:);
verts_children = zeros(N, 4);
edges_children = zeros(size(edges,1), 4);

%Loop through faces
for j=1:size(faces,1)
    
    %Determine the coordinates of current face vertices
    X = vertices(faces(j, :),1);
    Y = vertices(faces(j, :),2);
    Z = vertices(faces(j, :),3);
    
    %Find the centroid of the current face
    F = [mean(X); mean(Y); mean(Z)];
    
    %loop through vertices of the current face and create their children
    vertices_refined(4*j - 3:4*j, 1) = (1 - alpha).*X + alpha.*F(1).*ones(1, length(X))';
    vertices_refined(4*j - 3:4*j, 2) = (1 - alpha).*Y + alpha.*F(2).*ones(1, length(X))';
    vertices_refined(4*j - 3:4*j, 3) = (1 - alpha).*Z + alpha.*F(3).*ones(1, length(X))';
    
    for k = 0:n-1

        ind = 1;
        while (verts_children(faces(j,k+1), ind) ~= 0 )
            ind = ind+1;
        end
        verts_children(faces(j, k+1), ind) = 4*j-3+k;
    end
    for k = 0:n-1
        clear ind1 ind2
        current_edge = [faces(j, k+1) faces(j, mod(k+1,4)+1)];
        ind1 = find(edges(:,1) == current_edge(1));
        ind2 = find(edges(:,2) == current_edge(1));
      
        if (size(find(edges(ind1, 2) == current_edge(2)),1) == 0 ) || (size(find(edges(ind1, 2) == current_edge(2)),2) == 0 )
            current_edge_id =  ind2(find(edges(ind2, 1) == current_edge(2)));
        else
            current_edge_id = ind1(find(edges(ind1, 2) == current_edge(2)));
        end
        ind = 1;
        
        while (edges_children(current_edge_id, ind) ~= 0 )
            ind = ind+1;
        end
        edges_children(current_edge_id, ind) = 4*j-3+k;
        edges_children(current_edge_id, ind+1) = 4*j -4 + mod(k+1,4) + 1;
        
    end
    
    %add the face formed by children vertices of the old face j
    faces_refined(j, :) = 4*j-3:4*j;
    colours(j) = 1;
end

%loop through old vertices
counter = size(faces,1);
for i = 1:N
    new_face = verts_children(i, :);
    if (length(find(new_face)) == 4)
        
        vec1 = vertices_refined(new_face(2),:)-vertices_refined(new_face(1),:);
        vec2 = vertices_refined(new_face(3),:)-vertices_refined(new_face(2),:);
        vec3 = vertices_refined(new_face(4),:)-vertices_refined(new_face(3),:);
        
        normal_1 = cross(vec1, vec2);
        normal_2 = cross(vec2, vec3);
        if (sum(normal_1.*normal_2) < 0)
            temp = new_face(3);
            new_face(3) = new_face(4);
            new_face(4) = temp;
        end
         counter = counter + 1;
    
        faces_refined(counter,:) = new_face;
        colours(counter) = 2;
    end
end

%loop through old edges
counter = size(faces_refined, 1);
for i=1:size(edges, 1)
    new_face = edges_children(i, :);
    if (length(find(new_face)) == 4)
        
        vec1 = vertices_refined(new_face(2),:)-vertices_refined(new_face(1),:);
        vec2 = vertices_refined(new_face(3),:)-vertices_refined(new_face(2),:);
        vec3 = vertices_refined(new_face(4),:)-vertices_refined(new_face(3),:);
        
        normal_1 = cross(vec1, vec2);
        normal_2 = cross(vec2, vec3);
        if (sum(normal_1.*normal_2) < 0)
            temp = new_face(3);
            new_face(3) = new_face(4);
            new_face(4) = temp;
        end
         counter = counter + 1;
    
        faces_refined(counter,:) = new_face;
        colours(counter) = 3;
    end
end
end