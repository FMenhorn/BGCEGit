
loadingScript
coefs = createGlobalControlMeshCoefs(parameters,quads_Torus,newA,newB1,newB2,newC,regularPoints);
vertices = coefs\torus_verts_fine; 
plotBezierSurfaceWhole(quads_Torus,newA,newB1,newB2,newC,regularPoints,vertices);

% Create matrices for exporting the patches (note - indexing in matlab
% format)
% [biqPatchPoints,biqIndices,bicPatchPoints,bicIndices] = createBezierPointMatrices(quads_Torus,newA,newB1,newB2,newC,regularPoints,vertices);
% csvwrite('biquadraticPatchPoints.csv',biqPatchPoints);
% csvwrite('biquadraticPatchIndices.csv',biqIndices);
% csvwrite('bicubicPatchPoints.csv',bicPatchPoints);
% csvwrite('bicubicPatchIndices.csv',bicIndices);