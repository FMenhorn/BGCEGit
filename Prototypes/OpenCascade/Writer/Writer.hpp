/*
 * STEPReader.hpp
 *
 *  Created on: Oct 6, 2015
 *      Author: saumitra
 */

#ifndef _WRITER_
#define _WRITER_

#include <string>

#include <Voxel_BoolDS.hxx>

class Writer{
public:
    Writer(std::string _filename) : filename(_filename) {}

    virtual ~Writer() {};

    virtual bool write(Voxel_BoolDS &voxelShape) = 0;

protected:
    std::string filename;
};

#endif // _WRITER_
