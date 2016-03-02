#!/bin/bash
cd ../../
cd OpenCascade/Code
./build/CADToVoxel $1 $2 $3 $4 $5 $6
cd ..
cd ..
#python OpenCascade/Code/optimise.py OpenCascade/Code/topy_${2}.tpd
#cp topy_${2}_099.vtk PYTHON/Extraction/WorkUnstructuredGrid/
#cd PYTHON/Extraction/WorkUnstructuredGrid 
#python Ugrid_to_Python.py topy_${2}_099.vtk
#cd ..
#cd ..
#cp Extraction/WorkUnstructuredGrid/Cells NURBSReconstruction/
#cp Extraction/WorkUnstructuredGrid/Dimensions NURBSReconstruction/
#cd DualContouring
#python example_Cantilever.py

