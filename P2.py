# -*- coding: utf-8 -*-
from gurobipy import *

############################################################
#### Please run extractor.py before running this script ####
############################################################

print("Optimizing best secure points location")

#### Model iniciation ####

m=Model("P2")

#### Decision Variables ####
B=900000000
M=1000000000000
x={}    
y={}
P={}
T={}
for j in idsecure:
    #### Integer, Quantity of people in node j ####
    T[j]=m.addVar(vtype="I", name="T_%s" %(j), lb=0)
    #### Binary, if node j is safe point ####
    x[j]=m.addVar(vtype=GRB.BINARY, name="x_%s" %(j))
    for i in N:   
        #### Binary, if people travels from i to j ####
        y[i,j]=m.addVar(vtype=GRB.BINARY, name="y_%s_%s" %(i,j))
        #### Interger, Flow of people from i to j ####
        P[i,j]=m.addVar(vtype="I", name="P_%s_%s" %(i,j), lb=0)
        
#for i in N:
#    for j in idsecure:
#        #### Binary, if people travels from i to j ####
#        y[i,j]=m.addVar(vtype=GRB.BINARY, name="y_%s_%s" %(i,j))
#        #### Interger, Flow of people from i to j ####
#        P[i,j]=m.addVar(vtype="I", name="P_%s_%s" %(i,j), lb=0)

m.update()        
        
#### Objective Function ####

m.setObjective(quicksum(P[i,j]*ultimatematrix[i,j] for (i,j) in nodetosecure))

#### Constraints ####

#### Budget ####
m.addConstr(quicksum(C[j]*x[j]+V[j]*T[j] for j in idsecure) + quicksum(D[j]*y[i,j] for (i,j) in nodetosecure) <= B)

#### Demand point distribution ####
for i in N:
    m.addConstr(quicksum(y[i,j] for j in idsecure) <= 2)
    m.addConstr(quicksum(y[i,j] for j in idsecure) >= 1)
    
#### Consistency ####
for j in idsecure:
    m.addConstr((quicksum(y[i,j] for i in N))/M <= x[j])

for (i,j) in nodetosecure:
    m.addConstr(y[i,j] >= ((P[i,j])/M))  
    

#### Total Demand ####
for i in N:
    m.addConstr(quicksum(P[i,j] for j in idsecure) == p[i])

#### Total Influx ####    
for j in idsecure:
    m.addConstr(quicksum(P[i,j] for i in N) == T[j])
 

m.update()

m.optimize()
    
    
if m.Status == GRB.OPTIMAL:
    print("Opt.Value", m.ObjVal)

import networkx as nx
#### Draw nodes and edges ####
G = nx.Graph()
G.add_nodes_from(N)
#G.add_nodes_from(idsecure)
#for (i,j) in A:
#    G.add_edge(i,j)
securenodes=[]
for (i,j) in nodetosecure:
    if y[i,j].X==1:
        G.add_edge(i,j)
        securenodes.append(j)
#        print(y[i,j])   
G.add_nodes_from(securenodes)
position={}
for i in range(len(nodeswithposition)+1):
    if i == 0:
        pass
    else:
        a=nodeswithposition[i]
        position[i]=a
        print(position[i])
nx.draw(G, position, node_color="red",node_size=20, nodelist=N)
nx.draw(G, position, node_color="blue",node_size=70, nodelist=securenodes)
    
    
    
    
    
    
    
    
    
    
    