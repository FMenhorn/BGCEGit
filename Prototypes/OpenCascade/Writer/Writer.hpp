#ifndef _WRITER_
#define _WRITER_

#include <string>

#include <Voxel_BoolDS.hxx>

class Writer{
public:
    Writer(std::string _filename) : filename(_filename) {}

    ~Writer();

    virtual bool write(Voxel_BoolDS voxelShape) {
        int warningEliminator = voxelShape.GetXLen(); warningEliminator++;
        return false;
    }

protected:
    std::string filename;
};

#endif // _WRITER_
