/*
 * UnitTestsuite.cpp
 *
 *  Created on: Nov 24, 2015
 *      Author: friedrich
 */

#include "UnitTest_suite.hpp"

#include "HelperTests/Helper_suite.hpp"

UnitTest_suite::UnitTest_suite() {
	// TODO Auto-generated constructor stub

}

UnitTest_suite::~UnitTest_suite() {
	// TODO Auto-generated destructor stub
}

CppUnit::TestSuite* UnitTest_suite::suite() {
	CppUnit::TestSuite *unitTestSuite = new CppUnit::TestSuite( "unitTestSuite" );
	unitTestSuite->addTest(Helper_suite::suite());
	return unitTestSuite;
}
