/*
 * ColorHandler.hpp
 *
 *  Created on: Oct 7, 2015
 *      Author: BGCE
 */

#ifndef COLORHANDLER_COLORHANDLER_HPP_
#define COLORHANDLER_COLORHANDLER_HPP_

#include <TDocStd_Document.hxx>
#include <Handle_TDocStd_Document.hxx>
#include <XCAFDoc_ShapeTool.hxx>
#include <Handle_XCAFDoc_ShapeTool.hxx>
#include <Quantity_Color.hxx>
#include <XCAFDoc_ColorTool.hxx>
#include <TDF_LabelSequence.hxx>
#include <TopoDS_Face.hxx>

#include <vector>
/*
 *
 */
class ColorHandler {
public:
	ColorHandler();
	virtual ~ColorHandler();

	void getColoredFaces(std::vector<TopoDS_Face>& faceVector);
	Handle_TDocStd_Document& getDoc();
	void initializeMembers();

private:
    Handle_TDocStd_Document aDoc;
    Handle_XCAFDoc_ShapeTool myAssembly;
    TDF_LabelSequence aLabel;
    Handle_XCAFDoc_ColorTool myColors;

	bool isDocumentValid();
};

#endif /* COLORHANDLER_COLORHANDLER_HPP_ */
