/*
 * STEPCAFReader.hpp
 *
 *  Created on: Oct 7, 2015
 *      Author: friedrich
 */

#ifndef READER_IGESCAFREADER_HPP_
#define READER_IGESCAFREADER_HPP_

#include <TopoDS_Shape.hxx>

#include "Reader.hpp"
#include <string>
/*
 *
 */
class IGESCAFReader:public Reader {
public:
	IGESCAFReader();
	virtual ~IGESCAFReader();

	TopoDS_Shape read(const std::string filename);
};

#endif /* READER_IGESCAFREADER_HPP_ */
