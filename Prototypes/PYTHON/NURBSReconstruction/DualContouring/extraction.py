from dualcontouring import tworesolution_dual_contour
from projection import create_parameters
from quad import Quad
import cPickle


def transform_dict(cellsDict):
    dataset = {}
    for key in cellsDict:
        dataset[key] = -1

    return dataset

def read_from_path(path, coarse_scale):
    wfFile = open(path+'/Cells', 'rb')
    cellsDict = cPickle.load(wfFile)
    wfFile.close()

    wfFile = open(path+'/Dimensions', 'rb')
    dimensions = cPickle.load(wfFile)
    wfFile.close()

    res_fine = 1.0
    res_coarse = res_fine * coarse_scale

    resolutions = {'fine': res_fine,'coarse': res_coarse}

    fine_data = transform_dict(cellsDict)

    return fine_data, dimensions, resolutions


def extraction_algorithm(fine_data, resolutions, dimensions):
    print "###Dual Contouring###"
    [verts_out_dc, quads_out_dc, manifolds] = tworesolution_dual_contour(fine_data, resolutions, dimensions)
    print "###Dual Contouring DONE###"

    N_quads = {'coarse': quads_out_dc['coarse'].__len__(), 'fine': quads_out_dc['fine'].__len__()}
    N_verts = {'coarse': verts_out_dc['coarse'].__len__(), 'fine': verts_out_dc['fine'].__len__()}

    quads = {'coarse': [None] * N_quads['coarse'], 'fine': quads_out_dc['fine']}
    verts = {'coarse': verts_out_dc['coarse'], 'fine': verts_out_dc['fine']} # todo substitute with vertex objects

    for i in range(N_quads['coarse']):
        quads['coarse'][i]=Quad(i,quads_out_dc['coarse'],verts_out_dc['coarse'])

    print "### Projecting Datapoints onto coarse quads ###"
    # do projection of fine verts on coarse quads
    param = create_parameters(verts, quads)
    print "### Projecting Datapoints onto coarse quads DONE ###"

    return verts_out_dc, quads_out_dc, param


def extract_surface_from_path_w_plot(path):

    fine_data, dimensions, resolutions = read_from_path(path,2.0)
    [verts, quads, params] = extraction_algorithm(fine_data=fine_data,
                                                  resolutions=resolutions,
                                                  dimensions=dimensions)
    return verts, quads, params, dimensions


def extract_surface_from_path_wrapped(path):
    verts,quads,params,notused=extract_surface_from_path_w_plot(path)
    return verts, quads, params

def extract_surface(path):
    verts,quads,params,notused=extract_surface_from_path_w_plot(path)
    return verts['coarse'], quads['coarse'], verts['fine'], params