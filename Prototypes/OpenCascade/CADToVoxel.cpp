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
#include "Reader/STEPReader.hpp"
#include "Reader/IGESReader.hpp"
#include "Voxelizer/Voxelizer.hpp"
#include "Writer/Writer_VTK.hpp"

#include <Voxel_BoolDS.hxx>
#include <STEPControl_Reader.hxx>

int main(void){
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


    /// Voxelize file
    Voxelizer voxelizer;
    int refinementLevel = 0;
    Voxel_BoolDS voxelShape = voxelizer.voxelize(shape, refinementLevel);

    /// Write output
    Writer_VTK writer_vtk("output");
    writer_vtk.write(voxelShape);

	return EXIT_SUCCESS;
}
