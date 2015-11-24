/*
 * Helpersuite.hpp
 *
 *  Created on: Nov 24, 2015
 *      Author: friedrich
 */

#ifndef CODE_SRC_UNITTESTS_HELPERTESTS_HELPER_SUITE_HPP_
#define CODE_SRC_UNITTESTS_HELPERTESTS_HELPER_SUITE_HPP_

#include <cppunit/TestSuite.h>
/*
 *
 */
class Helper_suite {
public:
	Helper_suite();
	virtual ~Helper_suite();

	static CppUnit::TestSuite* suite();
};

#endif /* CODE_SRC_UNITTESTS_HELPERTESTS_HELPER_SUITE_HPP_ */
