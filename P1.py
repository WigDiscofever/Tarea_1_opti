# -*- coding: utf-8 -*-

#### To compare solutions from both algorithms, please go to the end of the document ####
#### Please run extractor.py before running this script ####


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


#### Function: creates model for every pair of node given ####

def spmanual(a,b):
    print("Conecting nodes "+str(a)+" and "+str(b))
    model = Model("P1")

    #### Decision Variables ####

    #### Binary for every arc ####
    x={}
    for (i,j) in A:
        x[(i,j)]=model.addVar(vtype=GRB.BINARY, name="x_%s,%s" %(i,j), obj=largoreal[(i,j)], ub=1)
        model.update()
    
    #### Constraints ####

    ### Outflux ####
    model.addConstr(quicksum(x[(a,j)] for j in N if (a,j) in A)==1)
    model.update()
    
    ### Influx ####
    model.addConstr(quicksum(x[(i,b)] for i in N if (i,b) in A)==1)     
    model.update()
           
    ### Flow Conservation ####
    for i in N:
        model.addConstr(quicksum(x[(i,j)] for j in N if (i,j) in A and i != a) - quicksum(x[(k,i)] for k in N if (k,i) in A and i != b)==0)
        model.update()
          
    #### Set model objective to minimize ####
    model.ModelSense = 1   
    model.update()
    
    #### Optimize and return optimal value ####
    model.optimize()
    if model.Status == GRB.OPTIMAL:
        print("Opt.Value", model.ObjVal)
        return model.Objval

#### Function to compare both SP solutions ####
    
comparelist = []
timelist = []

def compare(start, finish):
    nxmethod = []
    pplmethod = []
    
    t11=time.time()
    a=spmanual(start,finish)
    pplmethod.append(a)
    t12=time.time()
    t1=int(t12-t11)
    t21=time.time()
    b=compute_shortest_path_fast(start,finish,N,A,largoreal)
    t22=time.time()
    t2=int(t22-t21)
    nxmethod.append(b)
    comparelist.append(tuple((a,b)))
    timelist.append(tuple((t1,t2)))
    return
    
#### Compare solutions ####

import secrets
import time

startpoints = []
finishpoints = []
finallist = []

def solvesolutions(q=1):
    for i in range(1,q+1,1):
        startpoints.append(secrets.choice(N))
        finishpoints.append(secrets.choice(N))
    for i in range(1,q+1,1):
        compare(startpoints[i-1], finishpoints[i-1])
        finallist.append(tuple((comparelist[i-1], timelist[i-1])))
        print(finallist)

#### Start Compairing ####
        
#### Define q=Quantity # Default q=1 ####
        
q=2
solvesolutions(q)       
        
        
        
        
        