%% script for loading data and preformatting the indices for matlab

%% PART 1: JUST DEFINING A LOT OF NAMES FOR LATER (ignore if you want)
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

%% PART 2: Actually loading the data, using the previous strings as file names.

%a): load quad csv-file (indices of the vertices of all quads in a Nx4
%array
quads_Torus = load(data_quads);

%b): load .mat file with DooSabin information for indexing of the patch
%points
load(data_vertices);

%c) load parameters csv-file with Mx3 array of [quad index],[u],[v] for
%ever datapoint (fine grid point)
parameters = load(data_parameters);

%d) load the datapoint (fine grid point) locations as a Mx3 array of
%[x],[y],[z]
torus_verts_fine = load(data_datapoints);


%% PART 3: Preprocess to change from Python to Matlab indexing etc.

%a): Throw away any datapoints which are outside the parameter range [0,1]
%since these cause trouble. (+ Scale the resulting ones so that max and min
%param values are 1 and 0 repspectively in both u and v)
[parameters,torus_verts_fine] = scaleAwayParameters(parameters,torus_verts_fine);

%b): Reindex 
A = A + 1;
B1 = B1 + 1;
B2 = B2 + 1;
C = C + 1;

%c): Sort the A, B1, B2 and C so that the second index corresponds to the
%same quad for all arrays and stuff
[newA,newB1,newB2,newC] = sortAB1B2VIndices(A,B1,B2,C);

%d): Final reindexing
parameters(:,1) = parameters(:,1) + 1;
quads_Torus = quads_Torus + 1;
regularPoints = regularPoints + 1;