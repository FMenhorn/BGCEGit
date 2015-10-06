/*
 * CADtoVoxel.cpp
 *
 *  Created on: Oct 6, 2015
 *      Author: BGCE
 */


#include <stdio.h>
#include <stdlib.h>
#include <iostream>

#include "Reader/Reader.hpp"
#include "Reader/STEPReader.hpp"
#include <STEPControl_Reader.hxx>

int main(void){
	STEPControl_Reader ocreader;
	Reader* reader = new STEPReader(&ocreader);
	TopoDS_Shape shape = reader->read("some file path");
	return EXIT_SUCCESS;
}




