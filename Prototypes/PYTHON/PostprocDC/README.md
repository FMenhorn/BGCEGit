# Postproc DC
This folder contains postprocessing tools for our DC output.

## Postproc STEP 
### Provided Files
In PetersSchemeInput one can find the raw ```.csv``` output of DC. In PostprocOutput one can find the following files for each scenario (currently torus and cantilever):

- ```mesh.step``` (holds the coarse mesh)
- ```verts_coarse.asc``` and ```verts_fine.asc``` (hold the fine and coarse resolution point clound in ASCII format, which can be opened using freecad)
- ```verts_fine.fcstd``` (point cloud of fine resolution in freecad format)
- ```composite.fcstd``` (point cloud of fine resolution and mesh of the coarse resolution in freecad format)

### File generation
For generating the ```.step``` files with mesh or point data, please run ```CoarseMeshToSTEP.py``` (fast) or ```PointsToSTEP.py``` (awfully slow... should be replaced).