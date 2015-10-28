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

	void calculateIndexForVoxelShape(VoxelShape& voxelShape, bool isElem);
	void calculatePassiveIndexFromBody(VoxelShape& bodyVoxelShape, VoxelShape& passiveVoxelShape);
	void removeDoubleIndices(std::vector<std::vector<VoxelShape>>& matrixVoxelShapes);
	void setDimensions(const std::vector<int> dimensions);
	void setOrigin(const std::vector<double> origin);
private:
	std::vector<int> dimensions;
	std::vector<double> origin;
};

#endif /* VOXELIZER_VOXELINDEXCALCULATOR_HPP_ */
