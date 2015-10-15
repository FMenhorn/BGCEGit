close all
clear all
%X = [0 1 1 0];
%Y = [0 0 1 1];
[X1, Y1, Z1] = cylinder;

stride = size(X1,2);
vert = zeros(size(X1,2),3);
faces = zeros(size(X1, 2)-1, 4);

X = [X1(1, :) X1(2, :)];
Y = [Y1(1, :) Y1(2, :)];
Z = [Z1(1, :) Z1(2, :)];

n = 4;
alpha_f = 0.5;
alpha = alpha_f*(1 - cos(2*pi/n));
verts = [X' Y' Z'];
N = size(X1, 2);
for i=1:N-1
    faces(i, 1) = i;
    faces(i, 2) = i+1;
    faces(i, 3) = stride+i+1;
    faces(i, 4) = stride +i;
end

% faces_ids = [];
% for i=1:size(faces,1)
%     for j = 1:size(faces,2)
%         clear row column
%         [row, column] = find(faces_ids==faces(i, j));
%         for k = 1:length(row)
%             if (faces_ids(k, mod(column(k),2)+1) == faces(i, mod(j, n)+1))
%             end
%         end
% %         if (any(abs(faces_ids(:, 1) - faces(i, j))<10e-10) && any(abs(faces_ids(:, 2) - faces(i, mod(j, n)+1))<10e-10) )
% %             
% %         end
%         faces_ids = [faces_ids; [faces(i, j) faces(i, mod(j, n)+1)]];
%     end
% end
verts_new = zeros(4*N-4,3);
faces_new =  zeros(size(X1, 2)-1, 4);
for j=1:size(faces,1)
    X = verts(faces(j, :),1);
    Y = verts(faces(j, :),2);
    Z = verts(faces(j, :),3);
    F = [mean(X); mean(Y); mean(Z)];
    for k = 1:n
        verts_new(4*j - 3:4*j, 1) = (1 - alpha).*X + alpha.*F(1).*ones(1, length(X))';
        verts_new(4*j - 3:4*j, 2) = (1 - alpha).*Y + alpha.*F(2).*ones(1, length(X))';
        verts_new(4*j - 3:4*j, 3) = (1 - alpha).*Z + alpha.*F(3).*ones(1, length(X))';
    end
    faces_new(j, :) = 4*j-3:4*j;
end
patch('Faces', faces_new, 'Vertices', verts_new, 'FaceColor', 'b');
% X_new = [];
% Y_new = [];
% Z_new = [];
% for i = 1:N
%     X = [X1(1, i:i+1) X1(2, i+1) X1(2, i)];
%     Y = [Y1(1, i:i+1) Y1(2, i+1) Y1(2, i)];
%     Z = [Z1(1, i:i+1) Z1(2, i+1) Z1(2, i)];
%     F = [mean(X); mean(Y); mean(Z)];
%     x_temp = (1 - alpha).*X + alpha*F(1).*ones(1, length(X));
%     y_temp = (1 - alpha).*Y + alpha*F(2).*ones(1, length(X));
%     z_temp = (1 - alpha).*Z + alpha*F(3).*ones(1, length(X));
%     X_new = [X_new x_temp];
%     Y_new = [Y_new y_temp];
%     Z_new = [Z_new z_temp];
% end

%plot(X, Y, X_new, Y_new);
%surf(X_new, Y_new, Z_new);