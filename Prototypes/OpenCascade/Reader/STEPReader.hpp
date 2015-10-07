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
#include <Interface_Static.hxx>
#include <Standard_CString.hxx>

#include "Reader.hpp"
#include <string>
/*
 *
 */
class STEPReader: public Reader {
public:

	STEPReader(XSControl_Reader* stepControlReader);
	virtual ~STEPReader();

	TopoDS_Shape read(const std::string filename);
};

#endif /* READER_STEPREADER_HPP_ */
