/*
 * STEPReader.hpp
 *
 *  Created on: Oct 6, 2015
 *      Author: saumitra
 */

#ifndef _VOXELIZER_
#define _VOXELIZER_

#include <stdlib.h>

#include <TopoDS_Shape.hxx>

#include "VoxelShape.hpp"

class Voxelizer {
public:
    Voxelizer() {};

    ~Voxelizer() {};

    void voxelize(const TopoDS_Shape topoDSShape,const int refinementLevel, VoxelShape& voxelShape);

    void fillVolume(VoxelShape& voxelShape);
private:
    void getBoundingBox(const TopoDS_Shape topoDSShape, std::vector<double>& origin, std::vector<double>& shapeDimensions);
};

#endif // _VOXELIZER_
