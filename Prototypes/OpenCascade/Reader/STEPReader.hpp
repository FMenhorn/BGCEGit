/*
 * STEPReader.hpp
 *
 *  Created on: Oct 6, 2015
 *      Author: friedrich
 */

#ifndef READER_STEPREADER_HPP_
#define READER_STEPREADER_HPP_

#include <TopoDS_Shape.hxx>

#include "Reader.hpp"
#include <string>
/*
 *
 */
class STEPReader: public Reader {
public:

	STEPReader();
	virtual ~STEPReader();

	TopoDS_Shape read(const std::string filename);

private:
	//STEPControl_Reader stepReader;
};

#endif /* READER_STEPREADER_HPP_ */
