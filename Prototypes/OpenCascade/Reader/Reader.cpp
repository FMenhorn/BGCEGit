/*
 * Reader.cpp
 *
 *  Created on: Oct 19, 2015
 *      Author: Saumitra Joshi
 */

#include <dirent.h>

#include "Reader.hpp"

Reader::~Reader() {
	// TODO Auto-generated destructor stub
}

void Reader::read() {
	// Check file extension
	int len;
	bool stpFlag = false, igsFlag = false;
	struct dirent *pDirent;
	DIR *pDir;

	pDir = opendir(sourceFilePath.c_str());
	if (pDir != NULL) {
		while ((pDirent = readdir(pDir)) != NULL) {
			len = strlen (pDirent->d_name);
			if (len >= 4) {
				if (strcmp (".stp", &(pDirent->d_name[len - 4])) == 0) {
					stpFlag = true;
				} else if (strcmp (".igs", &(pDirent->d_name[len - 4])) == 0) {
					igsFlag = true;
				}
			}
		}
		closedir (pDir);
	}

	if (stpFlag) {
		std::cout << "Reader: Reading " << sourceFilePath + sourceFileName + ".stp" << std::endl;
		readerStep.read(sourceFilePath + sourceFileName + ".stp");
	}
	else {
		std::cout << "Reader: Reading " << sourceFilePath + sourceFileName + ".step" << std::endl;
		readerStep.read(sourceFilePath + sourceFileName + ".step");
	}

	if (igsFlag) {
		std::cout << "Reader: Reading " << sourceFilePath + sourceFileName + ".igs" << std::endl;
		readerIges.read(sourceFilePath + sourceFileName + ".igs");
	}
	else {
		std::cout << "Reader: Reading " << sourceFilePath + sourceFileName + ".iges" << std::endl;
		readerIges.read(sourceFilePath + sourceFileName + ".iges");
	}
}

void Reader::transfer(ColorHandler& colorHandler) {
	readerStep.transfer(colorHandler.getDocStep());
	readerIges.transfer(colorHandler.getDocIges());
}
