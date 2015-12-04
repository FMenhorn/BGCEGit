function isReversed = checkB1B2Reversal(B1,quad_list,quad_index,vertex_index,regularPoints)

isReversed = -1; %error!!

mod_index = @(i,modul) mod(i-1,modul) + 1;

B1s_this_vertex = B1(vertex_index+1,:,:);

quadNumberLocal = find(B1(vertex_index+1,:,2) == quad_index);
couldBeB1Edge = reshape(B1(vertex_index+1,quadNumberLocal,3:4),1,2);
thisQuad_cornerVertices = quad_list(quad_index+1,:);
whichQuadCorner = find(thisQuad_cornerVertices == vertex_index);

%in peter's scheme, and therefore in the parameters, B1 is the left one if
%looking into the quad corner. Since the quad corners go clockwise, that
%means the relevant quad corner and the one after should be
shouldBeB1Edge = thisQuad_cornerVertices([whichQuadCorner,mod_index(whichQuadCorner+1,4)]);
shouldBeB2Edge = thisQuad_cornerVertices([whichQuadCorner,mod_index(whichQuadCorner-1,4)]);

if (length(intersect(couldBeB1Edge,shouldBeB1Edge)) == 2)
    isReversed = 0;
elseif(length(intersect(couldBeB1Edge,shouldBeB2Edge)) == 2)
    isReversed = 1;
else
    error('ERROR! Something wrong with the edges around the quads! Function checkB1B2Reversal')
end



end