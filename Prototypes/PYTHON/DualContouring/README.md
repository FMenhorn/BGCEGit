# B-Splines
Benni & Juan Carlos , 8.10.15

## Short description
Our dual contouring algorithm in PYTHON is able to produce approximations of surfaces on different resolutions. One can visualize the results with the respective MATLAB scripts on.
In the doubletorus example one can see, that a to coarse resolution results in errors: The shape of the torus is note one connected volume, but multiple volumes which result out of "dents".

## Example
First run one of the scripts "dc2D.py" or "dc3D.py" in PYTHON. For vizualisation run "plotDC2D.m" respectively "plotDC3D.m" in MATLAB.

## Data Structures
We use a dictionary for storing the voxel data. This dictionary can be accessed via '''dict[key]''' where the key is a tuple of the coordinates we want to access.

## Theory and References
- See this [article](http://www.mattkeeter.com/projects/contours/) for a nice explanation with colorful pictures
- The code we use is based (with some modifications) on the following code from [Stackoverflow](http://stackoverflow.com/questions/6485908/basic-dual-contouring-theory)
- This [paper](http://www.frankpetterson.com/publications/dualcontour/dualcontour.pdf) explains the theory of DC.

## Possible Improvements
Our datastructure for the voxel data is very comfortable for supporting different resolutions, still there is no interpolation or something else applied. This could be improved by applying a sufficient coarsening scheme.
The hermite data approximaiton is a very simple scheme: We just approximate the midpoint of an edge as the root. This is the best guess we can get on the finest resolution. But for coarse resolutions one could also incorporate information from finer levels for finding the root.
