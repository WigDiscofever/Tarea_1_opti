# -*- coding: utf-8 -*-

from gurobipy import *

import networkx as NX
def compute_shortest_path_fast(a,b,N,A,largo):
    G = NX.DiGraph()
    G.add_nodes_from(N)
    for (i,j) in A:
        G.add_edge(i,j, weight = largo[(i,j)])
    print("Conectados los nodos "+str(a)+"\t"+str(b))
    yay=NX.shortest_path_length(G,a,b, weight="weight")
    print(yay)
    return yay


#### Run Data Base ####

import os
os.system("python testossystem.py 1")


def spmanual(a,b):
    print("Conecting nodes "+str(a)+" and "+str(b))
    model = Model("P1")

    #### Decision Variables ####

    x={}

    for (i,j) in A:
        x[(i,j)]=model.addVar(vtype=GRB.BINARY, name="x_%s,%s" %(i,j), obj=largo[(i,j)], ub=1)
        model.update()
        #print(x[i,j])
        
    
    #### Constraints ####

    ### Outflux ####
    model.addConstr(quicksum(x[(a,j)] for j in N if (a,j) in A)==1)
    model.update()
    
    ### Influx ####

    model.addConstr(quicksum(x[(i,b)] for i in N if (i,b) in A)==1)     
    model.update()
           
    ### Flow Conservation ####
#    model.addConstr(quicksum(x[i,j] for (i,j) in A if i != a) - quicksum(x[j,i] for (j,i) in A if i != b) == 0 )
    for i in N:
#        if i != a and i != b:
            model.addConstr(quicksum(x[(i,j)] for j in N if (i,j) in A and i != a) - quicksum(x[(k,i)] for k in N if (k,i) in A and i != b)==0)
            model.update()
#    for (i,j) in A:
#        if i == a:
#            model.addConstr(quicksum(x[i,j] for j in tail if i!=j )==1)
#        if i == b:
#            model.addConstr(quicksum(x[j,i] for j in tail if i!=j)==-1)
#        else:        
#            model.addConstr(quicksum(x[i,j] for (i,j) in A) == quicksum(x[j,i] for (j,i) in A))
            

    
    model.ModelSense = 1   
    model.update()
    
    model.setObjective(quicksum(x[(i,j)]*largo[(i,j)] for (i,j) in A), GRB.MINIMIZE)
    model.update()
    model.optimize()
    if model.Status == GRB.OPTIMAL:
        print("Opt.Value", model.ObjVal)

aa=1
bb=407

spmanual(aa,bb)
compute_shortest_path_fast(aa,bb,N,A,largo)