#include <iostream>
#include <stdlib.h>
#include <string>

#include <IGESCAFControl_Reader.hxx>
#include <TDocStd_Document.hxx>
#include <Handle_TDocStd_Document.hxx>
#include <XCAFApp_Application.hxx>
#include <Handle_XCAFApp_Application.hxx>
#include <XCAFDoc_ShapeTool.hxx>
#include <Handle_XCAFDoc_ShapeTool.hxx>
#include <XCAFDoc_DocumentTool.hxx>
#include <Handle_TDocStd_Document.hxx>
#include <Quantity_Color.hxx>
#include <XCAFDoc_ColorTool.hxx>
#include <TDF_LabelSequence.hxx>
#include <BRepBuilderAPI_Sewing.hxx>
#include <STEPControl_Writer.hxx>
#include <STEPControl_StepModelType.hxx>
#include <BRepBuilderAPI_MakeSolid.hxx>

#include <TopoDS_Compound.hxx>
#include <BRep_Builder.hxx>
#include <TopExp_Explorer.hxx>
#include <TopoDS_Shape.hxx>
#include <TopoDS_Shell.hxx>
#include <TopoDS_Face.hxx>
#include <TopoDS.hxx>

int main() {
	/// Alter the following based on where OCF source-code is located on your system
	//setenv("CSF_PluginDefaults", "/home/friedrich/Programme/OpenCascade/git/oce-master/src/StdResource", 1);
	//setenv("CSF_XCAFDefaults", "/home/friedrich/Programme/OpenCascade/git/oce-master/src/StdResource", 1);

	///File:
	std::string filePath =
			"./Testing/TestFiles/circuit-board-pcb-mock-example.snapshot.4/";
	std::string fileName = "Buoy_Circuitbuoy.igs";
	std::string file = filePath + fileName;

	/// Read file using IGESACFControl_Reader
	IGESCAFControl_Reader igesCAFReader;
	IFSelect_ReturnStatus returnStatus = igesCAFReader.ReadFile(file.c_str());
	switch (returnStatus) {
	case IFSelect_RetDone:
		std::cout << "COLORDETECTION: File read successful" << std::endl;
		break;
	default:
		std::cout << "COLORDETECTION: File read not succesful!" << std::endl;
		exit(-1);
	}

    /// Transfer the file to a Document
    Handle_TDocStd_Document aDoc;
	Handle_XCAFApp_Application anApp = XCAFApp_Application::GetApplication();
	anApp->NewDocument("MDTV-XCAF", aDoc);
	if (igesCAFReader.Transfer(aDoc)) {
		std::cout << "COLORDETECTION: Transfer succeded!" << std::endl;
	} else {
		std::cout << "COLORDETECTION: Transfer failed!" << std::endl;
		exit(-1);
	}

    /// ShapeTool for holding and handling STEP/IGES assembly
	Handle_XCAFDoc_ShapeTool myAssembly = XCAFDoc_DocumentTool::ShapeTool(aDoc->Main());
	TDF_LabelSequence aLabel;
	myAssembly->GetShapes(aLabel); // aLabel holds sequence of shapes held in the assembly

    /// If only one label, assign it. If multiple, assign a compound.
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

    BRepBuilderAPI_Sewing shellMaker(0.001);

    /// Create an explorer object to go through the shape. Explore each face, look for color, print it.
	XCAFDoc_ColorType ctype = XCAFDoc_ColorGen;
	Handle_XCAFDoc_ColorTool myColors = XCAFDoc_DocumentTool::ColorTool(aDoc->Main());
	for (TopExp_Explorer ex(shape, TopAbs_FACE); ex.More(); ex.Next()) {
		Quantity_Color color;
		const TopoDS_Face &face = TopoDS::Face(ex.Current());

		if (myColors->IsSet(face, ctype)) {
			myColors->GetColor(face, XCAFDoc_ColorGen, color);
			std::cout << "YES Color "<< color.Red()<< " " << color.Green()  << " " << color.Blue() << std::endl;
			shellMaker.Add(face);
		} else {
			std::cout << "No Color" << std::endl;
		}
	}

    shellMaker.Perform();
    TopoDS_Shape temp = shellMaker.SewedShape();

    STEPControl_Writer writer;
    STEPControl_StepModelType mode = STEPControl_AsIs;
    IFSelect_ReturnStatus stat = writer.Transfer(temp, mode);

    std::cout << std::endl << stat << std::endl;

    stat = writer.Write("checkOuterFaces.stp");

    std::cout << std::endl << stat << std::endl;

	return EXIT_SUCCESS;
}
