function [patch3 patch4 patch5 patch6] = visualisation(patch, verts_new)
    sizes = [];
    for i=1:size(patch,1)
        if isempty(find(sizes == length(find(patch(i, :)))))
            sizes = [sizes length(find(patch(i, :)))];
        end
    end
    patch3 = [];
    patch4 = [];
    patch5 = [];
    patch6 = [];
    for i=1:size(patch,1)
        if (length(find(patch(i,:))) == 3)
            patch3 = [patch3; patch(i, (1:nnz(patch(i,:))))];
        end
        if (length(find(patch(i,:))) == 4)
            patch4 = [patch4; patch(i, (1:nnz(patch(i,:))))];
        end
        if (length(find(patch(i,:))) == 5)
            patch5 = [patch5; patch(i, (1:nnz(patch(i,:))))];
        end
        if (length(find(patch(i,:))) == 6)
            patch6 = [patch6; patch(i, (1:nnz(patch(i,:))))];
        end
    end
%     size(patch3)
%     %patch3
%     size(verts_new)
%     patch3(1:10, :)
% %     figure
% %     hold on
% %     patch('Faces', patch3, 'Vertices', verts_new);
% %     patch('Faces', patch4, 'Vertices', verts_new);
% %     patch('Faces', patch5, 'Vertices', verts_new);
% %     patch('Faces', patch6, 'Vertices', verts_new);
%     res = patch3;

end