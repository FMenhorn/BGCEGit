class VerteX:
    def __init__(self, _id, quads_o, _vertexlist):
        import numpy as np
        if not ( type(_vertexlist) is np.ndarray):
            print "WRONG TYPE! exiting..."
            quit()
        #quads = {}
        #for point in _quadlist:
        #    quads[(int(point[0]), int(point[1]), int(point[2]))] = True

        #verts= {}
        #for point in _vertexlist:
        #    verts[(float(point[0]), float(point[1]), float(point[2]))] = True

        self.id = _id
        self.belongsTo= self.quad_belongs(quads_o)


    def quad_belongs(self, quads):
        import numpy as np

        owners = np.array([])

        for q in quads:
             if self.id in q.vertices:
                owners= np.append(owners, q.id)

        return owners.astype(int)


