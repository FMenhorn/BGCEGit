function isReversed = checkB1B2Reversal_opt(B1,quad_list,quad_index,vertex_index,regularPoints)

isReversed = -1; %error!!

mod_index = @(i,modul) mod(i-1,modul) + 1;

B1s_this_vertex = reshape(B1(vertex_index,:,:),size(B1,2),size(B1,3));

quadNumberLocal = find(B1(vertex_index,:,2) == quad_index);
B1fromList = B1(vertex_index,quadNumberLocal,1);
thisQuad_cornerVertices = quad_list(quad_index,:);
whichQuadCorner = find(thisQuad_cornerVertices == vertex_index);
localB1s = [2 8 15 9] ;
localB2s = [5 3 12 14];
shouldBeB1 = regularPoints(quad_index,localB1s(whichQuadCorner));
shouldBeB2 = regularPoints(quad_index,localB2s(whichQuadCorner));



%in peter's scheme, and therefore in the parameters, B1 is the left one if
%looking into the quad corner. Since the quad corners go clockwise, that
%means the relevant quad corner and the one after should be
% shouldBeB1Edge = thisQuad_cornerVertices([whichQuadCorner,mod_index(whichQuadCorner+1,4)]);
% shouldBeB2Edge = thisQuad_cornerVertices([whichQuadCorner,mod_index(whichQuadCorner-1,4)]);

if (B1fromList == shouldBeB1)
    isReversed = 0;
elseif(shouldBeB2 == B1fromList)
    isReversed = 1;
else
    disp('quad_index: ');
    disp(quad_index);
    disp('vertex_index');
    disp(vertex_index);
    error('ERROR! Something wrong with the edges around the quads! Function checkB1B2Reversal')
end



end