# 2D Surface Extraction Algorithm
Benni & Juan Carlos , 15.10.15

## Short description
The Surface Extraciton Algorithm uses dual contouring on two different resolutions for approximating the surface on a fine scale and finding a first guess for a patch net on a coarse scale. Then the datapoints from the fine scale are projected on approprotae patches and respective parameters are distributed to each datapoint.

## Example
First run run the script "main.py" with python.

## Data Structures
We use '''Edge''' objects handling the edges with all the necessary functionality for projection onto the edges.

## Theory and References
References for Dual Contouring can be found (here)[https://github.com/FMenhorn/BGCEGit/tree/master/Prototypes/PYTHON/DualContouring]. The remaining algorithm is based on our own work.
### Projection onto Edge
This also involves a coordinate transformation from the Id=\[e_x,e_y\] system of the datapoints to a system spanned by the normal on the edge and the edge. This coordinate system B=\[n,e\] is a orthogonal basis, which can be normalized easily. The Matrix \[n,e_normalized\] = Q gives us the QR decomposition of the basis transformation matrix B=\[n,e\] for free. We can therefore solve the projection of an arbitrary point P onto the edge by the coordinate transformation B\*PB=P, where PB = \[d,t\] is P in the coordinate system of the edge (t is the parameter, we are looking for and d the distance of the point to the edge). This can be solved easily with the known QR decompositon: B\*PB=P --> R\*PB=Q'P
This can be solved by solving the upper triangular system R.

## Possible Improvements
- Also include neighborhood information for the projection of one point onto an edge for avoiding oszillations

