/*
 * STEPReader.cpp
 *
 *  Created on: Oct 6, 2015
 *      Author: saumitra
 */

#include "IGESReader.hpp"

#include <iostream>

IGESReader::IGESReader(IGESControl_Reader* igesControlReader): Reader(igesControlReader) {

}

IGESReader::~IGESReader() {
	this->~Reader();
}

TopoDS_Shape IGESReader::read(std::string filename) {

    TopoDS_Shape topoDSShape;
	IGESControl_Reader igesReader;

	IFSelect_ReturnStatus returnStatus = igesReader.ReadFile(filename.c_str());
	switch(returnStatus){
	case IFSelect_RetDone:
		std::cout << "IGESReader: File read successful" << std::endl;
		break;
	default:
		std::cout << "IGESReader: File read not succesful!" << std::endl;
		exit(-1);
	}
	Standard_Boolean failsonly = Standard_False;
	IFSelect_PrintCount mode;
	igesReader.PrintCheckLoad(failsonly, mode);
	std::cout << "IGESReader: Mode: " << mode << std::endl;

	Standard_Integer ic =  Interface_Static::IVal("read.iges.bspline.continuity");
	std::cout << "IGESReader: ic: " << ic << std::endl;

	Handle_TColStd_HSequenceOfTransient list = igesReader.GiveList();
	Standard_Integer nbtrans =  igesReader.TransferList(list);
	std::cout << "IGESReader: Number of translations: " << nbtrans << std::endl;
	Standard_Integer nbs =  igesReader.NbShapes();
	std::cout << "IGESReader: Number of shapes: " << nbs << std::endl;

	topoDSShape = igesReader.OneShape();

	return topoDSShape;
}
