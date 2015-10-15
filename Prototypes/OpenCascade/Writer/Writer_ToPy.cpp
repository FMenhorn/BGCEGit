/*
 * STEPReader.hpp
 *
 *  Created on: Oct 6, 2015
 *      Author: saumitra
 */

#include "Writer_ToPy.hpp"


bool Writer_ToPy::write(std::string _filename,std::vector<Voxel_BoolDS> &voxelShape){
    std::vector<int> dimensions(3);
    dimensions[0]=voxelShape[0].GetNbX();
    dimensions[1]=voxelShape[0].GetNbY();
    dimensions[2]=voxelShape[0].GetNbZ();
    ofstream outfile;
    std::cout << "Writer: Writing Tpd file for " + _filename + " .." << std::endl;
    outfile.open(_filename + ".tpd", ios::out | ios::trunc);

    writeHeader(outfile, _filename);
    writeDimensions(outfile, dimensions);
    writeGreyScaleFilters(outfile);
//Write active nodes
//    writeNodes("ACTV_ELEM", outfile,voxelShape[0],dimensions);
//use different voxel shape vector and do the same for the others
// writeNodes("PASV_ELEM",outfile,voxelShape[1],dimensions);
//writeNodes("FXTR_NODE_X",outfile,voxelShape[2],dimensions);

    outfile.close();

    std::cout << "Writer: .. done!" << std::endl;

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


 void Writer_ToPy::writeNodes(std::string name, std::ofstream &outfile, Voxel_BoolDS &voxelShape, std::vector<int> dimensions){
	outfile<< name << ": ";
	float hx=voxelShape.GetX();
	float hy=voxelShape.GetY();
	float hz=voxelShape.GetZ();
        for (int k = 0; k < voxelShape.GetNbZ(); k++){
        for (int i = 0; i < voxelShape.GetNbX(); i++){
            for (int j = 0; j < voxelShape.GetNbY(); j++){
	        if (voxelShape.Get(i,j,k)==Standard_True){
//change to list.append
//		std::cout<<"X: "<< i*hx<<" Y:  "<<j*hy<<" Z: "<<k*hz << " Index: "<<(j+(voxelShape.GetNbY())*(i+k*(voxelShape.GetNbZ()))) << std::endl;
  	        outfile << (j+(voxelShape.GetNbY())*(i+k*(voxelShape.GetNbZ()))) <<"; ";
                }
            }
        }
        }
}
int Writer_ToPy::getIndex(int x, int y, int z, std::vector<int> dimensions){

return y + (dimensions[1]+1)*(x + (dimensions[0]+1) * z);

}

