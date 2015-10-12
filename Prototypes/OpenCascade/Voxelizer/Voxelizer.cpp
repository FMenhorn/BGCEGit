/*
 * STEPReader.hpp
 *
 *  Created on: Oct 6, 2015
 *      Author: saumitra
 */

#include "Voxelizer.hpp"

#include <iostream>

#include <Voxel_FastConverter.hxx>
#include <Bnd_Box.hxx>
#include <BRepBndLib.hxx>
#include <Voxel_BoolDS.hxx>

#include "../Helper/Helper.hpp"

void Voxelizer::voxelize(const TopoDS_Shape topoDSShape,const int refinementLevel, VoxelShape& voxelShape){

    std::cout << "Voxelizer: Getting domain bounds .." << std::endl;

    std::vector<double> origin(3);
    std::vector<double> shapeDimensions(3);
    getBoundingBox(topoDSShape, origin, shapeDimensions);

    int voxelCount[3];
    for (size_t i = 0; i < 3; i++)
        voxelCount[i] = pow(2, refinementLevel) * shapeDimensions[i];

    //Voxel_BoolDS* voxelShapeOCE = new Voxel_BoolDS(); // Result holder of the voxelization
    Standard_Integer progress; // Progress of voxelization (useful in case of parallel code)
    std::cout << "Voxelizer: Voxelizing .." << std::endl;
    std::cout << "Voxelizer: with number of voxels: " << voxelCount[0]*voxelCount[1]*voxelCount[2] << std::endl;
	Voxel_FastConverter voxelConverter(topoDSShape, voxelShape.getVoxelShape(), 0.1, voxelCount[0], voxelCount[1], voxelCount[2]);
	voxelConverter.Convert(progress);
	std::cout << "Voxelizer: Progress of Conversion: " << progress << std::endl;
    std::cout << "Voxelizer: .. done!" << std::endl;
    //voxelShape.setVoxelShape(*voxelShapeOCE);
    voxelShape.setOrigin(origin);
}

void Voxelizer::getBoundingBox(const TopoDS_Shape topoDSShape, std::vector<double>& origin, std::vector<double>& shapeDimensions){
    Bnd_Box B; // Bounding box
	double Xmin, Ymin, Zmin, Xmax, Ymax, Zmax; // Bounding box bounds
    BRepBndLib::Add(topoDSShape, B);
    B.Get(Xmin, Ymin, Zmin, Xmax, Ymax, Zmax);

    origin[0] = Xmin;
    origin[1] = Ymin;
    origin[2] = Zmin;

    shapeDimensions[0] = absolut(Xmax - Xmin);
    shapeDimensions[1] = absolut(Ymax - Ymin);
    shapeDimensions[2] = absolut(Zmax - Zmin);

    std::cout << "Voxelizer-getBoundingBox:" << std::endl;
    std::cout << "    X[" << Xmin << ", " << Xmax << "]     | xDimension: " << shapeDimensions[0] << std::endl;
    std::cout << "    Y[" << Ymin << ", " << Ymax << "]     | yDimension: " << shapeDimensions[1] << std::endl;
    std::cout << "    Z[" << Zmin << ", " << Zmax << "]     | zDimension: " << shapeDimensions[2] << std::endl;
}
