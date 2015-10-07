/*
 * STEPReader.hpp
 *
 *  Created on: Oct 6, 2015
 *      Author: saumitra
 */

#ifndef READER_IGESREADER_HPP_
#define READER_IGESREADER_HPP_

#include <TopoDS_Shape.hxx>

#include "Reader.hpp"
#include <string>
/*
 *
 */
class IGESReader: public Reader {
public:

	IGESReader();
	virtual ~IGESReader();

	TopoDS_Shape read(const std::string filename);

private:
	//IGESControl_Reader igesReader;
};

#endif /* READER_IGESREADER_HPP_ */

