from numpy import Inf
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
            neighbors[k] = v

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

#root = int
#distances = dict of naive dijckstras
#destinations = list
def multi_node(root, distances, destinations):
    tempdests = list(destinations)
    tempdests.append(root)
    # get only relevant dists + how to get there
    relevantdists = {}
    for k,v in distances:
        if k in tempdests:
            value = {k: v[k] for v in destinations}
            relevantdists[k] = value
    
    totdistmin = [0, []]
    nvisitedd = dict(relevantdists)
    shortest = [Inf, []]
    #baseline min
    currentnode = root
    nvisitedd.pop(root)
    while(len(nvisitedd) > 0):
        for k,v in nvisitedd[currentnode]:
            if (v[0] < shortest.values()[0] and k != currentnode):
                shortest = v
        
        #shortest was in format [dist, [[route], [route2]]]
        totdistmin[0] += shortest[0]
        #just want 1 shortest route to avoid confusion
        shortest[1].extend(shortest[1][0])
        nvisitedd.pop(shortest[0])
        currentnode = shortest[0]
    
print(naive_dijkstras(graph,0))
bel = pgeocode.Nominatim('BE')
df = pd.DataFrame(bel._data)
d2 = df.loc[:,"latitude", "longitude"]
display(d2)