/*
 * UnitTestsuite.hpp
 *
 *  Created on: Nov 24, 2015
 *      Author: friedrich
 */

#ifndef CODE_SRC_UNITTESTS_UNITTEST_SUITE_HPP_
#define CODE_SRC_UNITTESTS_UNITTEST_SUITE_HPP_

#include <cppunit/TestSuite.h>
/*
 *
 */
class UnitTest_suite {
public:
	UnitTest_suite();
	virtual ~UnitTest_suite();

	static CppUnit::TestSuite* suite();
};

#endif /* CODE_SRC_UNITTESTS_UNITTEST_SUITE_HPP_ */
