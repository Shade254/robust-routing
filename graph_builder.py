import numpy as np
import random
from enum import Enum

class NeigbourDirection(Enum):
    Up = 1
    Down = 2
    Left = 3
    Right = 4

def graph_builder(x_size, y_size, num_of_fatal_nodes, num_of_clusters, output_path, ensure_connected=True):
    graph = []
    fatal_nodes_placed = []
    output_file = open(output_path, "w")
    
    for i in range(x_size):
        graph.append([])
        for j in range(y_size):
            graph[i].append('.')
    
    for i in range(num_of_clusters):
        x = np.random.randint(0, x_size)
        y = np.random.randint(0, y_size)
        graph[x][y] = 'x'
        fatal_nodes_placed.append((x, y))
    
    while(len(fatal_nodes_placed) < num_of_fatal_nodes):
        random.shuffle(fatal_nodes_placed)
        cluster_node_x,cluster_node_y = fatal_nodes_placed[-1]
        x,y = get_neigbour(graph,cluster_node_x,cluster_node_y,random.choice(list(NeigbourDirection)))
        if graph[x][y] == 'x':
            continue
        if(all_neigbours_are_fatal(graph,x,y)):
            continue
        graph[x][y] = 'x'
        fatal_nodes_placed.append((x, y)) 
        if(ensure_connected):
            if(not graph_is_connected(graph,x_size,y_size,len(fatal_nodes_placed))):
                graph[x][y] = '.'
                fatal_nodes_placed.pop()
    
    #Fill out all the holes in fatal clusters
    if(not ensure_connected):
        for x in range(x_size):
            for y in range(y_size):
                if all_neigbours_are_fatal(graph,x,y) and graph[x][y] != 'x':
                    graph[x][y] = 'x'
                    fatal_nodes_placed.append((x, y))
 
    if graph_is_connected(graph,x_size,y_size,len(fatal_nodes_placed)):
        for i in range(x_size):
            for j in range(y_size):
                output_file.write(graph[i][j])
            output_file.write('\n')
        output_file.close()
        return graph
    else :
        return None


def all_neigbours_are_fatal(graph, x, y):
    fatal_neigbours = 0
    if(not coordinate_is_inside_graph(graph, x-1, y) or (graph[x-1][y] == 'x')):
            fatal_neigbours += 1
    if(not coordinate_is_inside_graph(graph, x+1, y) or (graph[x+1][y] == 'x')):
            fatal_neigbours += 1
    if(not coordinate_is_inside_graph(graph, x, y-1) or (graph[x][y-1] == 'x')):
            fatal_neigbours += 1
    if(not coordinate_is_inside_graph(graph, x, y+1) or (graph[x][y+1] == 'x')):
            fatal_neigbours += 1
    
    if(fatal_neigbours == 4):
        return True
    else:
        return False

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


#A function that returns true if all non fatal nodes in a graph is interreachable from any other non fatal node
def graph_is_connected(graph,x_size,y_size,fatal_nodes):
    x,y = get_random_node(graph,x_size,y_size)
    visited_nodes = [(x,y)]
    frontier = [(x,y)]
    while(len(frontier) > 0):
        x,y = frontier.pop(0)
        neighbours = [(-1,0),(1,0),(0,-1),(0,1)]
        for neigbour in neighbours:
            i = x+neigbour[0]
            j = y+neigbour[1]
            if(not coordinate_is_inside_graph(graph,i,j)):
                continue
            if(graph[i][j] == 'x'):
                continue
            if(i,j) in visited_nodes:
                continue
            visited_nodes.append((i,j))
            frontier.append((i,j))
    if len(visited_nodes) == (x_size*y_size)-fatal_nodes:
        return True
    else: 
        return False


   
def get_random_node(graph,x_size,y_size):
    x,y = None,None
    while x == None and y == None:
        x = np.random.randint(0, x_size)
        y = np.random.randint(0, y_size)
        if(graph[x][y] == 'x'):
            x,y = None,None
    return x,y

def count_fatal_nodes(graph,x_size,y_size):
    count = 0
    for i in range(x_size):
        for j in range(y_size):
            if graph[i][j] == 'x':
                count += 1
    return count

def graph_x_size(graph):
    return len(graph)

def graph_y_size(graph):
    return len(graph[0])

#function that converts txt file to graph
def txt_to_graph(txt_path):
    graph = []
    file = open(txt_path, "r")
    for line in file:
        graph.append(list(line.strip()))
    file.close()
    return graph



"""
Graphs are only created if, the graph is connected. If not, the function will return None.
Below is an example of genereating a number of graphs.

for i in range(95, 101):
        num_of_fatal_nodes = round(7.07*i + 292.93)
        
        num_of_clusters = random.randint(1, 5)
        counter = 0
        while(True):
            print(f'building graph: {i} try {counter}')
            graph = graph_builder(50,50,num_of_fatal_nodes,num_of_clusters,f'test_cases_50/test_case_{i}.txt',ensure_connected=False)
            if(graph != None):
                break
            else:
                counter += 1
"""
