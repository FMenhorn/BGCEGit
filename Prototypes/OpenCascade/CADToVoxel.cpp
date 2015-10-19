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

#include "Reader/Reader.hpp"
#include "Reader/IGESCAFReader.hpp"
#include "Reader/STEPCAFReader.hpp"
#include "Voxelizer/Voxelizer.hpp"
#include "Voxelizer/VoxelShape.hpp"
#include "Writer/Writer_VTK.hpp"
#include "Writer/Writer_ToPy.hpp"
#include "ColorHandler/ColorHandler.hpp"
#include "DataWrappers/ListOfShape.hpp"

int main(void){
	///File:
	std::string filePath = "./TestGeometry/";
	std::string fileName = "RedGreenBlueCube";
	std::string fileNameStep = fileName + ".stp";
	std::string fileNameIges = fileName + ".igs";
	std::string fileStep = filePath + fileNameStep;
	std::string fileIges = filePath + fileNameIges;

	/**
	 *  INPUT
	 */
    STEPCAFReader readerStep;
    IGESCAFReader readerIges;

    readerStep.read(fileStep);
    readerIges.read(fileIges);

    /**
     * FACE DETECTION
     */
    ColorHandler colorDetector;
    readerStep.transfer(colorDetector.getDocStep());
    readerIges.transfer(colorDetector.getDocIges());
    colorDetector.initializeMembers();
	std::vector<TopoDS_Face> facesVector;

    TopoDS_Shape fullShape;
    colorDetector.getCompleteShape(fullShape);
	ListOfShape fixtureFacesList;
	colorDetector.getFixtureShapes(fixtureFacesList);
	ListOfShape loadFacesList;
	colorDetector.getLoadShapes(loadFacesList);
	ListOfShape passiveFacesList;
	colorDetector.getPassiveShapes(passiveFacesList);

    /**
     * VOXELIZE AND OUTPUT
     */
    int refinementLevel = 0;
    Voxelizer voxelizer;
    TopTools_ListIteratorOfListOfShape shapeIterator;
	VoxelShape voxelShape;

	std::vector<std::vector<VoxelShape>> outputVoxelVector;


    /**Full Body Treatment**/
    voxelizer.voxelize(fullShape, refinementLevel, voxelShape);
    voxelizer.fillVolume(voxelShape);

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
			counter++;
		}
	}
    outputVoxelVector.push_back(fixtureVector);

    counter = 0;
    /**Load Treatment**/
	std::vector<VoxelShape> loadVector;
	if(loadFacesList.getSize() > 0){
		loadVector.resize(loadFacesList.getSize());
		for(shapeIterator.Initialize(loadFacesList.getListOfShape()); shapeIterator.More(); shapeIterator.Next() ){
			voxelizer.voxelize(shapeIterator.Value(), refinementLevel, loadVector[counter]);
			counter++;
		}
	}
    outputVoxelVector.push_back(loadVector);

    counter = 0;
    /**Passive Treatment**/
	std::vector<VoxelShape> passiveVector;
	if(passiveFacesList.getSize()>0){
		passiveVector.resize(passiveFacesList.getSize());
		for(shapeIterator.Initialize(passiveFacesList.getListOfShape()); shapeIterator.More(); shapeIterator.Next() ){
			voxelizer.voxelize(shapeIterator.Value(), refinementLevel, passiveVector[counter]);
			counter++;
		}
	}
    outputVoxelVector.push_back(passiveVector);


    Writer_ToPy writerToPy;
    writerToPy.write("topy", outputVoxelVector);

    Writer_VTK writerVTK;
    writerVTK.write("vtk", outputVoxelVector);

	return EXIT_SUCCESS;
}
