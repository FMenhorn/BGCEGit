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
#include <TopoDS_Shell.hxx>
#include <TopLoc_Location.hxx>
#include <TopLoc_Datum3D.hxx>

#include <Bnd_Box.hxx>
#include <BRepBndLib.hxx>
#include <BRepBuilderAPI_Transform.hxx>
#include <BRepOffsetAPI_MakeThickSolid.hxx>

ColorHandler::ColorHandler() {
    Handle_XCAFApp_Application anApp = XCAFApp_Application::GetApplication();
    anApp->NewDocument("MDTV-XCAF", aDocStep);
    anApp->NewDocument("MDTV-XCAF", aDocIges);
}

ColorHandler::~ColorHandler() {
	// TODO Auto-generated destructor stub
}


Handle_TDocStd_Document& ColorHandler::getDocStep(){
	return aDocStep;
}

Handle_TDocStd_Document& ColorHandler::getDocIges(){
	return aDocIges;
}

void ColorHandler::initializeMembers() {
	// Create label and add our shape
	myAssemblyStep = XCAFDoc_DocumentTool::ShapeTool(aDocStep->Main());
	myAssemblyStep->GetShapes(aLabelStep);

	myAssemblyIges = XCAFDoc_DocumentTool::ShapeTool(aDocIges->Main());
	myAssemblyIges->GetShapes(aLabelIges);
}

void ColorHandler::getFixtureShapes(TopTools_ListOfShape& listOfShapes) {
	Quantity_Color red(1,0,0,Quantity_TOC_RGB);
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
	TopoDS_Shape shapeStep;
	if (aLabelStep.Length() == 1) {
		TopoDS_Shape result = myAssemblyStep->GetShape(aLabelStep.Value(1));
		shapeStep = result;
	} else {
		TopoDS_Compound C;
		BRep_Builder B;
		B.MakeCompound(C);
		for (Standard_Integer i = 1; i < aLabelStep.Length(); ++i) {
			TopoDS_Shape S = myAssemblyStep->GetShape(aLabelStep.Value(i));
			B.Add(C, S);
		}
		shapeStep = C;
	}
	TopoDS_Shape shapeIges;
	if (aLabelIges.Length() == 1) {
		TopoDS_Shape result = myAssemblyStep->GetShape(aLabelIges.Value(1));
		shapeIges = result;
	} else {
		TopoDS_Compound C;
		BRep_Builder B;
		B.MakeCompound(C);
		for (Standard_Integer i = 1; i < aLabelIges.Length(); ++i) {
			TopoDS_Shape S = myAssemblyIges->GetShape(aLabelIges.Value(i));
			B.Add(C, S);
		}
		shapeIges = C;
	}
	XCAFDoc_ColorType ctype = XCAFDoc_ColorGen;
	Handle_XCAFDoc_ColorTool myColors = XCAFDoc_DocumentTool::ColorTool(aDocIges->Main());
	Quantity_Color color;
	std::vector<TopoDS_Face> coloredFacesVector;
	std::vector<TopoDS_Face> allFacesVector;
	//BRepBuilderAPI_Sewing bRepSewer;
	int i = 0;
	TopExp_Explorer exStep(shapeStep, TopAbs_FACE);
	TopExp_Explorer exIges(shapeIges, TopAbs_FACE);
	for (; exStep.More(); exStep.Next()) {
		const TopoDS_Face &faceStep = TopoDS::Face(exStep.Current());
		const TopoDS_Face &faceIges = TopoDS::Face(exIges.Current());
		if (myColors->IsSet(faceIges, ctype)
				|| myColors->IsSet(faceIges, XCAFDoc_ColorSurf)
				|| myColors->IsSet(faceIges, XCAFDoc_ColorCurv)) {
			myColors->GetColor(faceIges, XCAFDoc_ColorGen, color);
			if( (color.Red()==wantedColor.Red() && color.Green()==wantedColor.Green() && color.Blue()==wantedColor.Blue())){
				//bRepSewer.Add(face);
				coloredFacesVector.push_back(faceStep);
				std::cout << "YES Color found "<< color.Red()<< " " << color.Green()  << " " << color.Blue() << std::endl;
			}
		}else{
			std::cout << "No Color" << std::endl;
		}
		exIges.Next();
		i++;
	}
	/**If we want to sew the faces together
		bRepSewer.SetFaceMode(false);
		bRepSewer.Perform();
		sewedShape = bRepSewer.SewedShape();
	**/

	for(size_t i = 0; i < coloredFacesVector.size(); ++i){
		std::cout << "i: " << i << std::endl;
		gp_Vec extrudVec;
		computeInvertedNormal(coloredFacesVector[i], extrudVec);

	    TopoDS_Face tmpFace = coloredFacesVector[i];

	    /**For output of bounding box**/
	    /*BRepBuilderAPI_Sewing bRepSewer;
	    bRepSewer.Add(tmpFace);
	    bRepSewer.SetFaceMode(false);
		bRepSewer.Perform();
		shape = bRepSewer.SewedShape();
		Bnd_Box B1; // Bounding box
	    BRepBndLib::Add(shape, B1);
	    B1.Get(Xmin, Ymin, Zmin, Xmax, Ymax, Zmax);
	    bool xEq = absolut(Xmin-Xmax) < 0.000001;
	    bool yEq = absolut(Ymin-Ymax) < 0.000001;
	    bool zEq = absolut(Zmin-Zmax) < 0.000001;
	    std::cout << "    X[" << Xmin << ", " << Xmax << "]     " << "Equality: " << xEq << std::endl;
	    std::cout << "    Y[" << Ymin << ", " << Ymax << "]     " << "Equality: " << yEq << std::endl;
	    std::cout << "    Z[" << Zmin << ", " << Zmax << "]     " << "Equality: " << zEq << std::endl;*/

	    /**First Solution**/
	    //TopLoc_Location location = tmpFace.Location();
	    //Handle_TopLoc_Datum3D defaultDatum;
	    //TopLoc_Location defaultLocation(defaultDatum);
	    //tmpFace.Move(defaultLocation);
	    BRepPrimAPI_MakePrism mkPrism(tmpFace, extrudVec, Standard_False, Standard_True);
		const TopoDS_Shape &extrudedFace = mkPrism.Shape();

		/**Second Solution**/
	    /*BRepBuilderAPI_Sewing bRepSewer;
	    bRepSewer.Add(tmpFace);
	    bRepSewer.SetFaceMode(false);
		bRepSewer.Perform();
		shape = bRepSewer.SewedShape();
		Bnd_Box B1; // Bounding box
	    BRepBndLib::Add(shape, B1);
	    B1.Get(Xmin, Ymin, Zmin, Xmax, Ymax, Zmax);
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
	    */

	    /**Third solution**/
    	/*TopTools_ListOfShape removeFaces;
	    for(size_t j = 0; j < allFacesVector.size(); ++j){
	    	if(allFacesVector[j].IsNotEqual(tmpFace)){
	    		removeFaces.Append(allFacesVector[j]);
	    	}
	    }
	    BRepOffsetAPI_MakeThickSolid bRepMakeThickSolid(shape, removeFaces, -1, 1.0e-3);
	    bRepMakeThickSolid.Build();
        const TopoDS_Shape &extrudedFace = bRepMakeThickSolid.Shape();
        removeFaces.Clear();*/

		/**For output of bounding box**/
		/*double Xmin, Ymin, Zmin, Xmax, Ymax, Zmax; // Bounding box bounds
		Bnd_Box B2; // Bounding box
	    BRepBndLib::Add(extrudedFace, B2);
	    B2.Get(Xmin, Ymin, Zmin, Xmax, Ymax, Zmax);
	    std::cout << "    X[" << Xmin << ", " << Xmax << "]     "<< std::endl;
	    std::cout << "    Y[" << Ymin << ", " << Ymax << "]     "<< std::endl;
	    std::cout << "    Z[" << Zmin << ", " << Zmax << "]     "<< std::endl;*/
		listOfShapes.Append(extrudedFace);
	}
}

void ColorHandler::computeInvertedNormal(const TopoDS_Face& findNormalTo, gp_Vec& normal) {
    Standard_Real umin, umax, vmin, vmax;
    BRepTools::UVBounds(findNormalTo, umin, umax, vmin, vmax);
    std::cout << "ColorHandler::computeInvertedNormal: Umin: " << umin << "Umax: " << umax << "Vmin " << vmin << "Vmax " << vmax << std::endl;
    Handle_Geom_Surface surf = BRep_Tool::Surface(findNormalTo); // create surface
    GeomLProp_SLProps props(surf, umin, vmin, 1, 0.01); // get surface properties
    normal = props.Normal(); // get surface normal
    if(findNormalTo.Orientation() == TopAbs_REVERSED){
    	std::cout << "ColorHandler::computeInvertedNormal: Reversing Normal vector" << std::endl;
    	normal.Reverse(); // check orientation
    }
    normal.Multiply(-1);
    std::cout << "ColorHandler::computeInvertedNormal: InvertedNormalVec: [" << normal.X()<< "," << normal.Y() << ","<< normal.Z() << "]" << std::endl;
}

bool ColorHandler::areDocumentsValid() {
	return XCAFDoc_DocumentTool::IsXCAFDocument(aDocStep) && XCAFDoc_DocumentTool::IsXCAFDocument(aDocIges) ;
}
