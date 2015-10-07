/*
 * STEPCAFReader.cpp
 *
 *  Created on: Oct 7, 2015
 *      Author: friedrich
 */

#include "IGESCAFReader.hpp"

#include <IGESCAFControl_Reader.hxx>
#include <Interface_Static.hxx>
#include <Standard_CString.hxx>

IGESCAFReader::IGESCAFReader(): Reader() {
	xsReader = new IGESCAFControl_Reader();
}

IGESCAFReader::~IGESCAFReader() {
	this->~Reader();
}

TopoDS_Shape IGESCAFReader::read(const std::string filename) {

    TopoDS_Shape topoDSShape;

	std::cout << "IGESCAFReader: dummy IGESCAFreader" << std::endl;

	return topoDSShape;
}
