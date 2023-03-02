from numpy import Inf

class Node:

    def __init__(self, value, neighbors=None):
        self.value=value
        if neighbors is None:
            self.neighbors = []
        else:
            self.neighbors = neighbors
    
    def has_neighbors(self):
        if len(self.neighbors) == 0:
            return False
        return True

    def number_of_neighbors(self):
        return len(self.neighbors)
    
    def add_neighboor(self, neighboor):
        self.neighbors.append(neighboor)

class Graph:

    def __init__(self, nodes=None):
        if nodes is None:
            self.nodes = []
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
    n = len(graph)
    # initialize distance list as all infinities
    dist = {}
    for keys in graph.keys():
        dist[keys] = [Inf, []]

    # set the distance for the root to be 0
    dist[root] = [0, [[]]]

    # initialize seperate dictionary of temporary distances wich will be removed when 
    tempdist = dict(dist)
    
    #set starting node
    curnode = root

    #remove root from nonvisited list
    tempdist.pop(root)

    #while not all nodes were visited
    while(len(tempdist) > 0):
        #calculate every for every node connected to current node if curnode + their len is shorter then the current nodes minimum length
        for x,y in graph[curnode].items():
            #if the new len is shorter set the new len and add the new shortest route
            if dist[x][0] > (dist[curnode][0] + y):
                dist[x][0] = dist[curnode][0] + y
                dist[x][1] = []
                for lists in dist[curnode][1]:
                    templist = list(lists)
                    templist.append(x)
                    dist[x][1].append(templist)
                tempdist[x] = dist[x]
            #if they are equal append the new route of travel
            elif dist[x][0] == (dist[curnode][0] + y):
                for lists in dist[curnode][1]:
                    templist = list(lists)
                    templist.append(x)
                    dist[x][1].append(templist)
                tempdist[x] = dist[x]
        
        #get the shortest distance key and set it as the current node
        curmin = Inf
        for x,y in tempdist.items():
            if curmin > y[0]:
                curmin = y[0]
                curnode = x

        #remove curnode from not visited
        tempdist.pop(curnode)
    
    return dist
    
print(naive_dijkstras(graph,0))
