/*
 * CADtoVoxel.cpp
 *
 *  Created on: Oct 6, 2015
 *      Author: BGCE
 */


#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <iostream>
#include <vector>
#include <assert.h>

#include <IGESControl_Reader.hxx>
#include <TopoDS.hxx>
#include <TopoDS_Face.hxx>
#include <TopoDS_Solid.hxx>
#include <STEPControl_StepModelType.hxx>
#include <STEPControl_Writer.hxx>
#include <STEPControl_Reader.hxx>
#include <BRepTools.hxx>

#include "Voxelizer/Voxelizer.hpp"
#include "Voxelizer/VoxelShape.hpp"
#include "Voxelizer/VoxelIndexCalculator.hpp"
#include "Writer/Writer_VTK.hpp"
#include "Writer/Writer_ToPy.hpp"
#include "ColorHandler/ColorHandler.hpp"
#include "DataWrappers/ListOfShape.hpp"
#include "Reader/Reader.hpp"
#include "Reader/CAFReader.hpp"
#include "Reader/IGESCAFReader.hpp"
#include "Reader/STEPCAFReader.hpp"

int main(int argc, char** argv){

	std::cout << "Starting CADToVoxel Pipeline..." << std::endl;
	if ( argc != 6 )
	{
		std::cout << std::endl;
		std::cout << "CADToVoxel: Usage: " << argv[0] << " /path/to/file/ fileName forceScalingFactor refinementLevel activeFileSpecified" << std::endl;
		std::cout << "And not: " << std::endl;
		for(int i = 0; i < argc; i++){
			std::cout << argv[i];
		}
		std::cout << std::endl;

		return -1;
	}

	///File:
	std::string filePath = argv[1];
	std::string fileName = argv[2];
	double forceScalingFactor = atof(argv[3]);
	assert(forceScalingFactor>0);
    int refinementLevel = atoi(argv[4]);
    assert(refinementLevel>=0);
    bool activeFileSpecified = atoi(argv[5]);

	/**
	 *  INPUT
	 */
	Reader reader(filePath, fileName);
	reader.read();

	STEPCAFReader activeReader;
	if(activeFileSpecified){
		activeReader.read(filePath+fileName+"_Fixed.step");
	}

    /**
     * FACE DETECTION
     */
    ColorHandler colorDetector;
    reader.transfer(colorDetector);

    if(activeFileSpecified){
    	activeReader.transfer(colorDetector.getDocStepActive());
    	colorDetector.buildActiveShapeFromDocs();
    }

    colorDetector.initializeMembers();
	std::vector<TopoDS_Face> facesVector;

    TopoDS_Shape fullShape;
    colorDetector.getCompleteShape(fullShape);

    TopoDS_Shape activeShape;
    if(activeFileSpecified){
    	colorDetector.getActiveShape(activeShape);
    }

	ListOfShape fixtureFacesList;
	colorDetector.getFixtureShapes(fixtureFacesList);

	ListOfShape loadFacesList;
	std::vector<std::vector<double>> loadList;
	colorDetector.getLoadShapes(loadFacesList, loadList);
	for(size_t i = 0; i < loadList.size(); ++i){
		for(size_t j = 0; j < loadList[i].size(); ++j){
			loadList[i][j] *= forceScalingFactor;
		}
	}

	/*ListOfShape activeFacesList;
	colorDetector.getActiveShapes(activeFacesList);*/

    /**
     * VOXELIZE
     */
    Voxelizer voxelizer;
	std::vector<std::vector<VoxelShape>> outputVoxelVector;
    VoxelIndexCalculator voxelIndexCalculator;

    /**Full Body Treatment**/
    std::cout << "###Full Body###" << std::endl;
	VoxelShape voxelShape;
	std::vector<VoxelShape> bodyVector;
    voxelizer.voxelize(fullShape, refinementLevel, voxelShape);
    voxelIndexCalculator.setDimensions(voxelShape.getVoxelDimension());
    voxelIndexCalculator.setOrigin(voxelShape.getOrigin());
    voxelizer.fillVolume(voxelShape);
    voxelIndexCalculator.calculateIndexForVoxelShape(voxelShape, true);
	bodyVector.push_back(voxelShape);
    outputVoxelVector.push_back(bodyVector);

	/**Fixture Treatment**/
    std::cout << "###Fixture Body###" << std::endl;
	std::vector<VoxelShape> fixtureVector;
	fixtureVector.resize(fixtureFacesList.getSize());
	voxelizer.voxelizeWholeVector(refinementLevel, false, fixtureFacesList, fixtureVector);
	voxelIndexCalculator.calculateIndicesForWholeVector(fixtureVector, false);
    outputVoxelVector.push_back(fixtureVector);

    /**Load Treatment**/
    std::cout << "###Load Body###" << std::endl;
	std::vector<VoxelShape> loadVector;
	//std::vector<VoxelShape> activeVector; /**Treat Loadelements as active cells aswell**/
	//activeVector.resize(loadFacesList.getSize()+activeFacesList.getSize());
	loadVector.resize(loadFacesList.getSize());
	voxelizer.voxelizeWholeVector(refinementLevel, false, loadFacesList, loadVector);
	voxelIndexCalculator.calculateIndicesForWholeVector(loadVector, false);
	//voxelizer.voxelizeWholeVector(refinementLevel, true, loadFacesList, activeVector);
    outputVoxelVector.push_back(loadVector);

    /**Active Treatment**/
    std::cout << "###Active Body###" << std::endl;
	VoxelShape voxelShapeActive;
	std::vector<VoxelShape> activeVector;
	if(activeFileSpecified){
		voxelizer.voxelize(activeShape, refinementLevel, voxelShapeActive);
		voxelizer.fillVolume(voxelShapeActive);
		voxelIndexCalculator.calculateIndexForVoxelShape(voxelShapeActive, true);
		activeVector.push_back(voxelShapeActive);
	}
	outputVoxelVector.push_back(activeVector);

    /*voxelizer.voxelizeWholeVector(refinementLevel, true, activeFacesList, activeVector, loadFacesList.getSize());
    voxelIndexCalculator.calculateIndicesForWholeVector(activeVector, true);
    outputVoxelVector.push_back(activeVector);*/

	/**Passive Treatment**/
    std::cout << "###Passive Body###" << std::endl;
    VoxelShape passiveShape;
    voxelIndexCalculator.calculatePassiveIndexFromBody(bodyVector[0], passiveShape);
    std::vector<VoxelShape> passiveVector;
    passiveVector.push_back(passiveShape);
    outputVoxelVector.push_back(passiveVector);

    //voxelIndexCalculator.removeDoubleIndices(outputVoxelVector);

    /**
     * OUTPUT
     */
    Writer_ToPy writerToPy;
    writerToPy.write("topy_"+fileName, outputVoxelVector, loadList);

    Writer_VTK writerVTK;
    writerVTK.write("vtk_"+fileName, outputVoxelVector, loadList);

	return EXIT_SUCCESS;
}
