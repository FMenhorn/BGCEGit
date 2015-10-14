/*
 * VoxelShape.hpp
 *
 *  Created on: Oct 12, 2015
 *      Author: friedrich
 */

#ifndef VOXELIZER_VOXELSHAPE_HPP_
#define VOXELIZER_VOXELSHAPE_HPP_

#include <Voxel_BoolDS.hxx>
#include <stdlib.h>
#include <vector>
/*
 *
 */
class VoxelShape {
public:
	VoxelShape();
	VoxelShape(Voxel_BoolDS voxelShape, std::vector<double> origin);

	virtual ~VoxelShape();

	double getOriginX();
	double getOriginY();
	double getOriginZ();
	Voxel_BoolDS& getVoxelShape();
	void setVoxelShape(const Voxel_BoolDS voxelShape);
	void setOrigin(const std::vector<double> origin);
	const std::vector<double>& getDimension() const;
	void setDimension(const std::vector<double> dimension);
	const std::vector<double>& getOrigin() const;

private:
	Voxel_BoolDS _voxelShape;
	std::vector<double> _dimension;
	std::vector<double> _origin;
};

#endif /* VOXELIZER_VOXELSHAPE_HPP_ */
