%% script to create model torus quads
clear all
close all
quadsToPlot = 1:3;


%create data
createTorusParams;
loadingTorus;
coefs = createGlobalControlMeshCoefs(parameters,quads_Torus,newA,newB1,newB2,newC,regularPoints);
vertices = coefs\torus_verts_fine; 
numQuads = size(regularPoints,1);



%plot
fig_handle = figure('Name', 'Plot with hairs');

quads_patchvertices = zeros(3,numQuads,16);
for i = 1:numQuads
    temp_patchvertices = getPatchPointsOnQuad(quads_Torus,createdQuadVerts,i,fig_handle);
    for j = 1:4
        for k = 1:4
            quads_patchvertices(:,i,k + (j-1)*4) = temp_patchvertices(:,k,j);
        end
    end
end

regular_quadpoints = shiftToRegularPointsFormat(regularPoints,quads_patchvertices);
axis off
for i = 1:length(quadsToPlot)
    %plotAllHairsOnQuad(quads_Torus,createdQuadVerts,createdPoints,parameters,i,fig_handle);
%     plotOneQuadWhole(quads_Torus,newA,newB1,newB2,newC,regularPoints,vertices,i,fig_handle);
    plotLinesOnQuad(quads_Torus,createdQuadVerts,quadsToPlot(i),fig_handle);
    plotPatchPointsOnQuad(quads_Torus,createdQuadVerts,quadsToPlot(i),fig_handle);
    plotPatchesOnQuad(quads_Torus,newA,newB1,newB2,newC,regularPoints,regular_quadpoints,i,[5,8,9,12],fig_handle);
    
    
    %------------------------
    %ADDED FOR ANNA'S PURPOSES
    %plotQuad(quads_Torus,createdQuadVerts,i,fig_handle);
    %[figure_dummy, patch_points] =  plotPatchPointsOnQuad(quads_Torus,createdQuadVerts,i,fig_handle);
    %hold on
    %bezier_points = getBiquadraticPatch(patch_points);
    %plotPoints(bezier_points);
    %-------------------------
end

