function [face_Array,vertices_Array]= DualContouring(n)
%INSTANTIATION OF CELLS

%n=Grid resolution
num_points=n^2;
num_cells=(n-1)^2;

Cells=struct('points',zeros(num_cells,5),'vertex',zeros(num_cells,2),...
    'Right_Neighbour', zeros(num_cells,1),'Top_Neighbour',zeros(num_cells,1));

%Vertices of cube: Order from lower left edge in a counterclockwise fashion
i=1;
for j=1:n-1
    for k=1:n-1
        Cells.points(i,1)=i+(j-1);
        i=i+1;
    end
end
Cells.points(:,5)=Cells.points(:,1);

for i=1:num_cells
    Cells.points(i,2)=Cells.points(i,1)+1;
    Cells.points(i,4)=Cells.points(i,1)+n;
    Cells.points(i,3)=Cells.points(i,4)+1;
end

%Cells Neighbours

%RIGHT
i=1;
for j=1:n-1
    for k=1:n-2
    Cells.Right_Neighbour(i)=i+1;
    i=i+1;
    end
    i=i+1;
end

%UP

for i=1:num_cells-(n-1)
    Cells.Top_Neighbour(i)=i+(n-1);
end


%% Function Set Up

f=@(x,y) (x-3)^2+(y-3)^2-1.8;

%Assigning points

vertices=zeros(num_points,2);

X=linspace(1,5,n);
Y=linspace(1,5,n);
[Y,X]=meshgrid(X,Y);
vertices(:,1)=reshape(X,[num_points,1]);
vertices(:,2)=reshape(Y,[num_points,1]);

%Sign values

cube_signs=zeros(num_points,1);
for i=1:num_points
    if (f(vertices(i,1),vertices(i,2))<0) 
        cube_signs(i)=1;
    end
end


% Dual Contouring 

% Finding the central vertix per cell


for i=1:num_cells
    a=[];
    for j=1:4
       if(cube_signs(Cells.points(i,j))~=cube_signs(Cells.points(i,j+1)))
           a=[a;mean([vertices(Cells.points(i,j),:);vertices(Cells.points(i,j+1),:)])];
       end
       if(~isempty(a))
       Cells.vertex(i,:)=mean(a);
       end
    end   
end


%Unite the edges
%First condition: neighbours with vertix different to zero!
%Second condition!: Only on the edges where there is change of sign!
face_Array=[];
counter=1;

for i=1:num_cells
   
    if (Cells.Right_Neighbour(i)~=0&&Cells.vertex(i,1)~=0)
        if(Cells.vertex(Cells.Right_Neighbour(i),1)~=0&&...
                                        cube_signs(Cells.points(i,2))~=cube_signs(Cells.points(i,3)))
            plot([Cells.vertex(i,1), Cells.vertex(Cells.Right_Neighbour(i),1)] ,...
                [ Cells.vertex(i,2), Cells.vertex(Cells.Right_Neighbour(i),2) ],'g')
            hold on
            face_Array(counter,1)=i;
            face_Array(counter,2)=i+1;
            counter=counter+1;
            
            
        end
    end
    
    if (Cells.Top_Neighbour(i)~=0&&Cells.vertex(i,1)~=0)
        if(Cells.vertex(Cells.Top_Neighbour(i),1)~=0&&...
                                        cube_signs(Cells.points(i,3))~=cube_signs(Cells.points(i,4)))
            plot([Cells.vertex(i,1), Cells.vertex(Cells.Top_Neighbour(i),1)] ,...
                [ Cells.vertex(i,2), Cells.vertex(Cells.Top_Neighbour(i),2) ],'g')
            hold on
            
            face_Array(counter,1)=i;
            face_Array(counter,2)=i+(n-1);
            counter=counter+1;
            
        end
    end
    
end

%plotting the points
% for i=1:num_points
%     if (cube_signs(i)==1)
%         plot(vertices(i,1),vertices(i,2),'r+')      
%     else
%         plot(vertices(i,1),vertices(i,2),'ko')
%     end
% end

axis([1 5 1 5])

vertices_Array=Cells.vertex();
% fv=struct('faces',zeros(size(face_Array)),'vertices',zeros(size(Cells.vertex)));
% fv.faces=face_Array;
% fv.vertices=Cells.vertex();
% 
% patch(fv,'EdgeColor','black','FaceColor','blue');

end


