%% script for loading data and preformatting the indices for matlab

data_given_parameters = 'TestData/params_DCTorus.csv';
data_made_parameters = 'TestData/parameters.csv';

data_given_datapoints = 'TestData/torus_verts_fine.csv';
data_made_datapoints = 'TestData/torus_datapoints.csv';

data_given_torus_quads = 'TestData/quads_Torus_erik.csv';
data_made_torus_quads = 'TestData/quads_Torus.csv';

data_given_torus_vertices = 'TestData/torus_point_data_bak.mat';
data_made_torus_vertices = 'TestData/torus_point_data.mat';

quads_Torus = load(data_made_torus_quads);
load(data_made_torus_vertices);
parameters = load(data_made_parameters);
torus_verts_fine = load(data_made_datapoints);

A = A + 1;
B1 = B1 + 1;
B2 = B2 + 1;
C = C + 1;
[newA,newB1,newB2,newC] = sortAB1B2VIndices(A,B1,B2,C);
parameters(:,1) = parameters(:,1) + 1;
quads_Torus = quads_Torus + 1;
regularPoints = regularPoints + 1;