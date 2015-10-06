function [  ] = plotMeshgrid( X,Y,Z )
%PLOTMESHGRID Summary of this function goes here
%   Detailed explanation goes here

hold on
for i = 1:size(X,3)
    for d = 1:3
        plot3(X(:,:,i),Y(:,:,i),Z(:,:,i),'k--')
        X=shiftdim(X,1);
        Y=shiftdim(Y,1);
        Z=shiftdim(Z,1);
    end
end
hold off


end

