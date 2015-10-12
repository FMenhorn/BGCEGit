/*
 * STEPReader.hpp
 *
 *  Created on: Oct 6, 2015
 *      Author: saumitra
 */

#ifndef _WRITER_VTK_
#define _WRITER_VTK_

#include "Writer.hpp"

#include <stdlib.h>
#include <iostream>
#include <math.h>

#include <TopoDS_Shape.hxx>
#include <Voxel_BoolDS.hxx>
#include <Voxel_FastConverter.hxx>
#include <Bnd_Box.hxx>
#include <BRepBndLib.hxx>

class Writer_VTK: public Writer{
public:
    Writer_VTK() : Writer() {}

    ~Writer_VTK() {this->~Writer();};

    bool write(std::string _filename, Voxel_BoolDS &voxelShape);

private:
    void writeHeader(std::ofstream &outfile);

	void writeStructuredGrid(std::ofstream &outfile, Voxel_BoolDS &voxelShape);

	void writeScalars(std::ofstream &outfile, Voxel_BoolDS &voxelShape);
};

#endif // _WRITER_VTK_
