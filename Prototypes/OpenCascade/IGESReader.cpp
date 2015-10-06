/*
 * IGESReader.cpp
 *
 *  Created on: Oct 5, 2015
 *      Author: friedrich
 */

#include <stdio.h>
#include <stdlib.h>
#include <iostream>

#include <TopoDS_Shape.hxx>
#include <IGESControl_Reader.hxx>
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
	IGESControl_Reader igesReader;

	IFSelect_ReturnStatus returnStatus = igesReader.ReadFile("./TestFiles/circuit-board-pcb-mock-example.snapshot.4/Buoy_Circuitbuoy.igs");

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
	igesReader.PrintCheckLoad(failsonly,mode);
	std::cout << "Mode: " << mode << std::endl;

	Standard_Integer ic =  Interface_Static::IVal("read.iges.bspline.continuity");
	std::cout << "ic: " << ic << std::endl;
	//All Entities:
	//Handle(TColStd_HSequenceOfTransient)  list = igesReader.GiveList();
	//All faces:
	Handle_TColStd_HSequenceOfTransient list = igesReader.GiveList("iges-faces");
	//Translate all entitites in one operation

//	for (Standard_Integer i = 1; i  <= 425; i ++) {
//	    Handle(Standard_Transient) ent = list.;
//	    Standard_Boolean OK = reader.TransferEntity (ent);
//	}

	Standard_Integer nbtrans =  igesReader.TransferList(list);
	std::cout << "Number of translations: " << nbtrans << std::endl;
	Standard_Integer nbs =  igesReader.NbShapes();
	std::cout << "Number of shapes: " << nbs << std::endl;
	TopoDS_Shape shape;
//	for(Standard_Integer i = 1; i <= nbs; i++){
//		std::cout << "i: " << i << " ... ";
//		shape = igesReader.Shape(i);
//		std::cout << "successful!" << std::endl;
//	}
	TopoDS_Shape shape2 = igesReader.OneShape();
	StlAPI_Writer stlWriter;
	stlWriter.Write(shape2, "./buoyCircuit.stl");
	return EXIT_SUCCESS;
}

