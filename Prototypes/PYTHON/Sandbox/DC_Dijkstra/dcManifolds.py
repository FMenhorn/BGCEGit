__author__ = 'benjamin'


def detectManifolds2d(dc_edges):
    def create_vertex_usage_dict(dc_edges):
        vertex_usage_dict = dict()

        for e in dc_edges:  # traverse all edges
            vertex_keys = e # keys of the vertices

            for v_key in vertex_keys:  # traverse all vertex keys of this edge
                if v_key in vertex_usage_dict:  # if the key is already in global list
                    vertex_usage_dict[v_key] += 1  # increase usage by one
                else:
                    vertex_usage_dict[v_key] = 1  # add key to dict and initialize with one usage

        return vertex_usage_dict

    vertex_usage_dict = create_vertex_usage_dict(dc_edges)
    manifold_vertices = set()

    for v_key, use_no in vertex_usage_dict.items():
        if use_no > 2:
            manifold_vertices.add(v_key)

    return manifold_vertices


def detectManifolds3d(dc_quads):
    raise Exception("TO BE IMPLEMENTED!")

