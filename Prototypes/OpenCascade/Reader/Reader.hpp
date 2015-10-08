/*
 * Reader.hpp
 *
 *  Created on: Oct 6, 2015
 *      Author: friedrich
 */

#ifndef READER_READER_HPP_
#define READER_READER_HPP_

#include <TopoDS_Shape.hxx>
#include <Handle_TDocStd_Document.hxx>
#include <string>

class Reader{
public:
	Reader(){};
	virtual ~Reader(){};
	virtual void read(const std::string filename) = 0;
	virtual void transfer(Handle_TDocStd_Document& doc) = 0;
protected:

};




#endif /* READER_READER_HPP_ */
