/*
 * STEPCAFReader.cpp
 *
 *  Created on: Oct 7, 2015
 *      Author: friedrich
 */

#include "IGESCAFReader.hpp"

#include <IGESCAFControl_Reader.hxx>
#include <Interface_Static.hxx>
#include <Standard_CString.hxx>
#include <TDocStd_Document.hxx>
#include <Handle_TDocStd_Document.hxx>
#include <XCAFApp_Application.hxx>
#include <Handle_XCAFApp_Application.hxx>
#include <XCAFDoc_ShapeTool.hxx>
#include <Handle_XCAFDoc_ShapeTool.hxx>
#include <XCAFDoc_DocumentTool.hxx>
#include <Quantity_Color.hxx>
#include <XCAFDoc_ColorTool.hxx>

IGESCAFReader::IGESCAFReader(): Reader() {
	xsReader = new IGESCAFControl_Reader();
}

IGESCAFReader::~IGESCAFReader() {
	this->~Reader();
}

TopoDS_Shape IGESCAFReader::read(const std::string filename) {
	TopoDS_Shape topoDSShape;

	IFSelect_ReturnStatus returnStatus = xsReader->ReadFile(filename.c_str());
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
	xsReader->PrintCheckLoad(failsonly, mode);
	std::cout << "IGESReader: Mode: " << mode << std::endl;

	Standard_Integer ic =  Interface_Static::IVal("read.iges.bspline.continuity");
	std::cout << "IGESReader: ic: " << ic << std::endl;

	Handle_TColStd_HSequenceOfTransient list = xsReader->GiveList();
	Standard_Integer nbtrans =  xsReader->TransferList(list);
	std::cout << "IGESReader: Number of translations: " << nbtrans << std::endl;
	Standard_Integer nbs =  xsReader->NbShapes();
	std::cout << "IGESReader: Number of shapes: " << nbs << std::endl;

	topoDSShape = xsReader->OneShape();

	return topoDSShape;
}
