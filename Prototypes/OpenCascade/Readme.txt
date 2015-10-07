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