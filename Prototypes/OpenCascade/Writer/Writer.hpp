/*
 * STEPReader.hpp
 *
 *  Created on: Oct 6, 2015
 *      Author: saumitra
 */

#ifndef _WRITER_
#define _WRITER_

#include <string>

#include "../Voxelizer/VoxelShape.hpp"

class Writer{
public:
    Writer() {};

    virtual ~Writer() {};

    virtual bool write(std::string _filename, VoxelShape &voxelShape) = 0;

protected:
};

#endif // _WRITER_
