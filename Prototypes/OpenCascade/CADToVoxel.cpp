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

#include <IGESControl_Reader.hxx>
#include <TopoDS.hxx>
#include <TopoDS_Face.hxx>
#include <TopoDS_Solid.hxx>
#include <TopTools_ListIteratorOfListOfShape.hxx>
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
	if ( argc != 5 )
	{
		std::cout << std::endl;
		std::cout << "CADToVoxel: Usage: " << argv[0] << " /path/to/file/ fileName forceScalingFactor refinementLevel" << std::endl;
		std::cout << std::endl;

		return -1;
	}

	///File:
	std::string filePath = argv[1];
	std::string fileName = argv[2];
	double forceScalingFactor = atof(argv[3]);
    int refinementLevel = atoi(argv[4]);

	/**
	 *  INPUT
	 */
	Reader reader(filePath, fileName);
	reader.read();

    /**
     * FACE DETECTION
     */
    ColorHandler colorDetector;
    reader.transfer(colorDetector);
    colorDetector.initializeMembers();
	std::vector<TopoDS_Face> facesVector;

    TopoDS_Shape fullShape;
    colorDetector.getCompleteShape(fullShape);

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

	ListOfShape activeFacesList;
	colorDetector.getActiveShapes(activeFacesList);

    /**
     * VOXELIZE AND OUTPUT
     */

    Voxelizer voxelizer;
    TopTools_ListIteratorOfListOfShape shapeIterator;
	VoxelShape voxelShape;
	std::vector<std::vector<VoxelShape>> outputVoxelVector;
    VoxelIndexCalculator voxelIndexCalculator;

    /**Full Body Treatment**/
    voxelizer.voxelize(fullShape, refinementLevel, voxelShape);
    voxelIndexCalculator.setDimensions(voxelShape.getVoxelDimension());
    voxelIndexCalculator.setOrigin(voxelShape.getOrigin());
    voxelizer.fillVolume(voxelShape);
    voxelIndexCalculator.calculateIndexForVoxelShape(voxelShape, true);

	std::vector<VoxelShape> bodyVector;
	bodyVector.push_back(voxelShape);
    outputVoxelVector.push_back(bodyVector);

    /**TODO: wrap size variable**/
    int counter = 0;
	/**Fixture Treatment**/
	std::vector<VoxelShape> fixtureVector;
	if(fixtureFacesList.getSize() > 0){
		fixtureVector.resize(fixtureFacesList.getSize());
		for(shapeIterator.Initialize(fixtureFacesList.getListOfShape()); shapeIterator.More(); shapeIterator.Next() ){
			voxelizer.voxelize(shapeIterator.Value(), refinementLevel, fixtureVector[counter]);
			std::cout << "FixtureIndices: " << std::endl;
		    voxelIndexCalculator.calculateIndexForVoxelShape(fixtureVector[counter], false);
			counter++;
		}
	}
    outputVoxelVector.push_back(fixtureVector);

    counter = 0;
    /**Load Treatment**/
	std::vector<VoxelShape> loadVector;
	std::vector<VoxelShape> activeVector; /**Treat Loadelements as active cells aswell**/
	activeVector.resize(loadFacesList.getSize()+activeFacesList.getSize());
	if(loadFacesList.getSize() > 0){
		loadVector.resize(loadFacesList.getSize());
		for(shapeIterator.Initialize(loadFacesList.getListOfShape()); shapeIterator.More(); shapeIterator.Next() ){
			voxelizer.voxelize(shapeIterator.Value(), refinementLevel, loadVector[counter]);
			voxelizer.voxelize(shapeIterator.Value(), refinementLevel, activeVector[counter]);
			std::cout << "LoadIndices: " << std::endl;
			voxelIndexCalculator.calculateIndexForVoxelShape(loadVector[counter], false);
			voxelIndexCalculator.calculateIndexForVoxelShape(activeVector[counter], true);
			counter++;
		}
	}
    outputVoxelVector.push_back(loadVector);

    counter = loadFacesList.getSize();
    /**Active Treatment**/
	//std::vector<VoxelShape> activeVector;
	if(activeFacesList.getSize()>0){
		activeVector.resize(activeFacesList.getSize());
		for(shapeIterator.Initialize(activeFacesList.getListOfShape()); shapeIterator.More(); shapeIterator.Next() ){
			voxelizer.voxelize(shapeIterator.Value(), refinementLevel, activeVector[counter]);
			std::cout << "ActiveIndices: " << std::endl;
			voxelIndexCalculator.calculateIndexForVoxelShape(activeVector[counter], true);
			counter++;
		}
	}
    outputVoxelVector.push_back(activeVector);

    VoxelShape passiveShape;
    voxelIndexCalculator.calculatePassiveIndexFromBody(bodyVector[0], passiveShape);
    std::vector<VoxelShape> passiveVector;
    passiveVector.push_back(passiveShape);
    outputVoxelVector.push_back(passiveVector);

    //voxelIndexCalculator.removeDoubleIndices(outputVoxelVector);

    Writer_ToPy writerToPy;
    writerToPy.write("topy_"+fileName, outputVoxelVector, loadList);

    Writer_VTK writerVTK;
    writerVTK.write("vtk_"+fileName, outputVoxelVector, loadList);

	return EXIT_SUCCESS;
}
