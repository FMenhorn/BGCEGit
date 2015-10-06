/*
 * STEPReader.cpp
 *
 *  Created on: Oct 6, 2015
 *      Author: friedrich
 */

#include "STEPReader.hpp"

#include <iostream>

STEPReader::STEPReader(STEPControl_Reader* stepControlReader): Reader(stepControlReader) {

}

STEPReader::~STEPReader() {
	this->~Reader();
}

TopoDS_Shape STEPReader::read(std::string filename) {
	std::cout << "STEPReader: Dummy read in_ "<< filename << "_" << std::endl;
	return TopoDS_Shape();
}
