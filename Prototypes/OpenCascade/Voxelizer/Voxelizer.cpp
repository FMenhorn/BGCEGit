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
	voxelConverter.FillInVolume(1, topoDSShape);
	voxelConverter.Convert(progress);
	voxelConverter.FillInVolume(1, topoDSShape);
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

void Voxelizer::fillVolume(VoxelShape& voxelShape){
	//Voxel_BoolDS hollowVoxelShapeDS = voxelShape.getVoxelShape();
	Standard_Real xLen = voxelShape.getVoxelShape().GetXLen();
	Standard_Real yLen = voxelShape.getVoxelShape().GetYLen();
	Standard_Real zLen = voxelShape.getVoxelShape().GetZLen();

	Standard_Real nbX = voxelShape.getVoxelShape().GetNbX();
	Standard_Real nbY = voxelShape.getVoxelShape().GetNbY();
	Standard_Real nbZ = voxelShape.getVoxelShape().GetNbZ();

	std::cout << "Size: " << xLen << "," << yLen << "," << zLen << std::endl;

	Standard_Real xStep = xLen/nbX;
	Standard_Real yStep = yLen/nbY;
	Standard_Real zStep = zLen/nbZ;

	bool inside = false;
	//Voxel_BoolDS filledVoxelShapeDS = hollowVoxelShapeDS;
	for (Standard_Integer x = 0; x < nbX; x++) {
		for (Standard_Integer y = 0; y < nbY; y++) {
			for (Standard_Integer z = 0; z < nbZ; z++) {
				//std::cout << "Voxelizer::fillVolume: [" << x << "," << y << "," << z << "]="<<
				//		voxelShape.getVoxelShape().Get(x,y,z) << std::endl;

				if(voxelShape.getVoxelShape().Get(x, y, z) && !inside){ // true and false
					inside = true;
				}else if(voxelShape.getVoxelShape().Get(x, y, z) && inside){ //true and true
					inside = !inside;
				}else if(!voxelShape.getVoxelShape().Get(x, y, z) && !inside){ //false and false
					inside = false;
				}else{	//false and true
					inside = !inside;
				}
				if(!voxelShape.getVoxelShape().Get(x, y, z) && inside){
					voxelShape.getVoxelShape().Set(x,y,z,Standard_True);
					std::cout << "Voxelizer::fillVolume: [" << x << "," << y << "," << z << "]="<<
							voxelShape.getVoxelShape().Get(x,y,z) << std::endl;
				}
			}
		}
	}
	//voxelShape.setVoxelShape(hollowVoxelShapeDS);
}
