/*
 * STEPReader.cpp
 *
 *  Created on: Oct 6, 2015
 *      Author: friedrich
 */

#include "STEPReader.hpp"

#include <iostream>

STEPReader::STEPReader(STEPControl_Reader* stepControlReader): Reader(stepControlReader) {

}

STEPReader::~STEPReader() {
	this->~Reader();
}

TopoDS_Shape STEPReader::read(std::string filename) {

    TopoDS_Shape topoDSShape;
	STEPControl_Reader stepReader;

	IFSelect_ReturnStatus returnStatus = stepReader.ReadFile(filename.c_str());
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
	stepReader.PrintCheckLoad(failsonly, mode);
	std::cout << "STEPReader: Mode: " << mode << std::endl;

	Standard_Integer ic =  Interface_Static::IVal("read.precision.mode");
	std::cout << "STEPReader: ic: " << ic << std::endl;

	Handle_TColStd_HSequenceOfTransient list = stepReader.GiveList();
	Standard_Integer nbtrans =  stepReader.TransferList(list);
	std::cout << "STEPReader: Number of translations: " << nbtrans << std::endl;
	Standard_Integer nbs =  stepReader.NbShapes();
	std::cout << "STEPReader: Number of shapes: " << nbs << std::endl;

	topoDSShape = stepReader.OneShape();

	return topoDSShape;
}
