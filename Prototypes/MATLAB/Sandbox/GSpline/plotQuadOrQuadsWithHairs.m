%% script to create model torus quads

quadsToPlot = [1];

%create data
createTorusParams;
loadingTorus;
coefs = createGlobalControlMeshCoefs(parameters,quads_Torus,newA,newB1,newB2,newC,regularPoints);
vertices = coefs\torus_verts_fine; 


%plot
fig_handle = figure('Name', 'Plot with hairs');
for i = quadsToPlot
    plotAllHairsOnQuad(quads_Torus,createdQuadVerts,createdPoints,parameters,i,fig_handle);
    plotOneQuadWhole(quads_Torus,newA,newB1,newB2,newC,regularPoints,vertices,1,fig_handle);
    plotLinesOnQuad(quads_Torus,createdQuadVerts,i,fig_handle);
    plotPatchPointsOnQuad(quads_Torus,createdQuadVerts,i,fig_handle);
end