/*
 * STEPCAFReader.hpp
 *
 *  Created on: Oct 8, 2015
 *      Author: friedrich
 */

#ifndef READER_STEPCAFREADER_HPP_
#define READER_STEPCAFREADER_HPP_

#include "Reader.hpp"

#include <TopoDS_Shape.hxx>
#include <STEPCAFControl_Reader.hxx>
#include <string>
/*
 *
 */
class STEPCAFReader: public Reader {
public:
	STEPCAFReader();
	virtual ~STEPCAFReader();

	void read(const std::string filename);
	void transfer(Handle_TDocStd_Document& doc);

private:
	STEPCAFControl_Reader stepCAFControlReader;
};

#endif /* READER_STEPCAFREADER_HPP_ */
