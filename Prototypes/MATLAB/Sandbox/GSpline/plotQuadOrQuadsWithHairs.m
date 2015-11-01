%% script to create model torus quads
clear all
close all
quadsToPlot = 1:3;

%create data
createTorusParams;
loadingTorus;
coefs = createGlobalControlMeshCoefs(parameters,quads_Torus,newA,newB1,newB2,newC,regularPoints);
vertices = coefs\torus_verts_fine; 


%plot
fig_handle = figure('Name', 'Plot with hairs');
axis off
for i = quadsToPlot
    %plotAllHairsOnQuad(quads_Torus,createdQuadVerts,createdPoints,parameters,i,fig_handle);
    %plotOneQuadWhole(quads_Torus,newA,newB1,newB2,newC,regularPoints,vertices,i,fig_handle);
    plotLinesOnQuad(quads_Torus,createdQuadVerts,i,fig_handle);
    plotPatchPointsOnQuad(quads_Torus,createdQuadVerts,i,fig_handle);
    
    %------------------------
    %ADDED FOR ANNA'S PURPOSES
    %plotQuad(quads_Torus,createdQuadVerts,i,fig_handle);
    %[figure_dummy, patch_points] =  plotPatchPointsOnQuad(quads_Torus,createdQuadVerts,i,fig_handle);
    %hold on
    %bezier_points = getBiquadraticPatch(patch_points);
    %plotPoints(bezier_points);
    %-------------------------
end