from distutils.log import fatal
from queue import PriorityQueue, Queue
from graph import EdgeClass, Graph,Node, NodeClass
from path import Path
from marking import Marking
from abc import ABC, abstractmethod
import datetime


class PathGenerator(ABC):    
    def __init__(self, graph: Graph, goalnodeid, startnodeid, marking: Marking):
        self.current_path = None
        self.build_path(graph, goalnodeid, startnodeid, marking)
        pass
    
    @abstractmethod
    def build_path(self, graph: Graph, goalnode_id, startnode_id, marking: Marking) -> Path:
        pass

    def get_full_path(self):
        return self.current_path
        
    def get_strategy(self, graph: Graph,goal_node,current_node_id):
        if(current_node_id not in self.current_path.get_all_nodes()):
            self.build_path(graph,goal_node,current_node_id)
        return self.get_next_recommended_edge(current_node_id)
    
    def get_next_recommended_edge(self,current_node_id):
        return self.current_path.get_edge_out_from_node(current_node_id)
        
        
    

from heapq import heappush, heappop
class ShortestPathGenerator(PathGenerator):
    def build_path(self, graph: Graph, goalnode_id , startnode_id, marking: Marking) -> Path:
        self.current_path = self.dijkstra(graph,goalnode_id,startnode_id, marking)

    def dijkstra(self, graph: Graph, goal_node_id, startnodeid, marking: Marking) -> Path:
        #loosely inspired by https://stackabuse.com/dijkstras-algorithm-in-python/
        frontier = []

        startedges = graph.get_out_edges(startnodeid,EdgeClass.NORMAL)
        for edge in startedges:
            if graph.get_node(edge.to_id).kind == NodeClass.OK:
                start_path = [edge]
                heappush(frontier, (edge.cost, id(start_path), start_path))

        cost_to_reach_nodes = dict()    
        visited_nodes = []
        while not frontier == []:
            print(len(frontier))
            next_edge_path = heappop(frontier)
            (dist,id_,current_edge_path) = next_edge_path
            current_edge = self.get_last_added_edge(current_edge_path)
            current_node_id = current_edge.to_id
            visited_nodes.append(current_node_id)
            cost_to_reach_nodes[current_node_id] = dist

            if current_node_id == goal_node_id:
                print(visited_nodes)
                return Path(current_edge_path,graph,marking)

            for edge in graph.get_out_edges(current_node_id, EdgeClass.NORMAL):
                neighbor_node = graph.get_node(edge.to_id)
                cost = dist + edge.cost
                if  (neighbor_node.id not in visited_nodes) and (neighbor_node.kind == NodeClass.OK):
                    if (neighbor_node.id in cost_to_reach_nodes):
                        if cost_to_reach_nodes[neighbor_node.id] > cost:
                            cost_to_reach_nodes[neighbor_node.id] = cost
                            path_to_neighbor = current_edge_path+[edge]
                            heappush(frontier, (cost,id(path_to_neighbor),path_to_neighbor))
                    else :
                            cost_to_reach_nodes[neighbor_node.id] = cost
                            path_to_neighbor = current_edge_path+[edge]
                            heappush(frontier, (cost,id(path_to_neighbor),path_to_neighbor))

        #No route was found
        return None
    
    def get_last_added_edge(self, path):
        return path[-1]