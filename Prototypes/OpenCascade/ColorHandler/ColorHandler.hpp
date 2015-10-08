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
	/**
	 * Initializes the doc
	 */
	ColorHandler();
	virtual ~ColorHandler();

	/**
	 * Returns the Document aDoc
	 * @return
	 */
	Handle_TDocStd_Document& getDoc();

	/**
	 * Initializes the other members
	 */
	void initializeMembers();

	/**
	 * Assembles the shape with the help of the XCAFDoc_ShapeTool myAssembly and the TDF_LabelSequence aLabel.
	 * Steps then through the faces, if they are colored they are added to the std::vector<TopoDS_Face>& faceVector
	 * and to the TopoDS_Shape& sewedShape
	 * @param faceVector after the call, holds the colored faces of the object
	 * @param sewedShape after the call, holds the TopoDS_Shape sewed together out of the colored shapes/faces
	 */
	void getColoredFaces(std::vector<TopoDS_Face>& faceVector, TopoDS_Shape& sewedShape);

private:
    Handle_TDocStd_Document aDoc;
    Handle_XCAFDoc_ShapeTool myAssembly;
    TDF_LabelSequence aLabel;
    Handle_XCAFDoc_ColorTool myColors;

	bool isDocumentValid();
};

#endif /* COLORHANDLER_COLORHANDLER_HPP_ */
