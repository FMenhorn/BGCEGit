#ifndef _VOXELIZER_
#define _VOXELIZER_

#include <stdlib.h>
#include <iostream>
#include <math.h>

#include <TopoDS_Shape.hxx>
#include <Voxel_BoolDS.hxx>
#include <Voxel_FastConverter.hxx>
#include <Bnd_Box.hxx>
#include <BRepBndLib.hxx>

class Voxelizer {
public:
    Voxelizer();

    ~Voxelizer();

    Voxel_BoolDS voxelize(TopoDS_Shape topoDSShape, int refinementLevel);

private:
    double* getBoundingBox();
};

#endif // _VOXELIZER_
