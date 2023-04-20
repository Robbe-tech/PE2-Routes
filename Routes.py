from numpy import Inf
import numpy as np
import pgeocode
import pandas as pd
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
    for keys in graph.keys():
        dist[keys] = [Inf, []]

    # set the distance for the root to be 0 with no shortest routes
    dist[root] = [0, [[]]]

    # initialize seperate dictionary of temporary distances wich will be removed after they are visited
    tempdist = {}
    for keys in graph.keys():
        tempdist[keys] = Inf
    
    #set starting node as current node
    curnode = root

    #remove root from nonvisited list
    tempdist.pop(root)

    #while not all nodes were visited
    while(len(tempdist) > 0):

        #calculate every for every node connected to current node if curnode + their len is shorter then the current nodes minimum length
        for k,v in graph[curnode].items():

            #if the new len is shorter set the new len and add the new shortest route
            if dist[k][0] > (dist[curnode][0] + v):
                dist[k][0] = dist[curnode][0] + v
                dist[k][1] = []

                for lists in dist[curnode][1]:
                    templist = list(lists)
                    templist.append(k)
                    dist[k][1].append(templist)
                
                #update the tempdist with up to date info
                tempdist[k] = dist[k][0]
            
            #if they are equal append the new route of travel
            elif dist[k][0] == (dist[curnode][0] + v):
                for lists in dist[curnode][1]:
                    templist = list(lists)
                    templist.append(k)
                    dist[k][1].append(templist)
                
                #update the tempdist with up to date info
                tempdist[k] = dist[k][0]
        
        #get the shortest distance key and set it as the current node
        curmin = Inf
        for k,v in tempdist.items():
            if curmin > v:
                curmin = v
                curnode = k

        #remove curnode from not visited
        tempdist.pop(curnode)
    
    return dist

#function used to remove any nodes with another remaining destination in one of its shortest paths
def irrelevant_node(relevantdists, routes):
    #currentroute = [node, dist, remainingdests, availabledests] of latest node
    currentroute = routes[-1]
    #node = {to : [len, [[route1], [route2]]} for current node
    node = relevantdists[currentroute[0]]
    for dest in currentroute[2]:
        #every shortest path from the current node to an available node
        paths = node[dest][1]
        i = 0
        #if another node is found in the shortest path, immediately stop the loops
        noccured = True
        while (i < len(paths) and noccured):
            j = 0
            while (j < len(paths[i]) and noccured):
                #if on the shortest path another required destination is found remove it from availabledests
                if (paths[i][j] in currentroute[2] and paths[i][j] != dest):
                    noccured = False
                    currentroute[3].remove(dest)
                j += 1
            i += 1
    
    routes[-1] = currentroute
    return (routes)

#root = int, postal code
#distances = dict of naive dijckstras {from : {to : [len, [[shortest route1]]]}}
#destinations = list of postal codes
def multi_node(root, distances, destinations):
    #create list with root included
    tempdests = list(destinations)
    tempdests.append(root)
    #get only relevant dists + how to get there
    #same format as distances
    relevantdists = {}
    for k,v in distances.items():
        if k in tempdests:
            value = {}
            #get all destinations that arent the current node
            for z in v.keys():
                if (z in tempdests and z != k):
                    value[z] = v[z]
            relevantdists[k] = value
    
    #shortest distance and path
    totdistmin = [0, []]
    #non visted nodes
    nvisited = dict(relevantdists)
    #for baseline calcs
    
    #shortestnode = next closest node
    shortestnode = root
    currentnode = root

    #1 is the lowest because the information needed cannot be popped before using it
    while(len(nvisited) > 1):
        #shortest = next closest distance
        shortest = [Inf, []]
        #find next closest node
        for k,v in nvisited[currentnode].items():
            #v is formatted [min, [[route], [route2]]]
            #nvisited.keys() = all remaining dests + current node
            #current node is never in nvisisted[currentnode], because of z != k in creation of relevantdists
            if (k in nvisited.keys() and v[0] < shortest[0]):
                shortest = v
                shortestnode = k
        
        #pop current node
        nvisited.pop(currentnode)
        totdistmin[0] += shortest[0]
        #just want 1 shortest route to avoid confusion
        totdistmin[1].extend(shortest[1][0])
        currentnode = shortestnode
    
    #go back to root
    totdistmin[0] += relevantdists[currentnode][root][0]
    totdistmin[1].extend(relevantdists[currentnode][root][1][0])

    #remainingdests = every remaining dest
    remainingdests = list(destinations)
    #availabledests is the list of destinations relevant to the then current node
    availabledests = list(remainingdests)
    routes = [[root, 0, remainingdests, availabledests, []]]

    routes = irrelevant_node(relevantdists, routes)

    #while there still is an available destination
    while(len(routes) != 0):
        #go to next available dest if it exists
        latestroute = routes[-1]
        if (len(latestroute[3]) == 0):
            #if there are no more available dests pop the latest route
            routes.pop(-1)
        else:
            #check if going into the first available node + returning to root is shorter then the current min dist
            #relevantdists[from][to][0] = distance between nodes
            lfrom = latestroute[0]
            lto = latestroute[3][0]
            #remove the first element from available because it will be longer then the shortest route or it will be appended to routes making it the latestroute
            latestroute[3].pop(0)
            if((latestroute[1] + relevantdists[lfrom][lto][0] + relevantdists[lto][root][0]) < totdistmin[0]):
                remainingdests = list(latestroute[2])
                remainingdests.remove(lto)
                #check if every destination has been reached
                if (len(remainingdests) == 0):
                    #if it every destination has been reached it is the new shortest route as shown by the if before
                    totdistmin[0] = latestroute[1] + relevantdists[lfrom][lto][0] + relevantdists[lto][root][0]
                    totdistmin[1] = list(latestroute[4])
                    #relevantdists[from][to][1][x] is the list of nodes that are passed when going to the from one location to another 0 is taken since it is irrelevant which is taken and every route has at least one 
                    totdistmin[1].extend(relevantdists[lfrom][lto][1][0])
                    totdistmin[1].extend(relevantdists[lto][root][1][0])
                else:
                    #if not the last destination add it as the new latest route
                    availabledests = list(remainingdests)
                    currentdist = latestroute[1] + relevantdists[lfrom][lto][0]
                    currentstops = list(latestroute[4])
                    currentstops.extend(relevantdists[lfrom][lto][1][0])
                    currentroute = [lto, currentdist, remainingdests, availabledests, currentstops]
                    routes.append(currentroute)
                    routes = irrelevant_node(relevantdists, routes)
    
    return (totdistmin)
            
fulldijkstra = {}
for k in graph.keys():
    fulldijkstra[k] = naive_dijkstras(graph, k)
print(fulldijkstra)
print(multi_node(3, fulldijkstra, [2, 4, 1]))