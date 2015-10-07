/*
 * STEPReader.cpp
 *
 *  Created on: Oct 6, 2015
 *      Author: friedrich
 */

#include "STEPReader.hpp"

#include <iostream>

STEPReader::STEPReader(): Reader() {
    xsReader = new STEPControl_Reader();
}

STEPReader::~STEPReader() {
	this->~Reader();
}

TopoDS_Shape STEPReader::read(const std::string filename) {

    TopoDS_Shape topoDSShape;

	IFSelect_ReturnStatus returnStatus = xsReader->ReadFile(filename.c_str());
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
	xsReader->PrintCheckLoad(failsonly, mode);
	std::cout << "STEPReader: Mode: " << mode << std::endl;

	Standard_Integer ic =  Interface_Static::IVal("read.precision.mode");
	std::cout << "STEPReader: ic: " << ic << std::endl;

	Handle_TColStd_HSequenceOfTransient list = xsReader->GiveList();
	Standard_Integer nbtrans =  xsReader->TransferList(list);
	std::cout << "STEPReader: Number of translations: " << nbtrans << std::endl;
	Standard_Integer nbs =  xsReader->NbShapes();
	std::cout << "STEPReader: Number of shapes: " << nbs << std::endl;

	topoDSShape = xsReader->OneShape();

	return topoDSShape;
}
