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

#include "Reader/Reader.hpp"
#include "Reader/IGESCAFReader.hpp"
#include "Voxelizer/Voxelizer.hpp"
#include "Writer/Writer_VTK.hpp"
#include <Voxel_BoolDS.hxx>
#include <IGESControl_Reader.hxx>
#include <Quantity_Color.hxx>
#include "ColorHandler/ColorHandler.hpp"

int main(void){
	///File:
	std::string filePath = "./Testing/TestFiles/x-wing-fighter-star-wars.snapshot.11/";
	std::string fileName = "X-Wing-complete.igs";
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
	Quantity_Color col = colorDetector.getColor();

    /// Voxelize file
    Voxelizer voxelizer;
    int refinementLevel = 0;
    Voxel_BoolDS voxelShape = voxelizer.voxelize(shape, refinementLevel);

    /// Write output
    Writer_VTK writer_vtk("output");
    writer_vtk.write(voxelShape);

	return EXIT_SUCCESS;
}
