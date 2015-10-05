//============================================================================
// Name        : OpenCascade.cpp
// Author      : FMenhorn
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <unistd.h>

#include <TopoDS_Shape.hxx>
#include <StlAPI_Reader.hxx>
#include <Voxel_BoolDS.hxx>
#include <Voxel_FastConverter.hxx>
#include <Voxel_Writer.hxx>
#include <Voxel_VoxelFileFormat.hxx>
#include <Bnd_Box.hxx>
#include <BRepBndLib.hxx>
#include <TCollection_ExtendedString.hxx>

int main(void) {

	TopoDS_Shape topoDSShape;
	StlAPI_Reader stlReader;

	stlReader.Read(topoDSShape, "./Moon.stl");

    Bnd_Box B; // Bounding box
	double Xmin, Ymin, Zmin, Xmax, Ymax, Zmax; // Bounding box bounds

    BRepBndLib::Add(topoDSShape, B);
    B.Get(Xmin, Ymin, Zmin, Xmax, Ymax, Zmax);

    int N_X = 20 * (Xmax - Xmin);
    int N_Y = 20 * (Ymax - Ymin);
    int N_Z = 20 * (Zmax - Zmin);

    std::cout << "Domain bounds: X[" << Xmin << ", " << Xmax << "]:" << N_X << " | Y[" << Ymin << ", " << Ymax << "]:" << N_Y << " | Z[" << Zmin << ", " << Zmax << "]:" << N_Z << std::endl;

	Voxel_BoolDS voxelBool;
	Voxel_FastConverter voxelConverter(topoDSShape, voxelBool, 0.01, N_X, N_Y, N_Z);

	Standard_Integer progress;
	voxelConverter.Convert(progress);
	//voxelConverter.FillInVolume(1,topoDSShape);
	std::cout << "Progress of Conversion: " << progress << std::endl;

	Standard_Real xLen = voxelBool.GetXLen();
	Standard_Real yLen = voxelBool.GetYLen();
	Standard_Real zLen = voxelBool.GetZLen();

	Standard_Real nbX = voxelBool.GetNbX();
	Standard_Real nbY = voxelBool.GetNbY();
	Standard_Real nbZ = voxelBool.GetNbZ();

	std::cout << "Size: " << xLen << "," << yLen << "," << zLen << std::endl;

	Standard_Real xStep = voxelBool.GetXLen() / voxelBool.GetNbX();
	Standard_Real yStep = voxelBool.GetYLen() / voxelBool.GetNbY();
	Standard_Real zStep = voxelBool.GetZLen() / voxelBool.GetNbZ();

	std::cout << "Steps: " << xStep << "," << yStep << "," << zStep
			<< std::endl;

	Voxel_Writer voxelWriter;
	TCollection_ExtendedString fileString("./StarAscii");

	voxelWriter.SetFormat(Voxel_VFF_ASCII);
	voxelWriter.SetVoxels(voxelBool);
	voxelWriter.Write(fileString);

	for (Standard_Real x = 0; x < nbX; x++) {
		for (Standard_Real y = 0; y < nbY; y++) {
			for (Standard_Real z = 0; z < nbZ; z++) {
				std::cout << "[x,y,z]=[" << x << "," << y << "," << z << "]"
						<< " " << "Voxel=" << voxelBool.Get(x, y, z)
						<< std::endl;
			}
		}
	}

	for (Standard_Real y = 0; y < nbY; y++) {
		for (Standard_Real x = 0; x < nbX; x++) {
			for (Standard_Real z = 0; z < nbZ; z++) {
				std::cout << voxelBool.Get(x, y, z);
			}
			std::cout << std::endl;
		}
		std::cout << "#######" << std::endl;
	}
	return EXIT_SUCCESS;
}
