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
#include <BRepTools.hxx>

#include <gp_Vec.hxx>
#include <gp_Dir.hxx>
#include <Handle_Geom_Surface.hxx>
#include <GeomLProp_SLProps.hxx>

#include <TopoDS_Compound.hxx>
#include <BRep_Builder.hxx>
#include <BRepBuilderAPI_Sewing.hxx>
#include <TopExp_Explorer.hxx>

#include <TopoDS.hxx>
#include <TopoDS_Face.hxx>
#include <TopoDS_Shape.hxx>

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

void ColorHandler::getColoredFaces(TopTools_ListOfShape& faceVector, TopoDS_Shape& sewedShape) {
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
	BRepBuilderAPI_Sewing bRepSewer;
	for (TopExp_Explorer ex(shape, TopAbs_FACE); ex.More(); ex.Next()) {
		const TopoDS_Face &face = TopoDS::Face(ex.Current());
		if (myColors->IsSet(face, ctype)
				|| myColors->IsSet(face, XCAFDoc_ColorSurf)
				|| myColors->IsSet(face, XCAFDoc_ColorCurv)) {
			myColors->GetColor(face, XCAFDoc_ColorGen, color);
			if( (color.Red()==0 && color.Green()==0 && color.Blue()==0)){
				faceVector.Append(face);
				bRepSewer.Add(face);
				std::cout << "YES Color "<< color.Red()<< " " << color.Green()  << " " << color.Blue() << std::endl;
			}
		}else{
			std::cout << "No Color" << std::endl;
		}
	}
	//bRepSewer.SetFloatingEdgesMode(true);
	bRepSewer.SetFaceMode(false);
	bRepSewer.Perform();
	sewedShape = bRepSewer.SewedShape();
}

void computeNormal(TopoDS_Face& findNormalTo, gp_Vec& normal) {
    Standard_Real umin, umax, vmin, vmax;
    BRepTools::UVBounds(findNormalTo, umin, umax, vmin, vmax);
    Handle_Geom_Surface surf = BRep_Tool::Surface(findNormalTo); // create surface
    GeomLProp_SLProps props(surf, umin, vmin, 1, 0.01); // get surface properties
    normal = props.Normal(); // get surface normal
    if(findNormalTo.Orientation() == TopAbs_REVERSED) normal.Reverse(); // check orientation
}

bool ColorHandler::isDocumentValid() {
	return XCAFDoc_DocumentTool::IsXCAFDocument(aDoc);
}
