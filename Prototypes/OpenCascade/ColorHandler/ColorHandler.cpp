/*
 * ColorDetector.cpp
 *
 *  Created on: Oct 7, 2015
 *      Author: friedrich
 */

#include "ColorHandler.hpp"

#include <IGESCAFControl_Reader.hxx>
#include <XCAFApp_Application.hxx>
#include <Handle_XCAFApp_Application.hxx>
#include <XCAFDoc_DocumentTool.hxx>
#include <Handle_TDocStd_Document.hxx>

#include <TopoDS_Compound.hxx>
#include <BRep_Builder.hxx>
#include <TopExp_Explorer.hxx>
#include <TopoDS_Shape.hxx>
#include <TopoDS.hxx>

ColorHandler::ColorHandler() {
    Handle_XCAFApp_Application anApp = XCAFApp_Application::GetApplication();
    anApp->NewDocument("MDTV-XCAF", aDoc);
}

ColorHandler::~ColorHandler() {
	// TODO Auto-generated destructor stub
}


Handle_TDocStd_Document& ColorHandler::getDoc(){
	return aDoc;
}

void ColorHandler::initializeMembers() {
	// Create label and add our shape
	myAssembly = XCAFDoc_DocumentTool::ShapeTool(aDoc->Main());
	myAssembly->GetShapes(aLabel);
}

void ColorHandler::getColoredFaces(std::vector<TopoDS_Face>& faceVector) {
	TopoDS_Shape shape;
	if (aLabel.Length() == 1) {
		TopoDS_Shape result = myAssembly->GetShape(aLabel.Value(1));
		shape = result;
	} else {
		TopoDS_Compound C;
		BRep_Builder B;
		B.MakeCompound(C);
		for (Standard_Integer i = 1; i < aLabel.Length(); ++i) {
			TopoDS_Shape S = myAssembly->GetShape(aLabel.Value(i));
			B.Add(C, S);
		}
		shape = C;
	}
	XCAFDoc_ColorType ctype = XCAFDoc_ColorGen;
	Handle_XCAFDoc_ColorTool myColors = XCAFDoc_DocumentTool::ColorTool(aDoc->Main());
	Quantity_Color color;
	for (TopExp_Explorer ex(shape, TopAbs_FACE); ex.More(); ex.Next()) {
		const TopoDS_Face &face = TopoDS::Face(ex.Current());
		if (myColors->IsSet(face, ctype)
				/*|| myColors->IsSet(face, XCAFDoc_ColorSurf)
				|| myColors->IsSet(face, XCAFDoc_ColorCurv)*/) {
			myColors->GetColor(face, XCAFDoc_ColorGen, color);
			faceVector.push_back(face);
			std::cout << "YES Color "<< color.Red()<< " " << color.Green()  << " " << color.Blue() << std::endl;
		}else{
			std::cout << "No Color" << std::endl;
		}
	}
}

bool ColorHandler::isDocumentValid() {
	return XCAFDoc_DocumentTool::IsXCAFDocument(aDoc);
}
