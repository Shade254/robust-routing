import enum
import numpy as np
import random
from enum import Enum

class NeigbourDirection(Enum):
    Up = 1
    Down = 2
    Left = 3
    Right = 4

#A function that builds a graph from the following inputs: x size, y size, number of fatal nodes, location of output
#The graph should have a size of x by y
#The graph is made of the characters '.' and 'X' with 'X' representing a fatal node
#the graph should be outputtet to a txt file, location of txt file is given as input
#The graph should have a number of fatal nodes equal to the number of fatal nodes inputted
#fatal nodes are randomly placed on the graph
def graph_builder(x_size, y_size, num_of_fatal_nodes, num_of_clusters, output_path):
    graph = []
    fatal_nodes_placed = []
    num_of_fatal_nodes_placed = 0
    output_file = open(output_path, "w")
    
    for i in range(x_size):
        graph.append([])
        for j in range(y_size):
            graph[i].append('.')
    
    for i in range(num_of_clusters):
        x = np.random.randint(0, x_size)
        y = np.random.randint(0, y_size)
        graph[x][y] = 'X'
        fatal_nodes_placed.append((x, y))
    
    counter = 0
    while(num_of_fatal_nodes_placed < num_of_fatal_nodes):
        counter += 1
        random.shuffle(fatal_nodes_placed)
        cluster_node_x,cluster_node_y = fatal_nodes_placed[-1]
        x,y = get_neigbour(graph,cluster_node_x,cluster_node_y,random.choice(list(NeigbourDirection)))
        if graph[x][y] == 'X':
            continue
        graph[x][y] = 'X'
        fatal_nodes_placed.append((x, y))
        num_of_fatal_nodes_placed += 1    
        print(counter)
    
    for i in range(x_size):
        for j in range(y_size):
            output_file.write(graph[i][j])
        output_file.write('\n')
    output_file.close()
    return graph


def get_neigbour(graph, x, y, direction):
    if(direction == NeigbourDirection.Up):
        if(coordinate_is_inside_graph(graph, x-1, y)):
            return ((x-1,y))
        else:
            return get_neigbour(graph,x,y,NeigbourDirection.Down)
    if(direction == NeigbourDirection.Down):
        if(coordinate_is_inside_graph(graph, x+1, y)):
            return ((x+1,y))
        else:
            return get_neigbour(graph,x,y,NeigbourDirection.Up)
    if(direction == NeigbourDirection.Left):
        if(coordinate_is_inside_graph(graph, x, y-1)):
            return ((x,y-1))
        else:
            return get_neigbour(graph,x,y,NeigbourDirection.Right)
    if(direction == NeigbourDirection.Right):
        if(coordinate_is_inside_graph(graph, x, y+1)):
            return ((x,y+1))
        else:
            return get_neigbour(graph,x,y,NeigbourDirection.Left)


def coordinate_is_inside_graph(graph, x, y):
    if(x < 0 or x >= len(graph)):
        return False
    if(y < 0 or y >= len(graph[0])):
        return False
    return True

def neighbouring_nodes_is_fatal(graph, x, y):
    if(graph[x][y] == 'X'):
        return True
    if(graph[x-1][y] == 'X'):
        return True
    if(graph[x+1][y] == 'X'):
        return True
    if(graph[x][y-1] == 'X'):
        return True
    if(graph[x][y+1] == 'X'):
        return True
    return False




for i in range(5):
    print(f'creating graph {i}')
    graph_builder(40,60,250,5,f'test_cases/test_case_{i}.txt')