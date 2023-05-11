import numpy as np
import math
import pgeocode
import pandas as pd
import time
from IPython.display import display

class Node:

    def __init__(self, value, neighbors=None):
        self.value=value
        if neighbors is None:
            self.neighbors = {}
        else:
            self.neighbors = neighbors
    
    def has_neighbors(self):
        if len(self.neighbors) == 0:
            return False
        return True

    def number_of_neighbors(self):
        return len(self.neighbors)
    
    #neighbor is dict
    def add_neighbor(self, neighbor):
        for k, v in neighbor.items():
            neighbor[k] = v

class Graph:

    def __init__(self, nodes=None):
        if nodes is None:
            self.nodes = {}
        else:
            self.nodes = nodes

    def add_node(self, value, neighboors=None):
        self.nodes.append(Node(value, neighboors))

    def find_node(self, value):
        for node in self.nodes:
            if node.value == value:
                return node
            return None

    def add_edge(self, value1, value2, weight = 1):
        node1 = self.find_node(value1)
        node2 = self.find_node(value2)

        if(node1 is not None) and (node2 is not None):
            node1.add_neighboor((node1, weight))
            node2.add_neighboor((node2, weight))
        else:
            print("Error: One or more nodes were not found!")

    def number_of_nodes(self):
        return f"The graph has {len(self.nodes)} nodes"

    def are_connected(self, node_one, node_two):
        node_one = self.find_node(node_one)
        node_two = self.find_node(node_two)

        for neighboor in node_one.neighbors:
            if neighboor[0].value == node_two.value:
                return True
        return False

graph = {
    0: {1: 1},
    1: {0: 1, 2: 2, 3: 3},
    2: {1: 2, 3: 1, 4: 5},
    3: {1: 3, 2: 1, 4: 1},
    4: {2: 5, 3: 1}
}

def naive_dijkstras(graph, root):
    # initialize distance dictionary as all infinities, with as off yet a no lists of shortest routes
    dist = {}
    route = {}
    for keys in graph.keys():
        dist[keys] = math.inf
        route[keys] = np.array([[]])

    # set the distance for the root to be 0
    dist[root] = 0

    dist = pd.Series(dist)
    route = pd.Series(route)

    # initialize seperate dictionary of temporary distances wich will be removed after they are visited
    tempdist = {}
    for keys in graph.keys():
        tempdist[keys] = math.inf
    
    tempdist = pd.Series(tempdist)

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
        #change the lists to np arrays
        length = max(map(len, route[curnode]))
        route[curnode]=np.array([xi+[None]*(length-len(xi)) for xi in route[curnode]])
        #remove curnode from not visited
        tempdist.pop(curnode)
    
    dist[root] = None
    return dist, route

#function used to remove any nodes with another remaining destination in one of its shortest paths
def irrelevant_node(relevantroutes, routes):
    #currentroute = [node, dist, remainingdests, availabledests] of latest node
    currentroute = routes[-1]
    #node = {to : [[route1], [route2]]} for current node
    node = relevantroutes[currentroute[0]]
    #change to set, because quicker for large lists
    s = set(currentroute[2])
    for dest in s:
        broken = False
        #every shortest path from the current node to an available node
        for i in node[dest]:
            for x in i:
                if (x in s and x != dest):
                    currentroute[3].remove(dest)
                    broken = True
                    break
            if (broken):
                break
    
    routes[-1] = currentroute
    return (routes)

#root = int, postal code
#distances = dataframe of shortest dists distances[from][to] = dist
#droutes = dataframe of shortests routes
#destinations = list of postal codes
def multi_node(root, distances, droutes, destinations):
    #create list with root included
    tempdests = list(destinations)
    tempdests.append(root)
    tempdests.sort()
    #get only relevant dists + how to get there
    #same format as distances and droutes
    df = distances.filter(tempdests)
    relevantdists = df.filter(tempdests, axis=0)
    df2 = droutes.filter(tempdests)
    relevantroutes = df2.filter(tempdests, axis=0)
    
    #shortest distance and path
    totdistmin = 0
    notablepath = []
    #non visted nodes
    nvisited = list(destinations)

    #for baseline calcs
    #shortestnode = next closest node
    shortestnode = root
    currentnode = root

    while(len(nvisited) > 0):
        relevantsearch = relevantdists[currentnode].filter(nvisited)
        currentnode = relevantsearch.idxmin()
        totdistmin += relevantsearch.min()
        notablepath.append(currentnode)
        nvisited.remove(currentnode)
    
    #go back to root
    totdistmin += relevantdists[currentnode][root]
    notablepath.append(root)

    #remainingdests = every remaining dest
    remainingdests = list(destinations)
    #availabledests is the list of destinations relevant to the then current node
    availabledests = list(remainingdests)
    routes = [[root, 0, remainingdests, availabledests]]

    routes = irrelevant_node(relevantroutes, routes)

    #while there still is an available destination
    while(len(routes) != 0):
        #go to next available dest if it exists
        latestroute = routes[-1]
        if (len(latestroute[3]) == 0):
            #if there are no more available dests pop the latest route
            routes.pop(-1)
        else:
            #check if going into the first available node + returning to root is shorter then the current min dist
            #relevantdists[from][to] = distance between nodes
            lfrom = latestroute[0]
            lto = latestroute[3][0]
            #remove the first element from available because it will be longer then the shortest route or it will be appended to routes making it the latestroute
            latestroute[3].pop(0)
            if((latestroute[1] + relevantdists[lfrom][lto] + relevantdists[lto][root]) < totdistmin):
                remainingdests = list(latestroute[2])
                remainingdests.remove(lto)
                #check if every destination has been reached
                if (len(remainingdests) == 0):
                    #if it every destination has been reached it is the new shortest route as shown by the if before
                    totdistmin = latestroute[1] + relevantdists[lfrom][lto] + relevantdists[lto][root]
                    #find notable path
                    notablepath = []
                    for i in routes:
                        notablepath.append(i[0])
                    notablepath.append(lto)
                    notablepath.append(root)
                else:
                    #if not the last destination add it as the new latest route
                    availabledests = list(remainingdests)
                    currentdist = latestroute[1] + relevantdists[lfrom][lto]
                    currentroute = [lto, currentdist, remainingdests, availabledests]
                    routes.append(currentroute)
                    routes = irrelevant_node(relevantroutes, routes)
    
    absolutepath = [root]
    for i in notablepath:
        #finds the path + removes none values
        currentpath = droutes[absolutepath[-1]][i][0][droutes[absolutepath[-1]][i][0] != None]
        absolutepath.extend(currentpath)
    
    return (totdistmin, notablepath, absolutepath)

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

node_time = time.time()

totdistmin, notablepath, absolutepath = multi_node(0, fulldists, fullroutes, [3, 2, 1])

totaltime = time.time() - start_time
multi_time = time.time() - node_time

print(totdistmin)
print(notablepath)
print(absolutepath)
print(totaltime)
print(multi_time)
bel = pgeocode.Nominatim(country="BE")
data = pd.DataFrame(bel._data)

data.to_csv("data.csv", mode="w")