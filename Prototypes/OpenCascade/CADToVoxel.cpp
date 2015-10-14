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
#include "ColorHandler/ColorHandler.hpp"

int main(void){
	///File:
	std::string filePath = "./TestGeometry/";
	std::string fileName = "RedGreenBlueCube";
	std::string fileNameStep = fileName + ".stp";
	std::string fileNameIges = fileName + ".igs";
	std::string fileStep = filePath + fileNameStep;
	std::string fileIges = filePath + fileNameIges;
    /// Read file
    STEPCAFReader readerStep;
    IGESCAFReader readerIges;

    readerStep.read(fileStep);
    readerIges.read(fileIges);

    ColorHandler colorDetector;
    readerStep.transfer(colorDetector.getDocStep());
    readerIges.transfer(colorDetector.getDocIges());
    colorDetector.initializeMembers();
	std::vector<TopoDS_Face> facesVector;
	TopoDS_Shape fullBody;

	TopTools_ListOfShape fixtureFacesList;
	colorDetector.getFixtureShapes(fixtureFacesList);
	TopTools_ListOfShape loadFacesList;
	colorDetector.getLoadShapes(loadFacesList);
	TopTools_ListOfShape passiveFacesList;
	colorDetector.getPassiveShapes(passiveFacesList);

	/**Not used right now
	sewedShape = facesList.First();

	STEPControl_Writer stepWriter;
	stepWriter.Transfer(sewedShape, STEPControl_AsIs);
	stepWriter.Write("sewed.stp");
	**/

    /// Voxelize file
    Voxelizer voxelizer;
    int refinementLevel = 0;
    Writer_VTK writer_vtk;
    TopTools_ListIteratorOfListOfShape shapeIterator;
    int i = 1;
	VoxelShape voxelShape;
	std::cout << "FixtureListEmpty?: " << fixtureFacesList.IsEmpty() << std::endl;
    for(shapeIterator.Initialize(fixtureFacesList); shapeIterator.More(); shapeIterator.Next() ){
    	std::cout << "Fixture I: " << i << std::endl;
    	voxelizer.voxelize(shapeIterator.Value(), refinementLevel, voxelShape);
		writer_vtk.write("outputFixtures" + std::to_string(i), voxelShape);
		i++;
    }
    i = 1;

	std::cout << "LoadListEmpty?: " << loadFacesList.IsEmpty() << std::endl;
    for(shapeIterator.Initialize(loadFacesList); shapeIterator.More(); shapeIterator.Next() ){
    	std::cout << "Load I: " << i << std::endl;
    	voxelizer.voxelize(shapeIterator.Value(), refinementLevel, voxelShape);
		writer_vtk.write("outputLoad" + std::to_string(i), voxelShape);
		i++;
    }
    i = 1;

	std::cout << "PassiveListEmpty?: " << passiveFacesList.IsEmpty() << std::endl;
    for(shapeIterator.Initialize(passiveFacesList); shapeIterator.More(); shapeIterator.Next() ){
    	std::cout << "Passive I: " << i << std::endl;
    	voxelizer.voxelize(shapeIterator.Value(), refinementLevel, voxelShape);
		writer_vtk.write("outputPassive" + std::to_string(i), voxelShape);
		i++;
    }

    TopoDS_Shape fullShape;
    colorDetector.getAllShapes(fullShape);
    voxelizer.voxelize(fullShape, refinementLevel, voxelShape);
    voxelizer.fillVolume(voxelShape);
	for (int k = 0; k < voxelShape.getVoxelShape().GetNbZ(); k++){
        for (int j = 0; j < voxelShape.getVoxelShape().GetNbY(); j++){
            for (int i = 0; i < voxelShape.getVoxelShape().GetNbX(); i++){
            	std::cout << "CADToVoxel::writeScalars: [" << i << "," << j << "," << k << "]="<<
            								voxelShape.getVoxelShape().Get(i,j,k) << std::endl;
            }
        }
	}
    writer_vtk.write("outputFullBody", voxelShape);

	return EXIT_SUCCESS;
}
