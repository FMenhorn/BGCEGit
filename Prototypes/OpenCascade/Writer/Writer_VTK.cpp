/*
 * STEPReader.hpp
 *
 *  Created on: Oct 6, 2015
 *      Author: saumitra
 */

#include "Writer_VTK.hpp"

#include <Voxel_BoolDS.hxx>

bool Writer_VTK::write(std::string filename,  std::vector<std::vector<VoxelShape>> &voxelShape){
    /*ofstream outfile;
    std::cout << "Writer: Writing VTK file for " + filename + " .." << std::endl;
    outfile.open(filename + ".vtk", ios::out | ios::trunc);

    writeHeader(outfile);
    writeStructuredGrid(outfile, voxelShape);
    writeScalars(outfile, voxelShape);

    outfile.close();

    std::cout << "Writer: .. done!" << std::endl;
	*/
    return true;
}

void Writer_VTK::writeHeader(std::ofstream &outfile) {
    outfile << "# vtk DataFile Version 2.0\n";
	outfile << "BGCE Project 2015-16\n";
	outfile << "ASCII\n";
	outfile << "\n";
}

void Writer_VTK::writeStructuredGrid(std::ofstream &outfile, VoxelShape &voxelShape){
	const Voxel_BoolDS& voxelBoolShape = voxelShape.getVoxelShape();
	outfile << "DATASET STRUCTURED_POINTS\n";
	outfile << "DIMENSIONS  " << (int)voxelBoolShape.GetNbX() << " " << (int)voxelBoolShape.GetNbY() << " " << (int)voxelBoolShape.GetNbZ() << "\n";
	outfile << "ORIGIN " << voxelShape.getOriginX() << " " << voxelShape.getOriginY() << " " << voxelShape.getOriginZ() << "\n";
	outfile << "SPACING " << voxelBoolShape.GetXLen() / voxelBoolShape.GetNbX() << " " << voxelBoolShape.GetYLen() / voxelBoolShape.GetNbY() << " " << voxelBoolShape.GetZLen() / voxelBoolShape.GetNbZ() << "\n";
	outfile << "\n";
}


void Writer_VTK::writeScalars(std::ofstream &outfile, VoxelShape &voxelShape){
	const Voxel_BoolDS& voxelBoolShape = voxelShape.getVoxelShape();
	int totalSize = voxelBoolShape.GetNbX() * voxelBoolShape.GetNbY() * voxelBoolShape.GetNbZ();
	//std::cout << voxelShape.GetNbX() << " " << voxelShape.GetNbY() << " " << voxelShape.GetNbZ() << std::endl;
	outfile << "POINT_DATA " << totalSize << " \n";
	outfile << "SCALARS density int 1 \n";
	outfile << "LOOKUP_TABLE default \n";
	for (int k = 0; k < voxelBoolShape.GetNbZ(); k++){
        for (int j = 0; j < voxelBoolShape.GetNbY(); j++){
            for (int i = 0; i < voxelBoolShape.GetNbX(); i++){
                outfile << (int)(voxelBoolShape.Get(i, j, k)) << "\n";
            }
        }
	}
}
