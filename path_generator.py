from queue import PriorityQueue
from graph import Graph,Node, NodeClass
from path import Path
from abc import ABC, abstractmethod


class path_generator(ABC):
    
    @abstractmethod
    def __init__(self, graph: Graph, goalnode: Node, startnode: Node):
        return Path


class shortest_path_generator(path_generator):
    
    def __init__(self, graph: Graph, goalnode: Node, startnode: Node):
        
        return self.dijkstra(graph,goalnode,startnode)

    def dijkstra (graph: Graph, goalnode: Node, startnode: Node):
        #loosely inspired by https://stackabuse.com/dijkstras-algorithm-in-python/
        shortest_path = Path()
        
        
        frontier = PriorityQueue()
        frontier.put((0,startnode))
        visited = []
        #work in progress
        while not frontier.empty():
            (dist,current_node) = frontier.get()
            visited.append(current_node)

            for edge in graph.get_out_edges(current_node.id,NodeClass.OK):
                neighbor_node = graph.get_node(edge.to_id)
                cost = dist + edge.cost
                if neighbor_node not in visited:
                    frontier.put()

        return shortest_path
    

