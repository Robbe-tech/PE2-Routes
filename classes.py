import pandas as pd
import pgeocode
from pathlib import Path

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
    
def read_from_file(self):
    thing = pd.read_table(self)
    print(thing)
        
def write_to_file(frame, file):
    filepath = Path('./' + file)
    postCode = frame.postal_code 
    Steden = frame.place_name
    Steden.to_csv(filepath, index_label=None, mode='a')
    postCode.to_csv(filepath, index_label=None, mode='a')
    

x = pgeocode.Nominatim("BE")
df = pd.DataFrame(x._data)
filename = 'out.csv'
write_to_file(df, filename)
#read_from_file(filename)