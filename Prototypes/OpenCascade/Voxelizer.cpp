#include "Voxelizer.hpp"

Voxel_BoolDS Voxelizer::voxelize(TopoDS_Shape topoDSShape, int refinementLevel){

    std::cout << "Voxelizer: Getting domain bounds .." << std::endl;

    double* shapeDimensions = getBoundingBox(topoDSShape);

    int voxelCount[3];
    for (sizt_t i = 0; i < 3; i++)
        voxelCount[i] = pow(2, refinementLevel) * shapeDimensions[i];

    Voxel_BoolDS voxelShape = voxelBool; // Result holder of the voxelization
    Standard_Integer progress; // Progress of voxelization (useful in case of parallel code)
    std::cout << "Voxelizer: Voxelizing .." << std::endl;
	Voxel_FastConverter voxelConverter(topoDSShape, voxelShape, 0.1, N_X, N_Y, N_Z);
	voxelConverter.Convert(progress);
	std::cout << "Voxelizer: Progress of Conversion: " << progress << std::endl;

    std::cout << "Voxelizer: .. done!" << std::endl;

    return voxelShape;
}

double* Voxelizer::getBoundingBox(TopoDS_Shape topoDSShape){
    Bnd_Box B; // Bounding box
	double Xmin, Ymin, Zmin, Xmax, Ymax, Zmax; // Bounding box bounds
    BRepBndLib::Add(topoDSShape, B);
    B.Get(Xmin, Ymin, Zmin, Xmax, Ymax, Zmax);

    double shapeDimensions[3];
    shapeDimensions[0] = abs(Xmax - Xmin);
    shapeDimensions[1] = abs(Ymax - Ymin);
    shapeDimensions[2] = abs(Zmax - Zmin);

    std::cout << "Voxelizer-getBoundingBox:" << std::endl;
    std::cout << " X[" << Xmin << ", " << Xmax << "] | xDimension: " << shapeDimensions[0] << std::endl;
    std::cout << " Y[" << Ymin << ", " << Ymax << "] | yDimension: " << shapeDimensions[1] << std::endl;
    std::cout << " Z[" << Zmin << ", " << Zmax << "] | zDimension: " << shapeDimensions[2] << std::endl;

    return shapeDimensions;
}
