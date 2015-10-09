/*
 * CADtoVoxel.cpp
 *
 *  Created on: Oct 6, 2015
 *      Author: BGCE
 */


#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <iostream>
#include <vector>

#include <Voxel_BoolDS.hxx>
#include <IGESControl_Reader.hxx>
#include <TopoDS.hxx>
#include <TopoDS_Face.hxx>
#include <TopoDS_Solid.hxx>
#include <STEPControl_StepModelType.hxx>
#include <STEPControl_Writer.hxx>
#include <STEPControl_Reader.hxx>

#include <BRepOffset_MakeOffset.hxx>
#include <BRepOffsetAPI_MakeThickSolid.hxx>
#include <BRepBuilderAPI_MakeSolid.hxx>

#include "Reader/Reader.hpp"
#include "Reader/IGESCAFReader.hpp"
#include "Reader/STEPCAFReader.hpp"
#include "Voxelizer/Voxelizer.hpp"
#include "Writer/Writer_VTK.hpp"
#include "ColorHandler/ColorHandler.hpp"

int main(void){
	///File:
	std::string filePath = "./TestGeometry/";
	std::string fileName = "BlackWhiteCube.igs";
	std::string file = filePath + fileName;
    /// Read file
    Reader* reader;
    if(fileName.find(".igs")!=std::string::npos){
    	reader = new IGESCAFReader();
    }else if(fileName.find(".stp")!=std::string::npos || fileName.find(".step")!=std::string::npos){
    	reader = new STEPCAFReader();
    }else{
    	std::cout << "CADToVoxel: Wrong type of input file. Neither .stp nor .igs" << std::endl;
    	return EXIT_FAILURE;
    }
	reader->read(file);
	ColorHandler colorDetector;
	reader->transfer(colorDetector.getDoc());
	colorDetector.initializeMembers();
	std::vector<TopoDS_Face> facesVector;
	TopoDS_Shape sewedShape;

	TopTools_ListOfShape facesList;
	colorDetector.getColoredFaces(facesList, sewedShape);

	STEPControl_Writer stepWriter;
	stepWriter.Transfer(sewedShape, STEPControl_AsIs);
	stepWriter.Write("sewed.stp");

    /// Voxelize file
    Voxelizer voxelizer;
    int refinementLevel = 0;
    Voxel_BoolDS voxelShape = voxelizer.voxelize(sewedShape, refinementLevel);
    Writer_VTK writer_vtk("outputSewed");
	writer_vtk.write(voxelShape);
	return EXIT_SUCCESS;
}
