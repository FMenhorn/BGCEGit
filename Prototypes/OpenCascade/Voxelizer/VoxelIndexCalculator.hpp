/*
 * VoxelIndexCalculator.hpp
 *
 *  Created on: Oct 20, 2015
 *      Author: friedrich
 */

#ifndef VOXELIZER_VOXELINDEXCALCULATOR_HPP_
#define VOXELIZER_VOXELINDEXCALCULATOR_HPP_

#include "VoxelShape.hpp"
/*
 *
 */
class VoxelIndexCalculator {
public:
	VoxelIndexCalculator();
	virtual ~VoxelIndexCalculator();

	void calculateIndexForVoxels(std::vector<std::vector<VoxelShape>>& matrixVoxelShapes);
	void removeDoubleIndices(std::vector<std::vector<VoxelShape>>& matrixVoxelShapes);
};

#endif /* VOXELIZER_VOXELINDEXCALCULATOR_HPP_ */
