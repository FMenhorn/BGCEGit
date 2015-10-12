/*
 * ColorDetector.cpp
 *
 *  Created on: Oct 7, 2015
 *      Author: friedrich
 */

#include "ColorHandler.hpp"

#include "../Helper/Helper.hpp"

#include <IGESCAFControl_Reader.hxx>
#include <XCAFApp_Application.hxx>
#include <Handle_XCAFApp_Application.hxx>
#include <XCAFDoc_DocumentTool.hxx>
#include <Handle_TDocStd_Document.hxx>
#include <BRepTools.hxx>

#include <gp_Vec.hxx>
#include <gp_Dir.hxx>
#include <BRepPrimAPI_MakePrism.hxx>
#include <Handle_Geom_Surface.hxx>
#include <GeomLProp_SLProps.hxx>

#include <TopoDS_Compound.hxx>
#include <BRep_Builder.hxx>
#include <BRepBuilderAPI_Sewing.hxx>
#include <TopExp_Explorer.hxx>
#include <BRepBuilderAPI_MakeFace.hxx>
#include <TopAbs_Orientation.hxx>
#include <BRepOffsetAPI_MakeOffsetShape.hxx>
#include <BRepPrimAPI_MakeBox.hxx>

#include <TopoDS.hxx>
#include <TopoDS_Face.hxx>
#include <TopoDS_Shape.hxx>

#include <Bnd_Box.hxx>
#include <BRepBndLib.hxx>

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

void ColorHandler::getFixtureShapes(TopTools_ListOfShape& listOfShapes) {
	Quantity_Color red(1,1,1,Quantity_TOC_RGB);
	getColoredFaces(listOfShapes, red);
}

void ColorHandler::getPassiveShapes(TopTools_ListOfShape& listOfShapes) {
	Quantity_Color green(0,1,0,Quantity_TOC_RGB);
	getColoredFaces(listOfShapes, green);
}

void ColorHandler::getLoadShapes(TopTools_ListOfShape& listOfShapes) {
	Quantity_Color blue(0,0,1,Quantity_TOC_RGB);
	getColoredFaces(listOfShapes, blue);
}

void ColorHandler::getColoredFaces(TopTools_ListOfShape& listOfShapes,const Quantity_Color wantedColor) {
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
	std::vector<TopoDS_Face> tmpVector;
	//BRepBuilderAPI_Sewing bRepSewer;
	int i = 0;
	for (TopExp_Explorer ex(shape, TopAbs_FACE); ex.More(); ex.Next()) {
		const TopoDS_Face &face = TopoDS::Face(ex.Current());
		if (myColors->IsSet(face, ctype)
				|| myColors->IsSet(face, XCAFDoc_ColorSurf)
				|| myColors->IsSet(face, XCAFDoc_ColorCurv)) {
			myColors->GetColor(face, XCAFDoc_ColorGen, color);
			//if( (color.Red()==wantedColor.Red() && color.Green()==wantedColor.Green() && color.Blue()==wantedColor.Blue())){
				//bRepSewer.Add(face);
			//if(i%2!=0){
				tmpVector.push_back(face);
				std::cout << "YES Color found "<< color.Red()<< " " << color.Green()  << " " << color.Blue() << std::endl;
			//}
			//}
		}else{
			std::cout << "No Color" << std::endl;
		}
		i++;
	}
	/**If we want to sew the faces together
		bRepSewer.SetFaceMode(false);
		bRepSewer.Perform();
		sewedShape = bRepSewer.SewedShape();
	**/

    Standard_Real umin, umax, vmin, vmax;
	double Xmin, Ymin, Zmin, Xmax, Ymax, Zmax; // Bounding box bounds
	for(size_t i = 0; i < tmpVector.size(); ++i){
		std::cout << "i: " << i << std::endl;
		gp_Vec extrudVec;
		computeNormal(tmpVector[i], extrudVec);
		//if(i == 1){
		//	extrudVec.SetX(-1);
		//}
	    std::cout << "NormalVec: [" << extrudVec.X()<< "," << extrudVec.Y() << ","<< extrudVec.Z() << "]" << std::endl;
	    const TopoDS_Face tmpFace = tmpVector[i];
	    BRepBuilderAPI_Sewing bRepSewer;
	    bRepSewer.Add(tmpFace);
	    bRepSewer.SetFaceMode(false);
		bRepSewer.Perform();
		shape = bRepSewer.SewedShape();
		Bnd_Box B; // Bounding box
	    BRepBndLib::Add(shape, B);
	    B.Get(Xmin, Ymin, Zmin, Xmax, Ymax, Zmax);
	    bool xEq = absolut(Xmin-Xmax) < 0.000001;
	    bool yEq = absolut(Ymin-Ymax) < 0.000001;
	    bool zEq = absolut(Zmin-Zmax) < 0.000001;
	    std::cout << "    X[" << Xmin << ", " << Xmax << "]     " << "Equality: " << xEq << std::endl;
	    std::cout << "    Y[" << Ymin << ", " << Ymax << "]     " << "Equality: " << yEq << std::endl;
	    std::cout << "    Z[" << Zmin << ", " << Zmax << "]     " << "Equality: " << zEq << std::endl;
	    gp_Pnt boxOrig(Xmin,Ymin,Zmin);
	    double dx,dy,dz;
	    dx = xEq ? 1 : Xmax-Xmin;
	    dy = yEq ? 1 : Ymax-Ymin;
	    dz = zEq ? 1 : Zmax-Zmin;
	    BRepPrimAPI_MakeBox madeBox(boxOrig,dx,dy,dz);
	    madeBox.Build();
	    const TopoDS_Shape &extrudedFace = madeBox.Shape();

	    /*BRepPrimAPI_MakePrism mkPrism(tmpFace, extrudVec);
	    mkPrism.Build();
		const TopoDS_Shape &extrudedFace = mkPrism.Shape();*/
	    //Bnd_Box B; // Bounding box
		double Xmin, Ymin, Zmin, Xmax, Ymax, Zmax; // Bounding box bounds
		Bnd_Box B2; // Bounding box
	    BRepBndLib::Add(extrudedFace, B2);
	    B2.Get(Xmin, Ymin, Zmin, Xmax, Ymax, Zmax);
	    std::cout << "    X[" << Xmin << ", " << Xmax << "]     "<< std::endl;
	    std::cout << "    Y[" << Ymin << ", " << Ymax << "]     "<< std::endl;
	    std::cout << "    Z[" << Zmin << ", " << Zmax << "]     "<< std::endl;
		listOfShapes.Append(extrudedFace);
	}
}

void ColorHandler::computeNormal(const TopoDS_Face& findNormalTo, gp_Vec& normal) {
    Standard_Real umin, umax, vmin, vmax;
    BRepTools::UVBounds(findNormalTo, umin, umax, vmin, vmax);
    std::cout << "Umin: " << umin << "Umax: " << umax << "Vmin " << vmin << "Vmax " << vmax << std::endl;
    Handle_Geom_Surface surf = BRep_Tool::Surface(findNormalTo); // create surface
    GeomLProp_SLProps props(surf, umin, vmin, 1, 0.01); // get surface properties
    normal = props.Normal(); // get surface normal
    if(findNormalTo.Orientation() == TopAbs_REVERSED) normal.Reverse(); // check orientation
    std::cout << "NormalVec: [" << normal.X()<< "," << normal.Y() << ","<< normal.Z() << "]" << std::endl;
}

bool ColorHandler::isDocumentValid() {
	return XCAFDoc_DocumentTool::IsXCAFDocument(aDoc);
}
