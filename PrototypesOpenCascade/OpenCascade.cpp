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

#include <TopoDS_Shape.hxx>
#include <StlAPI_Reader.hxx>
#include <Voxel_BoolDS.hxx>
#include <Voxel_FastConverter.hxx>
#include <Voxel_Writer.hxx>
#include <Voxel_VoxelFileFormat.hxx>
#include <TCollection_ExtendedString.hxx>

int main(void) {

	TopoDS_Shape moonShape;
	StlAPI_Reader stlReader;

	stlReader.Read(moonShape, "/home/friedrich/Documents/Studium/Master_CSE/BGCE/Project/Program/OpenCascadeTesting/Moon.stl");

	Voxel_BoolDS voxelBool;
	Voxel_FastConverter voxelConverter(moonShape, voxelBool, 0.1, 4,4,4);
	Standard_Integer progress;
	voxelConverter.Convert(progress);
	voxelConverter.FillInVolume(1);
	std::cout << "Progress of Converstion: " << progress << std::endl;

	Standard_Real xLen = voxelBool.GetXLen();
	Standard_Real yLen = voxelBool.GetYLen();
	Standard_Real zLen = voxelBool.GetZLen();

	std::cout << "Size: " << xLen << "," << yLen << "," << zLen << std::endl;

	Standard_Real xStep = voxelBool.GetXLen()/voxelBool.GetNbX();
	Standard_Real yStep = voxelBool.GetYLen()/voxelBool.GetNbY();
	Standard_Real zStep = voxelBool.GetZLen()/voxelBool.GetNbZ();

	std::cout << "Steps: " << xStep << "," << yStep << "," << zStep << std::endl;

	Voxel_Writer voxelWriter;
	TCollection_ExtendedString fileString("/home/friedrich/Documents/Studium/Master_CSE/BGCE/Project/Program/OpenCascadeTesting/MoonAscii");
	voxelWriter.SetFormat(Voxel_VFF_ASCII);
	voxelWriter.SetVoxels(voxelBool);
	voxelWriter.Write(fileString);


	for(Standard_Real x = 0; x < xLen; x += xStep){
		for(Standard_Real y = 0; y < yLen; y += yStep){
			for(Standard_Real z = 0; z < zLen; z += zStep){
				std::cout << "[x,y,z]=[" << x << "," << y << "," << z << "]" << " " << "Voxel=" << voxelBool.Get(x,y,z) << std::endl;
			}
		}
	}
	return EXIT_SUCCESS;
}
