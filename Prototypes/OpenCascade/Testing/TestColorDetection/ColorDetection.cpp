#include <iostream>
#include <stdlib.h>

#include <TDocStd_Document.hxx>
#include <TDocStd_Document.hxx>
#include <Handle_TDocStd_Document.hxx>
#include <XCAFApp_Application.hxx>
#include <Handle_XCAFApp_Application.hxx>
#include <XCAFDoc_ShapeTool.hxx>
#include <Handle_XCAFDoc_ShapeTool.hxx>
#include <XCAFDoc_DocumentTool.hxx>

#include "../../Reader/Reader.hpp"
#include "../../Reader/STEPReader.hpp"
#include "../../Reader/IGESReader.hpp"

int main() {
    /// Alter the following based on where OCF source-code is located on your system
    //setenv("CSF_PluginDefaults", "/home/saumi/Academica/BGCE/OpenCascade/oce/src/StdResource/", 1);
    //setenv("CSF_XCAFDefaults", "/home/saumi/Academica/BGCE/OpenCascade/oce/src/StdResource/", 1);

    ///File:
	std::string filePath = "./TestGeometry/circuit-board-pcb-mock-example.snapshot.4/";
	std::string fileName = "Buoy_Circuitbuoy.igs";
	std::string file = filePath + fileName;

    /// Read file
    Reader* reader;
    if(fileName.find(".stp")!=std::string::npos){
    	reader = new STEPReader();
    }else if(fileName.find(".igs")!=std::string::npos){
    	reader = new IGESReader();
    }else{
    	std::cout << "CADToVoxel: Wrong type of input file. Neither .stp nor .igs" << std::endl;
    	return EXIT_FAILURE;
    }
	TopoDS_Shape shape = reader->read(file);

    Handle(TDocStd_Document) aDoc;
    Handle(XCAFApp_Application) anApp = XCAFApp_Application::GetApplication();
    anApp->NewDocument("MDTV-XCAF", aDoc);

    // Create label and add our shape
    Handle (XCAFDoc_ShapeTool) myShapeTool = XCAFDoc_DocumentTool::ShapeTool(aDoc->Main());
    TDF_Label aLabel = myShapeTool->NewShape();
    myShapeTool->SetShape(aLabel, shape);

    if (XCAFDoc_DocumentTool::IsXCAFDocument(aDoc)) {
        std::cout << "... yes ..." << std::endl;
    }

    return EXIT_SUCCESS;
}
