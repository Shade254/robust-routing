import numpy as np

#A function that builds a graph from the following inputs: x size, y size, number of fatal nodes, location of output
#The graph should have a size of x by y
#The graph is made of the characters '.' and 'X' with 'X' representing a fatal node
#the graph should be outputtet to a txt file, location of txt file is given as input
#The graph should have a number of fatal nodes equal to the number of fatal nodes inputted
#fatal nodes are randomly placed on the graph
def graph_builder(x_size, y_size, num_of_fatal_nodes, output_path):
    graph = []
    output_file = open(output_path, "w")
    for i in range(x_size):
        graph.append([])
        for j in range(y_size):
            graph[i].append('.')
    for i in range(num_of_fatal_nodes):
        x = np.random.randint(0, x_size)
        y = np.random.randint(0, y_size)
        graph[x][y] = 'X'
    for i in range(x_size):
        for j in range(y_size):
            output_file.write(graph[i][j])
        output_file.write('\n')
    output_file.close()
    return graph

graph_builder(10,10,5,'test_cases/test_case_1.txt')