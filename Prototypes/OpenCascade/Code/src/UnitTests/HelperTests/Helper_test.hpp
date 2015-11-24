/*
 * Helper_test.h
 *
 *  Created on: Nov 24, 2015
 *      Author: friedrich
 */

#ifndef CODE_SRC_UNITTESTS_HELPERTESTS_HELPER_TEST_HPP_
#define CODE_SRC_UNITTESTS_HELPERTESTS_HELPER_TEST_HPP_

#include <cppunit/TestCase.h>

class Helper_test: public CppUnit::TestFixture {
public:
	Helper_test();
	virtual ~Helper_test();

	void setUp();
	void tearDown();

	void testAbsolute();
};


#endif /* CODE_SRC_UNITTESTS_HELPERTESTS_HELPER_TEST_HPP_ */
