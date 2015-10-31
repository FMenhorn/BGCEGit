%% script for loading data and preformatting the indices for matlab

parametersString = 'param.csv';
dataPointsString = 'verts_fine.csv';
quadsString = 'quads_coarse.csv';
verticesString = 'matlabData.mat';
baseFolder = 'TorusData/BGCE/';
subFolder = 'Cantilever_Out/';
folder = strcat(baseFolder,subFolder);

data_parameters = strcat(folder,parametersString);
data_datapoints = strcat(folder,dataPointsString);
data_quads = strcat(folder,quadsString);
data_vertices = strcat(folder,verticesString);



data_given_parameters = 'TestData/params_DCTorus.csv';
data_made_parameters = 'TestData/parameters.csv';
data_given_parameters_new = '../../../PYTHON/Sandbox/SurfaceFitting/Cantilever_data/parameters.csv';
data_given_sphere_parameters = '../../../PYTHON/Sandbox/SurfaceFitting/Sphere_data/sphere_parameters.csv';
data_parameters_torus_new = 'TorusData/newTorus/param.csv';
data_parameters_torus_new_unscaled = 'TorusData/uncroppedTorus/param.csv';
data_parameters_torus_newdatavers = 'TorusData/Doubletorus_Data/param.csv';
data_parameters_torus_finer = 'TorusData/Torus_Data/param.csv';




data_given_datapoints = 'TestData/torus_verts_fine.csv';
data_given_datapoints_new = '../../../PYTHON/Sandbox/SurfaceFitting/Cantilever_data/torus_verts_fine.csv';
data_made_datapoints = 'TestData/torus_datapoints.csv';
data_given_sphere_datapoints = '../../../PYTHON/Sandbox/SurfaceFitting/Sphere_data/sphere_verts_fine.csv';
data_datapoints_torus_new = 'TorusData/newTorus/verts_fine.csv';
data_datapoints_torus_new_unscaled = 'TorusData/uncroppedTorus/verts_fine.csv';
data_datapoints_torus_newdatavers = 'TorusData/Doubletorus_Data/verts_fine.csv';
data_datapoints_torus_finer = 'TorusData/Torus_Data/verts_fine.csv';


data_given_torus_quads = 'TestData/quads_Torus_erik.csv';
data_given_torus_quads_new = '../../../PYTHON/Sandbox/SurfaceFitting/Cantilever_data/quads_Torus_erik.csv';
data_made_torus_quads = 'TestData/quads_Torus.csv';
data_given_sphere_quads = '../../../PYTHON/Sandbox/SurfaceFitting/Sphere_data/sphere_quads_coarse.csv';
data_quads_torus_new = 'TorusData/newTorus/quads_coarse.csv';
data_quads_torus_new_unscaled = 'TorusData/uncroppedTorus/quads_coarse.csv';
data_quads_torus_newdatavers = 'TorusData/Doubletorus_Data/quads_coarse.csv';
data_quads_torus_finer = 'TorusData/Torus_Data/quads_coarse.csv';

data_given_torus_vertices = 'TestData/torus_point_data_bak.mat';
data_given_torus_vertices_new = '../../../PYTHON/Sandbox/SurfaceFitting/Resolution2/torus_point_data_bak.mat';
data_made_torus_vertices = 'TestData/torus_point_data.mat';
data_given_sphere_vertices = '../../../PYTHON/Sandbox/DooSabin/torus_point_data.mat';
data_vertices_torus_new = 'TorusData/newTorus/matlabData.mat';
data_vertices_torus_new_unscaled = 'TorusData/uncroppedTorus/matlabData.mat';
data_vertices_torus_newdatavers = 'TorusData/Doubletorus_Data/matlabData.mat';
data_vertices_torus_finer = 'TorusData/Torus_Data/matlabData.mat';

quads_Torus = load(data_quads);
load(data_vertices);
parameters = load(data_parameters);
torus_verts_fine = load(data_datapoints);

[parameters,torus_verts_fine] = scaleAwayParameters(parameters,torus_verts_fine);

A = A + 1;
B1 = B1 + 1;
B2 = B2 + 1;
C = C + 1;
[newA,newB1,newB2,newC] = sortAB1B2VIndices(A,B1,B2,C);
parameters(:,1) = parameters(:,1) + 1;
quads_Torus = quads_Torus + 1;
regularPoints = regularPoints + 1;