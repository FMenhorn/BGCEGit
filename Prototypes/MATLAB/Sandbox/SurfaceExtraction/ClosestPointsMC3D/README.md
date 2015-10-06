# Surface Extraction
Benni, 16.9.2015

## Short description
Uses marching cubes on two different scales, a coarse scale for the tri patches and a fine scale for the data points. The coarse scale is constructed from the input voxel data by multi-level interpolation of 8 voxels on each level. The data points on the fine scale are distributed to the patches of the coarse scale by projecting them onto the closest patches. After this distribution one can use the information from the projection for giving an initial guess for the local parametrization of the datapoints on the respective patch.
## Example
The example uses the algorithm on a sphere or a torus. On can choose the geometry in sampleData.m and the coarsening level in main.m.

## Data Structures
We use the MATLAB built in data structure for storing triangle surfaces. See `help patch` for explanation.

## Theory and References
Basically this idea consideres the voxel data from our problem and originates from a proposal by Dirk Hartmann.

Unfortunatelly the algorithm scales very bad. It has a complexity of O(n*m) with n<<m where n is the number of patches on the coarse level and m the number of datapoints. We are iterating over all n patches for finding the closes patch to each of the m datapoints. Eventhough n should be very small, usually it is not for complex geometries, if one wants to keep the same topology.

###Possible Optimizations
- [ ] Find more efficient routines for calcultion of the distance point to patch (perhaps even a better algorithm?)
- [ ] Dual Contouring produces less patches, so n will get smaller.
- [ ] Storing the datapoints and the patches in an octree and using the provided space information for decreasing the number of patches one has to iterate over.

