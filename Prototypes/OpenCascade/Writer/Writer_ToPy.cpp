/*
 * STEPReader.hpp
 *
 *  Created on: Oct 6, 2015
 *      Author: saumitra
 */

#include "Writer_ToPy.hpp"

bool Writer_ToPy::write(std::string _filename, Voxel_BoolDS &voxelShape){
    int warningEliminator = voxelShape.GetXLen(); warningEliminator++;
    std::cout << "Writer_ToPy: Functionality not yet implemented!" << std::endl;

    return false;
}
