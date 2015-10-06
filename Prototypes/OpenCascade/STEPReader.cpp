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

	IFSelect_ReturnStatus returnStatus = stepReader.ReadFile("./TestFiles/r2d2/STEP/R2D2.STEP");
	switch(returnStatus){
	case IFSelect_RetDone:
		std::cout << "File read successful" << std::endl;
		break;
	default:
		std::cout << "File read not succesful!" << std::endl;
		exit(-1);
	}
	return EXIT_SUCCESS;
}
