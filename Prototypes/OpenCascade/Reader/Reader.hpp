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

	/**
	 * virtual method which has to be implemented by children. reads the file with filename into the corresponding implementation of the reader
	 * @param filename
	 */
	virtual void read(const std::string filename) = 0;

	/**
	 * virtual method which has to be implemented by children. Transfers the object/model/shape from the reader into the the TDocStd_Document doc
	 * @param doc
	 */
	virtual void transfer(Handle_TDocStd_Document& doc) = 0;

protected:

};




#endif /* READER_READER_HPP_ */
