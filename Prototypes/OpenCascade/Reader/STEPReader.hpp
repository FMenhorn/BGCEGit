/*
 * STEPReader.hpp
 *
 *  Created on: Oct 6, 2015
 *      Author: friedrich
 */

#ifndef READER_STEPREADER_HPP_
#define READER_STEPREADER_HPP_

#include <TopoDS_Shape.hxx>
#include <STEPControl_Reader.hxx>
#include "Reader.hpp"
#include <string>
/*
 *
 */
class STEPReader: public Reader {
public:

	STEPReader(STEPControl_Reader* stepControlReader);
	virtual ~STEPReader();

	TopoDS_Shape read(std::string filename);
};

#endif /* READER_STEPREADER_HPP_ */
