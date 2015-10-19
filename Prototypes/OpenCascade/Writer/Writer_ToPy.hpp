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
#include <vector>

#include <TopoDS_Shape.hxx>
#include <Voxel_BoolDS.hxx>
#include <Voxel_FastConverter.hxx>
#include <Bnd_Box.hxx>
#include <BRepBndLib.hxx>

class Writer_ToPy: public Writer{
public:
    Writer_ToPy() : Writer() {};

    ~Writer_ToPy() {this->~Writer();};

    bool write(std::string _filename, std::vector<std::vector<VoxelShape>> &voxelShape);

private:
    void writeHeader(std::ofstream &outfile, std::string _filename);
    void writeGreyScaleFilters(std::ofstream &outfile);
    void writeDimensions(std::ofstream &outfile,std::vector<int> dimensions);
    int writeNodes(std::string name, std::ofstream &outfile, std::vector<VoxelShape> &voxelShape, std::vector<int> dimensions); //later change to vector of shapes
    int getIndex(int x, int y, int z, std::vector<int> dimensions);
};
#endif // _WRITER_TOPY_
