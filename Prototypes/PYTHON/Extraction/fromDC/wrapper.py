__author__ = 'juan'

from Vertex import Vertex
from Edge import Edge
from Quad import Quad
import numpy as np

_verts=np.array(np.genfromtxt('cantilever_verts_coarse.csv',delimiter=';'))
_quads=np.array(np.genfromtxt('cantilever_quads_coarse.csv',delimiter=';'))
_parameters=np.genfromtxt('parameters.csv',delimiter=';')

#Create vertices
vertexList=[]
for i in range(_verts.shape[0]):
    vertexList.append(Vertex(_id=i,_x=_verts[i,0],_y=_verts[i,1],_z=_verts[i,2]))



#Creating edges
edgeDict={}
edge_id=0
for i in range(_quads.shape[0]):
    edges = [(_quads[i,0], _quads[i,1]),  # edges of this quad
             (_quads[i,1], _quads[i,2]),
             (_quads[i,2], _quads[i,3]),
             (_quads[i,3], _quads[i,0])]
    for e in edges:
        key = tuple(sorted(e))
        if key not in edgeDict:
            edgeDict[key]= Edge(edge_id,vertexList[int(key[0])],vertexList[int(key[1])])
            edge_id+=1

#Creating quads
quadList=[]
for i in range(_quads.shape[0]):
    a=int(_quads[i,0])
    b=int(_quads[i,1])
    c=int(_quads[i,2])
    d=int(_quads[i,3])
    e1=tuple(sorted([_quads[i,0], _quads[i,1]]))  # edges of this quad
    e2=tuple(sorted((_quads[i,1], _quads[i,2])))
    e3= tuple(sorted((_quads[i,2], _quads[i,3])))
    e4=tuple(sorted((_quads[i,3], _quads[i,0])))
    quadList.append(Quad(i,vertexList[a],vertexList[b],vertexList[c],vertexList[d],edgeDict[e1],edgeDict[e2],edgeDict[e3],edgeDict[e4]))

#Errasing hanging nodes

for i in range(vertexList.__len__()):
    if not vertexList[i].get_quads():
        vertexList[i]=None

#New Id's of vertices
new_id=0;
new_vertexList=[];
for i in range(vertexList.__len__()):
     if vertexList[i] is not None:
        new_vertexList.append(vertexList[i])
        vertexList[i].id=new_id
        new_id+=1

#Check if every edge has only two quads!
for e in edgeDict:
    if (edgeDict[e].get_quads().__len__() >2):
        print e

#Create parameterList
parameterList=[]
for i in range(_parameters.shape[0]):
   parameterList.append([quadList[int(_parameters[i,0])],_parameters[i,1],_parameters[i,2]])



#UNNECESARY CODE, BECAUSE ANNA WANTS IT, AND SHE IS CUTE--WRAPPER TO THE WRAPPER
def export_as_csv(data,name):
    import csv
    with open(name+'.csv', 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';',
                           quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for d in data:
            csvwriter.writerow(d)
verts=[];

quads=[];

verts= [new_vertexList[i].get_coordinates()  for i in range(new_vertexList.__len__())]

for i in range(quadList.__len__()):
    quads.append([quadList[i].get_vertices()[j].id for j in range(4)])

export_as_csv(verts, 'cantilever_verts_coarse_new')
export_as_csv(quads, 'cantilever_quads_coarse_new')














