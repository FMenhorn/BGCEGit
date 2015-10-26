
loadingScript
coefs = createGlobalControlMeshCoefs(parameters,quads_Torus,newA,newB1,newB2,newC,regularPoints);
vertices = coefs\torus_verts_fine;
plotBezierSurfaceWhole(quads_Torus,newA,newB1,newB2,newC,regularPoints,vertices)