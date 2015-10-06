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
LDFLAGSBASE= -L/usr/local/lib/oce-0.17-dev -lTKTopAlgo -lTKBRep -lTKernel -lTKMath\
-lTKVoxel -lTKXSBase 

LDFLAGSSTL= $(LDFLAGSBASE) -lTKSTL
LDFLAGSIGES= $(LDFLAGSSTL) -lTKIGES
LDFLAGSSTEP= $(LDFLAGSBASE) -lTKSTEP
INCLUDES= -I/usr/local/include/oce 

SOURCESSTL= ./STLReader.cpp
SOURCESIGES= ./IGESReader.cpp
SOURCESSTEP= ./STEPReader.cpp

OBJECTSSTL=$(SOURCESSTL:.cpp=.o)
OBJECTSIGES=$(SOURCESIGES:.cpp=.o)
OBJECTSSTEP=$(SOURCESSTEP:.cpp=.o)

EXECUTABLESTL=STLReader
EXECUTBALEIGES=IGESReader
EXECUTABLESTEP=STEPReader

all:
	make stl && make iges && make step

stl: $(SOURCESSTL) $(EXECUTABLESTL)

iges: $(SOURCESIGES) $(EXECUTBALEIGES)

step: $(SOURCESSTEP) $(EXECUTABLESTEP)

$(EXECUTABLESTL): $(OBJECTSSTL)
	$(CC) $(OBJECTSSTL) $(LDFLAGSSTL) -o $@ 

$(EXECUTBALEIGES): $(OBJECTSIGES)
	$(CC) $(OBJECTSIGES) $(LDFLAGSIGES) -o $@

$(EXECUTABLESTEP): $(OBJECTSSTEP)
	$(CC) $(OBJECTSSTEP) $(LDFLAGSSTEP) -o $@

clean:
	rm $(EXECUTABLESTL) $(EXECUTBALEIGES) $(EXECUTABLESTEP) $(OBJECTSSTL) $(OBJECTSIGES) $(OBJECTSSTEP)

.cpp.o:
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@
 
