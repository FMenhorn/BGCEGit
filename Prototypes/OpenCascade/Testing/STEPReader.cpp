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

	IFSelect_ReturnStatus returnStatus = stepReader.ReadFile("./TestFiles/tiefighter/tiefighter.STEP");
	switch(returnStatus){
	case IFSelect_RetDone:
		std::cout << "File read successful" << std::endl;
		break;
	default:
		std::cout << "File read not succesful!" << std::endl;
		exit(-1);
	}
	Standard_Boolean failsonly = Standard_False;
	IFSelect_PrintCount mode;
	stepReader.PrintCheckLoad(failsonly,mode);
	std::cout << "Mode: " << mode << std::endl;

	Standard_Integer ic =  Interface_Static::IVal("read.precision.mode");
	std::cout << "ic: " << ic << std::endl;

	Handle_TColStd_HSequenceOfTransient list = stepReader.GiveList();
	Standard_Integer nbtrans =  stepReader.TransferList(list);
	std::cout << "Number of translations: " << nbtrans << std::endl;
	Standard_Integer nbs =  stepReader.NbShapes();
	std::cout << "Number of shapes: " << nbs << std::endl;
	TopoDS_Shape shape = stepReader.OneShape();
	StlAPI_Writer stlWriter;
	stlWriter.Write(shape, "./tiefighter.stl");
	return EXIT_SUCCESS;
}
