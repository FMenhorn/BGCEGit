/*
 * STEPReader.hpp
 *
 *  Created on: Oct 6, 2015
 *      Author: saumitra
 */

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
    Voxelizer() {};

    ~Voxelizer() {};

    Voxel_BoolDS voxelize(const TopoDS_Shape topoDSShape,const int refinementLevel);

private:
    void getBoundingBox(const TopoDS_Shape topoDSShape, double* shapeDimensions);
};

#endif // _VOXELIZER_
