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

	/**
	 * Returns the origin of the voxelShape in the corresponding dimension
	 * @return
	 */
	double getOriginX();
	double getOriginY();
	double getOriginZ();

	/**
	 * Returns the size of the shape in the corresponding dimension
	 * @return
	 */
	double getXLen();
	double getYLen();
	double getZLen();

	/**
	 * Returns the number of voxels in the corresponding dimension
	 * @return
	 */
	int getNbX();
	int getNbY();
	int getNbZ();

	/**
	 * Returns if the cell at (x,y,z) is a voxel
	 * @param x
	 * @param y
	 * @param z
	 * @return
	 */
	bool isVoxel(int x, int y, int z);

	/**
	 * Sets the cell at (x,y,z) as isVoxel
	 * @param x
	 * @param y
	 * @param z
	 * @param isVoxel
	 */
	void setVoxel(int x, int y, int z, bool isVoxel);

	Voxel_BoolDS& getVoxelShape();
	Voxel_BoolDS copyVoxelShape();
	void setVoxelShape(const Voxel_BoolDS voxelShape);
	void setOrigin(const std::vector<double> origin);
	const std::vector<double>& getDimension() const;
	void setDimension(const std::vector<double> dimension);
	const std::vector<double>& getOrigin() const;

	VoxelShape& operator=( const VoxelShape& other );
	const std::vector<int>& getIndices() const;
	void setIndices(const std::vector<int> indices);
	const std::vector<int> getVoxelDimension() const;
	void setVoxelDimension(const std::vector<int> voxelDimension);

private:
	Voxel_BoolDS _voxelShape;
	std::vector<int> _indices;
	std::vector<double> _dimension;
	std::vector<double> _origin;
	std::vector<int> _voxelDimension;
};

#endif /* VOXELIZER_VOXELSHAPE_HPP_ */
