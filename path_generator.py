from queue import PriorityQueue
from graph import Graph,Node, NodeClass
from path import Path
from abc import ABC, abstractmethod


class PathGenerator(ABC):
    current_path = Path()

    def __init__(self, graph: Graph, goalnode: Node, startnode: Node):
        self.buildPath(graph, goalnode, startnode)
        pass
    
    @abstractmethod
    def buildPath(self, graph: Graph, goalnode_id, startnode_id):
        pass

    def getFullPath(self):
        return self.current_path
        

    def getStrategy(self, graph: Graph,goalnode,currentnode):
        if(currentnode not in self.current_path.get_all_nodes()):
            self.buildPath(graph,goalnode,currentnode)
        
        return self.getnextRecommendedEdge()

    
    def getnextRecommendedEdge(self):
        return self.current_path.nodes_in_path.pop()

    


class ShortestPathGenerator(PathGenerator):
    
    def buildPath(self, graph: Graph, goalnode: Node, startnode: Node):
        self.current_path = self.dijkstra(graph,goalnode,startnode)

    def dijkstra (self, graph: Graph, goalnode: Node, startnode: Node):
        #loosely inspired by https://stackabuse.com/dijkstras-algorithm-in-python/
        shortest_path = Path()
        
        frontier = PriorityQueue()
        frontier.put((0,[startnode]))
        visited = []
        #work in progress
        while not frontier.empty():
            (dist,current_path) = frontier.get()
            current_node = self.getLastAddedNode(current_path)
            visited.append(current_node)

            for edge in graph.get_out_edges(current_node.id,NodeClass.OK):
                neighbor_node = graph.get_node(edge.to_id)
                cost = dist + edge.cost
                if neighbor_node not in visited:
                    frontier.put(cost,current_path.append())
        

        return shortest_path
    
    def getLastAddedNode(path: list):
        return path[-1]

