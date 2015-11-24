/*
 * Helper_test.cpp
 *
 *  Created on: Nov 24, 2015
 *      Author: friedrich
 */

#include "Helper_test.hpp"

#include <assert.h>

#include "../../Helper/Helper.hpp"
Helper_test::Helper_test() {
	// TODO Auto-generated constructor stub

}

Helper_test::~Helper_test() {
	// TODO Auto-generated destructor stub
}

void Helper_test::setUp() {
}

void Helper_test::tearDown() {
}

void Helper_test::testAbsolute() {

	const double pos = 1;
	const double neg = -1;

	const double expected = 1;

	const double resultAbsOnPos = absolut(pos);
	CPPUNIT_ASSERT_EQUAL(expected, resultAbsOnPos);

	const double resultAbsOnNeg = absolut(neg);
	CPPUNIT_ASSERT_EQUAL(expected, resultAbsOnNeg);
}
