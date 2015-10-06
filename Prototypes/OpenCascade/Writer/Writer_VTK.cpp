#include "Writer_VTK.hpp"


bool Writer_VTK::write(Voxel_BoolDS voxelShape){
    ofstream outfile;
    std::cout << "Writer: ";
    outfile.open(filename + ".vtk", ios::out | ios::trunc);

    writeHeader(outfile);
    writeStructuredGrid(outfile, voxelShape);
    writeScalars(outfile, voxelShape);

    outfile.close();

    return true;
}

void Writer_VTK::writeHeader(std::ofstream &outfile) {
    outfile << "# vtk DataFile Version 2.0\n";
	outfile << "BGCE Project 2015-16\n";
	outfile << "ASCII\n";
	outfile << "\n";
}

void Writer_VTK::writeStructuredGrid(std::ofstream &outfile, Voxel_BoolDS voxelShape){
	outfile << "DATASET STRUCTURED_POINTS\n";
	outfile << "DIMENSIONS  " << (int)voxelShape.GetNbX() << " " << (int)voxelShape.GetNbY() << " " << (int)voxelShape.GetNbZ() << "\n";
	outfile << "ORIGIN " << 0 << " " << 0 << " " << 0 << "\n";
	outfile << "SPACING " << voxelShape.GetXLen() / voxelShape.GetNbX() << " " << voxelShape.GetYLen() / voxelShape.GetNbY() << " " << voxelShape.GetZLen() / voxelShape.GetNbZ() << "\n";
	outfile << "\n";
}


void Writer_VTK::writeScalars(std::ofstream &outfile, Voxel_BoolDS voxelShape){
	int totalSize = voxelShape.GetNbX() * voxelShape.GetNbY() * voxelShape.GetNbZ();
	outfile << "POINT_DATA " << totalSize << " \n";
	outfile << "SCALARS density float 1 \n";
	outfile << "LOOKUP_TABLE default \n";
	for (int i = 0; i < voxelShape.GetNbX(); i++){
        for (int j = 0; j < voxelShape.GetNbY(); j++){
            for (int k = 0; k < voxelShape.GetNbZ(); k++){
                outfile << (float)voxelShape.Get(i, j, k) << "\n";
            }
        }
	}
}
