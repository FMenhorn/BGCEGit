#!/bin/bash
cd OpenCascade
./build/CADToVoxel $1 $2 $3 $4
cd ..
python OpenCascade/optimise.py OpenCascade/topy_${2}.tpd
cp topy_${2}_099.vtk PYTHON/Extraction/WorkUnstructuredGrid/
cd PYTHON/Extraction/WorkUnstructuredGrid 
python Ugrid_to_Python.py topy_${2}_099.vtk
cd ..
cd ..
cp Extraction/WorkUnstructuredGrid/Cells DualContouring/Cantilever/
cp Extraction/WorkUnstructuredGrid/Dimensions DualContouring/Cantilever/
cd DualContouring
python example_Cantilever.py

