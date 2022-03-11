from dataclasses import dataclass
from enum import Enum


class NodeClass(Enum):
    FATAL = False
    OK = True


@dataclass(frozen=False)
class Node:
    id: str
    kind: NodeClass


class EdgeClass(Enum):
    DISTURBANCE = False
    NORMAL = True


@dataclass(frozen=False)
class Edge:
    from_id: str
    to_id: str
    # cost is constant on the grid - every move requires the same effort
    cost: int
    kind: EdgeClass


class Graph:
    def __init__(self, path_to_graph):
        self.num_of_normal_edges = 0
        self.num_of_disturbance_edges = 0
        self.max_row = 0
        self.max_column = 0
        self.__node_map = {}
        self.__normal_edge_map = {}
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
                        kind = NodeClass.OK
                    elif char == "x":
                        kind = NodeClass.FATAL
                    elif char == "\n":
                        column = 0
                        break
                    else:
                        raise ValueError("Char " + char + " is not supported")
                    cur_id = str(row) + ":" + str(column)
                    self.__node_map[cur_id] = Node(cur_id, kind)
                    self.__connect_to_grid(cur_id)

                    self.max_row = max(self.max_row, row)
                    self.max_column = max(self.max_column, column)

                    column += 1
                row += 1

            # uncomment to enable waiting (looped edges)
            # for node_id in self.__node_map:
            #     self.__edge_map[node_id][node_id] = Edge(node_id, node_id)

    def __get_edge_map(self, kind):
        map_to_get = self.__normal_edge_map
        if kind == EdgeClass.DISTURBANCE:
            map_to_get = self.__disturbance_edge_map
        return map_to_get

    def __add_edge_to_graph(self, from_id, to_id, edge):
        map_to_add = self.__get_edge_map(edge.kind)

        if from_id not in map_to_add:
            map_to_add[from_id] = {}

        if to_id not in map_to_add[from_id]:
            map_to_add[from_id][to_id] = edge
            if edge.kind == EdgeClass.NORMAL:
                self.num_of_normal_edges += 1
            else:
                self.num_of_disturbance_edges += 1
        else:
            raise ValueError(
                'Edge ' + from_id + "->" + to_id + " is already in the graph")

    def get_all_nodes(self, kind=None):
        all_ids = self.__node_map.keys()
        if kind:
            all_ids = list(filter(lambda node_id: self.__node_map[node_id].kind == kind,
                                  all_ids))
        return all_ids

    def remove_edge(self, from_id, to_id, kind):
        map_to_remove = self.__get_edge_map(kind)
        if kind == EdgeClass.DISTURBANCE:
            map_to_remove = self.__disturbance_edge_map

        if from_id in map_to_remove and to_id in map_to_remove[from_id]:
            map_to_remove[from_id].pop(to_id)
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

    def get_edge(self, from_id, to_id, kind):
        map_to_get = self.__get_edge_map(kind)

        if from_id in map_to_get and to_id in map_to_get[from_id]:
            return map_to_get[from_id][to_id]
        return None

    def get_out_edges(self, node_id, kind):
        map_to_get = self.__get_edge_map(kind)

        if node_id in map_to_get:
            return [map_to_get[node_id][to] for to in map_to_get[node_id]]
        return None

    def get_all_edges(self, kind=None):
        all_edges = []
        if not kind or kind == EdgeClass.NORMAL:
            for f in self.get_all_nodes():
                all_edges.extend(self.get_out_edges(f, EdgeClass.NORMAL))

        if not kind or kind == EdgeClass.DISTURBANCE:
            for f in self.get_all_nodes():
                all_edges.extend(self.get_out_edges(f, EdgeClass.DISTURBANCE))
        return all_edges

    def __connect_to_grid(self, cur_id):
        row = int(cur_id.split(":")[0])
        column = int(cur_id.split(":")[1])

        above_id = str(row - 1) + ":" + str(column)
        below_id = str(row + 1) + ":" + str(column)
        left_id = str(row) + ":" + str(column - 1)
        right_id = str(row) + ":" + str(column + 1)

        neighbours = [above_id, below_id, left_id, right_id]
        for n in neighbours:
            if self.get_node(n):
                if not self.get_edge(cur_id, n, EdgeClass.NORMAL):
                    self.__add_edge_to_graph(cur_id, n,
                                             Edge(cur_id, n, 1, EdgeClass.NORMAL))
                if not self.get_edge(n, cur_id, EdgeClass.NORMAL):
                    self.__add_edge_to_graph(n, cur_id,
                                             Edge(n, cur_id, 1, EdgeClass.NORMAL))

    def create_disturbance_edges(self, direction, min_force, max_force):
        vectors = []
        if len(direction) == 0:
            return

        if 'u' in direction:
            vectors.append([-1, 0])

        if 'b' in direction:
            vectors.append([1, 0])

        if 'l' in direction:
            vectors.append([0, -1])

        if 'r' in direction:
            vectors.append([0, 1])

        for n in self.get_all_nodes(NodeClass.OK):
            coords = n.split(':')
            y_coord = int(coords[0])
            x_coord = int(coords[1])
            for v in vectors:
                for i in range(min_force, max_force + 1):
                    total_v = [x * i for x in v]
                    to_n = [y_coord + total_v[0], x_coord + total_v[1]]
                    if to_n[0] < 0 or to_n[0] > self.max_row or to_n[1] < 0 or to_n[
                        1] > self.max_column:
                        continue
                    to_n_str = str(to_n[0]) + ":" + str(to_n[1])
                    if not self.get_edge(n, to_n_str,
                                         EdgeClass.DISTURBANCE) and self.get_node(
                        to_n_str) is not None:
                        self.__add_edge_to_graph(n, to_n_str,
                                                 Edge(n, to_n_str, 1,
                                                      EdgeClass.DISTURBANCE))
