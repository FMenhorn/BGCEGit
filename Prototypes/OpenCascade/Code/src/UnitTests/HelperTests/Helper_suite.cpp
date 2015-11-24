/*
 * Helpersuite.cpp
 *
 *  Created on: Nov 24, 2015
 *      Author: friedrich
 */

#include "Helper_suite.hpp"

#include <cppunit/TestCaller.h>

#include "Helper_test.hpp"
Helper_suite::Helper_suite() {
	// TODO Auto-generated constructor stub

}

Helper_suite::~Helper_suite() {
	// TODO Auto-generated destructor stub
}

CppUnit::TestSuite* Helper_suite::suite() {
	CppUnit::TestSuite *helperSuite = new CppUnit::TestSuite("Helper_suite");
	helperSuite->addTest(new CppUnit::TestCaller<Helper_test>(
						"testAbsolute",
						&Helper_test::testAbsolute));
	return helperSuite;
}
