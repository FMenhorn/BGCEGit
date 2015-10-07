/*
 * Reader.hpp
 *
 *  Created on: Oct 6, 2015
 *      Author: friedrich
 */

#ifndef READER_READER_HPP_
#define READER_READER_HPP_

#include <TopoDS_Shape.hxx>
#include <XSControl_Reader.hxx>
#include <string>

class Reader{
public:
	Reader(){};
	virtual ~Reader(){delete xsReader;};
	virtual TopoDS_Shape read(const std::string filename) = 0;
protected:
	XSControl_Reader* xsReader = nullptr;
};




#endif /* READER_READER_HPP_ */
