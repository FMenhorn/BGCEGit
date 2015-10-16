function [vertices_refined, faces_refined, colours] = DooSabin(vertices, faces, alpha)
%%function performs 1 refinement using Doo-Sabin algorithm

%determine the number of vertices of our faces
n = size(faces,2);

temp = 0;
weird_edges = [];
%Determine the number of points
N = size(vertices, 1);

%Create the arrays for the refined grid
vertices_refined = [];
faces_refined = [];

edges = [];
counter = 0;
colours = [];
n = 3;
%create an array  of edges
for i = 1:size(faces,1)
    if (nnz(faces(i, :)) > n)
        n = nnz(faces(i, :));
    end
    n_local = nnz(faces(i, :));
    if (size(edges,1) == 0)
        for j=0:n_local - 1
            new_edge = [faces(i, j+1) faces(i, mod(j+1,n_local-1)+1)];
            counter = counter + 1;
            edges(counter,:) = new_edge;
        end
    else
        for j=0:n_local - 1
            new_edge = [faces(i, j+1) faces(i, mod(j+1,n_local)+1)];
            ind1 = find(edges(:,1) == new_edge(1));
            ind2 = find(edges(:,2) == new_edge(1));
            if ((size(find(edges(ind1, 2) == new_edge(2)),1) == 0) || (size(find(edges(ind1, 2) == new_edge(2)),2) == 0)) && ...
                    ((size(find(edges(ind2, 1) == new_edge(2)),1) == 0) || (size(find(edges(ind2, 1) == new_edge(2)),2) == 0)) ...
                    && (isempty(find(new_edge == 0, 1)))
                counter = counter+1;
                edges(counter,:) = new_edge;
            end     
        end
    end
end
size(edges, 1)
verts_children = zeros(N, 7);%[]; %zeros(N, 4);
verts_children_faces = zeros(N, 7);
edges_children = zeros(size(edges,1), 4);
%verts_children = [];
%edges_children = [];
counter = 1;
%Loop through faces
for j=1:size(faces,1)
    
    %Determine the coordinates of current face vertices
    n_local = nnz(faces(j, :));
    X = vertices(faces(j, 1:n_local),1);
    Y = vertices(faces(j, 1:n_local),2);
    Z = vertices(faces(j, 1:n_local),3);
    
    %Find the centroid of the current face
    F = [mean(X); mean(Y); mean(Z)];
    
    %loop through vertices of the current face and create their children 
%     vertices_refined(n_local*j - n_local + 1:n_local*j, 1) = (1 - alpha).*X + alpha.*F(1).*ones(1, length(X))';
%     vertices_refined(n_local*j - n_local + 1:n_local*j, 2) = (1 - alpha).*Y + alpha.*F(2).*ones(1, length(X))';
%     vertices_refined(n_local*j - n_local + 1:n_local*j, 3) = (1 - alpha).*Z + alpha.*F(3).*ones(1, length(X
    
    vertices_refined(counter:counter+n_local-1, 1) = (1 - alpha).*X + alpha.*F(1).*ones(1, length(X))';
    vertices_refined(counter:counter+n_local-1, 2) = (1 - alpha).*Y + alpha.*F(2).*ones(1, length(X))';
    vertices_refined(counter:counter+n_local-1, 3) = (1 - alpha).*Z + alpha.*F(3).*ones(1, length(X))';
    
    for k = 0:n_local-1

        ind = 1;
        if size(verts_children,1) ~= 0
            while (verts_children(faces(j,k+1), ind) ~= 0 )
                ind = ind+1;
            end
        end
        verts_children(faces(j, k+1), ind) = counter+k;
        verts_children_faces(faces(j, k+1), ind) = j;
    end
    for k = 0:n_local-1
        clear ind1 ind2
        current_edge = [faces(j, k+1) faces(j, mod(k+1,n)+1)];
        ind1 = find(edges(:,1) == current_edge(1));
        ind2 = find(edges(:,2) == current_edge(1));
      
        if (size(find(edges(ind1, 2) == current_edge(2)),1) == 0 ) || (size(find(edges(ind1, 2) == current_edge(2)),2) == 0 )
            current_edge_id =  ind2(find(edges(ind2, 1) == current_edge(2)));
        else
            current_edge_id = ind1(find(edges(ind1, 2) == current_edge(2)));
        end
        
        ind = 1;
      %  current_edge_id
        while (edges_children(current_edge_id, ind) ~= 0 )
            ind = ind+1;
        end
        edges_children(current_edge_id, ind) = counter + k;
        edges_children(current_edge_id, ind+1) = counter + mod(k+1,n_local);
        
    end
    
    %add the face formed by children vertices of the old face j
    faces_refined(j, 1:n_local) = counter:counter + n_local - 1;
    counter = counter + n_local;
    colours(j) = 1;
end
%verts_children

%loop through old vertices
counter = size(faces_refined,1);
for i = 1:N

    new_face = verts_children(i, (1:nnz(verts_children(i, :))));
    neighbouring_faces = verts_children_faces(i, (1:nnz(verts_children_faces(i, :))));
    face_ordered = [new_face(1)];
    if (length(new_face) >= 3)
        %find the face adjacent to the face, containing the first child
        k = 1;
        for iter = 1:length(new_face)-1

            for j = 1:length(neighbouring_faces)
                %bad smell. this check is false when we compare the face to
                %itsel. In the final version there shouldn't be any
                %comparissons with itself at all, of course
              
                if (length(intersect(faces(neighbouring_faces(k),1:nnz(faces(neighbouring_faces(k),:))),faces(neighbouring_faces(j),1:nnz(faces(neighbouring_faces(j),:))))) == 2) && (isempty(find(face_ordered == new_face(j))))
                    face_ordered = [face_ordered, new_face(j)];
                    k = j;
                end
                iter = iter + 1;
            end

        end
        counter = counter + 1;
        faces_refined(counter,1:length(new_face)) = face_ordered;
        colours(counter) = 2;
    end
    
    
%     X = vertices_refined(new_face, 1)';
%     Y = vertices_refined(new_face, 2)';
%     Z = vertices_refined(new_face, 3)';
%     if (length(new_face) >= 3)
%         new_face_ordered = convhull(X, Y, Z);
%         counter = counter + 1;
%         faces_refined = new_face(new_face_ordered);
%         colours(counter) = 2;
%     end
%     if (length(find(new_face)) == 4)
%         
%         vec1 = vertices_refined(new_face(2),:)-vertices_refined(new_face(1),:);
%         vec2 = vertices_refined(new_face(3),:)-vertices_refined(new_face(2),:);
%         vec3 = vertices_refined(new_face(4),:)-vertices_refined(new_face(3),:);
%         
%         normal_1 = cross(vec1, vec2);
%         normal_2 = cross(vec2, vec3);
%         if (sum(normal_1.*normal_2) < 0)
%             temp = new_face(3);
%             new_face(3) = new_face(4);
%             new_face(4) = temp;
%         end
%          counter = counter + 1;
%     
%         faces_refined(counter,:) = new_face;
%         colours(counter) = 2;
%     end
end

%loop through old edges
counter = size(faces_refined, 1);
for i=1:size(edges, 1)
    new_face = edges_children(i, 1:length(find(edges_children(i,:))));
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
    
        faces_refined(counter,1:4) = new_face;
        colours(counter) = 3;
    end
     if (length(find(new_face)) == 3)
    
        faces_refined(counter,1:3) = new_face;
        colours(counter) = 3;
    end
end
end