__author__ = 'benjamin'

from Vertex import Vertex2
from Edge import Edge2
from coarsening import find_connected_sets, coarsen

v1 = Vertex2(1,2)
v2 = Vertex2(2,3)
v3 = Vertex2(3,4)
v4 = Vertex2(4,5)

e1 = Edge2(v1,v2)
e2 = Edge2(v2,v3)
e3 = Edge2(v3,v1)

orig_v_s = set([v1,v2,v4])

v_ss = find_connected_sets(orig_v_s)
print "connected sets:"
for v_s in v_ss:
    print v_s
    for v in set(v_s):
        print str(v) +"@"+str(v.get_position())

cv_s, ce_s = coarsen(orig_v_s)

print "coarsened:"
print "vertices"
for v in cv_s:
    print str(v) +"@"+str(v.get_position())
print "edges"
for e in ce_s:
    vs = e.get_vertices()
    print str(e) +"["+str(vs[0])+","+str(vs[1])+"]"
