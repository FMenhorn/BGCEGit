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
	exit(0);
	Handle_Standard_Transient entity;
	entity = igesReader.RootForTransfer();
	Standard_Integer numberOfValidTransferEntities = igesReader.NbRootsForTransfer();
	std::cout << "Candidates for transfer to shape: " << numberOfValidTransferEntities << std::endl;
	Standard_Integer numberOfShapes = igesReader.NbShapes();
	std::cout << "Number of shapes: " << numberOfShapes << std::endl;

	Standard_Integer transferedRoots = igesReader.TransferRoots();
	std::cout << "Number of transfered roots: " << transferedRoots << std::endl;

//	Standard_Boolean isTransfered = igesReader.TransferOne(1);
//	if(isTransfered){
//		std::cout << "Shape was produced" << std::endl;
//	}else{
//		std::cout << "Shape not produced. Not cool!" << std::endl;
//		//exit(-1);
//	}
	TopoDS_Shape shape = igesReader.OneShape();
	//TopoDS_Shape shape2 = TransferBRep::ShapeResult(igesReader.TransientProcess(),ent);


	StlAPI_Writer stlWriter;
	stlWriter.Write(shape, "./buoyCircuit.stl");
	return EXIT_SUCCESS;
}

