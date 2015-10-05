# This is a makefile template
# Compiler
# --------
CC=g++
#CC=icpc

#include files.mk
# Compiler flags
# -------------------------------------------------------------------------
CFLAGS=-g -O3 -std=c++0x
# Linker flags
# ------------
LDFLAGS= -L/usr/local/lib/oce-0.17-dev -lTKTopAlgo -lTKBRep -lTKernel -lTKMath\
-lTKSTL -lTKVoxel -lTKIGES -lTKXSBase
INCLUDES= -I/usr/local/include/oce 

SOURCESSTL= ./STLReader.cpp
SOURCESIGES= ./IGESReader.cpp

OBJECTSSTL=$(SOURCESSTL:.cpp=.o)
OBJECTSIGES=$(SOURCESIGES:.cpp=.o)
EXECUTABLESTL=STLReader
EXECTUBALEIGES=IGESReader

stl: $(SOURCESSTL) $(EXECUTABLESTL)

iges: $(SOURCESIGES) $(EXECTUBALEIGES)

$(EXECUTABLESTL): $(OBJECTSSTL)
	$(CC) $(OBJECTSSTL) $(LDFLAGS) -o $@ 

$(EXECTUBALEIGES): $(OBJECTSIGES)
	$(CC) $(OBJECTSIGES) $(LDFLAGS) -o $@

clean:
	rm $(EXECUTABLESTL) $(EXECTUBALEIGES) $(OBJECTSSTL) $(OBJECTSIGES)

.cpp.o:
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@
 
