from quadvertGenerator import quad_vert_generator
from DCtoPeter import dc_to_peter
import scipy.io as sio


vertices, quads, parameters, fine_vertices = quad_vert_generator()

# For now we use test data to not run Annas slow code
#dc_to_peter(vertex_list, quad_list)
mat_contents = sio.loadmat('Data/test_mat.mat')

A = mat_contents["A"]
B1 = mat_contents["B1"]
B2 = mat_contents["B2"]
C = mat_contents["C"]

