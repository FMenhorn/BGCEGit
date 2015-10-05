# This is a makefile template
# Compiler
# --------
CC=g++
#CC=icpc

include files.mk
# Compiler flags
# -------------------------------------------------------------------------
CFLAGS=-g -O3 -std=c++0x
# Linker flags
# ------------
LDFLAGS= -L/usr/local/lib/oce-0.17-dev -lTKTopAlgo -lTKBRep -lTKernel -lTKMath\
-lTKSTL -lTKVoxel
INCLUDES= -I/usr/local/include/oce 

OBJECTS=$(SOURCES:.cpp=.o)
EXECUTABLE=OpenCascade

all: $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(OBJECTS) $(LDFLAGS) -o $@ 

clean:
	rm $(OBJECTS)

.cpp.o:
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@
 
