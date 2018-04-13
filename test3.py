from gurobipy import *

import os
os.system("python testossystem.py 1")

#### Vertices all with demand 0 ####
verticesini = []
for i in N:
    verticesini.append(tuple((i, 0)))

vertices=dict(verticesini)

#### Edges ####
edgeini=[]
for (i,j) in A:
    d=abs(i-j)
    dd=tuple(((i,j), d))
    edgeini.append(dd)
edge=dict(edgeini)

m=Model()

y={}

edgeIn   = { v:[] for v in vertices }
edgeOut  = { v:[] for v in vertices }

for edge in edges:
    y[edge] = m.addVar(vtype=GRB.BINARY, name="y" + str(edge))

m.update()

for v in vertices:
    m.addConstr(quicksum(edgeOut[v]) - quicksum(edgeIn[v]) == vertices[v], name="v%d" % v)
    
m.setObjective(quicksum((edges[edge][0]*y[edge]) for edge in edges))
m.ModelSense = 1  
m.update()

def replace_value_with_definition(key_to_find, definition):
    for key in vertices.keys():
        if key == key_to_find:
            vertices[key] = definition

def prueba1(a,b):
    replace_value_with_definition(a, 1)
    replace_value_with_definition(b,-1)
    m.optimize()

prueba1(1,8)