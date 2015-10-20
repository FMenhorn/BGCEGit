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
#include "Writer/Writer_VTK.hpp"
#include "Writer/Writer_ToPy.hpp"
#include "ColorHandler/ColorHandler.hpp"
#include "Reader/Reader.hpp"
#include "Reader/CAFReader.hpp"
#include "Reader/IGESCAFReader.hpp"
#include "Reader/STEPCAFReader.hpp"

int main(void){
	///File:
	std::string filePath = "./TestGeometry/";
	std::string fileName = "RedGreenBlueCube";

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
	TopTools_ListOfShape fixtureFacesList;
	colorDetector.getFixtureShapes(fixtureFacesList);
	TopTools_ListOfShape loadFacesList;
	colorDetector.getLoadShapes(loadFacesList);
	TopTools_ListOfShape passiveFacesList;
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
	/**Fixture Treatment**/
	std::vector<VoxelShape> fixtureVector(1);
    for(shapeIterator.Initialize(fixtureFacesList); shapeIterator.More(); shapeIterator.Next() ){
    	voxelizer.voxelize(shapeIterator.Value(), refinementLevel, fixtureVector[0]);
    }
    outputVoxelVector.push_back(fixtureVector);

    /**Load Treatment**/
	std::vector<VoxelShape> loadVector(1);
    for(shapeIterator.Initialize(loadFacesList); shapeIterator.More(); shapeIterator.Next() ){
    	voxelizer.voxelize(shapeIterator.Value(), refinementLevel, loadVector[0]);
    }
    outputVoxelVector.push_back(loadVector);

    /**Passive Treatment**/
	std::vector<VoxelShape> passiveVector(1);
    for(shapeIterator.Initialize(passiveFacesList); shapeIterator.More(); shapeIterator.Next() ){
    	voxelizer.voxelize(shapeIterator.Value(), refinementLevel, passiveVector[0]);
    }
    outputVoxelVector.push_back(passiveVector);


    Writer_ToPy writerToPy;
    writerToPy.write("topy", outputVoxelVector);

    Writer_VTK writerVTK;
    writerVTK.write("vtk", outputVoxelVector);

	return EXIT_SUCCESS;
}
