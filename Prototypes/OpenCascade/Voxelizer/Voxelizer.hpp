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
#include "VoxelIndexCalculator.hpp"
#include "../DataWrappers/ListOfShape.hpp"

class Voxelizer {
public:
    Voxelizer() {};

    ~Voxelizer() {};

    void voxelizeWholeVector(const int refinementLevel, const bool isElem, const ListOfShape& listOfShapes, std::vector<VoxelShape>& voxelShapeVector, int counter = 0);

    void voxelize(const TopoDS_Shape topoDSShape,const int refinementLevel, VoxelShape& voxelShape);

    void fillVolume(VoxelShape& voxelShape);

    void getPassiveVoxels(const VoxelShape bodyVoxelShape, VoxelShape& passiveVoxelShape);

	void setVoxelIndexCalculator(
			const VoxelIndexCalculator& voxelIndexCalculator);

private:
    VoxelIndexCalculator voxelIndexCalculator;

    void getBoundingBox(const TopoDS_Shape topoDSShape, std::vector<double>& origin, std::vector<double>& shapeDimensions);
};

#endif // _VOXELIZER_
