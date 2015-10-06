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
	XSControl_Reader* ocReader = nullptr;

	Reader(XSControl_Reader* xsControlReader): ocReader(xsControlReader){};
	virtual ~Reader(){delete ocReader;};
	virtual TopoDS_Shape read(std::string filename) = 0;
private:
};




#endif /* READER_READER_HPP_ */
