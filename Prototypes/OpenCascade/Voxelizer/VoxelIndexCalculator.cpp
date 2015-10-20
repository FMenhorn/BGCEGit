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

void VoxelIndexCalculator::calculateIndexForVoxels(
		std::vector<std::vector<VoxelShape> >& matrixVoxelShapes) {

	int originVoxelX = 0;
	int originVoxelY = 0;
	int originVoxelZ = 0;
	double originX = 0;
	double originY = 0;
	double originZ = 0;
	double voxelSizeX = 0;
	double voxelSizeY = 0;
	double voxelSizeZ = 0;
	std::vector<int> voxelIndexTmp;
	for(size_t l = 0; l < matrixVoxelShapes.size(); ++l){
		for(size_t h = 0; h < matrixVoxelShapes[l].size(); ++h){
			originX =matrixVoxelShapes[l][h].getVoxelShape().GetX();
			originY =matrixVoxelShapes[l][h].getVoxelShape().GetY();
			originZ =matrixVoxelShapes[l][h].getVoxelShape().GetZ();
			voxelSizeX = matrixVoxelShapes[l][h].getVoxelShape().GetXLen()/matrixVoxelShapes[l][h].getVoxelShape().GetNbX();
			voxelSizeY = matrixVoxelShapes[l][h].getVoxelShape().GetYLen()/matrixVoxelShapes[l][h].getVoxelShape().GetNbY();
			voxelSizeZ = matrixVoxelShapes[l][h].getVoxelShape().GetZLen()/matrixVoxelShapes[l][h].getVoxelShape().GetNbZ();
			originVoxelX = originX * voxelSizeX;
			originVoxelY = originY * voxelSizeY;
			originVoxelZ = originZ * voxelSizeZ;
			std::cout << "Origin: "<< "[" << originX << "," << originY << "," << originZ << "] " <<
						 "VoxelOrigin: " << "[" << originVoxelX << "," << originVoxelY <<"," << originVoxelZ<< "] "
						 "VoxelSizes: "<<"[" << voxelSizeX << "," << voxelSizeY <<"," << voxelSizeZ<< "]" << std::endl;
			for (int k = 0; k < matrixVoxelShapes[l][h].getVoxelShape().GetNbZ(); k++){
				for (int i = 0; i < matrixVoxelShapes[l][h].getVoxelShape().GetNbX(); i++){
					for (int j = 0; j < matrixVoxelShapes[l][h].getVoxelShape().GetNbY(); j++){
						//std::cout << "Current Step: " << name << ":" << h << "," << k << "," << i << "," << j << std::endl;
					if (matrixVoxelShapes[l][h].getVoxelShape().Get(i,j,k)==Standard_True){
		//change to list.append
						//std::cout<<"X: "<< i*hx<<" Y:  "<<j*hy<<" Z: "<<k*hz << " Index: "<<(j+(voxelShape[h].getVoxelShape().GetNbY())*(i+k*(voxelShape[h].getVoxelShape().GetNbZ()))) << std::endl;
						voxelIndexTmp.push_back(originVoxelY + j+(matrixVoxelShapes[l][h].getVoxelShape().GetNbY())*(originVoxelX + i+(originVoxelZ + k)*(matrixVoxelShapes[l][h].getVoxelShape().GetNbZ())));
						}
					}
				}
			}
			matrixVoxelShapes[l][h].setIndices(voxelIndexTmp);
			voxelIndexTmp.clear();
		}
	}
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
	/**Compare with passive**/
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
	/**Load over Passive**/
	for(size_t i = 0; i < matrixVoxelShapes[3].size(); ++i){
		for(size_t j = 0; j < matrixVoxelShapes[2].size(); ++j){
			std::set_intersection(matrixVoxelShapes[3][i].getIndices().begin(), matrixVoxelShapes[3][i].getIndices().end(),
													  matrixVoxelShapes[2][j].getIndices().begin(), matrixVoxelShapes[2][j].getIndices().end(),
													  std::back_inserter(intersection));
			std::set_symmetric_difference(matrixVoxelShapes[3][i].getIndices().begin(), matrixVoxelShapes[3][i].getIndices().end(),
										  intersection.begin(), intersection.end(),
										  std::back_inserter(res));
			matrixVoxelShapes[3][i].setIndices(res);
			intersection.clear();
			res.clear();
		}
	}
	/**Fixture over Passive**/
	for(size_t i = 0; i < matrixVoxelShapes[3].size(); ++i){
		for(size_t j = 0; j < matrixVoxelShapes[1].size(); ++j){
			std::set_intersection(matrixVoxelShapes[3][i].getIndices().begin(), matrixVoxelShapes[3][i].getIndices().end(),
													  matrixVoxelShapes[1][j].getIndices().begin(), matrixVoxelShapes[1][j].getIndices().end(),
													  std::back_inserter(intersection));
			std::set_symmetric_difference(matrixVoxelShapes[3][i].getIndices().begin(), matrixVoxelShapes[3][i].getIndices().end(),
										  intersection.begin(), intersection.end(),
										  std::back_inserter(res));
			matrixVoxelShapes[3][i].setIndices(res);
			intersection.clear();
			res.clear();
		}
	}
}
