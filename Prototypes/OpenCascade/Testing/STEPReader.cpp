/*
 * STEPReader.cpp
 *
 *  Created on: Oct 6, 2015
 *      Author: friedrich
 */

#include <stdio.h>
#include <stdlib.h>
#include <iostream>

#include <TopoDS_Shape.hxx>
#include <STEPControl_Reader.hxx>
#include <Voxel_BoolDS.hxx>
#include <Voxel_FastConverter.hxx>
#include <Voxel_Writer.hxx>
#include <Voxel_VoxelFileFormat.hxx>
#include <TCollection_ExtendedString.hxx>
#include <TransferBRep.hxx>
#include <StlAPI_Writer.hxx>
#include <Interface_Static.hxx>


int main(void) {
	TopoDS_Shape topoDSShape;
	STEPControl_Reader stepReader;

	IFSelect_ReturnStatus returnStatus = stepReader.ReadFile("./TestFiles/Aircraft.stp");
	switch(returnStatus){
	case IFSelect_RetDone:
		std::cout << "STEPReader: File read successful" << std::endl;
		break;
	default:
		std::cout << "STEPReader: File read not succesful!" << std::endl;
		exit(-1);
	}

	Standard_Boolean failsonly = Standard_False;
	IFSelect_PrintCount mode;
	stepReader.PrintCheckLoad(failsonly,mode);
	std::cout << "STEPReader: Mode: " << mode << std::endl;

	Standard_Integer ic =  Interface_Static::IVal("read.precision.mode");
	std::cout << "STEPReader: ic: " << ic << std::endl;

	Handle_TColStd_HSequenceOfTransient list = stepReader.GiveList();
	Standard_Integer nbtrans =  stepReader.TransferList(list);
	std::cout << "STEPReader: Number of translations: " << nbtrans << std::endl;
	Standard_Integer nbs =  stepReader.NbShapes();
	std::cout << "STEPReader: Number of shapes: " << nbs << std::endl;

	return EXIT_SUCCESS;
}
