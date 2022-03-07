from dataclasses import dataclass
from re import I


@dataclass(frozen=False)
class Node:
    id: str
    fatal: bool


@dataclass(frozen=False)
class Edge:
    from_id: str
    to_id: str
    # cost is constant on the grid - every move requires the same effort
    cost: int

@dataclass(frozen=False)
class DisturbanceEdge(Edge):
    pass
    #from_id: str
    #to_id: str
    # cost is constant on the grid - every move requires the same effort
    #cost: int

class Graph:
    def __init__(self, path_to_graph):
        self.num_of_edges = 0
        self.num_of_disturbance_edges = 0
        self.__node_map = {}
        self.__edge_map = {}
        self.__disturbance_edge_map = {}
        print("Loading graph from file " + path_to_graph)

        with open(path_to_graph, 'r') as f:
            lines = f.readlines()

            row = 0
            column = 0

            for line in lines:
                for char in line:
                    # in test case files there are three symbols available
                    #   (space) - no node available in this place on the grid
                    # . (point) - normal node present in this place,
                    #               agent should use these to get to the final destination
                    # x (cross) - fatal node present in this place, agent should avoid it
                    if char == " ":
                        column += 1
                        continue
                    elif char == ".":
                        fatal = False
                    elif char == "x":
                        fatal = True
                    elif char == "\n":
                        column = 0
                        break
                    else:
                        raise ValueError("Char " + char + " is not supported")
                    cur_id = str(row) + ":" + str(column)
                    self.__node_map[cur_id] = Node(cur_id, fatal)
                    self.__connect_to_grid(cur_id)
                    column += 1
                row += 1

            print("Loaded %d nodes, %d edges and %d disturbance edges" % (
                len(self.__node_map), self.num_of_edges, self.num_of_disturbance_edges))

            # uncomment to enable waiting (looped edges)
            # for node_id in self.__node_map:
            #     self.__edge_map[node_id][node_id] = Edge(node_id, node_id)

    def __add_edge_to_graph(self, from_id, to_id, edge):
        if from_id not in self.__edge_map:
            self.__edge_map[from_id] = {}

        if to_id not in self.__edge_map[from_id]:
            self.__edge_map[from_id][to_id] = edge
            self.num_of_edges += 1
        else:
            raise ValueError(
                'Edge ' + from_id + "->" + to_id + " is already in the graph")

    def __add_disturbance_edge_to_graph(self,from_id,to_id,disturbance_edge):
        if from_id not in self.__disturbance_edge_map:
            self.__disturbance_edge_map[from_id] = {}

        if to_id not in self.__disturbance_edge_map[from_id]:
            self.__disturbance_edge_map[from_id][to_id] = disturbance_edge
            self.num_of_disturbance_edges += 1
        else:
            raise ValueError(
                'Disturbance edge ' + from_id + "->" + to_id + " is already in the graph")

    def get_all_nodes(self):
        return self.__node_map.keys()

    def remove_edge(self, from_id, to_id):
        if from_id in self.__edge_map and to_id in self.__edge_map[from_id]:
            self.__edge_map[from_id].pop(to_id)
            return True
        return False

    def remove_disturbance_edge(self, from_id, to_id):
        if from_id in self.__disturbance_edge_map and to_id in self.__disturbance_edge_map[from_id]:
            self.__disturbance_edge_map[from_id].pop(to_id)
            return True
        return False

    def remove_node(self, node_id):
        if node_id in self.__node_map:
            self.__node_map.pop(node_id)
            return True
        return False

    def get_node(self, node_id):
        if node_id not in self.__node_map:
            return None
        return self.__node_map[node_id]

    def get_edge(self, from_id, to_id):
        if from_id in self.__edge_map and to_id in self.__edge_map[from_id]:
            return self.__edge_map[from_id][to_id]
        return None

    def get_disturbance_edge(self, from_id, to_id):
        if from_id in self.__disturbance_edge_map and to_id in self.__disturbance_edge_map[from_id]:
            return self.__disturbance_edge_map[from_id][to_id]
        return None

    def get_out_edges(self, node_id):
        if node_id in self.__edge_map:
            return [self.__edge_map[node_id][to] for to in self.__edge_map[node_id]]
        return None

    def get_out_disturbance_edges(self, node_id):
        if node_id in self.__disturbance_edge_map:
            return [self.__disturbance_edge_map[node_id][to] for to in self.__disturbance_edge_map[node_id]]
        return None

    def get_all_edges(self):
        all_edges = []
        for f in self.get_all_nodes():
            all_edges.extend(self.get_out_edges(f))
        return all_edges

    def get_all_disturbance_edges(self):
        all_disturbance_edges = []
        for f in self.get_all_nodes():
            all_disturbance_edges.extend(self.get_out_disturbance_edges(f))
        return all_disturbance_edges

    def __connect_to_grid(self, cur_id):
        row = int(cur_id.split(":")[0])
        column = int(cur_id.split(":")[1])

        above_id = str(row-1) + ":" + str(column)
        below_id = str(row+1) + ":" + str(column)
        left_id = str(row) + ":" + str(column-1)
        right_id = str(row) + ":" + str(column+1)
        
        neighbours = [above_id, below_id, left_id, right_id]
        for n in neighbours:
            if self.get_node(n):
                if not self.get_edge(cur_id, n):
                    self.__add_edge_to_graph(cur_id, n, Edge(cur_id, n, 1))
                if not self.get_edge(n, cur_id):
                    self.__add_edge_to_graph(n, cur_id, Edge(n, cur_id, 1))

        if self.get_node(left_id):
            if not self.get_disturbance_edge(cur_id,left_id):
                self.__add_disturbance_edge_to_graph(cur_id,left_id,DisturbanceEdge(cur_id,left_id,1))
