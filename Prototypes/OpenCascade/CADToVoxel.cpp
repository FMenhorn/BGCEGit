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
#include <Quantity_Color.hxx>
#include <TopoDS_Face.hxx>

#include "Reader/Reader.hpp"
#include "Reader/IGESCAFReader.hpp"
#include "Voxelizer/Voxelizer.hpp"
#include "Writer/Writer_VTK.hpp"
#include "ColorHandler/ColorHandler.hpp"

int main(void){
	///File:
	std::string filePath = "./TestGeometry/circuit-board-pcb-mock-example.snapshot.4/";
	std::string fileName = "Buoy_Circuitbuoy.igs";
	std::string file = filePath + fileName;
    /// Read file
    Reader* reader;
    if(fileName.find(".igs")!=std::string::npos){
    	reader = new IGESCAFReader();
    }else{
    	std::cout << "CADToVoxel: Wrong type of input file. Neither .stp nor .igs" << std::endl;
    	return EXIT_FAILURE;
    }
	TopoDS_Shape shape = reader->read(file);
	ColorHandler colorDetector;
	reader->transfer(colorDetector.getDoc());
	colorDetector.initializeMembers();
	std::vector<TopoDS_Face> facesVector;
	colorDetector.getColoredFaces(facesVector);

    /// Voxelize file
    Voxelizer voxelizer;
    int refinementLevel = 0;
    Voxel_BoolDS voxelShape;
    for(size_t i = 0; i < facesVector.size(); ++i){
		voxelShape = voxelizer.voxelize(facesVector[i], refinementLevel);

		/// Write output
		Writer_VTK writer_vtk("output"+ std::to_string(i));
		writer_vtk.write(voxelShape);
    }
	return EXIT_SUCCESS;
}
