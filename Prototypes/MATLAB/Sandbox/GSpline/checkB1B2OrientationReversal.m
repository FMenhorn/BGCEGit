function isNotCounterClockwise = checkB1B2OrientationReversal(B1,B2,quad_list,quad_index,vertex_index)
%check if the B1 in the quad to the right lies along the same edge as the
%B2 in the current quad.


isNotCounterClockwise = -1; %error!!

mod_index = @(i,modul) mod(i-1,modul) + 1;

B1s_this_vertex = reshape(B1(vertex_index,:,:),size(B1,2),size(B1,3));
B2s_this_vertex = reshape(B2(vertex_index,:,:),size(B2,2),size(B2,3));

numberOfEdges = getNumOfEdgesMeetingMatlab(B1,vertex_index);

quadNumberLocal = find(B1(vertex_index,:,2) == quad_index);
B1EdgeFromB1 = reshape(B1(vertex_index,quadNumberLocal,3:4),1,2);
shouldBeSameAsB1Edge = reshape(B2(vertex_index,mod_index(quadNumberLocal - 1,numberOfEdges),3:4),1,2);
isB1IfReversed = reshape(B2(vertex_index,mod_index(quadNumberLocal + 1,numberOfEdges),3:4),1,2);
B2EdgeFromB2 = reshape(B2(vertex_index,quadNumberLocal,3:4),1,2);
shouldBeSameAsB2Edge = reshape(B1(vertex_index,mod_index(quadNumberLocal + 1,numberOfEdges),3:4),1,2);
isB2IfReversed = reshape(B1(vertex_index,mod_index(quadNumberLocal - 1,numberOfEdges),3:4),1,2);

thisQuad_cornerVertices = quad_list(quad_index,:);
whichQuadCorner = find(thisQuad_cornerVertices == vertex_index);

%in peter's scheme, and therefore in the parameters, B1 is the left one if
%looking into the quad corner. Since the quad corners go clockwise, that
%means the relevant quad corner and the one after should be
shouldBeB1Edge = thisQuad_cornerVertices([whichQuadCorner,mod_index(whichQuadCorner+1,4)]);
shouldBeB2Edge = thisQuad_cornerVertices([whichQuadCorner,mod_index(whichQuadCorner-1,4)]);

if (length(intersect(B1EdgeFromB1,shouldBeB1Edge)) == 2 && length(intersect(B2EdgeFromB2,shouldBeB2Edge)) == 2)

    if(length(intersect(B1EdgeFromB1,shouldBeSameAsB1Edge)) == 2 ...
            && length(intersect(B2EdgeFromB2,shouldBeSameAsB2Edge)) == 2)
        isNotCounterClockwise = 0;
    elseif(length(intersect(B1EdgeFromB1,isB1IfReversed)) == 2 ...
            && length(intersect(B2EdgeFromB2,isB2IfReversed)) == 2)
        isNotCounterClockwise = 1;
    else
        error('something is seriously wrong because the edges don`t add upp. in checkB1B2OrientationReversal');
    end
elseif(length(intersect(B1EdgeFromB1,shouldBeB2Edge)) == 2)
    error('I didn`t write this function and the other one for you to be lazy and not use the other to check for reversed b1b2');
else
  
    disp('quad_index: ');
    disp(quad_index);
    disp('vertex_index');
    disp(vertex_index);
    error('ERROR! Something wrong with the edges around the quads! Function checkB1B2OrientationReversal')
end



end