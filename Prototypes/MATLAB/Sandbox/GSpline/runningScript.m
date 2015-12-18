
loadingScriptCant
disp('Loaded data. Creating matrices')

disp('Creating data point control mesh coefs...')
coefs = createGlobalControlMeshCoefs(parameters,quads_Torus,newA,newB1,newB2,newC,regularPoints);
disp('Done. Creating fairness control mesh coefs...')
fairCoefs = createFairnessControlMeshCoefs(quads_Torus,newA,newB1,newB2,newC,regularPoints);
disp('Done. Matrices created')


sparseCoefs = sparse(coefs);
sparseFairCoefs = sparse(fairCoefs);
disp('Matrices sparsified');

fairnessWeight = 2;
joinedCoefs = cat(1,sparseCoefs,fairnessWeight*sparseFairCoefs);
joinedVerts = (cat(1,torus_verts_fine,zeros(size(fairCoefs,1),3)));


disp('Matrices concatenated. Solving lin. system')
vertices = sparseCoefs\torus_verts_fine; 
disp('Small matrix solved, trying big...')
otherVertices = joinedCoefs\joinedVerts;


disp('Systems solved. Plotting')
plotBezierSurfaceWhole(quads_Torus,newA,newB1,newB2,newC,regularPoints,otherVertices);

% Create matrices for exporting the patches (note - indexing in matlab
% format)
% [biqPatchPoints,biqIndices,bicPatchPoints,bicIndices] = createBezierPointMatrices(quads_Torus,newA,newB1,newB2,newC,regularPoints,vertices);
% csvwrite('biquadraticPatchPoints.csv',biqPatchPoints);
% csvwrite('biquadraticPatchIndices.csv',biqIndices);
% csvwrite('bicubicPatchPoints.csv',bicPatchPoints);
% csvwrite('bicubicPatchIndices.csv',bicIndices);