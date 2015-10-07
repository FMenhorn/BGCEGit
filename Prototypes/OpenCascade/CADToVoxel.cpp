/*
 * CADtoVoxel.cpp
 *
 *  Created on: Oct 6, 2015
 *      Author: BGCE
 */


#include <stdio.h>
#include <stdlib.h>
#include <iostream>

#include "Reader/Reader.hpp"
#include "Reader/STEPReader.hpp"
#include "Reader/IGESReader.hpp"
#include "Voxelizer/Voxelizer.hpp"
#include "Writer/Writer_VTK.hpp"

#include <Voxel_BoolDS.hxx>
#include <STEPControl_Reader.hxx>

int main(void){
    /// Read file
	//STEPControl_Reader ocreader;
	//Reader* reader = new STEPReader(&ocreader);
	//TopoDS_Shape shape = reader->read("./TestGeometry/circuit-board-pcb-mock-example.snapshot.4/Buoy_Circuitbuoy.stp");
	//IGESControl_Reader ocreader;
	XSControl_Reader* ocReader = new STEPControl_Reader();
	Reader* reader = new IGESReader(ocReader);
	TopoDS_Shape shape = reader->read("./TestGeometry/circuit-board-pcb-mock-example.snapshot.4/Buoy_Circuitbuoy.igs");


    /// Voxelize file
    Voxelizer voxelizer;
    int refinementLevel = 0;
    Voxel_BoolDS voxelShape = voxelizer.voxelize(shape, refinementLevel);

    /// Write output
    Writer_VTK writer_vtk("output");
    writer_vtk.write(voxelShape);

	return EXIT_SUCCESS;
}
