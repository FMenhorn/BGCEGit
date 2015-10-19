/*
 * STEPReader.hpp
 *
 *  Created on: Oct 6, 2015
 *      Author: saumitra
 */

#include "Writer_ToPy.hpp"


bool Writer_ToPy::write(std::string _filename, std::vector<std::vector<VoxelShape>> &voxelShape){
    std::vector<int> dimensions(3);
    dimensions[0]=voxelShape[0][0].getVoxelShape().GetNbX();
    dimensions[1]=voxelShape[0][0].getVoxelShape().GetNbY();
    dimensions[2]=voxelShape[0][0].getVoxelShape().GetNbZ();
    ofstream outfile;
    std::cout << "Writer_ToPy: Writing Tpd file for " + _filename + " .." << std::endl;
    std::cout << "Writer_ToPy: with dimensions: " << dimensions[0] << "," << dimensions[1] << "," << dimensions[2] << std::endl;
    outfile.open(_filename + ".tpd", ios::out | ios::trunc);

    writeHeader(outfile, _filename);
    writeDimensions(outfile, dimensions);
    writeGreyScaleFilters(outfile);
	//Write active nodes
	writeNodes("ACTV_ELEM", outfile,voxelShape[0],dimensions);
	//use different voxel shape vector and do the same for the others
	writeNodes("PASV_ELEM",outfile,voxelShape[3],dimensions);
	writeNodes("FXTR_NODE_X",outfile,voxelShape[1],dimensions);
	writeNodes("FXTR_NODE_Y",outfile,voxelShape[1],dimensions);
	writeNodes("FXTR_NODE_Z",outfile,voxelShape[1],dimensions);
	//writeNodes("LOAD_NODE_X",outfile,voxelShape[2],dimensions);
	int noLoadVoxelsY = writeNodes("LOAD_NODE_Y",outfile,voxelShape[2],dimensions);
	//writeNodes("LOAD_NODE_Z",outfile,voxelShape[2],dimensions);

	outfile << "LOAD_VALU_Y: " << "-1@" << noLoadVoxelsY << "\n";
    outfile.close();

    std::cout << "Writer_ToPy: .. done!" << std::endl;

    return true;

}

void Writer_ToPy::writeHeader(std::ofstream &outfile, std::string outputName){
	outfile << "[ToPy Problem Definition File v2007]\n";
	outfile << "\n";

	outfile << "PROB_TYPE:   comp\n";
	outfile << "PROB_NAME:   " << outputName << "\n";
	outfile << "ETA:         0.4\n";
	outfile << "DOF_PN:      3\n";
	outfile << "VOL_FRAC:    0.15\n";
	outfile << "FILT_RAD:    1.5\n";
	outfile << "ELEM_K:      H8\n";
	outfile << "NUM_ITER:    100\n";
}

void Writer_ToPy::writeDimensions(std::ofstream &outfile, std::vector<int> dimensions){
	outfile << "NUM_ELEM_X:  " << dimensions[0] << "\n";
	outfile << "NUM_ELEM_Y:  " << dimensions[1] << "\n";
	outfile << "NUM_ELEM_Z:  " << dimensions[2] << "\n";
	outfile << "\n";
}

void Writer_ToPy::writeGreyScaleFilters(std::ofstream &outfile){
	outfile << "# Grey-scale filter (GSF)\n";
	outfile << "P_FAC      : 1\n";
	outfile << "P_HOLD     : 15\n";
	outfile << "P_INCR     : 0.2\n";
	outfile << "P_CON      : 1\n";
	outfile << "P_MAX      : 3\n";
	outfile << "\n";
	outfile << "Q_FAC      : 1\n";
	outfile << "Q_HOLD     : 15\n";
	outfile << "Q_INCR     : 0.05\n";
	outfile << "Q_CON      : 1\n";
	outfile << "Q_MAX      : 5\n";
}

 int Writer_ToPy::writeNodes(std::string name, std::ofstream &outfile, std::vector<VoxelShape> &voxelShape, std::vector<int> dimensions){
	int size = 0;
	outfile<< name << ": ";
	for(size_t h = 0; h < voxelShape.size(); ++h){
		float hx=voxelShape[h].getVoxelShape().GetX();
		float hy=voxelShape[h].getVoxelShape().GetY();
		float hz=voxelShape[h].getVoxelShape().GetZ();
		for (int k = 0; k < voxelShape[h].getVoxelShape().GetNbZ(); k++){
			for (int i = 0; i < voxelShape[h].getVoxelShape().GetNbX(); i++){
				for (int j = 0; j < voxelShape[h].getVoxelShape().GetNbY(); j++){
					//std::cout << "Current Step: " << name << ":" << h << "," << k << "," << i << "," << j << std::endl;
				if (voxelShape[h].getVoxelShape().Get(i,j,k)==Standard_True){
	//change to list.append
					//std::cout<<"X: "<< i*hx<<" Y:  "<<j*hy<<" Z: "<<k*hz << " Index: "<<(j+(voxelShape[h].getVoxelShape().GetNbY())*(i+k*(voxelShape[h].getVoxelShape().GetNbZ()))) << std::endl;
					outfile << (j+(voxelShape[h].getVoxelShape().GetNbY())*(i+k*(voxelShape[h].getVoxelShape().GetNbZ()))) <<"; ";
					size++;
					}
				}
			}
		}
	}
	outfile << "\n";
	return size;
}
int Writer_ToPy::getIndex(int x, int y, int z, std::vector<int> dimensions){

return y + (dimensions[1]+1)*(x + (dimensions[0]+1) * z);

}
