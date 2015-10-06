import enthought.mayavi.mlab as mlab

center = np.array([16,16,16])
radius = 10

def test_f(x):
    d = x-center
    return np.dot(d,d) - radius**2

def test_df(x):
    d = x-center
    return d / sqrt(np.dot(d,d))

verts, tris = dual_contour(f, df, n)

mlab.triangular_mesh( 
            [ v[0] for v in verts ],
            [ v[1] for v in verts ],
            [ v[2] for v in verts ],
            tris)
