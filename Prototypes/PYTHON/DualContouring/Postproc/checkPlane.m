quads = dlmread('quadsMATLAB.csv',';');
verts = dlmread('vertsMATLAB.csv',';');

for i = 1:size(quads,1)
    quad = quads(i,:);
    P=verts(quad,:);
    C=zeros(3);
    for j = 2:4
        C(j-1,:)=P(j,:)-P(1,:);
    end
    %if(rank(C)==3)
        %det(C)/norm(C)
        norm(C)
    %end
end