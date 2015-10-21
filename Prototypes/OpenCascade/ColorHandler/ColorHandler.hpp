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
#include <TopTools_ListOfShape.hxx>
#include <gp_Vec.hxx>

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
	 * Returns the Document aDocStep
	 * @return
	 */
	Handle_TDocStd_Document& getDocStep();

	/**
	 * Returns the Document aDocIges
	 * @return
	 */
	Handle_TDocStd_Document& getDocIges();

	/**
	 * Initializes the other members
	 */
	void initializeMembers();

	/**
	 * Calls getColoredFaces with color red
	 * @param listOfShapes holds all shapes with the color red
	 */
	void getFixtureShapes(TopTools_ListOfShape& listOfShapes);

	/**
	 * Calls getColoredFaces with color blue
	 * @param listOfShapes holds all shapes with the color blue
	 */
	void getPassiveShapes(TopTools_ListOfShape& listOfShapes);

	/**
	 * Calls getColoredFaces with color green
	 * @param listOfShapes holds all shapes with the color green
	 */
	void getLoadShapes(TopTools_ListOfShape& listOfShapes);

	/**
     * Returns the faces of the geometry as a TopoDS_Shape.
     */
	void getCompleteShape(TopoDS_Shape& TopoDSShape);

private:
    Handle_TDocStd_Document aDocStep;
    Handle_TDocStd_Document aDocIges;
    Handle_XCAFDoc_ColorTool myColors;
    TopoDS_Shape shapeStep;
    TopoDS_Shape shapeIges;

	void buildShapesFromDocs();

    void buildShapeFromDoc(const Handle_TDocStd_Document& doc, TopoDS_Shape& shape);

	/**
	 * Assembles the shape with the help of the XCAFDoc_ShapeTool myAssembly and the TDF_LabelSequence aLabel.
	 * Steps then through the faces, if they are colored with wantedColor they are added to the
	 * TopTools_ListOfShape& listOfShapes after being build from the faces.
	 * @param listOfShapes holds all shapes with the color wanted color
	 * @param wantedColor the color for which we are looking on the faces
	 */
	void getColoredFaces(TopTools_ListOfShape& listOfShapes,const Quantity_Color wantedColor);

	/**
	 * Computes normal of the face
	 */
    void computeInvertedNormal(const TopoDS_Face& findNormalTo, gp_Vec& normal);

	bool areDocumentsValid();
	void findColoredFaces(const Quantity_Color& wantedColor, std::vector<TopoDS_Face>& coloredFacesVector);
	void buildColoredFaces(const std::vector<TopoDS_Face>& coloredFacesVector, TopTools_ListOfShape& listOfShapes);
};

#endif /* COLORHANDLER_COLORHANDLER_HPP_ */