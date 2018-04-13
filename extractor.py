# -*- coding: utf-8 -*-

import csv
import numpy as np
import math

#### For Secure Points #####

idsecure = []
V = []
D = []
C = []

for d in csv.DictReader(open('secure_points.csv'), delimiter=','):
    idsecure.append(int(d['id']))
    V.append(int(d['V']))
    D.append(int(d['D']))
    C.append(int(d['C']))

#print("id_secure= ", idsecure)
#print("V = ", V)
#print("D =", D)
#print("C =", C)

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
    

#### Create node list ####

N=[]
for i in range(len(head)):
    if head[i] not in N:
        N.append(head[i])
#print(N)


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





























