/*
 * VoxelIndexCalculator.cpp
 *
 *  Created on: Oct 20, 2015
 *      Author: friedrich
 */

#include "VoxelIndexCalculator.hpp"

#include <iostream>
#include <algorithm>

VoxelIndexCalculator::VoxelIndexCalculator() {
	// TODO Auto-generated constructor stub

}

VoxelIndexCalculator::~VoxelIndexCalculator() {
	// TODO Auto-generated destructor stub
}

void VoxelIndexCalculator::removeDoubleIndices(
		std::vector<std::vector<VoxelShape> >& matrixVoxelShapes) {
	/**Check if body has indices in passive, fixture or load**/
	std::vector<int> res; // Will contain the symmetric difference
	std::vector<int> intersection;
	/**Compare with fixture**/
	for(size_t j = 0; j < matrixVoxelShapes[1].size(); ++j){
		std::set_intersection(matrixVoxelShapes[0][0].getIndices().begin(), matrixVoxelShapes[0][0].getIndices().end(),
			    							  matrixVoxelShapes[1][j].getIndices().begin(), matrixVoxelShapes[1][j].getIndices().end(),
			                                  std::back_inserter(intersection));
	    std::set_symmetric_difference(matrixVoxelShapes[0][0].getIndices().begin(), matrixVoxelShapes[0][0].getIndices().end(),
	    							  intersection.begin(), intersection.end(),
	                                  std::back_inserter(res));
	    matrixVoxelShapes[0][0].setIndices(res);
	    intersection.clear();
	    res.clear();
	}
	/**Compare with loads**/
	for(size_t j = 0; j < matrixVoxelShapes[2].size(); ++j){
		std::set_intersection(matrixVoxelShapes[0][0].getIndices().begin(), matrixVoxelShapes[0][0].getIndices().end(),
			    							  matrixVoxelShapes[2][j].getIndices().begin(), matrixVoxelShapes[2][j].getIndices().end(),
			                                  std::back_inserter(intersection));
	    std::set_symmetric_difference(matrixVoxelShapes[0][0].getIndices().begin(), matrixVoxelShapes[0][0].getIndices().end(),
	    							  intersection.begin(), intersection.end(),
	                                  std::back_inserter(res));
	    matrixVoxelShapes[0][0].setIndices(res);
	    intersection.clear();
	    res.clear();
	}
	/**Compare with active**/
	for(size_t j = 0; j < matrixVoxelShapes[3].size(); ++j){
		std::set_intersection(matrixVoxelShapes[0][0].getIndices().begin(), matrixVoxelShapes[0][0].getIndices().end(),
			    							  matrixVoxelShapes[3][j].getIndices().begin(), matrixVoxelShapes[3][j].getIndices().end(),
			                                  std::back_inserter(intersection));
	    std::set_symmetric_difference(matrixVoxelShapes[0][0].getIndices().begin(), matrixVoxelShapes[0][0].getIndices().end(),
	    							  intersection.begin(), intersection.end(),
	                                  std::back_inserter(res));
	    matrixVoxelShapes[0][0].setIndices(res);
	    intersection.clear();
	    res.clear();
	}
	/**Active over Load**/
	for(size_t i = 0; i < matrixVoxelShapes[3].size(); ++i){
		for(size_t j = 0; j < matrixVoxelShapes[2].size(); ++j){
			std::set_intersection(matrixVoxelShapes[3][i].getIndices().begin(), matrixVoxelShapes[3][i].getIndices().end(),
													  matrixVoxelShapes[2][j].getIndices().begin(), matrixVoxelShapes[2][j].getIndices().end(),
													  std::back_inserter(intersection));
			std::set_symmetric_difference(matrixVoxelShapes[2][i].getIndices().begin(), matrixVoxelShapes[2][i].getIndices().end(),
										  intersection.begin(), intersection.end(),
										  std::back_inserter(res));
			matrixVoxelShapes[2][i].setIndices(res);
			intersection.clear();
			res.clear();
		}
	}
	/**Active over Fixture**/
	for(size_t i = 0; i < matrixVoxelShapes[3].size(); ++i){
		for(size_t j = 0; j < matrixVoxelShapes[1].size(); ++j){
			std::set_intersection(matrixVoxelShapes[3][i].getIndices().begin(), matrixVoxelShapes[3][i].getIndices().end(),
													  matrixVoxelShapes[1][j].getIndices().begin(), matrixVoxelShapes[1][j].getIndices().end(),
													  std::back_inserter(intersection));
			std::set_symmetric_difference(matrixVoxelShapes[1][i].getIndices().begin(), matrixVoxelShapes[1][i].getIndices().end(),
										  intersection.begin(), intersection.end(),
										  std::back_inserter(res));
			matrixVoxelShapes[1][i].setIndices(res);
			intersection.clear();
			res.clear();
		}
	}
	/**Load over Fixture**/
	for(size_t i = 0; i < matrixVoxelShapes[1].size(); ++i){
		for(size_t j = 0; j < matrixVoxelShapes[2].size(); ++j){
			std::set_intersection(matrixVoxelShapes[1][i].getIndices().begin(), matrixVoxelShapes[1][i].getIndices().end(),
													  matrixVoxelShapes[2][j].getIndices().begin(), matrixVoxelShapes[2][j].getIndices().end(),
													  std::back_inserter(intersection));
			std::set_symmetric_difference(matrixVoxelShapes[1][i].getIndices().begin(), matrixVoxelShapes[1][i].getIndices().end(),
										  intersection.begin(), intersection.end(),
										  std::back_inserter(res));
			matrixVoxelShapes[1][i].setIndices(res);
			intersection.clear();
			res.clear();
		}
	}
}

void VoxelIndexCalculator::calculateIndicesForWholeVector(std::vector<VoxelShape>& voxelShapeVector, const bool isElem) {
	for(unsigned int i = 0; i < voxelShapeVector.size(); ++i){
		this->calculateIndexForVoxelShape(voxelShapeVector[i], isElem);
	}
}

void VoxelIndexCalculator::calculateIndexForVoxelShape(VoxelShape& voxelShape, bool isElem) {
	int originVoxelX = 0;
	int originVoxelY = 0;
	int originVoxelZ = 0;
	int nbX = 0;
	int nbY = 0;
	int nbZ = 0;
	int localNbX = 0;
	int localNbY = 0;
	int localNbZ = 0;
	double originX = 0;
	double originY = 0;
	double originZ = 0;
	double voxelSizeX = 0;
	double voxelSizeY = 0;
	double voxelSizeZ = 0;
	std::vector<int> voxelIndexTmp;

	std::cout << "voxelShape.GetOrigin: " << voxelShape.getOriginX() << "," << voxelShape.getOriginY() << "," << voxelShape.getOriginZ() << std::endl;
	std::cout << "origin: " << origin[0] << "," << origin[1] << "," << origin[2] << std::endl;
	originX =origin[0]+voxelShape.getOriginX()-origin[0];
	originY =origin[0]+voxelShape.getOriginY()-origin[1];
	originZ =origin[0]+voxelShape.getOriginZ()-origin[2];
	voxelSizeX = voxelShape.getXLen()/voxelShape.getNbX();
	voxelSizeY = voxelShape.getYLen()/voxelShape.getNbY();
	voxelSizeZ = voxelShape.getZLen()/voxelShape.getNbZ();
	nbX = isElem ? dimensions[0] : dimensions[0] + 1;
	nbY = isElem ? dimensions[1] : dimensions[1] + 1;
	nbZ = isElem ? dimensions[2] : dimensions[2] + 1;
	originVoxelX = originX * 1./voxelSizeX + 1;
	originVoxelY = originY * 1./voxelSizeY + 1;
	originVoxelZ = originZ * 1./voxelSizeZ + 1;
	localNbX = voxelShape.getNbX();
	localNbY = voxelShape.getNbY();
	localNbZ = voxelShape.getNbZ();
	std::cout << "VoxelIndexCalulator::calculateIndexForVoxelShape: " << std::endl;
	std::cout << "Origin: "<< "[" << originX << "," << originY << "," << originZ << "] \n" <<
				 "VoxelOrigin: " << "[" << originVoxelX << "," << originVoxelY <<"," << originVoxelZ<< "] \n" <<
				 "VoxelSizes: "<<"[" << voxelSizeX << "," << voxelSizeY <<"," << voxelSizeZ<< "] \n" <<
				 "NoVoxelsGlobal: "<<"[" << nbX << "," << nbY <<"," << nbZ << "] \n"
				 "NoVoxelsLocal: "<< "[" << localNbX << ", " << localNbY << "," << localNbZ << "]" << std::endl;
	int curIndex;
	for (int k = 0; k < voxelShape.getNbZ(); k++){
		for (int i = 0; i < voxelShape.getNbX(); i++){
			for (int j = 0; j < voxelShape.getNbY(); j++){
				//std::cout << "Current Step: " << name << ":" << h << "," << k << "," << i << "," << j << std::endl;
			if (voxelShape.isVoxel(i,j,k)==Standard_True){
//change to list.append
				//std::cout<<"X: "<< i*hx<<" Y:  "<<j*hy<<" Z: "<<k*hz << " Index: "<<(j+(voxelShape[h].getVoxelShape().GetNbY())*(i+k*(voxelShape[h].getVoxelShape().GetNbZ()))) << std::endl;
				curIndex = (nbY-1-originVoxelY) + originVoxelX*nbY + originVoxelZ*nbX*nbY - j + i * nbY + k * nbY*nbX;
				voxelIndexTmp.push_back( curIndex );
				//std::cout << " " << curIndex;
				}
			}
		}
	}
	std::cout << std::endl;
	voxelShape.setIndices(voxelIndexTmp);
	voxelIndexTmp.clear();
}

void VoxelIndexCalculator::calculatePassiveIndexFromBody(VoxelShape& bodyVoxelShape, VoxelShape& passiveVoxelShape) {
	int originVoxelX = 0;
	int originVoxelY = 0;
	int originVoxelZ = 0;
	double originX = 0;
	double originY = 0;
	double originZ = 0;
	int nbX = 0;
	int nbY = 0;
	int nbZ = 0;
	double voxelSizeX = 0;
	double voxelSizeY = 0;
	double voxelSizeZ = 0;
	std::vector<int> voxelIndexTmp;

	originX =bodyVoxelShape.getOriginX()-origin[0];
	originY =bodyVoxelShape.getOriginY()-origin[1];
	originZ =bodyVoxelShape.getOriginZ()-origin[2];
	nbX = dimensions[0];
	nbY = dimensions[1];
	nbZ = dimensions[2];
	voxelSizeX = bodyVoxelShape.getXLen()/nbX;
	voxelSizeY = bodyVoxelShape.getYLen()/nbY;
	voxelSizeZ = bodyVoxelShape.getZLen()/nbZ;
	originVoxelX = originX * voxelSizeX;
	originVoxelY = originY * voxelSizeY;
	originVoxelZ = originZ * voxelSizeZ;
//	std::cout << "Origin: "<< "[" << originX << "," << originY << "," << originZ << "] " <<
//				 "VoxelOrigin: " << "[" << originVoxelX << "," << originVoxelY <<"," << originVoxelZ<< "] "
//				 "VoxelSizes: "<<"[" << voxelSizeX << "," << voxelSizeY <<"," << voxelSizeZ<< "]" << std::endl;

	int curIndex;
	for (int k = 0; k < bodyVoxelShape.getNbZ(); k++){
		for (int i = 0; i < bodyVoxelShape.getNbX(); i++){
			for (int j = 0; j < bodyVoxelShape.getNbY(); j++){
				//std::cout << "Current Step: " << name << ":" << h << "," << k << "," << i << "," << j << std::endl;
			if (bodyVoxelShape.isVoxel(i,j,k)==Standard_False){
//change to list.append
				//std::cout<<"X: "<< i*hx<<" Y:  "<<j*hy<<" Z: "<<k*hz << " Index: "<<(j+(voxelShape[h].getVoxelShape().GetNbY())*(i+k*(voxelShape[h].getVoxelShape().GetNbZ()))) << std::endl;
				curIndex = (nbY-1-originVoxelY) + originVoxelX*nbY + originVoxelZ*nbX*nbY - j + i * nbY + k * nbY*nbX;
				voxelIndexTmp.push_back( curIndex );
				//voxelIndexTmp.push_back(originVoxelY + j+(bodyVoxelShape.getVoxelShape().GetNbY())*(originVoxelX + i+(originVoxelZ + k)*(bodyVoxelShape.getVoxelShape().GetNbZ())));
				}
			}
		}
	}
	passiveVoxelShape.setIndices(voxelIndexTmp);
	voxelIndexTmp.clear();
}

void VoxelIndexCalculator::setDimensions(const std::vector<int> dimensions) {
	this->dimensions = dimensions;
}

void VoxelIndexCalculator::setOrigin(const std::vector<double> origin) {
	this->origin = origin;
}
