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

#include <TopoDS_Compound.hxx>
#include <BRep_Builder.hxx>
#include <TopExp_Explorer.hxx>
#include <TopoDS_Shape.hxx>
#include <TopoDS_Face.hxx>
#include <TopoDS.hxx>

int main() {
	/// Alter the following based on where OCF source-code is located on your system
	//setenv("CSF_PluginDefaults", "/home/friedrich/Programme/OpenCascade/git/oce-master/src/StdResource", 1);
	//setenv("CSF_XCAFDefaults", "/home/friedrich/Programme/OpenCascade/git/oce-master/src/StdResource", 1);

	///File:
	std::string filePath =
			"./Testing/TestFiles/x-wing-fighter-star-wars.snapshot.11/";
	std::string fileName = "X-Wing-complete.igs";
	std::string file = filePath + fileName;

	/// Read file
	IGESCAFControl_Reader igesCAFReader;

	Handle_TDocStd_Document aDoc;
	Handle_XCAFApp_Application anApp = XCAFApp_Application::GetApplication();
	anApp->NewDocument("MDTV-XCAF", aDoc);
	IFSelect_ReturnStatus returnStatus = igesCAFReader.ReadFile(file.c_str());
	switch (returnStatus) {
	case IFSelect_RetDone:
		std::cout << "IGESReader: File read successful" << std::endl;
		break;
	default:
		std::cout << "IGESReader: File read not succesful!" << std::endl;
		exit(-1);
	}
	if (igesCAFReader.Transfer(aDoc)) {
		std::cout << "COLORDETECTION: Transfer succeded!" << std::endl;
	} else {
		std::cout << "COLORDETECTION: Transfer failed!" << std::endl;
		exit(-1);
	}
	Handle_XCAFDoc_ShapeTool myAssembly = XCAFDoc_DocumentTool::ShapeTool(aDoc->Main());
	TDF_LabelSequence aLabel;
	myAssembly->GetShapes(aLabel);

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
	for (TopExp_Explorer ex(shape, TopAbs_FACE); ex.More(); ex.Next()) {
		Quantity_Color color;
		const TopoDS_Face &face = TopoDS::Face(ex.Current());
		myColors->SetColor(face, col2, ctype);
		if (myColors->IsSet(face, ctype)
				/*|| myColors->IsSet(face, XCAFDoc_ColorSurf)
				|| myColors->IsSet(face, XCAFDoc_ColorCurv)*/) {
			myColors->GetColor(face, XCAFDoc_ColorGen, color);
			std::cout << "YES Color "<< color.Red()<< " " << color.Green()  << " " << color.Blue() << std::endl;
		}else{
			std::cout << "No Color" << std::endl;
		}
	}


	return EXIT_SUCCESS;
}
