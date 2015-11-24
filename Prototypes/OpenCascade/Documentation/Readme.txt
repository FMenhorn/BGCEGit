If you get the following error:
	Could not open shared library something something, check your LD_LIBRARY_PATH:
		echo $LD_LIBRARY_PATH
	should say:
		/usr/local/lib
	If not:
		export LD_LIBRARY_PATH=$(LD_LIBRARY_PATH):/usr/local/lib

Makefile:
	Make stlreader executable: 
		make stl 
	Make igesreader executable:
		make iges

Documentation:
	http://dev.opencascade.org/doc/refman/html/index.html

IGESReaderTutorial: 
	http://dev.opencascade.org/doc/overview/html/occt_user_guides__iges.html

STEPReaderTutorial:
	http://dev.opencascade.org/doc/overview/html/occt_user_guides__step.html

STL/IGESFiles (needs account):
	https://grabcad.com/library/most-downloaded?page=1&per_page=100


STEP/IGES Color Detection lead:
	http://dev.opencascade.org/doc/overview/html/occt_user_guides__xde.html
	https://www.quora.com/What-is-the-most-popular-file-format-used-for-sharing-CAD-files
	
Voxel_BoolDS functions:
        Voxel_BoolDS::GetCenter(x, y, z, cX, cY, cZ)
                Returns the value of the center of the voxel (Standard_Real) located at indices x, y, z in cX, cY, cZ.
        Voxel_BoolDS::GetNbX/Y/Z()
                Returns the number of voxels (Standard_Integer) in X/Y/Z direction.
        Voxel_BoolDS::GetX/Y/ZLen()
                Returns the actual dimension (Standard_Real) in the X/Y/Z direction
        Voxel_BoolDS::GetX/Y/Z()
                Returns the X/Y/Z direction width of each voxel in the grid
