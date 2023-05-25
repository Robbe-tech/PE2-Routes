import math
import pandas as pd
import time
import json

with open("graph.txt", "r") as fp:
    graph = json.load(fp)

def naive_dijkstras(graph, root):
    # initialize distance dictionary as all infinities, with as off yet a no lists of shortest routes
    dist = {}
    route = {}
    for keys in graph.keys():
        dist[keys] = math.inf
        route[keys] = [[]]

    # set the distance for the root to be 0
    dist[root] = 0

    dist = pd.Series(dist)
    route = pd.Series(route)

    # initialize seperate se of temporary distances wich will be removed after they are visited
    tempdist = pd.Series(dist)

    #set starting node as current node
    curnode = root

    #remove root from nonvisited list
    tempdist.pop(root)

    #while not all nodes were visited
    while(tempdist.size > 0):

        #calculate every for every node connected to current node if curnode + their len is shorter then the current nodes minimum length
        for k,v in graph[curnode].items():

            #if the new len is shorter set the new len and add the new shortest route
            if dist[k] > (dist[curnode] + v):
                dist[k] = dist[curnode] + v
                route[k] = []

                for lists in route[curnode]:
                    templist = list(lists)
                    templist.append(k)
                    route[k].append(templist)
                
                #update the tempdist with up to date info
                tempdist[k] = dist[k]
            
            #if they are equal append the new route of travel
            elif dist[k] == (dist[curnode] + v):
                for lists in route[curnode]:
                    templist = list(lists)
                    templist.append(k)
                    route[k].append(templist)
                
                #update the tempdist with up to date info
                tempdist[k] = dist[k]
        
        #get the shortest distance key and set it as the current node
        curnode = tempdist.idxmin()
        #remove curnode from not visited
        tempdist.pop(curnode)
    
    dist[root] = None
    return dist, route

def fill(graph):
    for k in graph.keys():
        dist, route = naive_dijkstras(graph, k)
        fulldists[k] = dist
        fullroutes[k] = route
    
    return(fulldists, fullroutes)

start_time = time.time()

fulldists = pd.DataFrame(columns = graph.keys(), index = graph.keys())
fullroutes = pd.DataFrame(columns = graph.keys(), index = graph.keys())

fulldists, fullroutes = fill(graph)

fulldists.to_csv("fulldists.csv")
fullroutes.to_csv("fullroutes.csv")

totaltime = time.time() - start_time

print(totaltime)