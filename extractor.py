# -*- coding: utf-8 -*-

import csv
import numpy as np
import math
##############################################################################################
#### Please run this code first, it creates all data base needed for every other function ####
##############################################################################################

#######################################################################################
####################################  #################################################
###################################    ################################################
##################################      ###############################################
#################################    #   ##############################################
################################     #    #############################################
###############################      #     ############################################
##############################       #      ###########################################
#############################                ##########################################
############################         #        #########################################
###########################                    ########################################
#######################################################################################
#######################################################################################
######### Remember to comment last part of this script, else it with generate #########
############### the same matrix of distances, taking very long ########################
#######################################################################################


#### For A ####

head = []
tail = []

for c in csv.DictReader(open("arcos_def.csv", "r"), delimiter=","):
    head.append(int(c["head"]))
    tail.append(int(c["tail"]))
    
#print("head =", head)
#print("tail", tail)
  
#### Create node list ####

N=[]
for i in range(len(head)):
    if head[i] not in N:
        N.append(head[i])
#print(N)

#### For Secure Points #####

idsecure = []
CV = []
CD = []
CC = []

for d in csv.DictReader(open('secure_points.csv'), delimiter=','):
    idsecure.append(int(d['id']))
    CV.append(int(d['V']))
    CD.append(int(d['D']))
    CC.append(int(d['C']))

#print("id_secure= ", idsecure)
#print("CV = ", CV)
#print("CD =", CD)
#print("CC =", CC)

#### For Demographics ####

iddemo = []
lon = []
lat = []
demanda = []

for b in csv.DictReader(open("demographic.csv", "r"), delimiter=","):
    iddemo.append(int(b['id']))
    lon.append(float(b["lon"]))
    lat.append(float(b['lat']))
    demanda.append(int(b['demanda']))
    
#print("id_demo= ", iddemo)
#print("lon = ", lon)
#print("lat =", lat)
#print("demanda =", demanda)
    
    
#### Dictionaries ####

Vmaker=[]
for i in range(len(idsecure)):
    b=tuple((idsecure[i],CV[i]))
    Vmaker.append(b)
V=dict(Vmaker)

Cmaker=[]
for i in range(len(idsecure)):
    b=tuple((idsecure[i],CC[i]))
    Cmaker.append(b)
C=dict(Cmaker)

Dmaker=[]
for i in range(len(idsecure)):
    b=tuple((idsecure[i],CD[i]))
    Dmaker.append(b)
D=dict(Dmaker)

pmaker=[]
for i in range(len(N)):
    b=tuple((N[i],demanda[i]))
    pmaker.append(b)
p=dict(pmaker)



#### For A ####

head = []
tail = []

for c in csv.DictReader(open("arcos_def.csv", "r"), delimiter=","):
    head.append(int(c["head"]))
    tail.append(int(c["tail"]))
    
#print("head =", head)
#print("tail", tail)
  
#### Create arc tuples #####

A=[]
for i in range(len(head)):
    A.append(tuple((head[i], tail[i])))

#for j in range(len(A)):
#    print(A[j])

#### Calculate Distances #####

distances=[]
for l in range(len(A)):
    distances.append(abs(A[l][0]-A[l][1]))
#    print(distances[l])
    



####### Create Distance Dictionary ########

#### Assuming linear distribution for nodes ####
largotuples=[]
for k in range(len(A)):
    largotuples.append(tuple((A[k], distances[k])))
#    print(largotuples[k])
    
largo=dict(largotuples)
#print(largo)

#### Assuming plane distribution for nodes ####
nodeswithpositionmaker = []
nodeswithposition = []


for k in range(len(N)):
    x=lon[k]
    y=lat[k]
    position=tuple((x,y))
    nodeswithpositionmaker.append(tuple((k+1, position)))
    nodeswithposition = dict(nodeswithpositionmaker)
#print(nodeswithposition)

largorealtuples = []

# Euclidean distance between two points

def distance(points, i, j):
    dx = points[i][0] - points[j][0]
    dy = points[i][1] - points[j][1]
    return math.sqrt(dx*dx + dy*dy)

for (i,j) in A:
    largorealtuples.append(((i,j), distance(nodeswithposition, i, j)))
#print(largorealtuples)
largoreal=dict(largorealtuples)

nodetosecure=[]
for i in N:
    for j in idsecure:
        pair=tuple((i,j))
        nodetosecure.append(pair)

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

#### Create d_j matrix containg SP from each node to each safe node ####  

##################################################################################
#### Please comment if matrix already created, or else it will take more time ####
##################################################################################

ultimatematrixmaker=[]
for i in N:
    for j in idsecure:
        pair=tuple((i,j))
        d=compute_shortest_path_fast(i,j,N,A,largoreal)
        ultimatematrixmaker.append(tuple((pair,d)))
ultimatematrix=dict(ultimatematrixmaker)






















