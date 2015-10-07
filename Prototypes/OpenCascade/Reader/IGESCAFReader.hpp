/*
 * STEPCAFReader.hpp
 *
 *  Created on: Oct 7, 2015
 *      Author: friedrich
 */

#ifndef READER_IGESCAFREADER_HPP_
#define READER_IGESCAFREADER_HPP_

#include "Reader.hpp"

#include <TopoDS_Shape.hxx>
#include <IGESCAFControl_Reader.hxx>
#include <string>
/*
 *
 */
class IGESCAFReader:public Reader {
public:
	IGESCAFReader();
	virtual ~IGESCAFReader();

	TopoDS_Shape read(const std::string filename);
	void transfer(Handle_TDocStd_Document& doc);

private:
	IGESCAFControl_Reader igesCAFControlReader;
};

#endif /* READER_IGESCAFREADER_HPP_ */
