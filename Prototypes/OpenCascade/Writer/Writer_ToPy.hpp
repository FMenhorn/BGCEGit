/*
 * STEPReader.hpp
 *
 *  Created on: Oct 6, 2015
 *      Author: saumitra
 */

#ifndef _WRITER_TOPY_
#define _WRITER_TOPY_

#include "Writer.hpp"

#include <stdlib.h>
#include <iostream>
#include <math.h>

#include <TopoDS_Shape.hxx>
#include <Voxel_BoolDS.hxx>
#include <Voxel_FastConverter.hxx>
#include <Bnd_Box.hxx>
#include <BRepBndLib.hxx>

class Writer_ToPy: public Writer{
public:
    Writer_ToPy() : Writer() {}

    ~Writer_ToPy() {this->~Writer();}

    bool write(std::string _filename, Voxel_BoolDS &voxelShape);
};

#endif // _WRITER_TOPY_
