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
    0: [(1, 1)],
    1: [(0, 1), (2, 2), (3, 3)],
    2: [(1, 2), (3, 1), (4, 5)],
    3: [(1, 3), (2, 1), (4, 1)],
    4: [(2, 5), (3, 1)]
}

def naive_dijkstras(graph, root):
    n = len(graph)
    # initialize distance list as all infinities
    dist = [Inf for _ in range(n)]

    # set the distance for the root to be 0
    dist[root] = 0

    # initialize list of visited nodes
    visited = [False for _ in range(n)]

    # loop through all the nodes
    for _ in range(n):
        # "start" our node as -1 (so we don't have a start/next node yet)
        u = -1
        # loop through all the nodes to check for visitation status
        for i in range(n):
            # if the node 'i' hasn't been visited and
            # we haven't processed it or the distance we have for it is less
            # than the distance we have to the "start" node
            if not visited[i] and (u == -1 or dist[i] < dist[u]):
                u = i
        # all the nodes have been visited or we can't reach this node
        if dist[u] == Inf:
            break

        # set the node as visited
        visited[u] = True

        # compare the distance to each node from the "start" node
        # to the distance we currently have on file for it
        for v, l in graph[u]:
            if dist[u] + l < dist[v]:
                dist[v] = dist[u] + l
        
    return dist
    
print(naive_dijkstras(graph,0))