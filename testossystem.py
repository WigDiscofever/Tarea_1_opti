# -*- coding: utf-8 -*-

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

import os
os.system("python extractor.py 1")

for a in N:
    for b in N:
        if a != b:
            x=compute_shortest_path_fast(a,b,N,A,largo)
            dm[a-1][b-1]=x
