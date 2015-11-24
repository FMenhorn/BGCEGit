/*
 * UnitTest.cpp
 *
 *  Created on: Nov 24, 2015
 *      Author: friedrich
 */

#include <iostream>
#include <cppunit/ui/text/TestRunner.h>

#include "UnitTest_suite.hpp"

using namespace std;

int main() {
	CppUnit::TextUi::TestRunner runner;
	runner.addTest(UnitTest_suite::suite());
	runner.run();

	return 0;
}


