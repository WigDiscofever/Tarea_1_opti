from gurobipy import *

import os
os.system("python testossystem.py 1")

nodes = N
arcs = A
costs = largo
inflow = vertices

m=Model('netflow')

flow = {}
for i,j in arcs:
    flow[i,j] = m.addVar(ub=1, obj=costs[i,j],name='flow_%s_%s' % (i, j))
    
for j in nodes:
    m.addConstr(quicksum(flow[i,j] for i,j in arcs) == quicksum(flow[j,k] for j,k in arcs),'node_%s' % (j))
    
m.optimize()