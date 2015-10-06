#ifndef _WRITER_TOPY_
#define _WRITER_TOPY_

#include <stdlib.h>
#include <iostream>
#include <math.h>

#include <TopoDS_Shape.hxx>
#include <Voxel_BoolDS.hxx>
#include <Voxel_FastConverter.hxx>
#include <Bnd_Box.hxx>
#include <BRepBndLib.hxx>

class Writer_ToPy: public Writer{
    bool write(Voxel_BoolDS voxelShape);
};

#endif // _WRITER_TOPY_
